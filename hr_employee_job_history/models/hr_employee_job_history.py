# -*- coding:utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import *

class HrCarrier(models.Model):
    _name= "hr.employee.job.history"
    _description= "Carrier managment"
    _rec_name="job_id"


    date_from= fields.Date(string="De", required=True)
    date_to= fields.Date(string="À", required=False)
    job_id= fields.Many2one('hr.job', 'Poste', required=True)
    employee_id= fields.Many2one('hr.employee', 'Employé', required=False)
    description= fields.Text("Description")