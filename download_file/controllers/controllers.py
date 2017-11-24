# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request,content_disposition
import json,base64,cgi

class DownloadFile(http.Controller):

    @http.route(['/web/binary/download_document'], type='http', auth='public')
    def download_file(self, **kwargs):
        model = kwargs.get('model')
        id = kwargs.get('id')
        if type(id) is not int:
            id = int(id)
        order = request.env[model].sudo().browse(id)#销售订单
        filecontent = order.name or ''
        filename = 'cs.txt'
        return request.make_response(filecontent, [('Content-Type', 'application/octet-stream'),
                                                   ('Content-Disposition', content_disposition(filename))])
