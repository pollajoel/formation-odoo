# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    training_income_account_id = fields.Many2one(
        "account.account",
        string="Compte de revenus des formations",
        domain="[('account_type', '=', 'income'), ('company_ids', 'in', id)]",
        help="Compte de revenus utilisé automatiquement pour les produits "
             "créés lors de la création d'une formation.",
    )
