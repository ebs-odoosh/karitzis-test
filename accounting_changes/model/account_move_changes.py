# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api
from odoo.exceptions import UserError


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    journal_entry_no = fields.Char(string='Journal NO.', readonly=True)

    @api.model
    def create(self, vals):
        vals['journal_entry_no'] = self.env['ir.sequence'].next_by_code('journal_entry.seq') or 'New Journal'
        result = super(AccountMoveInherit, self).create(vals)
        return result


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    fee = fields.Float()