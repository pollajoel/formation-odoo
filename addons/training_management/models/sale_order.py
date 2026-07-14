# -*- coding: utf-8 -*-
from odoo import models



class SaleOrder(models.Model):
    _inherit="sale.order"

    def action_confirm(self):
        res = super().action_confirm()
        registration = self.env["training.registration"].search([
            ("sale_order_id", "in", self.ids)
        ])
        registration.write({
            "state": "confirm"
        })
        return res