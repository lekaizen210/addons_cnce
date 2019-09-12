# -*- coding:utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import *

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.multi
    def _job_history_count(self):
        for each in self:
            job_ids = self.env['hr.employee.job.history'].sudo().search([('employee_id', '=', each.id)])
            each.job_history_count = len(job_ids)

    history_carrier_ids= fields.One2many('hr.employee.job.history', 'employee_id', string="Historiques de carrière")
    job_history_count = fields.Integer(compute='_job_history_count', string='# jobs historique')

    @api.multi
    def carrier_view(self):
        self.ensure_one()
        print(self)
        print(self.id)
        for employee in self :
            domain = [
                ('employee_id', '=', employee.id)]
            context = {'default_employee_id': employee.id}
            return {
                'name': _('Historique des jobs'),
                'domain': domain,
                'res_model': 'hr.employee.job.history',
                'type': 'ir.actions.act_window',
                'view_id': False,
                'view_mode': 'tree,form',
                'view_type': 'form',
                'help': _('''<p class="oe_view_nocontent_create">
                                   Click to Create for jobs history of employee
                                </p>'''),
                'limit': 80,
                'context': context,
            }



