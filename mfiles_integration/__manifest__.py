# Copyright 2015 2011,2013 Michael Telahun Makonnen <mmakonnen@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": 'MFiles Integration',
    "version": '13.0.0',
    "license": "AGPL-3",
    "category": "Uncategorized",
    "author": 'Everteam Business Solutions',
    "category": 'Mail',
    "website": "https://www.everteam.com/",
    "depends": ['base','hr','hr_changes'],
    "data": [
        'security/ir.model.access.csv',
        'views/configuration.xml',
        'data/mfiles_integration_cron_job.xml',
        'views/mfiles_integration_views.xml'
    ],
    "installable": True,


}


