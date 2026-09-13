# -*- coding: utf-8 -*-
from odoo import models, fields

class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Library Category'

    name = fields.Char("Nama Kategori")
    book_ids = fields.Many2many('library.book', string="Daftar Buku")