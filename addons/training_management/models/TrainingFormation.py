# -*- coding: utf-8 -*-
from odoo import models, fields, api


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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("product_id"):
                product_vals = {
                    "name": vals.get("name"),
                    "list_price": vals.get("price", 0.0),
                    "type": "service",
                    "invoice_policy": "order",
                }
                income_account = self.env.company.training_income_account_id
                if income_account:
                    product_vals["property_account_income_id"] = income_account.id
                product = self.env["product.template"].create(product_vals)
                vals["product_id"] = product.id
        return super().create(vals_list)

    @api.model
    def get_formation_data(self):
        total_formations = self.env["training.formation"].search_count([])
        return {
             'nbFormations': total_formations
        }