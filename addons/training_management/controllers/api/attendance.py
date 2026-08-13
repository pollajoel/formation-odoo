# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class TrainingAttendanceApiController(http.Controller):
    @http.route('/api/training/attendance', type='jsonrpc', auth='bearer', methods=['POST'], csrf=False)
    def send_attendance(self, attendance_ids=None, sheet_id=None, session_id=None, **kwargs):
        domain = [('signed', '=', False)]
        if attendance_ids:
            domain = [('id', 'in', attendance_ids)]
        elif sheet_id:
            domain.append(('sheet_id', '=', sheet_id))
        elif session_id:
            domain.append(('session_id', '=', session_id))

        attendances = request.env['training.attendance'].sudo().search(domain)

        sent_ids = []
        errors = []
        for attendance in attendances:
            try:
                attendance.action_send_signature_email()
                sent_ids.append(attendance.id)
            except Exception as exc:
                errors.append({'attendance_id': attendance.id, 'error': str(exc)})

        return {
            'status': 'success' if not errors else 'partial',
            'sent': sent_ids,
            'errors': errors,
        }
