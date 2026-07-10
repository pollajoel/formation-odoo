# -*- coding: utf-8 -*-
from odoo import models, fields


class TrainingFormation(models.Model):
    _name = "training.formation"
    _description = "Training Formation"
    _inherits = {'product.template': 'product_id'}  # délègue à res.partner
    product_id = fields.Many2one('product.template', required=True, ondelete='cascade') #  delegate=True ==> pour un Many2one simple.
    code = fields.Char()
    description = fields.Html()
    duration = fields.Float(string="Duration (Hours)")
    price    = fields.Float()
    active   = fields.Boolean(default=True)
    # def create(self, vals):
    #     # créer une nouvelle formation
    #     training = super().create(vals)
    #     product = self.env["product.product"].create({
    #         "name": training.name,
    #         "list_price": training.price,
    #         "type": "service"
    #     })
    #     # associer le produit à la formation
    #     training.product_id = product
    #     # retourner la formation courante
    #     return training