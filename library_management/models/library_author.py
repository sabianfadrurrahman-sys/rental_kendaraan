# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import UserError

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Library Author'

    name = fields.Char("Nama Penulis")
    book_ids = fields.One2many('library.book', 'author_id', string="Daftar Buku")   
    user_id = fields.Many2one('res.users', string='Akun User Odoo', default=lambda self: self.env.user)
    
    def write(self, vals):
        # 1. TAMBAHAN BARU: Jalur VIP untuk Superuser (Sistem Odoo)
        if self.env.su:
            return super(LibraryAuthor, self).write(vals)

        # 2. Pengecekan normal untuk user biasa
        for rec in self:
            # Cegah edit jika user bukan Manager/Administrator
            if not self.env.user.has_group('library_management.group_library_manager'):
                raise UserError('Akses Ditolak! Anda bukan Manager Perpustakaan.')
                
        return super(LibraryAuthor, self).write(vals)
    
    
    
"""_Summery on

book_age_category = fields.Char(compute='_compute_book_age_category', string='book_age_category')

@api.depends('published_year')
def _compute_book_age_category(self):
    for rec in self:
        if not rec.published_year:
            rec.book_age_category = "Tahun tidak diketahui"

        else:
            umur_sebuah_buku = 2026 - rec.published_year
        
        if umur_sebuah_buku <= 5:
            rec.book_age_category = "Buku terumasuk keluaran baru"
            
        elif 6 <= umur_sebuah_buku >= 20 :
            rec.book_age_category = "Buku termasuk kelauran lama"
         
        else:
            rec.book_age_category = "Antik-antik aseng"

    
@api.constrains('published_year')
def _check_checktahun_terbit(self):
    for sec in self:
        if sec.published_year:
            if  sec.published_year > 2026 or sec.published_year < 1000:
                raise ValidationError("Kayaknya masih error karena untuk memahami sebauh perintah aku masih kurang dalam memahaminya")
        
# Tidak perlu pakai @api.constrains atau @api.depends di sini
    def unlink(self):
        # 1. Ritual wajib: looping data yang mau dihapus (bisa lebih dari 1 buku sekaligus)
        for rec in self:
            
            # 2. Logika IF: Cek apakah status buku (rec.state) BUKAN 'draft'
            if rec.state == True and not False:
                
                # 3. Munculkan error (Anggap UserError sudah di-import)
                raise UserError("Buku yang sudah rilis tidak boleh dihapus sembarangan!")
                
        # 4. Kalau semua buku yang mau dihapus statusnya 'draft', 
        # izinkan Odoo melanjutkan proses hapus ke database.
        return super(LibraryBook, self).unlink()
"""