# -*- coding: utf-8 -*-

from odoo import models, fields

class TrainingSession(models.Model):
    _name = 'training.session'
    _description = 'Training session'
    name = fields.Char(required=True)
    formation_id = fields.Many2one(
        "training.formation",
        required=True
    )
    trainer_id= fields.Many2one("training.trainer", string="Trainer")
    trainee_ids = fields.Many2many("training.trainee", string="participants")
    start_date = fields.Date(required=True)
    end_date  = fields.Date(required=True)
    capacity  = fields.Integer(default=20)
    location  = fields.Char()
    state     = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("done", "Done"),
        ("cancel", "Cancel")
    ], default="draft")
    notes = fields.Text()

    def action_confirm(self):
        self.write({"state":"confirmed"})

    def action_done(self):
        self.write({"state":"done"})

    def action_cancel(self):
        self.write({"state":"cancel"})
