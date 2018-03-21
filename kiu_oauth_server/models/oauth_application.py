# -*- coding: utf-8 -*-

from odoo import models, fields, api
import uuid

class OAuthApplication(models.Model):
    _name = 'oauth.application'
    _description = 'OAuth Application'

    def generate_client_id(self):
        return str(uuid.uuid1())

    name = fields.Char('Application Name')
    client_id = fields.Char('Client ID', index=True, require=True, default=generate_client_id)
    user_id = fields.Many2one('res.users', string='User', required=True)
    redirect_uri = fields.Char('Redirect URI', require=True)
    logo = fields.Binary(string="Application Logo")
    token_ids = fields.One2many('oauth.access_token', 'application_id', 'Tokens')

    _sql_constraints = [
        ('client_id_uniq', 'unique (client_id)', 'client_id must be unique'),
    ]