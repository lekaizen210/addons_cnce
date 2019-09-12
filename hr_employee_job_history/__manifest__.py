# -*- coding: utf-8 -*-
###################################################################################

#
###################################################################################
{
    'name': 'HR Jobs history',
    'version': '11.0.1.0.0',
    'summary': """Manages Employee jobs history.""",
    'category': 'HR',
    'author': 'Jean Jonathan ARRA',
    'company': 'VEONE',
    'maintainer': 'VEONE',
    'website': "https://www.veone.net",
    'depends': ['base', 'hr', 'hr_contract'],
    'data': [
        #'security/ir.model.access.csv',
        'views/hr_history_job_employee_view.xml',
        'views/hr_employee_view.xml'
    ],
    #'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
