#-*- coding:utf-8 -*-

from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'


    number_holidays= fields.Float('Nombre de Jours de congés à attribuer')