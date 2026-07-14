# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import  ValidationError
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
    
    def action_open_trainee_view(self):
        return
        
    def action_confirm(self):
        self.write({"state":"confirmed"})

    def action_done(self):
        self.write({"state":"done"})

    def action_cancel(self):
        self.write({"state":"cancel"})

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