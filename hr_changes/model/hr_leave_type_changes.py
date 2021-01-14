# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api
from datetime import datetime , timedelta

class HrLeaveTypeInherit(models.Model):
    _inherit = 'hr.leave.type'

    annual_leave = fields.Boolean('Is Annual Leave')
    validation_type = fields.Selection(selection_add=[('static_validation', 'Static Validation')])
    approval_manager = fields.Many2one('res.users',string='Approval Manager')
    is_sick_leave_type = fields.Boolean(string='Is Sick Leave')

    def action_annual_leave_auto_create(self):
        annual_leave_types = self.search([('annual_leave', '=', True)],limit=1)
        vals = {
            'name': 'Carry Forward Balance of :'+str(datetime.now().strftime('%Y')),
            'request_unit': 'day',
            'validation_type': annual_leave_types.validation_type,
            'allocation_type': 'fixed',
            'validity_start': datetime.now().strftime('%Y-%m-%d'),
            'validity_stop': (datetime.now()+timedelta(days=90)).strftime('%Y-%m-%d')
        }
        time_off_type_id = self.env['hr.leave.type'].create(vals)
        employees = self.env['hr.employee'].search([])
        for employee in employees:
            employee_previous_annual_leaves = self.env['hr.leave.report'].search([
                ('employee_id', '=', employee.id),
                ('is_annual', '=', True),
                ('valid', '=', True)
            ])
            if employee_previous_annual_leaves:
                previous_balance = 0.00
                for leave in employee_previous_annual_leaves:
                    previous_balance += leave.number_of_days
                if previous_balance > 0.00:
                    allocation_vals = {
                        'name': 'Carry Forward Allocation',
                        'holiday_status_id': time_off_type_id.id,
                        'allocation_type': 'regular',
                        'holiday_type': 'employee',
                        'employee_id': employee.id,
                        'number_of_days': previous_balance
                    }
                    allocation = self.env['hr.leave.allocation'].create(allocation_vals)



class HrLeaveReportInherit(models.Model):
    _inherit = 'hr.leave.report'

    is_annual = fields.Boolean(related='holiday_status_id.annual_leave')
    valid = fields.Boolean(related='holiday_status_id.valid')