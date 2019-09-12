#-*- coding:utf-8 -*-


import time
from datetime import datetime
from dateutil import relativedelta
from openerp import api, fields, models, exceptions


class HrReverseContract(models.TransientModel):
    _name = 'hr.reverse.contract'

    type_calcul = fields.Selection([('brut', 'Par le brut'),('net','Par le net')], 'Méthode de calcul', requred=True)
    montant = fields.Integer("Montant ")
    contract_id = fields.Many2one('hr.contract', 'Contrat')
    payslip = fields.Many2one('hr.payslip', 'Bulletin de paie')

    @api.one
    def compute(self):
        payslip_obj = self.pool.get('hr.payslip')
        total_intrant = self.wage
        sursalaire = 0
        for prime in self.hr_payroll_prime_ids :
            total_intrant+= prime.montant_prime

        if total_intrant > self.montant :
            raise exceptions.Warning('Le montant est inféreur aux intrants')
        else :
            structure_salariale = self.struct_id
            use_anc = False
            for rule in structure_salariale.rule_ids:
                if rule.code == 'PANC':
                    use_anc = True
            if use_anc :
                prime_anciennete = 0.0
                if self.type_calcul == 'brut':
                    if 1 < self.an_anciennete < 26 :
                        prime_anciennete = 0.01 * self.wage * self.an_anciennete
                        total_intrant+=prime_anciennete
                        sursalaire = self.montant - total_intrant
                elif self.type_calcul == 'net':
                    date_from = time.strftime('%Y-%m-01')
                    date_to = str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10]
                    struct_id = self.struct_id.id
                    # print struct_id
                    inputs = payslip_obj.get_inputs(self._cr, self._uid, [self.id], date_from, date_to)
                    input_line_ids = []
                    if inputs :
                        for input in inputs :
                            temp = [0, False, input ]
                            input_line_ids+=[temp]

                    worked_days = payslip_obj.get_worked_day_lines(self._cr, self._uid, [self.id], date_from, date_to)
                    worked_days_line_ids = []
                    if worked_days :
                        for worked_day in worked_days:
                            temp = [0, False, worked_day]
                            worked_days_line_ids+=[temp]
                    vals = {
                                'employee_id': self.employee_id.id,
                                'date_from': date_from,
                                'date_to': date_to,
                                'contract_id': self.id,
                                'struct_id': self.struct_id.id,
                                'input_line_ids': input_line_ids,
                                'worked_days_line_ids': worked_days_line_ids,
                            }
                    payslip_id = payslip_obj.create(self._cr, self._uid, vals)
                    payslip_obj.compute_sheet(self._cr, self._uid, payslip_id)
                    net_amount = 0
                    while net_amount != self.montant :
                        net_amount = payslip_obj.get_net_paye(self._cr, self._uid, payslip_id )
                        print (net_amount)
                        if net_amount < self.montant :
                            sursalaire = self.montant - net_amount
                            print (sursalaire)
                        else :
                            sursalaire = net_amount - self.montant
                            print (sursalaire)
                        self.write({'sursalaire': sursalaire})
                        print ('le write est ok')
                        print( "********************************************************")
                        payslip_obj.compute_sheet(self._cr, self._uid, payslip_id)
            else :
                sursalaire = self.montant - total_intrant
        self.sursalaire = sursalaire

__author__ = 'lekaizen'
