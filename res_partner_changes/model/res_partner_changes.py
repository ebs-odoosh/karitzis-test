# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api
from odoo.exceptions import UserError


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    def _get_default_credit_id(self):
        default_credit_id = self.env['partner.credit.dates'].search([('default_credit','=','True')],limit=1)
        if default_credit_id:
            return default_credit_id.id
        else:
            return

    partner_title = fields.Char()
    partner_no = fields.Char(string='Client NO.', readonly=False)
    origin = fields.Many2one('res.country', string='Origin')
    ubo_origin = fields.Many2one('res.country', string='UBO-Origin')
    id_number = fields.Char(string='ID Number')
    passport_no = fields.Char(string='Passport Number')
    registration_no = fields.Char(string='Registration Number')
    credit_days = fields.Float()
    tax_residency = fields.Many2one('res.country', string='TAX RESIDENCY',
                                    default=lambda self: self.env['res.country'].search([('name', '=', 'Cyprus')]).id)
    vat_no = fields.Char(string='VAT')
    email2 = fields.Char(string='Email2')
    company_email = fields.Char(string='Company Email')
    is_branch = fields.Boolean()
    register_seat = fields.Char()
    other_branches = fields.Char()
    related_departments = fields.Char()
    is_associate = fields.Boolean()
    other_associates = fields.Char()
    selected_eu_country = fields.Boolean(default=False)
    active_customer = fields.Selection([('yes', 'Yes'),('no', 'NO')], default='yes')
    is_company_related = fields.Boolean(related='parent_id.is_company')
    contact_telephone = fields.Char(string='Telephone No')
    contact_fax = fields.Char(string='FAX')
    facebook_account = fields.Char(string='Facebook Account')
    linkedin_account = fields.Char(string='linkedin Account')
    is_main_contact = fields.Boolean(string='Main Contact')
    contact_website = fields.Char('Website')
    firstname = fields.Char(string='First Name')
    surname = fields.Char(string='Surname')
    is_accounting_contact = fields.Boolean(string='Accounting Contact')
    commission = fields.Boolean(string='Commission')
    entitle_commission = fields.Char()
    commission_fix = fields.Float(string='Commission Fix ')
    fix_commission_amount = fields.Float()
    birth_date = fields.Date(string='Date of Birth')
    arc_no = fields.Char(string='ARC NO.')
    profession = fields.Char(string='Profession')
    employer = fields.Char(string='Employer')
    legal_fees_commission = fields.Char(string='Commission of Legal Fees %')
    credit_dates_id = fields.Many2one('partner.credit.dates', string='Credit Dates', default=_get_default_credit_id)
    billing_info = fields.Boolean(string='Billing Info')
    billing_name = fields.Char(string='Billing Name')
    billing_road = fields.Char(string='Road')
    billing_road_no = fields.Char(string='Road No')
    building = fields.Char('Building')
    building_no = fields.Char('Building NO')
    flat_no = fields.Char(string='Flat No')
    billing_city = fields.Char(string='City')
    billing_state_id = fields.Many2one('res.country.state',string='State')
    billing_zip = fields.Char(string='Zip')
    billing_country_id = fields.Many2one('res.country',string='Country')
    is_group = fields.Boolean(string='Is Group')

    #Contact Form Changes

    contact_type = fields.Char(string='Contact Type')
    contact_auto_numbering = fields.Char(string='Contact Auto Numbering')
    link_with_client = fields.Char()

    # @api.onchange('name', 'street', 'stree2', 'city', 'state_id', 'zip', 'country_id')
    # def _set_default_billing_data(self):
    #     for rec in self:
    #         rec.billing_name = rec.name
    #         rec.billing_street = rec.street
    #         rec.billing_street2 = rec.street2
    #         rec.billing_city = rec.city
    #         rec.billing_state_id = rec.state_id
    #         rec.billing_zip = rec.zip
    #         rec.billing_country_id = rec.country_id

    @api.onchange('origin')
    def _check_eu_country(self):
        # eu_countries = ['Australia', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus','Czechia', 'Italy',
        #                 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Estonia',
        #                 'Portugal', 'Finland', 'Romania', 'France', 'Slovakia', 'Germany', 'Slovenia', 'Greece'
        #                 'Spain', 'Hungary', 'Sweden', 'Ireland']

        for rec in self:
            if rec.origin.is_eu_country:
                rec.selected_eu_country = True
            else:
                rec.selected_eu_country = False

    @api.onchange('active_customer')
    def active_archive_customer(self):
        for rec in self:
            if rec.active_customer == 'yes':
                rec.active = True
            elif rec.active_customer == 'no':
                rec.active = False

    # @api.model
    # def create(self, vals):
    #     print(vals)
    #     if vals['is_company']:
    #         vals['client_no'] = 'C-'+self.env['ir.sequence'].next_by_code('company.seq') or 'New Company'
    #     elif not vals['is_company']:
    #         vals['client_no'] = 'I-' + self.env['ir.sequence'].next_by_code('individual.seq') or 'New Individual'
    #     result = super(ResPartnerInherit, self).create(vals)
    #     return result


