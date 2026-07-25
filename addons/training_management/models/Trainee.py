# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Trainee(models.Model):
    _name = 'training.trainee'
    _description = 'Apprenant'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    level = fields.Selection(
        [('beginner', 'Debutant'), ('intermediate', 'Intermédiaire'), ('advanced', 'Avancée')],
        default="beginner"
    )
    organization = fields.Char()

    @api.model_create_multi
    def create(self, vals_list):
        trainees = super().create(vals_list)
        trainees._grant_portal_access()
        return trainees

    def _grant_portal_access(self):
        for trainee in self:
            if not trainee.partner_id.email:
                continue
            if trainee.partner_id.user_ids:
                continue  # déjà un utilisateur portail, on n'y touche pas

            wizard = self.env['portal.wizard'].with_context(
                active_model='res.partner',
                active_ids=trainee.partner_id.ids,
            ).create({})

            wizard_users = wizard.user_ids.filtered(
                lambda u: not u.is_portal and not u.is_internal
            )
            for wizard_user in wizard_users:
                wizard_user.action_grant_access()
    def unlink(self):
        self.mapped('user_id').unlink()
        return super().unlink()