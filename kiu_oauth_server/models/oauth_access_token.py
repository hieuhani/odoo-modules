# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta

class OAuthAccessToken(models.Model):
    _name = 'oauth.access_token'
    _description = 'OAuth Access Token'

    application_id = fields.Many2one('oauth.application', string='Application')
    token = fields.Char('Access Token', required=True)
    expires_in = fields.Datetime('Expiring Time', required=True)
    scopes = fields.Char('Scopes')

    @api.multi
    def is_valid(self, scopes=None):
        self.ensure_one()
        return not self.is_expired() and self.check_scopes(scopes)

    @api.multi
    def is_expired(self):
        self.ensure_one()
        return datetime.now() > datetime.strptime(self.expires_in, DEFAULT_SERVER_DATETIME_FORMAT)
    
    @api.multi
    def check_scopes(self, scopes):
        self.ensure_one()
        if not scopes:
            return True
        
        app_scopes = set(self.scopes.split(','))
        resource_scopes = set(scopes)
        return resource_scopes.issubset(app_scopes)