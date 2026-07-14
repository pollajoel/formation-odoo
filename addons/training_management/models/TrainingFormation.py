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
    def create(self, vals):
        # créer une nouvelle formation
        product = self.env["product.template"].create({
            "name": vals.get("name"),
            "list_price": vals.get("list_price", 0.0),
            "type": "service",
            "invoice_policy": "order" # order et delivery => odoo attends que le service soit marqué comme réalisé ( pour générer un facture)
        })
        # associer le produit à la formation
        vals["product_id"] = product.id
        # retourner la formation courante
        return super().create(vals)