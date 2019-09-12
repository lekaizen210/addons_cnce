# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2012 Veone - support.veone.net
# Author: Veone
#
# Fichier du module hr_synthese
# ##############################################################################
{
    "name" : "CNPS Mensuel",
    "version" : "1.0",
    "author" : "VEONE Technologies",
    'category': 'Human Resources',
    "website" : "www.veone.net",
    "depends" : ['base', 'hr_payroll_ci_raport'],
    "description": """ 
    Gestion de la CNPS mensuelle
    """,
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [

        ],
    "data":[
        "wizard/HrCnpsMonthlyView.xml",
        "reports/report_cnps_monthly.xml",
        "reports/report_menu.xml",
    ],
    "installable": True
}
