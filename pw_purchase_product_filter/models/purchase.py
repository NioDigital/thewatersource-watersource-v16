# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = super(PurchaseOrderLine, self).onchange_product_id()
        if not self.order_id.partner_id:
            return result
        if self.order_id.partner_id.product_filter:
            supplier_infos = self.env['product.supplierinfo'].search([('partner_id', '=', self.order_id.partner_id.id)])
            product_ids = self.env['product.product']
            for supplier_info in supplier_infos:
                 product_ids += supplier_info.product_tmpl_id.product_variant_ids
            if result:
                result.update({'domain': {'product_id': [('id', 'in', product_ids.ids)]}})
            return {'domain': {'product_id': [('id', 'in', product_ids.ids)]}}
        return result
