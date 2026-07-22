# -*- coding: utf-8 -*-
from odoo import models, fields


class Digest(models.Model):
    _inherit = "digest.digest"

    kpi_training_new_trainees = fields.Boolean('Nouveaux apprenants inscrits')
    kpi_training_new_trainees_value = fields.Integer(
        compute='_compute_kpi_traning_new_trainees_value'
    )

    def _compute_kpi_traning_new_trainees_value(self):
        for digest in self:
            start, end, compay = digest._get_kpi_compute_parameters()
            digest.kpi_training_new_trainees_value = self.env['training.trainee'].search_count([
                ('create_date', '>=', start),
                ('create_date', '<', end)
            ])