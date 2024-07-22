# -*- coding: utf-8 -*-
{
    'name' : "Documents Management Odoo App",
    "author": "Edge Technologies",
    'version': '16.0.1.1',
    'live_test_url': "https://youtu.be/XeSPg0gWuBU",
    "images":['static/description/main_screenshot.png'],
    'summary': 'Odoo documents management app dms document management system document directory document tags document directory tag document directory path directory document system document file management document directory hierarchy file document store document odoo',
    'description' : """Documents management odoo app
    """,
    "license" : "OPL-1",
    'depends': ['base','mail','portal'],
    'data': [        
        'security/document_security.xml',
        'security/ir.model.access.csv',
        'views/directory.xml',
        'views/attachment_template.xml',
        'views/document.xml',
        'data/data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'price': 18,
    'currency': "EUR",
    'category': 'Extra Tools',
}
