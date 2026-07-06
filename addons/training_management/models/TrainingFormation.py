# -*- coding: utf-8 -*-
from odoo import models, fields


class TrainingFormation(models.Model):
    _name = "training.formation"
    _description = " Training Formation"
    name = fields.Char(required=True)
    code = fields.Char()
    description = fields.Html()
    duration = fields.Float(string="Duration (Hours)")
    price    = fields.Float()
    active   = fields.Boolean()
    
