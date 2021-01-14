# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api


class AccountAnalyticLineInherit(models.Model):
    _inherit = 'account.analytic.line'

    project_id = fields.Many2one('project.project', domain='_get_customer_related_projects')
    timesheet_category_id = fields.Many2one('timesheet.category',string='Timesheet Category')
    partner_id = fields.Many2one('res.partner',string='Customer')

    @api.onchange('partner_id')
    def _get_customer_related_projects(self):
        project_obj = self.env['project.project']
        if self.partner_id:
            print(self.project_id.partner_id)
            print(self.partner_id.id)
            if self.project_id.partner_id.id != self.partner_id.id:
                self.project_id = False
            related_projects = project_obj.search([('partner_id', '=', self.partner_id.id)])
            domain = {'project_id': [('id', 'in', [p.id for p in related_projects])]}
            return {'domain': domain}
        elif not self.partner_id:
            related_projects = project_obj.search([])
            domain = {'project_id': [('id', 'in', [p.id for p in related_projects])]}
            return {'domain': domain}


    @api.onchange('project_id')
    def _get_related_customer(self):
        if self.project_id:
            self.partner_id = self.project_id.partner_id.id
        else:
            self.partner_id = False
