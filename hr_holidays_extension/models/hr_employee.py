#-*- coding:utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import AccessError
from datetime import datetime
#from dateutils import rela


class Employee(models.Model):

    _inherit = "hr.employee"

    current_leave_state = fields.Selection(compute='_compute_leave_status', string="Current Leave Status",
       selection_add=[('technical','Technical'), ('not_technical','No Technical'), ('chef_service','Chef de service'),
                      ('crh','Chargé des RH'), ('chef_depart','Chef de departement'),('cdaf','RAF'),])
    date_return_last_holidays= fields.Date(compute='_compute_remaining_leaves_legals', string="Date de retour Congés")
    date_depart_holidays= fields.Date(compute='_compute_remaining_leaves_legals', string='Date de depart en congés')
    holidays_legal_leaves = fields.Float(compute='_compute_remaining_leaves_legals', string='Congés légaux restants')


    def _getDateHolidays(self):
        """Checks that choosen address (res.partner) is not linked to a company.
        """
        type_holiday = self.env['hr.leave.type'].search([('time_type', '=', 'leave')])[0]
        vals = {
            'date_return_last_holidays': self.start_date,
            'date_depart_holidays': False
        }
        if type_holiday :

            today = fields.Datetime.now()
            print(today)
            # try:
            holidays = self.env['hr.leave'].search([('holiday_status_id', '=', type_holiday.id),
                               ('date_to', '<', today), ('employee_id', '=', self.id)],order="date_to desc", limit=1)
            print(holidays)
            if holidays :
                print(holidays.date_to)
                vals['date_return_last_holidays'] = str(holidays.date_from)[:10]
            holidays_next = self.env['hr.leave'].search(
                [('holiday_status_id', '=', type_holiday.id), ('date_from', '>', today), ('employee_id', '=', self.id)],
                order="date_from", limit=1)
            if holidays_next :
                vals['date_depart_holidays'] = str(holidays_next.date_from)[:10]
            # except : pass
            return vals



    def _get_remaining_leaves_legals(self):
        """ Helper to compute the remaining leaves for the current employees
            :returns dict where the key is the employee id, and the value is the remain leaves
        """
        self._cr.execute("""
            SELECT
                sum(h.number_of_days) AS days,
                h.employee_id
            FROM
                hr_leave h
                join hr_leave_type s ON (s.id=h.holiday_status_id)
            WHERE
                h.state='validate' AND
                h.employee_id in %s AND s.code='CONG'
            GROUP BY h.employee_id""", (tuple(self.ids),))
        result = self._cr.dictfetchall()
        print("Le result est %s"%result)
        if result :
            return dict((row['employee_id'], row['days']) for row in self._cr.dictfetchall())

    @api.multi
    def _compute_remaining_leaves_legals(self):
        for employee in self:
            remaining = employee._get_remaining_leaves_legals()
            if remaining :
                employee.holidays_legal_leaves = remaining.get(employee.id, 0.0)
            vals = employee._getDateHolidays()
            employee.date_return_last_holidays = vals['date_return_last_holidays']
            employee.date_depart_holidays = vals['date_depart_holidays']




