# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class TainingRegistration(models.Model):
    _name="training.registration"
    _description ="Training registration"

    session_id = fields.Many2one(
        "training.session",
         required=True,
         ondelete="cascade"
    )

    trainee_id = fields.Many2one(
        "training.trainee",
        required=True,
        ondelete="cascade"
    )

    formation_id = fields.Many2one(
        related="session_id.formation_id",
        store=True
    )
    sale_order_id = fields.Many2one("sale.order")

    state     = fields.Selection([
        ("draft", "Draft"),
        ("waiting", "waiting Quotation"),
        ("confirm", "Confirmed"),
        ("paid", "Paid"),
        ("done", "Training completed"),
        ("cancel", "Cancel")
    ], default="draft", tracking=True)

    def action_confirm(self):
        return
    def action_validate_registration(self):
        for registration in self:
            if registration.sale_order_id:
                continue
        partner = registration.trainee_id.partner_id
        if not partner:
            raise UseError(_("Le contact de l'apprenant est obligatoire"))
        # creation du dévis
        sale_order = self.env["sale.order"].create({
            "partner_id": partner.id,
            "origin": registration.session_id.name
        })

        #rajouter les lignes de commandes
        template = registration.formation_id
        product = template.product_variant_id
        self.env["sale.order.line"].create({
            "order_id": sale_order.id,
            "product_id": product.id,
            "product_uom_qty": 1
        })
        # Lier le dévis créé sur odoo au modèle d'enregistrement
        registration.sale_order_id = sale_order.id
        registration.state="waiting"
        # envois du devis pour validation
        return sale_order.action_quotation_send()

    def action_create_invoices(self):

        self.ensure_one()
        if not self.sale_order_id:
            raise UserError(
            _("Aucun devis lié à cette inscription.")
        )

        if self.sale_order_id.state != "sale":
            raise UserError(
            _("Le devis doit être confirmé avant la facturation.")
        )
        invoices = self.sale_order_id._create_invoices()
        
        return {
            "type": "ir.actions.act_window",
            "name": _("Facture"),
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": invoices.id
        }