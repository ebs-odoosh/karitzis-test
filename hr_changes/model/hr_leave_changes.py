# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api ,_
from odoo.exceptions import UserError
from datetime import datetime , timedelta

class HrLeaveInherit(models.Model):
    _inherit = 'hr.leave'

    surname = fields.Char(string='Surname')
    si_number = fields.Integer(string='SI number')
    # employee_document_ids = fields.One2many('employee.document','employee_id')
    doctor_certificate = fields.Binary(string='Doctor Certificate')
    is_sick_leave = fields.Boolean(related='holiday_status_id.is_sick_leave_type')
    other_leaves = fields.Integer(string='Other Simultaneous Leaves', compute='_get_other_leaves')
    employee_related_department = fields.Many2one('hr.department', related='employee_id.department_id')
    refusal_reasons = fields.Char(string='Refusal Reasons')

    @api.onchange('state')
    def _get_other_leaves(self):
        for record in self:
            if record.employee_id and record.employee_related_department:
                other_leaves = self.env['hr.leave'].search([
                    ('state', '=', 'validate'),
                    ('employee_related_department', '=', record.employee_related_department.id)])
                other_leaves_in_date = []
                if other_leaves:
                    for leave in other_leaves:
                        # (t1start <= t2start <= t1end) or (t2start <= t1start <= t2end)
                        if leave.id != record.id:
                            if (record.request_date_from <= leave.request_date_from <= record.request_date_to) or \
                                    (leave.request_date_from <= record.request_date_from <= leave.request_date_to):
                                other_leaves_in_date.append(leave)
                                record.other_leaves = len(other_leaves_in_date)
                            else:
                                record.other_leaves = len(other_leaves_in_date)
                else:
                    record.other_leaves = 0
            else:
                record.other_leaves = 0

    def action_confirm(self):
        for leave in self:
            if leave.other_leaves > 0:
                action = self.env.ref('hr_changes.'
                                      'action_hr_leave_warning_reason_wizard').read()[0]
                action['views'] = [(self.env.ref(
                    'hr_changes.hr_leave_warning_reason_wizard_form_view').id, 'form')]
                return action
            else:
                super(HrLeaveInherit, self).action_confirm()

    def action_approve(self):
        for leave in self:
            if leave.other_leaves > 0:
                action = self.env.ref('hr_changes.'
                                      'action_hr_leave_warning_reason_wizard').read()[0]
                action['views'] = [(self.env.ref(
                    'hr_changes.hr_leave_warning_reason_wizard_form_view').id, 'form')]
                return action
            else:
                super(HrLeaveInherit, self).action_approve()

    def open_refuse_wizard(self):
        action = self.env.ref('hr_changes.'
                              'action_refuse_reason_wizard').read()[0]
        action['views'] = [(self.env.ref(
            'hr_changes.refuse_reason_wizard_form_view').id, 'form')]
        return action
            # @api.model
    # def create(self, values):
    #     leaves = super(HrLeaveInherit, self).create(values)
    #     return leaves

    # Override default create function to check if there is a global time of at the day of
    # the time off the user want to create or not
    # Note !! the time of date_from and date_to im global time off is reduced by 3 hours
    # by odoo !!! so we add these two hours to both fields before we compare between dates in
    # global time off and time off user want to create

    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            start_date = datetime.strptime(vals.get('request_date_from'), '%Y-%m-%d')
            end_date = datetime.strptime(vals.get('request_date_to'), '%Y-%m-%d')
            # print(start_date)
            # print(end_date)
            employee_id = self.env['hr.employee'].browse(vals['employee_id'])
            global_times = employee_id.resource_calendar_id.global_leave_ids
            # start = 2 end = 5
            # global 3====>6
            # start = 4 end= 5
            # print("-----------------",global_times[0].date_from+timedelta(hours=2))
            # print("-----------------",global_times[0].date_to+timedelta(hours=2))

            for public_holiday in global_times:
                if (start_date <= public_holiday.date_from+timedelta(hours=2) <= end_date) or \
                        (start_date <= public_holiday.date_to+timedelta(hours=2)<= end_date) or \
                        (start_date >= public_holiday.date_from+timedelta(hours=2) and end_date <= public_holiday.date_to+timedelta(hours=2)):
                    reason = public_holiday.name
                    date = public_holiday.date_from+timedelta(hours=2)
                    raise UserError(_("This Time Off is conflicting with %s Public holiday , on the same time off date")% (reason))

            time_off = super(HrLeaveInherit, self).create(vals)
            return time_off
