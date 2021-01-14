# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api
from datetime import datetime , timedelta , date

class AccountAnalyticLineInherit(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def create(self, vals):
        # if not vals.get('project_id') and not vals.get('name'):
        #     vals['name'] = '/'
        if vals.get('unit_amount'):
            amount = vals['unit_amount'] * 4
            if 1.00 >= amount > 0.00:
                vals['unit_amount'] = 0.25
            elif amount > 1.00:
                decimal_part = (amount - int(amount))
                if decimal_part >= 0.5:
                    amount = int(amount)+1
                    vals['unit_amount'] = amount/4
                elif decimal_part < 0.5 :
                    amount = int(amount)
                    vals['unit_amount'] = amount / 4
        result = super(AccountAnalyticLineInherit, self).create(vals)
        return result
