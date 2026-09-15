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
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir.sequence.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'OPL-1',
}