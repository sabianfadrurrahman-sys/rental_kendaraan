# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class RentalOrder(models.Model):
    _name = 'rental.order'
    _description = 'Rental Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, id desc'
    _rec_name = 'name'

    name = fields.Char(string='Order Reference', default='New', readonly=True, copy=False)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    vehicle_id = fields.Many2one('rental.vehicle', string='Vehicle', required=True, tracking=True, domain=[('state', '!=', 'maintenance')])
    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.context_today, tracking=True)
    date_end = fields.Date(string='End Date', required=True, tracking=True)
    date_returned = fields.Date(string='Returned Date', readonly=True, copy=False)
    duration_days = fields.Integer(string='Duration (Days)', compute='_compute_duration', store=True)
    daily_rate = fields.Monetary(string='Daily Rate', related='vehicle_id.daily_rate', store=True, readonly=True)
    amount_total = fields.Monetary(string='Total Amount', compute='_compute_amount_total', store=True)
    deposit = fields.Monetary(string='Deposit', default=0.0)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('returned', 'Returned'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False)
    
    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True)
    note = fields.Text(string='Note')

    @api.depends('date_start', 'date_end')
    def _compute_duration(self):
        for record in self:
            if record.date_start and record.date_end:
                if record.date_end >= record.date_start:
                    delta = record.date_end - record.date_start
                    record.duration_days = delta.days + 1
                else:
                    record.duration_days = 0
            else:
                record.duration_days = 0

    @api.depends('duration_days', 'vehicle_id.daily_rate')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = record.duration_days * (record.daily_rate or 0.0)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_end < record.date_start:
                raise ValidationError("Tanggal Selesai (End Date) tidak boleh lebih awal dari Tanggal Mulai (Start Date).")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('rental.order') or 'New'
        return super().create(vals_list)