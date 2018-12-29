from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from instance.config import app_config
from .api.v1.views.auth_endpoints import auth, BLACKLIST
from .api.v1.views.question_endpoints import question

def create_app(config):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config])
    app.config["TESTING"] = True


    app.config['JWT_SECRET_KEY'] = 'mysecretkey'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    jwt = JWTManager(app)


    @jwt.user_claims_loader
    def add_claims_to_access_token(user_object):

        return {'username': user_object['username']}

    @jwt.user_identity_loader
    def user_identity_lookup(user_object):

        return user_object["username"]

    @jwt.token_in_blacklist_loader
    def check_if_token_blacklist(decrypted_token):

        json_token_identifier = decrypted_token['jti']
        return json_token_identifier in BLACKLIST


    @app.errorhandler(400)
    def bad_request(error):
        '''error handler for Bad request'''
        return jsonify(dict(error='Bad request')), 400

    @app.errorhandler(404)
    def Resource_not_found(error):

        return jsonify(dict(error='Resource not found')), 404

    @app.errorhandler(405)
    def unauthorized(error):

        return jsonify(dict(error='Method not allowed')), 405

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        return jsonify(dict(error='Internal server error')), 500

    app.register_blueprint(auth)
    app.register_blueprint(question)


    return app
