# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api
from odoo.exceptions import UserError


class ProjectProjectInherit(models.Model):
    _inherit = 'project.project'

    case_title = fields.Char()
    type_of_service = fields.Char()
    type_of_case = fields.Char()
    sub_type_of_case = fields.Char()
    case_no = fields.Char()
    partner_id = fields.Many2one('res.partner',domain="[('customer_rank', '=', 1)]")
    court = fields.Char()
    judge = fields.Char()
    primary_representative = fields.Char()
    other_representatives = fields.Char()
    administration_employee = fields.Many2one('hr.employee')
    engagement_letter = fields.Char()
    legal_fees_agreed = fields.Float()
    discount_agreed = fields.Float()
    estimated_days = fields.Float(string='Estimated Days for Completion')
    date_closed = fields.Date()
    file_type = fields.Char()
    storage_place = fields.Char(strung='Place of Storage')
    repeating = fields.Selection([('recurring', 'Recurring'), ('once_off', 'Once Off')])
    notes = fields.Char()