
{
    'name': 'KARITZIS Timesheet Changes',
    'version': '13.0.1.1.0',
    'author': 'Ever Business Solution',
    'category': 'Partner',
    'license': 'AGPL-3',
    'website': "https://www.everbsgroup.com/",
    'depends': ['analytic','hr_timesheet','timesheet_grid'],
    'data': [
        'security/ir.model.access.csv',
        'report/pending_timesheet_report_template.xml',
        'report/outstanding_timesheet_report_template.xml',
        'data/mail_templates.xml',
        'data/time_sheet_cron_job.xml',
        'view/timesheet_grid_form_changes.xml',
        'view/timesheet_category_view.xml'
    ],

    'auto_install': False,
    'installable': True,
}
