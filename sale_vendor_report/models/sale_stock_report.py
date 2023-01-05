from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError

class VendorReportWizard(models.TransientModel):
    _name = 'vendor.report.wizard'

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To") 
    vendor_ids = fields.Many2many('res.partner',string="Vendor")

    def vendor_filter_report(self):
        purchase = False
        sale = False
        vals = []
        remove_vals = self.env['vendor.filter.report'].sudo().search([])
        remove_vals.unlink()
        incoming_pick = self.env['stock.picking.type'].search([('code','=','incoming'),('sequence_code','=','IN')])
        print(incoming_pick,'incoming_pickincoming_pick')
        outgoing_pick = self.env['stock.picking.type'].search([('code','=','outgoing'),('sequence_code','=','OUT')])
        print(outgoing_pick,'----------------------')
        if self.date_from and self.date_to:
            if self.date_to < self.date_from:
                raise UserError(_('Please give the valid date'))
            if self.vendor_ids:
                purchase = self.env['stock.picking'].sudo().search([('picking_type_id','in',incoming_pick.ids),('scheduled_date','>=',self.date_from),('scheduled_date','<=',self.date_to),('partner_id','in',self.vendor_ids.ids)])
                sale = self.env['stock.picking'].sudo().search([('picking_type_id','in',outgoing_pick.ids),('scheduled_date','>=',self.date_from),('scheduled_date','<=',self.date_to),('partner_id','in',self.vendor_ids.ids)])
                print('if conditionnnnnnnnnnnn',purchase,'purchase',sale,'sale')
            else:
                purchase = self.env['stock.picking'].sudo().search([('picking_type_id','in',incoming_pick.ids),('scheduled_date','>=',self.date_from),('scheduled_date','<=',self.date_to)])
                sale = self.env['stock.picking'].sudo().search([('picking_type_id','in',outgoing_pick.ids),('scheduled_date','>=',self.date_from),('scheduled_date','<=',self.date_to)])
                print('elseeeeeeeee conditionnnnnnnnnnnn',purchase,'purchase',sale,'sale')
        else:
            purchase = self.env['stock.picking'].sudo().search([(('picking_type_id','in',incoming_pick.ids))])
            sale = self.env['stock.picking'].sudo().search([(('picking_type_id','in',outgoing_pick.ids))])
            print('noooo conditionnnnnnnnnnnn',purchase,'purchase',sale,'sale')
        
        if purchase:
            for loop in purchase:
                for lines in loop.move_ids_without_package:
                    print(loop.partner_id.id,'loop.partner_id.idloop.partner_id.id',lines.product_id.seller_ids.ids)
                    # and (loop.partner_id.id in lines.product_id.seller_ids.ids)
                    if lines.product_id.seller_ids : 
                        lst = {
                        'vendor':loop.partner_id.name,
                        'product_id':lines.product_id.name,
                        'purchase_qty': lines.product_id.purchased_product_qty,
                        'onhand':lines.product_id.qty_available,
                        'sale_qty':lines.product_id.sales_count
                        }
                        vals.append(lst)
            print('purchaseeee valsssssssssssss',vals)
        # if sale:
        #     for loop1 in sale:
        #         for lines2 in loop1.move_ids_without_package:
        #             for val_lst in vals:
        #                 if val_lst['product_id']==lines2.product_id.name:
        #                     val_lst['sale_qty']+=lines2.quantity_done
        #     print('final lst',vals)


        for lst in vals:
            rec = self.env['vendor.filter.report'].sudo().create(lst)
        view_id = self.env.ref('sale_vendor_report.sale_vendor_report_tree').id
        print(view_id,'=====================')
        return({
            "name":_('Vendor Filter Report'),
            'type': 'ir.actions.act_window',
            "res_model":'vendor.filter.report',
            "view_mode":'tree',
            "view_id":view_id,
            'target':'current'
            })

class VendorReport(models.TransientModel):
    _name = 'vendor.filter.report'

    vendor = fields.Char(string="Vendor Name") 
    product_id = fields.Char(string="Product")
    purchase_qty = fields.Float(string="Purchased Qty")
    sale_qty = fields.Float(string="Quantity Sold")
    onhand = fields.Float(string="Onhand")
    purchase_price = fields.Float(string="Purchase Price")
    sale_price = fields.Float(string="Sale Price")