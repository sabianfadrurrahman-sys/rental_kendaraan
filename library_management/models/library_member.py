# -*- coding: utf-8 -*-
from odoo import models, fields, api

class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    borrow_count = fields.Integer(string='Borrow Count', compute = "_compute_borrow_count")

    membership_code = fields.Char(string='Kode Anggota', required=True, readonly=True, default= 'New')
    user_id = fields.Many2one('res.users', string='Akun Sistem (User)')
    
    
    def return_view_history_borrow(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow',
            'view_mode': 'list,form',
            'name': 'History Borrow',
            'domain': [('membership_id', '=', self.id)],
            'context': {'default_membership_id': self.id},
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Sebelumnya vals.get('New') == 'New' yang mana menyebabkan error logika
            if not vals.get('membership_code') or vals.get('membership_code', 'New') == 'New':
                vals['membership_code'] = self.env['ir.sequence'].next_by_code('library.member') or 'New'
        return super(LibraryMember, self).create(vals_list)    
        
    def _compute_borrow_count(self):
        for rec in self:
            rec.borrow_count = self.env['library.borrow'].search_count([
                ('membership_id', '=', rec.id)
            ])
