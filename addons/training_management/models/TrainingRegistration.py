# -*- coding: utf-8 -*-
from odoo import _, fields, models, api
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

    @api.model
    def _cron_process_paid_orders(self):
        registrations = self.search([
        ("state", "=", "confirm"),
        ("sale_order_id.state", "=", "sale"),
        ("sale_order_id.invoice_ids", "=", False),
        ])
        for registration in registrations:
            registration.action_create_invoices()

    def action_create_invoices(self):
        self.ensure_one()
        if not self.sale_order_id:
            raise UserError(_("Aucun devis lié à cette inscription."))

        if self.sale_order_id.state != "sale":
            raise UserError(_("Le devis doit être confirmé avant la facturation."))
            
        # Création de la facture
        if self.sale_order_id.invoice_ids:
            raise UserError(_("Une facture a déjà été créée pour cette inscription."))
        else:
            invoices = self.sale_order_id._create_invoices()
        
        # Optionnel : Mettre à l'état confirmé si on facture
        if invoices:
            # Validation comptable : sans ça la facture reste en brouillon,
            # n'a pas de numéro définitif et Odoo ne génère pas de lien "Payer maintenant"
            invoices.action_post()

            # Si le paiement (ex: fait en ligne dès le devis) est déjà réconcilié
            # avec la facture, ne pas régresser l'état vers "en attente de paiement"
            if invoices.payment_state in ("paid", "in_payment"):
                self.state = "paid"
            else:
                self.state = "confirm"

            # Envoi automatique de la facture par mail
            template = self.env.ref("account.email_template_edi_invoice")

            if template:
                # Le corps par défaut du template ne contient pas de bouton de paiement
                # (uniquement le PDF joint) : on génère le mail sans l'envoyer tout de
                # suite, on y ajoute un lien direct vers la page portail de la facture
                # (où le paiement en ligne est disponible), puis on l'envoie nous-mêmes.
                mail_id = template.send_mail(
                    invoices.id,
                    force_send=False,
                    email_values={
                        "email_to": self.trainee_id.partner_id.email,
                    },
                )
                mail = self.env["mail.mail"].sudo().browse(mail_id)
                portal_url = invoices.get_base_url() + invoices.get_portal_url()
                mail.body_html = (mail.body_html or "") + (
                    '<div style="margin-top:16px;">'
                    '<a href="%s" '
                    'style="background-color:#875A7B;padding:8px 16px;'
                    'text-decoration:none;color:#fff;border-radius:5px;">'
                    "Voir et payer la facture</a></div>" % portal_url
                )
                mail.send()

        return True