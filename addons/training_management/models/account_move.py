# -*- coding: utf-8 -*-
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):
        """
        Surcharger la validation de la facture ou le paiement.
        Pour être certain de capter le paiement (qui arrive après la validation),
        on surcharge la méthode qui gère le changement d'état du paiement.
        """
        res = super(AccountMove, self)._post(soft=soft)
        self._update_training_registrations()
        return res

    def action_register_payment(self):
        """
        Déclenché lorsque l'utilisateur clique sur 'Enregistrer un paiement'.
        """
        res = super(AccountMove, self).action_register_payment()
        return res

    # La méthode magique d'Odoo qui est appelée quand le statut de paiement d'une facture change
    def _compute_amount(self):
        super(AccountMove, self)._compute_amount()
        for move in self:
            if move.payment_state in ('paid', 'in_payment'):
                move._update_training_registrations()

    def _update_training_registrations(self):
        """
        Retrouve l'inscription à une session de formation liée à la facture via le Sale->Order
        et passe son état à 'paid'.
        """
        for move in self:
            if move.payment_state in ('paid', 'in_payment'):
                # On remonte de la facture -> au devis d'origine -> à l'inscription
                sale_orders = move.line_ids.mapped('sale_line_ids.order_id')
                if sale_orders:
                    registrations = self.env['training.registration'].search([
                        ('sale_order_id', 'in', sale_orders.ids),
                        ('state', '!=', 'paid')
                    ])
                    if registrations:
                        registrations.write({'state': 'paid'})