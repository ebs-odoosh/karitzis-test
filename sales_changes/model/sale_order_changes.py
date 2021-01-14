# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api
from odoo.exceptions import UserError

class SAleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def action_quotation_send_proforma(self):

        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self.env.ref('sales_changes.mail_template_sale_confirmation_pro_forma').id
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_template(template.lang, 'sale.order', self.ids[0])
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def _get_bank_accounts(self):
        print("EEEEEEEEEEEEEEEEEEEEEE")
        bank_accounts = self.env['res.partner.bank'].search([])
        return bank_accounts
#     def _find_mail_template(self, force_confirmation_template=False):
#         template_id = False
#
#         if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
#             template_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_confirmation_template'))
#             template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
#             if not template_id:
#                 template_id = self.env['ir.model.data'].xmlid_to_res_id('sale.mail_template_sale_confirmation',
#                                                                         raise_if_not_found=False)
#         if not template_id:
#             template_id = self.env['ir.model.data'].xmlid_to_res_id('sales_changes.mail_template_sale_confirmation_pro_forma',
#                                                                     raise_if_not_found=False)

        # return template_id

class SAleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    fee = fields.Float()

