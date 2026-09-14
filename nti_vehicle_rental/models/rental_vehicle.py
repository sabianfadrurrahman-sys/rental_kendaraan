from odoo import models, fields, api

class RentalVehicle(models.Model):
    _name = 'rental.vehicle'
    _description = 'Rental Vehicle'
    _order = 'name'
    _rec_name = 'display_name'

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
    ], string='Status', default='available', readonly=True)
    
    note = fields.Text(string='Note')
    active = fields.Boolean(string='Active', default=True)
    image_1920 = fields.Image(string='Image')
    
    order_ids = fields.One2many('rental.order', 'vehicle_id', string='Rental Orders')
    order_count = fields.Integer(string='Order Count', compute='_compute_order_count')

    @api.depends('order_ids')
    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)