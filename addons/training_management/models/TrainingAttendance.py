# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import secrets


class TrainingAttendance(models.Model):
    _name = "training.attendance"
    _description = "Training attendance"
    session_id = fields.Many2one(
        "training.session",
        related="sheet_id.session_id",
        store=True,
    )
    trainee_id = fields.Many2one(
        "training.trainee",
        required=True
    )
    registration_trainee_ids = fields.Many2many(
        "training.trainee",
        compute="_compute_registration_trainee_ids",
        string="Apprenants inscrits",
    )
    state = fields.Selection([
        ("present", "Présent"),
        ("absent", "Absent"),
        ("late", "Rétard"),
        ("excused", "excusé"),
        ("pending", "En attente")
    ], default="absent")
    date = fields.Date(string="Date", required=True, default=fields.Date.today, readonly=True)
    sheet_id = fields.Many2one(
        "training.attendance.sheet",
        string="feuille d'appel",
        required=True,
        ondelete="cascade"
    )
    signature = fields.Binary(
        string="Signature",
        attachment=True
    )
    signed = fields.Boolean(default=False)
    signed_at = fields.Datetime()
    signature_token = fields.Char(copy=False)
    signature_ip = fields.Char(copy=False)
    signature_user_agent = fields.Text(copy=False)
    signature_state = fields.Selection([
        ("pending", "En attente"),
        ("signed", "Signé"),
    ], compute="_compute_signature_state", store=True, string="Signature")

    @api.depends("signed")
    def _compute_signature_state(self):
        for record in self:
            record.signature_state = "signed" if record.signed else "pending"

    @api.depends("session_id", "session_id.registration_ids.trainee_id")
    def _compute_registration_trainee_ids(self):
        for record in self:
            record.registration_trainee_ids = record.session_id.registration_ids.mapped("trainee_id")

    @api.constrains("sheet_id", "trainee_id")
    def _check_unique_trainee_per_sheet(self):
        for record in self:
            duplicate = self.search([
                ("sheet_id", "=", record.sheet_id.id),
                ("trainee_id", "=", record.trainee_id.id),
                ("id", "!=", record.id),
            ], limit=1)
            if duplicate:
                raise ValidationError(
                    "Cet apprenant a déjà une présence enregistrée sur cette feuille d'appel."
                )
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.setdefault(
                "signature_token",
                secrets.token_urlsafe(32)
            )
        return super().create(vals_list)

    def action_send_signature_email(self):
        self.ensure_one()
        if not self.trainee_id.email:
            raise UserError(_(
                "Impossible d'envoyer la demande de signature : "
                "%(trainee)s n'a pas d'adresse email renseignée.",
                trainee=self.trainee_id.name,
            ))
        template = self.env.ref(
            "training_management.mail_template_attendance_signature"
        )
        template.send_mail(
            self.id,
            force_send=True
        )