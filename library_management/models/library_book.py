# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    _sql_constraints = [
        ('unique_book_name', 'unique(name)', 'Judul buku harus unik!')
    ]
    # 1. FIELD INFORMASI BUKU

    name = fields.Char(string='Title', required=True)
    code = fields.Char(string="Kode Buku", readonly=True, default="New")
    published_year = fields.Char(string='Published Year')
    pages = fields.Integer(string="Jumlah Halaman")
    reading_time = fields.Float("Waktu Baca (Jam)", compute='_compute_reading_time')
    remark = fields.Text(string="Keterangan")
    active = fields.Boolean("Active Book", default=True)
    current_borrow_state = fields.Char(compute = '_compute_current_borrow_state')
    jumlah_pinjam = fields.Integer(string='Jumlah Peminjaman', compute= '_compute_jumlah_pinjam')
    available_copies_count = fields.Integer(string='Eksemplar Tersedia', compute='_compute_available_copies')    
    
    # 2. FIELD RELASI
    book_copies_ids = fields.One2many('book.copies', 'book_id', string='Eksemplar')
    author_id = fields.Many2one('library.author', string="Penulis")
    publisher_id = fields.Many2one('library.publisher', string="Penerbit")
    category_ids = fields.Many2many('library.category', string="Kategori")
    history_borrow_line_ids= fields.One2many('library.borrow', 'book_id', string='Peminjaman')    
    # 3. FIELD STATUS
    state = fields.Selection([
        ('draft', 'Draft'),
        ('available', 'Tersedia'),
        ('borrowed', 'Dipinjam'),
        ('lost', 'Hilang'),
    ], string='Status', default='draft', tracking=True)

    
    # 4. LOGIKA & VALIDASI
    @api.depends('pages')
    def _compute_reading_time(self):
        for record in self:
            record.reading_time = record.pages / 30 if record.pages else 0
            
    @api.depends('history_borrow_line_ids')
    def _compute_jumlah_pinjam(self):
        for record in self:
            # Menghitung jumlah baris data yang ada di history_borrow_line_ids
            record.jumlah_pinjam = len(record.history_borrow_line_ids)
  
    # Pemahaman terkait dengan bagaimana cara agar bisa menghasilkan jumlah dari 1 sampai ke jumlah lain
    # Dengan cara pemetaan terkait dengan object yang di ambil, ada yang salah pada library_borrow dan bagaimana caranya

    @api.onchange('pages')
    def _onchange_pages(self):
        if self.pages and self.pages < 50:
            self.remark = "Buku ini termasuk kategori bacaan ringan."
        else:
            self.remark = False

    @api.constrains('pages')
    def _check_pages(self):
        for record in self:
            if record.pages <= 0:
                raise ValidationError("Halaman harus lebih dari 0!")

    def action_check_books(self):
        books = self.env['library.book'].search([('pages', '>', 100)])
        _logger.warning("-------------Books--------------: %s", books)
        # books2 = library.book(1, 2, 3, 4, 5)
        # kumpulan_nama_buku = [book.name for book in books]
        # Bisa menggunakan 
        # Kalau menggunakan books2 dan dan dengan kumpulan_nama_buku gitu kasusnya malah jadi singleton
        # Kalau gitu kasusnya mending ga usah ada var lokal?
        # browse, search_count []
        # kalau terkait dengan dict  
        titles = books.mapped('name')
        return f"Ada {len(books)} buku tebal: {', '.join(titles)}"  

    def _compute_current_borrow_state(self):
        for book in self:
            # Mencari transaksi peminjaman yang aktif untuk buku ini
            active_borrow = self.env['library.borrow'].search([
                ('book_id', '=', book.id),
                ('state', 'in', ['ongoing', 'late'])
            ], limit=1)
            
            if active_borrow:
                book.current_borrow_state = active_borrow.state
            else:
                book.current_borrow_state = 'available'
    
    @api.depends('book_copies_ids.status')
    # 2. ...SAMA PERSIS dengan nama fungsi ini!
    def _compute_available_copies(self):
        for rec in self:
            jumlah_ready = 0
            for copy in rec.book_copies_ids:
                if copy.status == 'ready':
                    jumlah_ready += 1
            rec.available_copies_count = jumlah_ready

    # 5. ORM METHOD OVERRID-m
    @api.model
    def create(self, vals):
        # Memanggil nomor sequence dari XML jika field 'code' isinya masih 'New'
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('library.book') or 'New'
        return super(LibraryBook, self).create(vals)
    
    def write(self, vals):
        res = super(LibraryBook, self).write(vals)
        return res

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError("Buku yang berstatus selain draft tidak dapat dihapus.")
        return super(LibraryBook, self).unlink()