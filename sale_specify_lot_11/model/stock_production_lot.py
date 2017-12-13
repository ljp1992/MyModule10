# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        '''展示该仓库该产品预测数量大于0的批次 Added by 刘吉平 on 2017-12-13'''
        context = self.env.context
        if context.get('quotation'):
            product_id = context.get('product_id_qdodoo')
            warehouse_id = context.get('warehouse_id_qdodoo')
            if product_id and warehouse_id:
                lot_stock_id = self.env['stock.warehouse'].browse(warehouse_id).lot_stock_id.id
                quants = self.env['stock.quant'].read_group([
                    ('product_id', '=', product_id),
                    ('location_id', 'child_of', lot_stock_id),
                    ('virtual_available', '>', 0),
                    ('lot_id', '!=', False),
                ], ['lot_id'], ['lot_id'])
                # print("quants:",quants)
                available_lot_ids = []
                if quants:
                    available_lot_ids = [quant['lot_id'][0] for quant in quants]
                    available_lot_ids = list(set(available_lot_ids))
                args += [('id', 'in', available_lot_ids)]
            else:
                args = [('id', '=', False)]
        result = super(StockProductionLot, self).name_search(name, args, operator, limit)
        return result