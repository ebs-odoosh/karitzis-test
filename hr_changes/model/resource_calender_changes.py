# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api ,_

class ResourceCalenderInherit(models.Model):
    _inherit = 'resource.calendar'

    total_working_hours = fields.Float('Total Hours/Week')

    @api.depends('attendance_ids.hour_to','attendance_ids.hour_from')
    @api.onchange('attendance_ids')
    def _get_total_hours_per_week(self):
        print("Entered ................")
        for record in self:
            if record.attendance_ids:
                print(record.attendance_ids)
                total_hours = 0
                for line in record.attendance_ids:
                    duration = abs(line.hour_to - line.hour_from)
                    total_hours += duration
                    print(total_hours)
                record.total_working_hours = total_hours
                break
            else:
                print('55555555555')
                record.total_working_hours = 0.0
