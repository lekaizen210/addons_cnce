# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    number_holidays = fields.Float('Nombre de Jours de congés à atribuer', Related="company_id.number_holidays")
