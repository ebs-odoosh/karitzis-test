# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api
from odoo.exceptions import UserError


class PartnerCreditDates(models.Model):
    _name = 'partner.credit.dates'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    default_credit = fields.Boolean('Default')
