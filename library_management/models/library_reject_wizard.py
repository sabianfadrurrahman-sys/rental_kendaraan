from odoo import models, fields, api

class LibraryRejectWizard(models.TransientModel):
    _name = 'library.reject.wizard'
    _description = 'Wizard Alasan Penolakan Peminjaman'

    reason = fields.Text(string="Alasan Penolakan", required=True)

    def action_confirm_reject(self):
        # Ambil active_id dari context untuk tahu transaksi mana yang sedang dibuka
        active_id = self.env.context.get('active_id')
        if active_id:
            borrow_record = self.env['library.borrow'].browse(active_id)
            # Ubah status jadi cancelled/rejected dan catat alasan ke chatter
            borrow_record.write({'state': 'draft'}) # atau status reject jika ada
            borrow_record.message_post(body=f"Peminjaman ditolak. Alasan: {self.reason}")
        return {'type': 'ir.actions.act_window_close'}