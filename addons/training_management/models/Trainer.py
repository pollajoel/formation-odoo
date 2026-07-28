# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Trainer(models.Model):
    _name = 'training.trainer'
    _description = 'Formateur'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    speciality = fields.Char(string="Spécialité")
    user_id = fields.Many2one('res.users')
    available = fields.Boolean()

    def action_create_user(self):
        """Bouton manuel : crée un utilisateur pour un formateur qui n'en a pas."""
        for trainer in self:
            if not trainer.user_id:
                user = self.env['res.users'].create({
                    'name': trainer.name,
                    'email': trainer.email,
                    'partner_id': trainer.partner_id.id,
                    'groups_id': [
                        (6, 0, [self.env.ref('training_management.group_training_trainer').id])
                    ],
                })
                trainer.user_id = user.id

    @api.model_create_multi
    def create(self, vals_list):
        trainers = super().create(vals_list)
        for trainer in trainers:
            if trainer.user_id:
                continue
            existing_user = self.env['res.users'].sudo().search(
                [('login', '=', trainer.email)], limit=1
            )
            if existing_user:
                trainer.user_id = existing_user.id
                continue
            user = self.env['res.users'].create({
                    'name': trainer.name,
                    'email': trainer.email,
                    'login': trainer.email,
                    'partner_id': trainer.partner_id.id,
                    'group_ids': [
                        (6, 0, [self.env.ref('training_management.group_training_trainer').id])
                    ],
            })
            trainer.user_id = user.id
        return trainers
    @api.model
    def get_trainers_data(self):
        total_trainers = self.env["training.trainer"].search_count([])
        return {
             'nbTrainers': total_trainers
        }