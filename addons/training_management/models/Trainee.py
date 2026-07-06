# -*- coding: utf-8 -*-

from odoo import models, fields

class Trainee(models.Model):
    _name = 'training.trainee'
    _description = 'Apprenant'
    _inherits = {'res.partner': 'partner_id'}  # délègue à res.partner
    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    level = fields.Selection([('beginner', 'Debutant'), ('intermediate', 'Intermédiaire'), ('advanced', 'Avancée')], default="beginner")
    organization = fields.Char()