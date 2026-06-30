# -*- coding: utf-8 -*-

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"
    level = fields.Selection([('beginner', 'Debutant'), ('intermediate', 'Intermédiaire'), ('advanced', 'Avancée')], default="beginner")
    available = fields.Boolean()
    organization = fields.Char()
    is_trainee = fields.Boolean(default=False)