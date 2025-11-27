# -*- coding: utf-8 -*-

{
    'name': 'Agencia Test',
    'category': 'Test',
    'summary': 'Modulo para agencia',
    'version': '18.0.0.1',
    'description': """Test""",
    'author': 'Rapid Technologies SAC',
    'website': 'https://www.rapid.tech',
    'depends': ['base','sale', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
    ],
    'assets': {},
    'installable': True,
}