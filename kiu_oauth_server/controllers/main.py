# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import werkzeug.utils
import random

UNICODE_ASCII_CHARACTER_SET = ('abcdefghijklmnopqrstuvwxyz'
                               'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                               '0123456789')


def generate_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
    """Generates a non-guessable OAuth token

    OAuth (1 and 2) does not specify the format of tokens except that they
    should be strings of random characters. Tokens should not be guessable
    and entropy when generating the random characters is important. Which is
    why SystemRandom is used instead of the default random.choice method.
    """
    rand = random.SystemRandom()
    return ''.join(rand.choice(chars) for x in range(length))


class OAuth2(http.Controller):
    @http.route('/oauth/auth', type='http', auth='user', methods=['GET', 'POST'])
    def auth(self, **kwargs):
        """
        client_id
        scope: res_company:perm_read
        """
        client_id = request.params.get('client_id')
        scope = request.params.get('scope')
        if not client_id:
            return 'Client ID must be specified'
        if not scope:
            # TODO: Need to validate scope here
            return 'Scope must be specified'
        apps = request.env['oauth.application'].sudo().search([('client_id','=' , client_id)])
        if not apps or (apps and not apps[0]):
            return 'Invalid client ID'

        if request.httprequest.method == 'GET':
            scopes = scope.split(',')
            print apps[0].logo
            return request.render("kiu_oauth_server.scope_confirmation", {
                'app': apps[0],
                'user': request.env.user,
                'scopes': scopes,
            })

        elif request.httprequest.method == 'POST':
            ACCESS_TOKEN_EXPIRE_SECONDS = 3600
            expires = datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
            
            token = generate_token()
            request.env['oauth.access_token'].sudo().create({
                'application_id': apps[0].id,
                'scopes': scope,
                'expires_in': expires.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                'token': token,
            })
            return werkzeug.utils.redirect('{url}?oauth_token={token}'.format(url=apps[0].redirect_uri, token=token), 302)