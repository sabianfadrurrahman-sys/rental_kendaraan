# -*- coding: utf-8 -*-
from odoo import models, fields

class LibraryPublisher(models.Model):
    _name = 'library.publisher'
    _description = 'Library Publisher'
    _inherits = {'res.partner': 'partner_id'}  

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        ondelete='cascade'
    )
    
    publisher_code = fields.Char("Publisher Code", required=True)
    established_year = fields.Integer("Established Year")
    website = fields.Char("Website")
    active = fields.Boolean("Active Publisher", default=True)
    rating = fields.Selection([
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ], string="Rating", default='bronze')
    