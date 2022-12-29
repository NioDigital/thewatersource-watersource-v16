# -*- coding: utf-8 -*-
{
    "name": "Filter Products by Supplier",
    "version": "1.0",
    'summary': """
        This module is help you to filter products by supplier in purchase order | Vendor Products""",
    'description': """
filter products by supplier in purchase order
        """,    
    "category": "Purchase",
    'author': "Preway IT Solutions",
    "sequence": 2,
    "depends" : ["purchase"],
    "data" : [
        "views/res_partner_view.xml",
    ],
    'price': 10.0,
    'currency': 'EUR',
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
    'live_test_url': 'https://youtu.be/K5_IXDdjWNM',
    "images":["static/description/Banner.png"],
}
