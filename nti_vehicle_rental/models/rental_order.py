from odoo import models, fields, api

class RentalOrder(models.Model):
    _name = 'rental.order'
    _description = 'Rental Order'
    _order = 'name desc'
    _rec_name = 'name'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: 'New')