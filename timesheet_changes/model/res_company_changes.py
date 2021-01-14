# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api
from datetime import datetime , timedelta , date

class AccountAnalyticLineInherit(models.Model):
    _inherit = 'res.company'


    def get_last_week_time_sheet(self,reminder):
        active_lang =self.env['res.lang'].search([('active', '=', True)], limit=1)
        day_name = dict(active_lang._fields['week_start'].selection).get(active_lang.week_start)
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        first_day_index = days.index(day_name)
        today = datetime.now().strftime("%A")
        # 1- Automatic first reminder: Every Friday at 20: 00 sent reminder to all employees to
        # finalise their timesheet of the week if they did not.
        # if today == ''

        today_index = days.index(today)
        delay = today_index - first_day_index
        if delay <= 0:
            delay += 7
        if reminder == 1:
            date_from = date.today() - timedelta(int(delay))
            date_to = date_from + timedelta(days=4)
        elif reminder == 2:
            date_from = date.today() - timedelta(days=8)
            date_to = date_from + timedelta(days=6)
        elif reminder == 3:
            date_from = date.today() - timedelta(days=11)
            date_to = date_from + timedelta(days=6)
        elif reminder == 4:
            date_from = date.today() - timedelta(days=14)
            date_to = date_from + timedelta(days=6)
        employee_ids = []
        for employee in self.env['hr.employee'].search([]):
            employee_time_sheet = self.search([
                ('employee_id', '=', employee.id),
                ('date', '>=', date_from),
                ('date', '<=', date_to),
                ('is_timesheet', '=', True)])
            total_hours = 0.0
            for line in employee_time_sheet:
                total_hours += (line.unit_amount)
            if total_hours < 40:
                employee_ids.append(employee)
        return employee_ids

    def _send_timesheet_reminders(self,date_start,date_end):
        employees = self.env['hr.employee'].search([])
        work_hours_struct = employees.get_timesheet_and_working_hours(date_start, date_end)
        for employee in employees:
            if employee.user_id and work_hours_struct[employee.id]['timesheet_hours'] < work_hours_struct[employee.id]['working_hours']:
                print(employee)
                self._cron_timesheet_send_reminder(
                    employee,
                    'timesheet_grid.mail_template_timesheet_reminder_user',
                    'hr_timesheet.act_hr_timesheet_line',
                    additionnal_values=work_hours_struct[employee.id],
                )

    def timesheet_send_first_reminder(self):
        # employee_ids = self.get_last_week_time_sheet(reminder=1)
        # for employee in employee_ids:
        #     template = self.env.ref('timesheet_changes.mail_template_timesheet_reminder')
        #     template.send_mail(employee.id, force_send=True,
        #                        email_values={'email_to': employee.work_email, 'subject': 'Time Sheet Reminder'},
        #                        notif_layout='mail.mail_notification_light')
        date_start = date.today() - timedelta(days=4)
        date_end = date.today()
        self._send_timesheet_reminders(date_start,date_end)
        return


    def timesheet_send_second_reminder(self):
        # employee_ids = self.get_last_week_time_sheet(reminder=2)
        # for employee in employee_ids:
        #     template = self.env.ref('timesheet_changes.mail_template_timesheet_reminder')
        #     template.send_mail(employee.id, force_send=True,
        #                        email_values={'email_to': employee.work_email, 'subject': 'Timesheet Second Reminder'},
        #                        notif_layout='mail.mail_notification_light')
        date_start = date.today() - timedelta(days=8)
        date_end = date.today() - timedelta(days=2)
        self._send_timesheet_reminders(date_start, date_end)
        return

    def action_pending_timesheet_send(self):
        # employee_ids = self.get_last_week_time_sheet(reminder=3)
        # if employee_ids:
        #     template = self.env.ref('timesheet_changes.mail_template_timesheet_pending')
        #     template.send_mail(1,force_send=True,
        #                        email_values={'subject': 'Pending Timesheet'},
        #                        notif_layout='mail.mail_notification_light')
        date_start = date.today() - timedelta(days=11)
        date_end = date.today() - timedelta(days=5)
        employees = self.env['hr.employee'].search([])
        work_hours_struct = employees.get_timesheet_and_working_hours(date_start, date_end)
        delayed_employees = []
        for employee in employees:
            if employee.user_id and work_hours_struct[employee.id]['timesheet_hours'] < work_hours_struct[employee.id]['working_hours']:
                delayed_employees.append(employee)
                if delayed_employees:
                    template = self.env.ref('timesheet_changes.mail_template_timesheet_pending')
                    template_ctx = {'date_start': date_start,
                                    'date_end': date_end ,
                                    }
                    template.with_context(**template_ctx).send_mail(1)


    def action_outstanding_timesheet_send(self):
        date_start = date.today() - timedelta(days=14)
        date_end = date_start + timedelta(days=6)
        employees = self.env['hr.employee'].search([])
        work_hours_struct = employees.get_timesheet_and_working_hours(date_start, date_end)
        print(work_hours_struct)
        delayed_employees = []
        for employee in employees:
            if employee.user_id and work_hours_struct[employee.id]['timesheet_hours'] < work_hours_struct[employee.id]['working_hours']:
                delayed_employees.append(employee)
                if delayed_employees:
                    print(delayed_employees)
                    template = self.env.ref('timesheet_changes.mail_template_timesheet_outstanding')
                    template_ctx = {'date_start': date_start,
                                    'date_end': date_end,
                                    }
                    template.with_context(**template_ctx).send_mail(1)

    def _get_pending_time_sheet(self):
        date_start = date.today() - timedelta(days=8)
        date_end = date.today() - timedelta(days=2)
        employees = self.env['hr.employee'].search([])
        work_hours_struct = employees.get_timesheet_and_working_hours(date_start, date_end)
        time_sheet = []
        for employee in employees:
            if employee.user_id and work_hours_struct[employee.id]['timesheet_hours'] < work_hours_struct[employee.id]['working_hours']:
                time_sheet.append((employee.name,work_hours_struct[employee.id]['timesheet_hours']))
        data = {
            'date_from': date_start,
            'date_to': date_end,
            'timesheet': time_sheet
        }
        return data

    def _get_outstanding_time_sheet(self):
        date_start = date.today() - timedelta(days=14)
        date_end = date_start + timedelta(days=6)
        employees = self.env['hr.employee'].search([])
        work_hours_struct = employees.get_timesheet_and_working_hours(date_start, date_end)
        time_sheet = []
        for employee in employees:
            if employee.user_id and work_hours_struct[employee.id]['timesheet_hours'] < work_hours_struct[employee.id]['working_hours']:
                time_sheet.append((employee.name, work_hours_struct[employee.id]['timesheet_hours']))
        data = {
            'date_from': date_start,
            'date_to': date_end,
            'timesheet': time_sheet
        }

        return data
