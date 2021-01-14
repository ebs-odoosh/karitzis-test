# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api
from odoo.exceptions import UserError


class ResPartnerBankInherit(models.Model):
    _inherit = 'res.partner.bank'

    iban = fields.Char(string='IBAN')