from flask import jsonify
from flask_jwt_extended import JWTManager

from config.blacklist import BLACKLIST

def jwt_init(app):
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token_blacklist(decrypted_token):
        return decrypted_token['jti'] in BLACKLIST

    @jwt.user_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {'is_admin': True}
        return {'is_admin': False}

    @jwt.expired_token_loader
    def expired_token_callback():
        return jsonify({
            'message': 'The token has expired',
            'error': 'token_expired'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'description': 'Oi YAMERO',
            'error': 'invalid_token'
        }), 401

    @jwt.unauthorized_loader
    def unauthorized_token_callback():
        return jsonify({
            'desscription': 'Request does not contain an access token',
            'error': 'authorization_required'
        }), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback():
        return jsonify({
            'desscription': 'Current token is not fresh',
            'error': 'fresh_token_required'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback():
        return jsonify({
            'desscription': 'The current token is revoked',
            'error': 'token_revoked'
        }), 401