# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BookCopies(models.Model):
    _name = 'book.copies'
    _description = 'Fisik Eksemplar Buku'
    
    # Nama eksemplar (Kode Eksemplar) di-set default 'New' agar otomatis terisi oleh sequence
    name = fields.Char(string='Kode Eksemplar', required=True, default='New', readonly=True)
    code = fields.Char(string='Barcode/Rak')
    
    status = fields.Selection([
        ('ready', 'Tersedia'),
        ('borrowed', 'Dipinjam'),
        ('lost', 'Hilang')
    ], string='Status Eksemplar', default='ready', tracking=True)
    
    # Relasi
    book_id = fields.Many2one('library.book', string='Judul Buku', required=True, ondelete='cascade')
    membership_id = fields.Many2one('library.member', string='Dipinjam Oleh', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New' or not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('book.copies') or 'New'
                
        return super(BookCopies, self).create(vals_list)