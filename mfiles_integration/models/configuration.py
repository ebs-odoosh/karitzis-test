
from odoo import fields, models, api, exceptions , _
import json,requests
from odoo.exceptions import UserError, ValidationError
class MfilesConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    auth_url = fields.Char('Auth URL', default='http://172.16.100.4:8090/REST/server/authenticationtokens.aspx',required=True)
    auth_user_name = fields.Char('Auth User Name', default='Odoo',  required=True)
    auth_password = fields.Char('Auth Password', default='Odoo12345', required=True)
    auth_valutGuid = fields.Char('Auth ValutGuid',default='{407A4654-ABB8-4CAA-9E95-E36C47E48C55}',required=True)
    auth_token = fields.Char(string='Auth Token')
    auth_state = fields.Char(string='Auth State')
    base_url = fields.Char('Base Url', default='http://172.16.100.4:8090/REST/objects.aspx?',required=True)
    url_params = fields.Char('URL Params')
    mfiles_result = fields.Text('Mfiles Result')

    @api.model
    def get_values(self):
        res = super(MfilesConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            auth_url=get_param('auth_url'),
            auth_user_name=get_param('auth_user_name'),
            auth_password=get_param('auth_password'),
            auth_valutGuid=get_param('auth_valutGuid'),
            auth_token=get_param('auth_token'),
            base_url=get_param('base_url'),
            url_params=get_param('url_params'),
            mfiles_result=get_param('mfiles_result'),
        )
        return res

    def set_values(self):
        super(MfilesConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('auth_url', (self.auth_url or ''))
        set_param('auth_user_name', (self.auth_user_name or '').strip())
        set_param('auth_password', (self.auth_password or '').strip())
        set_param('auth_valutGuid', (self.auth_valutGuid or '').strip())
        set_param('auth_token', (self.auth_token or '').strip())
        set_param('base_url', (self.base_url or '').strip())
        set_param('url_params', (self.url_params or '').strip())
        set_param('mfiles_result', (self.mfiles_result or '').strip())

    def get_auth_token(self):
        data = json.dumps({"Username": self.auth_user_name, "Password": self.auth_password,
                           "VaultGuid": self.auth_valutGuid})
        res = requests.post(self.auth_url, data=data)
        self.env['ir.config_parameter'].sudo().set_param('auth_state', res.reason)
        self.env['ir.config_parameter'].sudo().set_param('auth_token', res.text[10:-2])

    def run_integrate(self):
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
        url_params = self.env['ir.config_parameter'].sudo().get_param('url_params') or False
        if base_url and url_params:
            print(''.join((base_url, url_params)))
            obj = requests.get(''.join((base_url, url_params)), headers=headers)
            self.env['ir.config_parameter'].sudo().set_param('mfiles_result', str(obj.content.decode()))
        else:
            raise ValidationError('You Have To Set URL and Parameters before Running Integration')