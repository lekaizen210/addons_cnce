# -*- coding:utf-8 -*-


from odoo import models, api, fields, exceptions

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def get_inputs(self, contracts, date_from, date_to):

        res = super(HrPayslip, self).get_inputs(contracts, date_from, date_to)
        for contract in contracts:
            primes = contract.hr_payroll_prime_ids
            for prime in primes:
                if prime.prime_id.code == "TRSP":
                    if prime.montant_prime > 25000:
                        montant_imp = prime.montant_prime - 25000
                        inputs = {
                            'name': "Prime de transport imposable",
                            'code': "TRSP_IMP",
                            'contract_id': contract.id,
                            'amount': montant_imp,
                        }
                        res += [inputs]
                        inputs = {
                            'name': prime.prime_id.name,
                            'code': prime.code,
                            'contract_id': contract.id,
                            'amount': 25000,
                        }
                        res += [inputs]
                    else:
                        inputs = {
                            'name': prime.prime_id.name,
                            'code': prime.code,
                            'contract_id': contract.id,
                            'amount': prime.montant_prime,
                        }
                        res += [inputs]
                else:
                    inputs = {
                        'name': prime.prime_id.name,
                        'code': prime.code,
                        'contract_id': contract.id,
                        'amount': prime.montant_prime,
                    }
                    res += [inputs]
        return res



