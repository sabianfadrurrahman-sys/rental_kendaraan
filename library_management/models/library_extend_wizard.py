from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError

class LibraryExtendWizard(models.TransientModel):
    _name = 'library.extend.wizard'
    _description = 'Wizard Perpanjangan Peminjaman'

    additional_days = fields.Integer(string="Tambah Durasi (Hari)", default=7, required=True)

    def action_confirm_extend(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            borrow_record = self.env['library.borrow'].browse(active_id)
            
            if borrow_record.state != 'ongoing':
                raise ValidationError("Hanya peminjaman yang sedang berlangsung (ongoing) yang dapat diperpanjang!")
            
            # Hitung tanggal kembali baru
            if borrow_record.datetime_to:
                new_date = borrow_record.datetime_to + timedelta(days=self.additional_days)
                borrow_record.datetime_to = new_date
                
                # Catat aktivitas / pesan ke chatter
                borrow_record.message_post(
                    body=f"Masa peminjaman diperpanjang selama {self.additional_days} hari. Tanggal kembali baru: {new_date}"
                )
                
        return {'type': 'ir.actions.act_window_close'}