# -*- coding: utf-8 -*-

from odoo import models, fields

class Trainer(models.Model):
    _name = 'training.trainer'
    _description = 'Formateur'
    _inherits = {'res.partner': 'partner_id'}  # délègue à res.partner
    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    speciality = fields.Char(string="Spécialité")
    available = fields.Boolean()