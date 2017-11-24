# -*- coding: utf-8 -*-
{
    'name': "点击按钮下载文件",

    'summary': """
        """,

    'description': """
    """,

    'author': "刘吉平",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale',],

    # always loaded
    'data': [
        'views/load_js.xml',
        'views/sale_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'qweb':[
        'static/src/xml/import.xml',
    ],
    'application': True,
}