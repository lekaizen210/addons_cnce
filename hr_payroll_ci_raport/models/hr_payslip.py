# -*- coding:utf-8 -*-

from odoo import api, fields, models, exceptions

class HrPayslip(models.Model):
    _inherit='hr.payslip'

    @api.multi
    def compute_sheet(self):
        result = super(HrPayslip, self).compute_sheet()
        hpana_obj = self.env['hr.payroll.analyse']
        for slip in self :
            hpana_obj.search([('slip_id', '=', slip.id)]).unlink()
            vals = {
                'employee_id': slip.employee_id.id,
                'date': slip.date_from,
                'slip_id': slip.id,
                'base': slip.get_amountbycode('BASE', slip.line_ids),
                'sursalaire': slip.get_amountbycode('SURSA', slip.line_ids),
                'primes': slip.get_amountbycode('TTPRIM', slip.line_ids),
                'brut': slip.get_amountbycode('BRUT', slip.line_ids),
                'retenues': slip.get_amountbycode('RET', slip.line_ids),
                'transport': slip.get_amountbycode('TRSP', slip.line_ids),
                'net_paie': slip.get_amountbycode('NET_PAIE', slip.line_ids),
                'emprunt': slip.get_amountbycode('EMP', slip.line_ids),
                'net': slip.get_amountbycode('NET', slip.line_ids),
            }
            hpana_obj.create(vals)
        return result

    @api.multi
    def unlink(self):
        for slip in self :
            self.env['hr.payroll.analyse'].search([('slip_id', '=', slip.id)]).unlink()
        return super(HrPayslip, self).unlink()

    @api.multi
    def action_payslip_done(self):
        for slip in self:
            analyse = self.env['hr.payroll.analyse'].search([('slip_id', '=', slip.id)])
            if analyse :
                analyse.write({'state': 'done'})
        return


