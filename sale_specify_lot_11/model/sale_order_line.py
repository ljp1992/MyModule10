# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import Warning
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_id = fields.Many2one('stock.production.lot', string=u'批次', copy=False)

    @api.onchange('product_id')
    def _onchange_product_id_uom_check_availability(self):
        '''修改原生方法 Modified by 刘吉平 on 2017-12-13'''
        if self.env.context.get('onchange_field') == 'product_id':
            print("@api.onchange('product_id')", self.env.context)
            if not self.product_uom or (self.product_id.uom_id.category_id.id != self.product_uom.category_id.id):
                self.product_uom = self.product_id.uom_id
            self.lot_id = False
            return self.check_inventory_qdodoo()

    @api.onchange('product_uom_qty', 'product_uom', 'route_id')
    def _onchange_product_id_check_availability(self):
        '''修改原生方法 Modified by 刘吉平 on 2017-12-13'''
        if self.env.context.get('onchange_field') in ['product_uom_qty', 'product_uom']:
            print("@api.onchange('product_uom_qty', 'product_uom', 'route_id')",self.env.context)
            return self.check_inventory_qdodoo()

    @api.onchange('lot_id')
    def onchange_lot_id_qdodoo(self):
        '''更改批次检查库存是否足够 Added by 刘吉平 on 2017-12-13'''
        if self.env.context.get('onchange_field') == 'lot_id':
            print("@api.onchange('lot_id')", self.env.context)
            return self.check_inventory_qdodoo()

    def check_inventory_qdodoo(self):
        print("检查库存：check_inventory_qdodoo")
        '''检查库存是否足够 Added by 刘吉平 on 2017-12-13'''
        if not self.lot_id:
            return self._onchange_product_id_check_availability_odoo()
        else:
            if not self.product_id or not self.product_uom_qty or not self.product_uom or \
                    not self.order_id.warehouse_id:
                self.product_packaging = False
                return {}
            if self.product_id.type == 'product':
                precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
                product_qty = self.product_uom._compute_quantity(self.product_uom_qty, self.product_id.uom_id)
                virtual_available = self.get_virtual_available_qdodoo(self.product_id.id, self.lot_id.id,
                                                                      self.order_id.warehouse_id.id)
                if float_compare(virtual_available, product_qty, precision_digits=precision) == -1:
                # if virtual_available < self.product_uom_qty:
                    is_available = self._check_routing()
                    if not is_available:
                        message = u'你打算出售%s%s，但是你在%s%s批次只有%s%s可以获得。' % \
                                  (self.product_uom_qty, self.product_uom.name, self.order_id.warehouse_id.name,
                                   self.lot_id.name, virtual_available, self.product_id.uom_id.name)
                        warning_mess = {
                            'title': u'库存不足!',
                            'message': message
                        }
                        return {'warning': warning_mess}

    def _onchange_product_id_check_availability_odoo(self):
        '''odoo原生方法_onchange_product_id_check_availability()内容，更改了方法名字 Added by 刘吉平 on 2017-12-13'''
        # print('_onchange_product_id_check_availability_odoo',self.env.context)
        if not self.product_id or not self.product_uom_qty or not self.product_uom:
            self.product_packaging = False
            return {}
        if self.product_id.type == 'product':
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            product = self.product_id.with_context(warehouse=self.order_id.warehouse_id.id)
            product_qty = self.product_uom._compute_quantity(self.product_uom_qty, self.product_id.uom_id)
            if float_compare(product.virtual_available, product_qty, precision_digits=precision) == -1:
                is_available = self._check_routing()
                if not is_available:
                    message = _('You plan to sell %s %s but you only have %s %s available in %s warehouse.') % \
                              (self.product_uom_qty, self.product_uom.name, product.virtual_available,
                               product.uom_id.name, self.order_id.warehouse_id.name)
                    # We check if some products are available in other warehouses.
                    if float_compare(product.virtual_available, self.product_id.virtual_available,
                                     precision_digits=precision) == -1:
                        message += _('\nThere are %s %s available accross all warehouses.') % \
                                   (self.product_id.virtual_available, product.uom_id.name)
                    warning_mess = {
                        'title': _('Not enough inventory!'),
                        'message': message
                    }
                    return {'warning': warning_mess}
        return {}

    @api.model
    def get_virtual_available_qdodoo(self, product_id, lot_id, warehouse_id):
        '''该仓库该批次产品的预测数量 Added by 刘吉平 on 2017-12-13'''
        if product_id and lot_id and warehouse_id:
            location = self.env['stock.warehouse'].browse(warehouse_id).lot_stock_id
            quants = self.env['stock.quant'].search([('product_id', '=', product_id),
                                                     ('lot_id', '=', lot_id),
                                                     ('location_id', 'child_of', location.id),])
            virtual_available = 0
            for quant in quants:
                virtual_available += quant.virtual_available
            return virtual_available

    @api.multi
    def check_lot_qdodoo(self):
        '''该产品该批次能否在该仓库中找到 Added by 刘吉平 on 2017-12-13'''
        if len(self) < 1:
            raise UserError(u'检查批次出现异常，len(self)<1')
        quant_obj = self.env['stock.quant']
        for line in self:
            product = line.product_id
            lot = line.lot_id
            warehouse = line.order_id.warehouse_id
            lot_stock_id = warehouse.lot_stock_id.id
            if product and lot and warehouse and lot_stock_id:
                result = quant_obj.search([('lot_id', '=', lot.id),
                                           ('product_id', '=', product.id),
                                           ('location_id', 'child_of', lot_stock_id),])
                if not result:
                    raise UserError(u'产品%s批次%s在仓库%s中没有找到' % (product.name, lot.name, warehouse.name))
            else:
                continue

    @api.model
    def create(self, vals):
        '''Added by 刘吉平 on 2017-12-13'''
        result = super(SaleOrderLine, self).create(vals)
        result.check_lot_qdodoo()
        return result

    @api.multi
    def write(self, vals):
        '''Added by 刘吉平 on 2017-12-13'''
        result = super(SaleOrderLine, self).write(vals)
        self.check_lot_qdodoo()
        return result

