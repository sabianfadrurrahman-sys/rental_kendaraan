{
    'name': 'Library Management',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Simple module to manage library books',
    'depends': ['base', 'mail'],
    'data': [
        # -- File Security --
        'security/security.xml',
        'security/ir.rule.xml',
        'security/ir.model.access.csv',
        
        # --- File Menu & Action Utama ---
        'views/menu_views.xml',
        
        # --- File Wizard (Wajib di atas borrow_views.xml karena dipanggil di sana) ---
        'views/reject_wizard_views.xml',
        'views/extend_wizard_views.xml',
        
        # --- File Views Model Lainnya ---
        'views/borrow_views.xml',
        'views/book_views.xml',
        'views/publisher_views.xml',
        'views/member_views.xml',
        'views/copies_views.xml',
        'views/category_views.xml',
        'views/author_views.xml',
        'views/action_excel.xml',
        
        # --- Data & Sequence ---
        'data/library_sequence.xml',
        'data/library_data.xml',
        'data/mail_template.xml',
        'data/cron.xml',
        
        # --- File Laporan QWeb ---
        'report/paperformat.xml',
        'report/report.xml',
        'report/report_template.xml',
    ],
    'installable': True,
    'application': True,
}