from odoo import fields, models, api, exceptions , _
from datetime import timedelta , date ,datetime
import json,requests
from odoo.exceptions import UserError, ValidationError

class MfilesIntegration(models.Model):

    _name = 'mfiles.integration'
    _rec_name = 'integration_date'

    integration_date = fields.Datetime()
    object_type = fields.Selection([
        ('employee', 'Employee'),
        ('client', 'Client'),
        ('supplier', 'Supplier'),
        ('case', 'Case'),
        ('bank_account', 'Bank Account'),
        ('other_contact', 'other Contact'),
    ])
    response_status = fields.Char()
    error_msg = fields.Text()
    object_ids = fields.One2many('mfiles.objects.log','integration_id')

    def _auth(self):
        auth_token = self.env['ir.config_parameter'].sudo().get_param('auth_token') or False
        if auth_token:
            headers = {
                'Content-type': 'application/json',
                'X-Authentication': auth_token,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'Connection': 'Keep-Alive',
                'Cache-Control': 'no-cache',
            }
        base_url = self.env['ir.config_parameter'].sudo().get_param('base_url') or False
        if auth_token and base_url:
            data = {'headers': headers, 'base_url': base_url}
            return data
        else:
            raise ValidationError('You Have To Set URL Or Make Sure That Auth Token is Set before Running Integration')

    def create_record_log(self, record_type):
        # log = self.env['mfiles.integration.log'].create()
        record_log = self.env['mfiles.integration'].create({
            'integration_date': datetime.now(),
            'object_type': record_type,
            'response_status': 'OK'
        })
        return record_log

    def _log_result(self, result, obj, object_type):
        record_log = self.create_record_log(record_type=object_type)
        for record in result:
            log_line =  self.env['mfiles.objects.log'].create({
                'integration_id': record_log.id ,
                'mfiles_id': record.id,
                'object_state': '',
                'error_msg': ''
                })
            try:
                #     try to create odoo object from mfiles data
                vals = {}
                employee = self.env[obj].create(vals)
            except Exception as E:
                log_line.object_state = 'Failed'
                log_line.error_msg = str(E)
        # if result.reason == 'OK':
        #     record_log.log_id.integration_status = result.reason
        # else:
        #     record_log.log_id.integration_status = result.reason
        #     record_log.log_id.error_msg = str(result.content.decode())

    # Bank_Account - 129
    # Case - 121
    # Client - 101
    # Employee - 109
    # Other Contact - 108
    # Supplier - 111

    def get_last_employees_data(self):
        obj = 'hr.employee'
        object_type = 'employee'
        result = self.env['hr.employee'].search([], limit=3)
        self._log_result(result, obj, object_type)
        # connection = self._auth()
        # if connection['base_url'] and connection['headers']['X-Authentication']:
        #     result = requests.get(''.join((connection['base_url'], 'o=109')), headers =connection['headers'])
        #     self._log_result(result, object_type)

    def get_last_clients_data(self):
        object_type = 'client'
        connection = self._auth()
        if connection['base_url'] and connection['headers']['X-Authentication']:
            result = requests.get(''.join((connection['base_url'], 'o=101')), headers=connection['headers'])
            self._log_result(result, object_type)

    def get_last_suppliers_data(self):
        object_type = 'supplier'
        connection = self._auth()
        if connection['base_url'] and connection['headers']['X-Authentication']:
            result = requests.get(''.join((connection['base_url'], 'o=111')), headers=connection['headers'])
            self._log_result(result, object_type)

    def get_last_cases_data(self):
        object_type = 'case'
        connection = self._auth()
        if connection['base_url'] and connection['headers']['X-Authentication']:
            result = requests.get(''.join((connection['base_url'], 'o=121')), headers=connection['headers'])
            self._log_result(result, object_type)

    def get_last_bank_accounts_data(self):
        object_type = 'bank_account'
        connection = self._auth()
        if connection['base_url'] and connection['headers']['X-Authentication']:
            result = requests.get(''.join((connection['base_url'], 'o=129')), headers=connection['headers'])
            self._log_result(result, object_type)

    def get_other_contact_data(self):
        object_type = 'other_contact'
        connection = self._auth()
        if connection['base_url'] and connection['headers']['X-Authentication']:
            result = requests.get(''.join((connection['base_url'], 'o=108')), headers=connection['headers'])
            self._log_result(result, object_type)


class MfilesObjectsLog(models.Model):
    _name = 'mfiles.objects.log'

    integration_id = fields.Many2one('mfiles.integration')
    mfiles_id = fields.Char('Mfiles ID')
    object_state  = fields.Char('State')
    error_msg = fields.Text()


