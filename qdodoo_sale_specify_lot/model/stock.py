# -*- coding: utf-8 -*-
from odoo import api, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def _prepare_procurement_from_move(self):
        self.ensure_one()
        vals = super(StockMove, self)._prepare_procurement_from_move()
        vals['lot_id'] = self.restrict_lot_id.id
        return vals
