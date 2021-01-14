# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api
from datetime import datetime , timedelta

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    surname = fields.Char(string='Surname')
    firstname = fields.Char(string='First Name')
    si_number = fields.Integer(string='SI number')
    tax_residency = fields.Many2one('res.country',string='TAX RESIDENCY',
                                    default=lambda self: self.env['res.country'].search([('name', '=', 'Cyprus')]).id)
    tax_number = fields.Char(string='TAX NUMBER')
    emergency_mobile = fields.Char(string='Emergency Mobile')
    approval_id = fields.Many2one('hr.employee',string='Approvals')
    certificate_char = fields.Char(string='Certificate Level')
    unique_code = fields.Char(string='Unique Code',readonly=True)
    employee_document_ids = fields.One2many('employee.document','employee_id')

    @api.model
    def create(self, values):
        if values.get('firstname') and values.get('surname'):
            values['name'] = values['firstname']+' '+values['surname']

        # values['unique_code'] = self.env['ir.sequence'].next_by_code('employee.code') or 'New Employee'
        employee = super(HrEmployeeInherit, self).create(values)
        return employee

    def write(self, vals):
        if vals.get('firstname') and vals.get('surname'):
            vals['name'] = vals['firstname']+' '+vals['surname']
        elif vals.get('firstname') and not vals.get('surname'):
            vals['name'] = vals['firstname'] + ' '+self.surname
        elif vals.get('surname') and not vals.get('firstname') :
            vals['name'] = self.firstname + ' '+vals['surname']
        res = super(HrEmployeeInherit, self).write(vals)
        return res


class EmployeeDocument(models.Model):
    _name = 'employee.document'

    document = fields.Binary(string='Document')
    file_name = fields.Char("File Name")
    document_type = fields.Selection([
        ('id_passport', 'ID/Passport'),
        ('resume', 'Resume'),
        ('bank_details', 'Bank Account Details'),
        ('seminars', 'Seminars'),
        ('professional_licenses', 'Professional Licenses'),
    ], string='Document Type')
    date_from = fields.Date(string='Date from')
    date_to = fields.Date(string='Date to')
    employee_id = fields.Many2one('hr.employee')

    @api.model
    def create(self, values):
        employee_document = super(EmployeeDocument, self).create(values)
        if employee_document:
            for document in employee_document:
                folder_id = self.env.ref('document_changes.documents_employees_folder').id
                document_vals = {
                    'name': document.file_name,
                    'datas': document.document,
                    'type': 'binary',
                    'create_uid': self.env.user.id or False,
                    'folder_id': 1
                }
                document = self.env['documents.document'].create(document_vals)
                print('Done')
        return employee_document
