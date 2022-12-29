# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
    "name":  "POS Invoice Details",
    "summary": """Allows the seller to view the invoice details related to a customer in POS.POS Invoice Details|POS Customer Invoice| Invoice related to Customer|""",
    "category":  "Point Of Sale",
    "version":  "1.0",
    "sequence":  1,
    "author":  "Webkul Software Pvt. Ltd.",
    "license":  "Other proprietary",
    "website":  "https://store.webkul.com/Odoo-POS-Invoice-Details.html",
    "description":  """https://webkul.com/blog/odoo-pos-invoice-details/""",
    "live_test_url":  "http://odoodemo.webkul.com/?module=pos_invoice_details&custom_url=/pos/auto",
    "depends":  ['point_of_sale'],
    "data":  [],
    'assets': {
        'point_of_sale.assets': [
            "/pos_invoice_details/static/src/js/main.js",
            "/pos_invoice_details/static/src/css/pos_invoice_details.css",
            'pos_invoice_details/static/src/xml/**/*',
        ],
    },
    "images":  ['static/description/Banner.gif'],
    "application":  True,
    "installable":  True,
    "auto_install":  False,
    "price":  39,
    "currency":  "USD",
    "pre_init_hook":  "pre_init_check",
}