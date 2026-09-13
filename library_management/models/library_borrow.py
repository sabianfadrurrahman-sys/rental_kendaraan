# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError, UserError

class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = 'Transaksi Peminjaman'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    membership_id = fields.Many2one('library.member', string='Anggota', required=True)
    book_id = fields.Many2one('library.book', string='Buku', required=True)
    # 1. Eksemplar DIBUAT REQUIRED agar tidak ada peminjaman tanpa wujud fisik
    copies_id = fields.Many2one('book.copies', string='Eksemplar', required=True) 
    
    remark = fields.Text(string="Keterangan")
    name = fields.Char(string='Referensi', default="New", readonly=True)
    datetime_from = fields.Date(string='Tanggal Pinjam', default=fields.Date.context_today, required=True)
    datetime_to = fields.Date(string='Tanggal Kembali')
    duration = fields.Integer(string='Durasi (Hari)', compute='_compute_duration', store=True)
    fine = fields.Float(string='Total Denda', default=0.0)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'Menunggu Persetujuan'),
        ('ongoing', 'Sedang Dipinjam'),
        ('returned', 'Dikembalikan'),
        ('late', 'Terlambat')
    ], string='Status', default='draft', tracking=True)

    # 2. AUTOMATION UI: Filter Eksemplar berdasarkan Buku yang dipilih
    @api.onchange('book_id')
    def _onchange_book_id(self):
        self.copies_id = False # Kosongkan eksemplar jika judul buku diganti
        if self.book_id:
            # Hanya tampilkan eksemplar milik buku ini yang statusnya 'ready'
            return {'domain': {'copies_id': [('book_id', '=', self.book_id.id), ('status', '=', 'ready')]}}
        return {'domain': {'copies_id': []}}

    @api.depends('datetime_from', 'datetime_to')
    def _compute_duration(self):
        for record in self:
            if record.datetime_from and record.datetime_to:
                delta = record.datetime_to - record.datetime_from
                record.duration = delta.days
            else:
                record.duration = 0

    # 3. MENGHAPUS METHOD DUPLIKAT action_request_approval
    def action_request_approval(self):
        for rec in self:
            rec.state = 'to_approve'

    # 4. AUTOMATION STATUS: Saat Disetujui
    def action_approve(self):
        for rec in self:
            if rec.copies_id.status != 'ready':
                raise ValidationError(f"Eksemplar {rec.copies_id.code} sedang tidak tersedia!")
            rec.write({'state': 'ongoing'})
            rec.copies_id.status = 'borrowed'
    
            # Catat nama peminjam ke fisik eksemplarnya
            rec.copies_id.membership_id = rec.membership_id.id 
            rec.message_post(body="Peminjaman disetujui. Eksemplar dibawa pengunjung.")

    def action_return(self):
        for rec in self:
            rec.write({'state': 'returned'})
            rec.copies_id.status = 'ready'
            
            # --- BARIS SAKTI ---
            # Hapus nama peminjam dari fisik eksemplarnya karena sudah dikembalikan
            rec.copies_id.membership_id = False 
            
            rec.message_post(body="Buku telah dikembalikan. Eksemplar tersedia kembali.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Sebelumnya vals.get('New') == 'New' yang mana menyebabkan error logika
            if not vals.get('name') or vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('library.borrow') or 'New'
        return super(LibraryBorrow, self).create(vals_list)
                     
    @api.model
    def action_update_late_books(self):
        today = fields.Date.today()
        late_records = self.search([
            ('state', '=', 'ongoing'), 
            ('datetime_to', '<', today)
        ])
        
        for rec in late_records:
            rec.state = 'late'
            rec.activity_schedule('mail.mail_activity_data_todo', summary='Tindak Lanjut Keterlambatan')
            
            template = self.env.ref('library_management.mail_template_borrow_overdue', raise_if_not_found=False)
            if template:
                template.send_mail(rec.id, force_send=True)
                
            rec.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=self.env.user.id,
                summary='Tindak Lanjut Keterlambatan',
                note='Hubungi anggota ini untuk mengingatkan denda buku yang terlambat.'
            )
                    
    # PERBAIKAN INDENTASI: Tarik sejajar ke kiri (tidak menjorok ke dalam)
    @api.constrains('datetime_to', 'datetime_from')
    def _check_datetime_from(self):
        for record in self:
            if record.datetime_to and record.datetime_from and record.datetime_to < record.datetime_from:
                raise ValidationError("Tanggal pengembalian tidak boleh lebih awal daripada tanggal peminjaman!")