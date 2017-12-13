# -*- coding: utf-8 -*-

from psycopg2 import OperationalError, Error
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_is_zero

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    virtual_available = fields.Float(string=u'可用数量', compute='get_virtual_available_qdodoo', store=True)

    @api.depends('quantity', 'reserved_quantity')
    def get_virtual_available_qdodoo(self):
        '''计算预测数量 Added by 刘吉平 on 2017-12-13'''
        for record in self:
            record.virtual_available = record.quantity - record.reserved_quantity

    @api.model
    def _update_reserved_quantity(self, product_id, location_id, quantity, lot_id=None, package_id=None,
                                  owner_id=None, strict=False):
        '''销售数量超过预测数量情况下的处理。隐藏raise可能会有潜在bug需要进一步核实 Added by 刘吉平 on 2017-12-13'''
        self = self.sudo()
        rounding = product_id.uom_id.rounding
        quants = self._gather(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=strict)
        available_quantity = self._get_available_quantity(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=strict)

        # if float_compare(quantity, 0, precision_rounding=rounding) > 0 and float_compare(quantity, available_quantity, precision_rounding=rounding) > 0:
        #     raise UserError(_('It is not possible to reserve more products of %s than you have in stock.') % (', '.join(quants.mapped('product_id').mapped('display_name'))))
        # elif float_compare(quantity, 0, precision_rounding=rounding) < 0 and float_compare(abs(quantity), sum(quants.mapped('reserved_quantity')), precision_rounding=rounding) > 0:
        #     raise UserError(_('It is not possible to unreserve more products of %s than you have in stock.') % (', '.join(quants.mapped('product_id').mapped('display_name'))))

        reserved_quants = []
        for quant in quants:
            if float_compare(quantity, 0, precision_rounding=rounding) > 0:
                max_quantity_on_quant = quant.quantity - quant.reserved_quantity
                if float_compare(max_quantity_on_quant, 0, precision_rounding=rounding) <= 0:
                    continue
                max_quantity_on_quant = min(max_quantity_on_quant, quantity)
                quant.reserved_quantity += max_quantity_on_quant
                reserved_quants.append((quant, max_quantity_on_quant))
                quantity -= max_quantity_on_quant
                available_quantity -= max_quantity_on_quant
            else:
                max_quantity_on_quant = min(quant.reserved_quantity, abs(quantity))
                quant.reserved_quantity -= max_quantity_on_quant
                reserved_quants.append((quant, -max_quantity_on_quant))
                quantity += max_quantity_on_quant
                available_quantity += max_quantity_on_quant

            if float_is_zero(quantity, precision_rounding=rounding) or float_is_zero(available_quantity, precision_rounding=rounding):
                break
        return reserved_quants