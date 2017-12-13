# -*- coding: utf-8 -*-
{
    'name': "在报价单指定批次发货",
    'summary': """""",
    'description': """
bug:
两个报价单，第一个报价单确认，用完库存。然后再确认第二个报价单，由于预测数量为0，批次没有带出来。
完善：
发货单同一产品应该合并起来。原生的也没有合并
    """,
    'author': "青岛欧度软件技术有限责任公司",
    'website': "http://www.qdodoo.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['sale_management','sale_stock',],
    'data': [
        'view/sale_view.xml',
             ],
    'installable': True,
    'application': True,
}
