# -*- coding: utf-8 -*-
{
    'name': "qdodoo_sale_specify_lot",
    'summary': """  """,
    'description': """
功能描述:
报价单指定批次发货

完善:
1.报价单明细选择产品、批次、数量时,若库存不足给出提示
    """,
    'author': "青岛欧度软件技术有限责任公司",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['sale_stock', 'procurement'],
    'data': ['view/sale_view.xml'],
    'installable': True,
    'application': True,
}