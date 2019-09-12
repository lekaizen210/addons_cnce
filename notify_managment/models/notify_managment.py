#-*- coding:utf-8 -*-

from odoo import api, fields, models, _
from dateutil import relativedelta

class NotifModel(models.Model):
    _name= 'notify.model'
    _description= 'Notify model'


    name= fields.Char("Libellé", required=True, size=255)
    line_ids= fields.One2many('notify.model.line', 'notif_id', 'Lignes', required=True)

class NotifModelLine(models.Model):
    _name= 'notify.model.line'
    _description= "Notify line model managment"

    type= fields.Selection([('an', 'Année'),('mois', 'Mois'),('day', 'Jours'), ('hours', 'Heures')],
           'Type', required=True)
    number= fields.Integer('Date', required=True, default=1)
    notif_id= fields.Many2one('notify.model', 'Notif')

class NotifLine(models.Model):
    _name = 'notif.line'
    _description= 'Gestion des notification'


    def generate_notification_line(self, model, notif_model, date_fin):
        if model and notif_model :
            for line in notif_model.line_ids :
                date = False
                if line.type == an :
                    date = date_fin + relativedelta.relativedelta(years=-line.number)
                elif line.type == mois :
                    date = date_fin + relativedelta.relativedelta(months=-line.number)
                elif line.type == day :
                    date = date_fin + relativedelta.relativedelta(days=-line.number)
                else :
                    if type(date_fin) == 'datetime' :
                        date = date_fin + relativedelta.relativedelta(hours=-line.number)
                val = {
                    'res_model': model._name,
                    'res_id': model.id,
                    'date_notifcation' : date

                }
                self.create(val)


    res_model= fields.Char('Nom du modèle', required=True, size=255)
    res_id = fields.Integer('Id', required=True)
    date_notifcation= fields.Date('Date de notification')