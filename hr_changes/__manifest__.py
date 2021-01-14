
{
    'name': 'KARITZIS HR Changes',
    'version': '13.0.1.1.0',
    'author': 'Ever Business Solution',

    'category': 'Partner',
    'license': 'AGPL-3',
    'website': "https://www.everbsgroup.com/",
    'depends': ['hr','hr_holidays','document_changes','resource'],
    'data': [
        'security/ir.model.access.csv',
        'data/annual_leaves_cron_job.xml',
        'data/employee_sequence.xml',
        'view/hr_employee_form_changes.xml',
        'view/hr_leave_form_changes.xml',
        'view/hr_leave_type_form_changes.xml',
        'view/hr_leave_report_form_changes.xml',
        'view/resource_calender_form_changes.xml',
        # 'view/hr_leave_allocation_form_changes.xml',
        'wizard/warning_wizard.xml',
        'wizard/refuse_Reason_wizard.xml'
    ],
    'auto_install': False,
    'installable': True,
}
