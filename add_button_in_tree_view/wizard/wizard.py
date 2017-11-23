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
        print self.env.context
        return



