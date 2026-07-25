# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import http
from odoo.http import request


class TrainingAttendanceSignatureController(http.Controller):

    def _get_attendance(self, attendance_id, token):
        attendance = request.env["training.attendance"].sudo().browse(attendance_id)
        if not attendance.exists() or not token or attendance.signature_token != token:
            return None
        return attendance

    @http.route(
        "/training/attendance/sign/<int:attendance_id>/<string:token>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def attendance_sign_page(self, attendance_id, token, **kwargs):
        attendance = self._get_attendance(attendance_id, token)
        if attendance is None:
            return request.render("training_management.attendance_signature_invalid", {})

        if attendance.signed:
            return request.render(
                "training_management.attendance_signature_already_signed",
                {"attendance": attendance},
            )

        return request.render(
            "training_management.attendance_signature_page",
            {"attendance": attendance, "token": token},
        )

    @http.route(
        "/training/attendance/sign/<int:attendance_id>/<string:token>/submit",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=True,
    )
    def attendance_sign_submit(self, attendance_id, token, signature=None, **kwargs):
        attendance = self._get_attendance(attendance_id, token)
        if attendance is None:
            return request.render("training_management.attendance_signature_invalid", {})

        if not attendance.signed and signature:
            attendance.write({
                "signature": signature.split(",")[-1],
                "signed": True,
                "signed_at": datetime.now(),
                "state": "present",
                "signature_ip": request.httprequest.remote_addr,
                "signature_user_agent": request.httprequest.user_agent.string,
            })

        return request.render(
            "training_management.attendance_signature_thanks",
            {"attendance": attendance},
        )
