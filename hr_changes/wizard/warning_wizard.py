# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class LeaveWarningWizard(models.TransientModel):
    _name = 'hr.leave.warning.wizard'

    def action_confirm(self):
        leave_id = self.env['hr.leave'].browse(
            self._context.get('active_id'))
        leave_id.action_confirm()

    def action_refuse(self):
        leave_id = self.env['hr.leave'].browse(
            self._context.get('active_id'))
        leave_id.action_refuse()
