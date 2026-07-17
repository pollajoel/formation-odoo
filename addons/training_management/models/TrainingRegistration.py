# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class TrainingRegistration(models.Model):  # Correction de la coquille "Taining"
    _inherit =["mail.thread", "mail.activity.mixin"]
    _name = "training.registration"
    _description = "Training registration"

    session_id = fields.Many2one(
        "training.session",
        required=True,
        ondelete="cascade",
         tracking=True
    )

    trainee_id = fields.Many2one(
        "training.trainee",
        required=True,
        ondelete="cascade",
         tracking=True
    )

    formation_id = fields.Many2one(
        related="session_id.formation_id",
        store=True,
         tracking=True
    )
    sale_order_id = fields.Many2one("sale.order",  tracking=True)

    state = fields.Selection([
        ("draft", "Brouillon"),
        ("waiting", "En attente de validation"),
        ("confirm", "En attente de paiement"),
        ("paid", "Payé"),
        ("done", "Formation validée"),
        ("cancel", "Terminée")
    ], default="draft", tracking=True)

    def action_confirm(self):
        # Vous pouvez passer l'état à 'confirm' manuellement ici si besoin
        self.write({'state': 'confirm'})

    def action_validate_registration(self):
        for registration in self:
            if registration.sale_order_id:
                continue
            
            partner = registration.trainee_id.partner_id
            if not partner:
                raise UserError(_("Le contact de l'apprenant est obligatoire")) # Correction de "UseError"
            
            # 1. Création du devis
            sale_order = self.env["sale.order"].create({
                "partner_id": partner.id,
                "origin": registration.session_id.name
            })

            # 2. Ajout de la ligne de commande (dans la boucle)
            template = registration.formation_id
            product = template.product_variant_id
            
            if not product:
                raise UserError(_("Aucun produit (variante) n'est lié à cette formation."))

            self.env["sale.order.line"].create({
                "order_id": sale_order.id,
                "product_id": product.id,
                "product_uom_qty": 1
            })
            
            # 3. Lier le devis et changer l'état
            registration.sale_order_id = sale_order.id
            registration.state = "waiting"
            
        # On renvoie l'action d'envoi de mail pour le dernier devis généré
        return sale_order.action_quotation_send()

    def action_create_invoices(self):
        self.ensure_one()
        if not self.sale_order_id:
            raise UserError(_("Aucun devis lié à cette inscription."))

        if self.sale_order_id.state != "sale":
            raise UserError(_("Le devis doit être confirmé avant la facturation."))
            
        # Création de la facture
        invoices = self.sale_order_id._create_invoices()
        
        # Optionnel : Mettre à l'état confirmé si on facture
        self.state = "confirm"
        
        return {
            "type": "ir.actions.act_window",
            "name": _("Facture"),
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": invoices.id
        }