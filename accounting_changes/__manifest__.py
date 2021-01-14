
{
    'name': 'KARITZIS Accounting Changes',
    'version': '13.0.1.1.0',
    'author': 'Ever Business Solution',

    'category': 'Partner',
    'license': 'AGPL-3',
    'website': "https://www.everbsgroup.com/",
    'depends': ['account','sale'],
    'data': [
        'data/journal_entry_sequence.xml',
        'views/account_coa_changes.xml',
        'views/account_move_changes.xml',
        'report/karitzis_invoice_template_report.xml'
    ],
    'auto_install': False,
    'installable': True,
}
