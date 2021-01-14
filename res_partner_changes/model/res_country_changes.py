# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api
from odoo.exceptions import UserError


class ResCountryInherit(models.Model):
    _inherit = 'res.country'

    is_eu_country = fields.Boolean(string='Eu Country')
