# -*- coding: utf-8 -*-
import werkzeug.exceptions

from odoo import models
from odoo.exceptions import AccessDenied
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"
    @classmethod
    def _auth_method_bearer(cls):
        auth_header = request.httprequest.headers.get("Authorization", "")
        scheme, _, token = auth_header.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise werkzeug.exceptions.Unauthorized()

        try:
            uid = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=token)
        except AccessDenied as exc:
            raise werkzeug.exceptions.Unauthorized() from exc

        if not uid:
            raise werkzeug.exceptions.Unauthorized()

        request.update_env(user=uid)
