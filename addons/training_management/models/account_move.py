# -*- coding: utf-8 -*-

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def write(self, vals):

        res = super().write(vals)

        if "payment_state" in vals:

            for invoice in self:

                if invoice.payment_state == "paid":

                    registrations = self.env["training.registration"].search([
                        (
                            "sale_order_id",
                            "in",
                            invoice.invoice_line_ids.sale_line_ids.order_id.ids
                        )
                    ])

                    registrations.write({
                        "state": "paid"
                    })

        return res