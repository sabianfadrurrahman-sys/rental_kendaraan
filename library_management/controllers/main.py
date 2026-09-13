import io
import xlsxwriter
from odoo import http
from odoo.http import request

class LibraryExcelReport(http.Controller):

    @http.route('/library/download_excel', type='http', auth='user')
    def download_excel_report(self, borrow_ids, **kw):
        # 1. Konversi ID dari string URL ('1,2,3') menjadi list integer [1, 2, 3]
        ids = [int(i) for i in borrow_ids.split(',')]
        
        # 2. Ambil data dari database
        docs = request.env['library.borrow'].browse(ids)

        # 3. Siapkan file Excel di dalam memori komputer (tanpa save ke hardisk)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # --- KODE EXCEL KAMU DIMULAI DI SINI ---
        for doc in docs:
            sheet_name = f'Bukti {doc.membership_id.name}'[:31]
            sheet = workbook.add_worksheet(sheet_name)

            title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center'})
            bold_format = workbook.add_format({'bold': True})
            header_table_format = workbook.add_format({'bold': True, 'bg_color': '#2c3e50', 'font_color': 'white', 'border': 1, 'align': 'center'})
            cell_format = workbook.add_format({'border': 1})
            cell_center = workbook.add_format({'border': 1, 'align': 'center'})
            alert_format = workbook.add_format({'bold': True, 'font_color': 'red'})

            sheet.set_column('A:A', 15)
            sheet.set_column('B:B', 20)
            sheet.set_column('C:C', 20)
            sheet.set_column('D:D', 15)

            sheet.merge_range('A1:D1', 'Perpustakaan Digital', title_format)
            sheet.merge_range('A2:D2', 'Jl. Gegerkalong Hilir, Ds. Ciwaruga, Bandung', workbook.add_format({'align': 'center', 'italic': True}))
            sheet.merge_range('A3:D3', 'Telp: (022) 2013789 | Email: layanan@perpustakaan.ac.id', workbook.add_format({'align': 'center', 'font_color': '#7f8c8d'}))
            
            sheet.merge_range('A5:D5', 'BUKTI PEMINJAMAN BUKU', title_format)

            sheet.write('A7', 'Nama Anggota', bold_format)
            sheet.write('B7', f': {doc.membership_id.name}')
            
            sheet.write('A8', 'Status Trx', bold_format)
            sheet.write('B8', f': {doc.state.upper()}')

            sheet.write('C7', 'Tgl Pinjam', bold_format)
            sheet.write('D7', f': {str(doc.datetime_from)}')
            
            sheet.write('C8', 'Tgl Kembali', bold_format)
            sheet.write('D8', f': {str(doc.datetime_to) if doc.datetime_to else "-"}')

            row = 10
            sheet.write(row, 0, 'Kode Buku', header_table_format)
            sheet.merge_range(row, 1, row, 2, 'Judul Buku', header_table_format)
            sheet.write(row, 3, 'Durasi (Hari)', header_table_format)

            row += 1
            book_code = getattr(doc.book_id, 'code', '-')
            
            sheet.write(row, 0, book_code if book_code else '-', cell_center)
            sheet.merge_range(row, 1, row, 2, doc.book_id.name or '-', cell_format)
            sheet.write(row, 3, doc.duration or 0, cell_center)

            row += 2
            if doc.fine > 0:
                sheet.merge_range(f'A{row+1}:D{row+1}', f'Perhatian! Terdapat denda: Rp {int(doc.fine)}', alert_format)

            row += 4
            sheet.write(row, 3, 'Petugas Perpustakaan,', workbook.add_format({'align': 'center'}))
            sheet.write(row + 4, 3, '( .................................... )', workbook.add_format({'align': 'center', 'bold': True}))
        # --- KODE EXCEL KAMU SELESAI DI SINI ---

        workbook.close()
        output.seek(0)

        # 4. Berikan instruksi ke browser untuk mendownload file
        file_name = f'Bukti_Peminjaman.xlsx'
        return request.make_response(
            output.read(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename={file_name}')
            ]
        )