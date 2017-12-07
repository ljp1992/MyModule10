# -*- coding: utf-8 -*-

import base64
import logging
import json

from openerp import http
from openerp.http import request
from openerp import _

_logger = logging.getLogger(__name__)

class Binary(http.Controller):

    @http.route('/web/binary/upload_formdata', type='http', auth='user')
    def upload_formdata(self, model, id, ufile):
        attachment_model = request.env['ir.attachment']
        try:
            attachment = attachment_model.create({
                'name': ufile.filename,
                'datas': base64.encodestring(ufile.read()),
                'datas_fname': ufile.filename,
                'res_model': model,
                'res_id': int(id)
            })
            args = {
                'filename': ufile.filename,
                'mimetype': ufile.content_type,
                'id':  attachment.id
            }
        except Exception, e:
            args = dict(error=_("Something horrible happened"), message=e.message)
            _logger.exception("Fail to upload attachment(%s) exception(%s)" % (ufile.filename, e.message))
        return request.make_response(json.dumps(args), [('Content-Type', 'application/json')])
