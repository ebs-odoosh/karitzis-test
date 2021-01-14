# -*- coding: utf-8 -*-
# Copyright 2013 Guewen Baconnier, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields,api
from odoo.exceptions import UserError


class DocumentDocumentInherit(models.Model):
    _inherit = 'documents.document'

    document_category_id = fields.Many2one('document.category')


class DocumentCategory(models.Model):

    _name = 'document.category'

    name = fields.Char(string='Category Name', required=True)
