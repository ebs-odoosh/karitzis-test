# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api ,_
from odoo.exceptions import Warning, UserError
import warnings
class HrLeaveAllocationInherit(models.Model):
    _inherit = 'hr.leave.allocation'

    # is_first_approver = fields.Boolean(compute='_check_approvers')
    #
    # def _check_approvers(self):
    #     current_employee = self.env.user.employee_id
    #     if self.holiday_status_id.validation_type == 'static_validation':
    #         first_approver = self.holiday_status_id.responsible_id
    #         if current_employee == first_approver:
    #             self.is_first_approver = True
    #         else:
    #             self.is_first_approver = False
    #     else:
    #         self.is_first_approver = False

    def action_approve(self):
        # if validation_type == 'both': this method is the first approval approval
        # if validation_type != 'both': this method calls action_validate() below
        if any(holiday.state != 'confirm' for holiday in self):
            raise UserError(_('Allocation request must be confirmed ("To Approve") in order to approve it.'))

        current_employee = self.env.user.employee_id
        if self.holiday_status_id.validation_type != 'static_validation':
            self.filtered(lambda hol: hol.validation_type == 'both').write(
                {'state': 'validate1', 'first_approver_id': current_employee.id})
            self.filtered(lambda hol: not hol.validation_type == 'both').action_validate()
            self.activity_update()
        elif self.holiday_status_id.validation_type == 'static_validation':
            if self.state == 'confirm' and current_employee == self.holiday_status_id.responsible_id.employee_id:
                self.write({'state': 'validate1', 'first_approver_id': current_employee.id})
            elif self.state == 'confirm' and current_employee != self.holiday_status_id.responsible_id.employee_id:
                raise Warning('Only Employee Responsible for this type of Allocation Can Approve it')

    def action_validate(self):
        current_employee = self.env.user.employee_id
        for holiday in self:
            if holiday.holiday_status_id.validation_type != 'static_validation':
                if holiday.state not in ['confirm', 'validate1']:
                    raise UserError(_('Allocation request must be confirmed in order to approve it.'))

                holiday.write({'state': 'validate'})
                if holiday.validation_type == 'both':
                    holiday.write({'second_approver_id': current_employee.id})
                else:
                    holiday.write({'first_approver_id': current_employee.id})

                holiday._action_validate_create_childs()
            elif holiday.holiday_status_id.validation_type == 'static_validation':
                if self.state == 'validate1' and current_employee == self.holiday_status_id.approval_manager.employee_id:
                    holiday.write({'state': 'validate'})
                    if holiday.validation_type == 'both':
                        holiday.write({'second_approver_id': current_employee.id})
                    else:
                        holiday.write({'first_approver_id': current_employee.id})
                elif self.state == 'validate1' and current_employee != self.holiday_status_id.approval_manager.employee_id:
                    raise Warning('Only Approval Manager Responsible for this type of Allocation Can Validate it')
        self.activity_update()
        return True
