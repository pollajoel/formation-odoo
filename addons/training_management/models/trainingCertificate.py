# -*- coding: utf-8 -*-
from odoo import models, fields, api


class trainingCertificate(models.Model):
    _name="training.certificate"
    _description= "training certificate"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char( 
        string = "reference",
        required = True,
        copy=False,
        default="New"
    )

    traine_id = fields.Many2one(
        "training.trainee",
        required=True
    )


    session_id = fields.Many2one(
        "training.session",
        required = True
    )

    formation_id = fields.Many2one(
        related ="session_id.formation_id", 
        store  =True
    )

    issue_date = fields.Date( 
        default = fields.Date.today, 
        required=True
    )

    state = fields.Selection([("draft", "Brouillon"),("issued", "Emis")], default="draft", tracking=True)

    pdf_attachment_id = fields.Many2one(
        "ir.attachment",
        readonly=True
    )

    verification_token = fields.Char(copy=False)