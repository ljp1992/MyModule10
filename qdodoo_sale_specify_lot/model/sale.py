# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import Warning


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_id = fields.Many2one('stock.production.lot', string=u'批次', copy=False)

    @api.onchange('product_id', 'product_uom_qty', 'lot_id')
    def check_qty_enough(self):
        '''若超过预测数量给出提示 Added by ljp on 2017-12-08'''
        if self.product_id and self.product_uom_qty and self.lot_id:
            result = self.product_id._compute_quantities_dict(self.lot_id.id, None, None, False, False)
            virtual_available = result[self.product_id.id]['virtual_available']
            if self.product_uom_qty > virtual_available:
                info = u'销售数量%s大于预测数量%s' % (self.product_uom_qty, virtual_available)
                raise UserError(info)

    @api.onchange('product_id')
    def _onchange_product_id_set_lot_domain(self):
        available_lot_ids = []
        if self.order_id.warehouse_id and self.product_id:
            location = self.order_id.warehouse_id.lot_stock_id
            quants = self.env['stock.quant'].read_group([
                ('product_id', '=', self.product_id.id),
                ('location_id', 'child_of', location.id),
                ('qty', '>', 0),
                ('lot_id', '!=', False),
            ], ['lot_id'], 'lot_id')
            available_lot_ids = [quant['lot_id'][0] for quant in quants]
        self.lot_id = False
        return {
            'domain': {'lot_id': [('id', 'in', available_lot_ids)]}
        }

    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
        res = super(
            SaleOrderLine, self)._prepare_order_line_procurement(
            group_id=group_id)
        res['lot_id'] = self.lot_id.id
        return res


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def get_move_from_line(self, line):
        move = self.env['stock.move']
        # i create this counter to check lot's univocity on move line
        lot_count = 0
        for p in line.order_id.picking_ids:
            for m in p.move_lines:
                if line.lot_id == m.restrict_lot_id:
                    move = m
                    lot_count += 1
                    # if counter is 0 or > 1 means that something goes wrong
                    if lot_count != 1:
                        raise Warning(_('Can\'t retrieve lot on stock'))
        return move

    @api.model
    def _check_move_state(self, line):
        if line.lot_id:
            move = self.get_move_from_line(line)
            if move.state == 'confirmed':
                move.action_assign()
                move.refresh()
            if move.state != 'assigned':
                raise Warning(_('Can\'t reserve products for lot %s') %
                              line.lot_id.name)
        return True

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            self._check_move_state(line)
        return res
