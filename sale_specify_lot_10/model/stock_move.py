# -*- coding: utf-8 -*-
from odoo import api, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _update_reserved_quantity(self, need, available_quantity, location_id, lot_id=None, package_id=None,
                                  owner_id=None, strict=True):
        '''传入批次号 Added by 刘吉平 on 2017-12-13'''
        if not lot_id and self.sale_line_id.lot_id:
            lot_id = self.sale_line_id.lot_id
        taken_quantity = super(StockMove, self)._update_reserved_quantity(need, available_quantity, location_id, lot_id, package_id, owner_id, strict)
        return taken_quantity
