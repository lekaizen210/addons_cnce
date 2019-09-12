# -*- coding: utf-8 -*-
import time
import babel
from odoo import models, fields, api, tools, _
from datetime import datetime


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

