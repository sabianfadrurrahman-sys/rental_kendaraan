# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RentalVehicle(models.Model):
    _name = 'rental.vehicle'
    _description = 'Rental Vehicle'
    _order = 'name'
    _rec_name = 'name'

    name = fields.Char(string='Vehicle Name', required=True)
    license_plate = fields.Char(string='License Plate', required=True, index=True)
    vehicle_type = fields.Selection([
        ('car', 'Car'),
        ('motorcycle', 'Motorcycle'),
        ('truck', 'Truck')
    ], string='Vehicle Type', required=True, default='car')
    brand = fields.Char(string='Brand')
    model_year = fields.Integer(string='Model Year')
    seat_count = fields.Integer(string='Seat Count', default=4)
    daily_rate = fields.Monetary(string='Daily Rate', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    state = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Maintenance')
    ], string='Status', default='available', tracking=True)

    note = fields.Text(string='Note')
    active = fields.BooleanField(string='Active', default=True)
    image_1920 = fields.Image(string='Image')

    order_ids = fields.One2many('rental.order', 'vehicle_id', string='Rental Orders')
    order_count = fields.Integer(string='Order Count', compute='_compute_order_count')

    _sql_constraints = [
        ('license_plate_uniq', 'unique(license_plate, company_id)', 'License plate must be unique!'),
    ]

    @api.depends('order_ids')
    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)

    @api.constrains('daily_rate')
    def _check_daily_rate(self):
        for record in self:
            if record.daily_rate <= 0:
                raise ValidationError('Daily rate harus > 0.')

    @api.constrains('seat_count')
    def _check_seat_count(self):
        for record in self:
            if record.seat_count < 1:
                raise ValidationError('Seat count harus >= 1.')

    @api.constrains('model_year')
    def _check_model_year(self):
        current_year = datetime.datetime.now().year
        for record in self:
            if record.model_year and (record.model_year < 1990 or record.model_year > current_year + 1):
                raise ValidationError(f'Model year harus antara 1990 dan {current_year + 1}.')