# -*- coding: utf-8 -*-

from odoo import models, _, fields, api
from odoo.exceptions import  ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)

class TrainingSession(models.Model):
    _inherit =["mail.thread", "mail.activity.mixin"]
    _name = 'training.session'
    _description = 'Training session'
    name = fields.Char(required=True)
    formation_id = fields.Many2one(
        "training.formation",
        required=True,
        tracking=True
    )
    trainer_id= fields.Many2one("training.trainer", string="Trainer", tracking=True)
    registration_ids = fields.One2many("training.registration", "session_id", string="participants", tracking=True)
    start_date = fields.Date(required=True, tracking=True)
    end_date  = fields.Date(required=True, tracking=True)
    capacity  = fields.Integer(default=0, tracking=True)
    location  = fields.Char(tracking=True)
    state     = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("done", "Done"),
        ("cancel", "Cancel")
    ], default="draft", tracking=True)
    notes = fields.Text()

    total_trainee = fields.Integer(
        compute="_compute_stats",
        default=0,
        string="nombre de participant",
        store=True,
        # store=True  => si on veut persister la donnée en base
        # compute_sudo=True => si le calcul doit contourner les règles de sécurités
    )

    total_trainer = fields.Integer(
        compute="_compute_trainer",
        default=0,
        string="Nombre de sessions du formateur",
        store=True
    )
    
    def action_open_trainee_view(self):
        return
        
    def action_confirm(self):
        self.write({"state":"confirmed"})

    def action_done(self):
        self.write({"state":"done"})

    def action_cancel(self):
        self.write({"state":"cancel"})
    
    def action_generate_attendance_sheet(self):
        self.ensure_one()
        sheet = self.env["training.attendance.sheet"].search([
            ("session_id", "=", self.id)
        ], limit=1)
        if not sheet:
            sheet = self.env["training.attendance.sheet"].create(
               {
                 "session_id": self.id,
                 "date": fields.Date.today()
               }
            )
        Attendance = self.env["training.attendance"]
        existing_trainee_ids = set(Attendance.search([
            ("sheet_id", "=", sheet.id)
        ]).trainee_id.ids)
        line = []
        for trainee in self.registration_ids.mapped("trainee_id"):
            if trainee.id in existing_trainee_ids:
                continue
            line.append(
                {
                    "sheet_id": sheet.id,
                    "session_id": self.id,
                    "trainee_id": trainee.id
            })
        if line:
            Attendance.create(line)
        return {
            "type": "ir.actions.act_window",
            "name": "Feuille d'appel",
            "res_model": "training.attendance.sheet",
            "view_mode": "form",
            "res_id": sheet.id
        }


    def open_add_trainee_wizard(self):
        self.ensure_one()
        return {
            "type" : "ir.actions.act_window",
            "name" : "Ajouter des participants",
            "res_model": "session.trainee.wizard",
            "view_mode": "form",
            "target"   : "new",
            "context"  : {
                "active_id": self.id, 
                "excluded_trainee_id": self.registration_ids.mapped("trainee_id")
            },
        }

    @api.depends("registration_ids")
    def _compute_stats(self):
        for trainingSession in self:
            trainingSession.total_trainee = len(trainingSession.registration_ids)

    @api.depends("trainer_id")
    def _compute_trainer(self):
        for trainingSession in self:
            if trainingSession.trainer_id:
                trainingSession.total_trainer = self.search_count(
                    [("trainer_id", "=", trainingSession.trainer_id.id)]
                )
            else:
                trainingSession.total_trainer = 0

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for trainingSession in self:
            if(trainingSession.end_date and trainingSession.start_date and trainingSession.end_date < trainingSession.start_date ):
              raise ValidationError("La date de fin doit être Postérieure à la date de début.")
            
    @api.constrains('capacity')
    def _check_capacity_linit(self):
        for trainingSession in self:
            if( trainingSession.capacity < len(trainingSession.registration_ids)):
                raise ValidationError("Le nombre participant dépasse la capacité de la session")
            if( trainingSession.capacity <= 0 ):
                raise ValidationError("La capacité doit être supérieur à 0")
    
    def action_send_attendance_requests( self ):
        self.ensure_one()
        if  not self.registration_ids:
            raise UserError(_("Aucun participant n'est inscrit à cette session."))
        sheet = self.env["training.attendance.sheet"].search([
            ("session_id", "=", self.id)
        ], limit=1)

        if not sheet:
            sheet = self.env["training.attendance.sheet"].create({
                "session_id": self.id,
                "date": fields.Date.today()
            })
        Attendance = self.env["training.attendance"]
        trainees_without_email = []

        for enrollment in self.registration_ids:
            # ne pas créer deux lignes pour le m^me participant
            line = Attendance.search([
                ("sheet_id", "=", sheet.id),
                ("trainee_id", "=", enrollment.trainee_id.id)
            ], limit=1)
            if not line:
                line = Attendance.create({
                    "sheet_id": sheet.id,
                    "session_id": self.id,
                    "trainee_id": enrollment.trainee_id.id,
                })
            if not line.trainee_id.email:
                trainees_without_email.append(line.trainee_id.name)
                continue
            line.action_send_signature_email()

        if trainees_without_email:
            raise UserError(_(
                "Les convocations ont été envoyées aux autres participants. "
                "Impossible d'envoyer à : %(trainees)s (email manquant).",
                trainees=", ".join(trainees_without_email),
            ))
        return True