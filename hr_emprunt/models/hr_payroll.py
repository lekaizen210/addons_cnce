# -*- coding: utf-8 -*-
import time
import babel
from odoo import models, fields, api, tools, _
from datetime import datetime


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    #@api.model
    def get_inputs(self, contracts, date_from, date_to):
        """This Compute the other inputs to employee payslip.
                           """
        res = super(HrPayslip, self).get_inputs(contracts, date_from, date_to)
        for contract in contracts :
            employee = contract.employee_id
            advance_salary = employee.getAdvancedSalaryMonthly(contract, date_from, date_to)
            if advance_salary != 0 :
                input = {
                    'name': "Avance sur salaire",
                    'code': "AVS",
                    'contract_id': contract.id,
                    'amount': advance_salary,
                }
                res +=[input]
            emprunts = employee.get_amount_emprunt(contract, date_from, date_to)
            if emprunts != 0:
                input = {
                    'name': "Emprunts à déduire",
                    'code': "EMP",
                    'contract_id': contract.id,
                    'amount': emprunts,
                }
        return res

