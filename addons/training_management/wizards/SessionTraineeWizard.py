# -*- coding: utf-8 -*-
from odoo import models, fields, Command


class SessionTraineeWizard(models.TransientModel):
    _name="session.trainee.wizard"
    _description="Ajouter des participants"
    participant_id = fields.Many2many("training.trainee", string="participants")

    def action_add_trainee(self):
        session = self.env["training.session"].browse(
            self.env.context.get("active_id")
        )
        for participant in self.participant_id:
            self.env['training.registration'].create(
                {
                    "session_id": session.id,
                    "trainee_id": participant.id
                }
            )
        return {"type":"ir.actions.act_window_close"}
    def action_cancel(self):
        return {"type":"ir.actions.act_window_close"}
        