# -*- coding: utf-8 -*-

from odoo import models, fields, api


class nti_vehicle_rental(models.Model):
     _name = 'nti_vehicle_rental.nti_vehicle_rental'
     _description = 'nti_vehicle_rental.nti_vehicle_rental'

     car = fields.Char(string ='mobil')
     l = fields.Integer()
     value2 = fields.Float(compute="_value_pc", store=True)
     description = fields.Text()

     @api.depends('value')
     def _value_pc(self):
         for record in self:
             record.value2 = float(record.value) / 100
             