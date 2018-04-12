# -*- coding: utf-8 -*-
import logging
import json
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import ensure_db, Home

_logger = logging.getLogger(__name__)

class AuthController(http.Controller):

    @http.route('/auth/exchange_token', type='json', auth='none', cors='*')
    def exchange_token(self, **args):
        ensure_db()
        uid = request.session.authenticate(request.session.db, args.get('login'), args.get('password'))
        if uid is not False:
            return {
                'token': request.httprequest.session.sid,
                'max_age': 90 * 24 * 60 * 60,

            }
        return 'Nothing'
