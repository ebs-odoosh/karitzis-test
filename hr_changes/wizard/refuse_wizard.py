# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class RefuseWizard(models.TransientModel):
    _name = 'refuse.wizard'

    refusal_reasons = fields.Char('Reasons')

    def action_refuse(self):
        leave_id = self.env['hr.leave'].browse(
            self._context.get('active_id'))
        leave_id.refusal_reasons = self.refusal_reasons
        leave_id.action_refuse()
