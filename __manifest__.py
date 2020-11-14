{
    'name': 'Report POS by Product Category',
    'author': 'technoindo.com',
    'category': 'hidden',
    'version': '10.0',
    'summary': 'Summary the addon.',
    'description': '''Description the addon'''
                   ,
    'depends': ['point_of_sale'],
    'data': [
        'wizard/wizard_report.xml',
        'reports/pos_report.xml',
        'reports/pos_temp.xml',
    ],
    'images': [''],
    'auto_install': False,
    'installable': True,
    'application': False,
}
