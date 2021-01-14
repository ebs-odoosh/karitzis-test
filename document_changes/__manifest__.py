
{
    'name': 'KARITZIS Documents Changes',
    'version': '13.0.1.1.0',
    'author': 'Ever Business Solution',

    'category': 'Partner',
    'license': 'AGPL-3',
    'website': "https://www.everbsgroup.com/",
    'depends': ['documents'],
    'data': [
        'security/ir.model.access.csv',
        'data/documents_folder_data.xml',
        'view/document_document_form_changes.xml',
    ],
    'auto_install': False,
    'installable': True,
}
