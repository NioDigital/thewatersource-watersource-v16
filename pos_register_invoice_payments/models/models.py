# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
from odoo import api, models
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def wk_register_invoice_payment(self, kwargs):
        if(kwargs.get('invoice_id')):
            invoice = self.browse(kwargs.get('invoice_id'))

            journal_id = self.env['account.journal'].search(
                [('id', '=', kwargs.get('journal_id'))])
            available_payment_methods = journal_id.inbound_payment_method_line_ids
            payment_method_line_id = False
            if available_payment_methods:
                payment_method_line_id = available_payment_methods[0].id

            payment_vals = {
                'amount': kwargs.get('amount'),
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'ref': kwargs.get('payment_memo') or '',
                'journal_id': kwargs.get('journal_id'),
                'currency_id': invoice.currency_id.id,
                'partner_id': invoice.partner_id.id,
                'partner_bank_id': False,
                'payment_method_line_id': payment_method_line_id,
                'write_off_line_vals': {}
            }
            payment_id = self.env['account.payment'].create([payment_vals])

            if payment_id:
                payment_id.action_post()
                line_id = False
                for line in payment_id.line_ids:
                    line_id = line.id
                if line_id:
                    self.wk_assign_outstanding_credit_current(
                        invoice.id, line_id)

            return {
                'residual': invoice.amount_residual,
                'state': invoice.state,
            }

    def wk_assign_outstanding_credit_current(self, invoice_id, line_id):
        invoice = self.env['account.move'].search([('id', '=', invoice_id)])
        if invoice:
            lines = self.env['account.move.line'].browse(line_id)
            lines += invoice.line_ids.filtered(
                lambda line: line.account_id == lines[0].account_id and not line.reconciled)
            wk_register = invoice.js_assign_outstanding_line(line_id)
            if(wk_register):
                return invoice.read(['invoice_outstanding_credits_debits_widget', 'invoice_payments_widget', 'state', 'amount_total', 'amount_residual'])
            else:
                return False

    def wk_assign_outstanding_credit(self, line_id):
        self.ensure_one()
        _logger.info("self-------------------------%r-------------------",self)
        _logger.info("line_id-------------------------%r-------------------",line_id)
        wk_register = self.js_assign_outstanding_line(line_id)
        if(wk_register):
            return self.read(['invoice_outstanding_credits_debits_widget', 'invoice_payments_widget', 'state', 'amount_total', 'amount_residual'])
        else:
            return False

    @api.model
    def enable_accounting_group(self):
        try:
            self.env.ref('account.group_account_user').write(
                {'users': [(4, self.env.ref('base.user_admin').id)]})
        except Exception as e:
            _logger.info("*****************Exception**************", e)

    def wk_js_remove_outstanding_partial(self, partial_id):
        self.ensure_one()
        _logger.info("self----------------------:%r",self)

        partial = self.env['account.partial.reconcile'].browse(partial_id)
        _logger.info("partial----------------------:%r",partial)
        return partial.unlink()
        self.ensure_one()
        partial = self.env['account.partial.reconcile'].browse(partial_id)
        return partial.unlink()


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_account_journal(self):
        return {"search_params": {
            "fields": [],
            "domain": [('company_id', '=', self.company_id.id), ('type', 'in', ['bank', 'cash'])]
        }}

    def _get_pos_ui_account_journal(self, params):
        return self.env["account.journal"].search_read(**params["search_params"])

    def _pos_ui_models_to_load(self):
        models = super()._pos_ui_models_to_load()
        if "account.journal" not in models:
            models.append("account.journal")
        return models

    # def _loader_params_account_move(self):
    #     result = super()._loader_params_account_move()
    #     result['search_params']['fields'].append('payment_id')
    #     return result
