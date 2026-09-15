# -*- coding: utf-8 -*-
{
    'name': "nti_vehicle_rental",

    'summary': "Module for managing vehicle rentals",

    'description': """
        Module for managing vehicle rentals and rental orders.
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # Modul pendukung (ditambahkan 'mail' agar mail.thread tidak error)
    'depends': ['base', 'mail'],

    # File data dan views yang dimuat
    'data': [
        'security/ir.model.access.csv',
        'data/ir.sequence.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}