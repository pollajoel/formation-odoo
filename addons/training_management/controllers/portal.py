
from odoo import http
from odoo.http import request


class TrainingPortalController(http.Controller):
    @http.route(
        ['/my/trainings'],
        type="http",
        auth='user',
        website=True
    )
    def portal_my_trainings(self, **kw):
        trainee = request.env["training.trainee"].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id)
        ], limit=1)
        sessions = request.env['training.registration'].sudo().search([('trainee_id', '=', trainee.id)])
        return request.render(
            'training_management.portal_my_trainngs',
            {
                'sessions': sessions
            }
        )