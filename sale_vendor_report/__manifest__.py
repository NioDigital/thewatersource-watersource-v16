{
    'name' : 'Sale Inventory Report',
    'version' : '3.2.3',
    'category': 'Sale',
    'summary' : 'Vendor Stock Request',
    'description': """This app allows to view vendor sale report
    """,
    'author' : 'NioDigital',
    'website' : '',
    'depends' : ['sale','purchase'],
    'data' : [
    'security/ir.model.access.csv',
        'views/sale_stock_view.xml',
    ],
    'installable' : True,
    'application' : False,
}

