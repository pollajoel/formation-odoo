# -*- coding: utf-8 -*-
from odoo import api, models, fields


class TrainingAttendanceSheet(models.Model):
    _name = "training.attendance.sheet"
    _description = "Feuille d'appel"

    name = fields.Char()
    session_id = fields.Many2one(
        "training.session",
        required=True,
        ondelete="cascade",
    )

    trainer_id = fields.Many2one(
        "training.trainer",
        related="session_id.trainer_id",
        store=True,
        string="Formateur",
    )

    date = fields.Date(
        required=True,
        default=fields.Date.today
    )

    line_ids = fields.One2many( 
        "training.attendance",
        "sheet_id",
        string="présences"
    )
    

    @api.onchange("session_id", "date")
    def _onchange_session_date(self):
        for record in self:
            if record.session_id and record.date:
                record.name = f"{record.session_id.name} - {record.date}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name"):
                session = self.env["training.session"].browse(vals.get("session_id"))
                sheet_date = vals.get("date") or fields.Date.today()
                vals["name"] = f"{session.name} - {sheet_date}"
        return super().create(vals_list)
