# -*- coding: utf-8 -*-
# Part of Niodigital Pvt Ltd.
{
    'name': 'Invoice Print Sheet',
    'version': '1.0',
    'summary': """Custom report for printing the invoice receipt in dot matrix printer""",
    'description': """
                    Custom report for printing the invoice receipt in dot matrix printer                                    
                    """,
    'author': "Nio Digital",
    'category': 'Accounting',
    'website': 'https://www.niodigital.co/',
    'license': 'OPL-1',
    'depends': ['base', 'account'],
    "data": [
            'views/invoice_report_custom.xml',
            ],
    'demo': [],
    'qweb': [],
    'installable': True,
}
