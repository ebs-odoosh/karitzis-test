
{
    'name': 'KARITZIS Partner Changes',
    'version': '13.0.1.1.0',
    'author': 'Ever Business Solution',
    'category': 'Partner',
    'license': 'AGPL-3',
    'website': "https://www.everbsgroup.com/",
    'depends': ['base','account'],
    'data': [
        'security/ir.model.access.csv',
        'data/client_sequence.xml',
        'view/res_partner_form_view_changes.xml',
        'view/res_country_form_view_changes.xml',
        'view/res_partner_bank_form_view_changes.xml'
    ],
    'auto_install': False,
    'installable': True,
}
