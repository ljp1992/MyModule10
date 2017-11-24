# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import xlrd,base64,datetime


class ImportWizard(models.TransientModel):
    _name = 'import.wizard'

    name = fields.Char(default=u'导入excel', string=u'')
    data = fields.Binary(string=u'文件')

    #导入客户资料excel
    def import_excel(self):
        print 'import excel'
        return

    #下载模板文件
    def download_template_file(self):
        model = 'excel.template'
        field = 'template_file'
        id = 1
        filename = u'模板.xlsx'
        # url = '/web/binary/download_document/?model=excel.template&field=template_file&id=%d&filename=%s' % (1, u'模板.xlsx')
        return {
            'type': 'ir.actions.client',
            'tag': 'download_excel_ljp',
            'context': {'model': model,
                        'field': field,
                        'id': id,
                        'filename': filename,
                        }
        }

