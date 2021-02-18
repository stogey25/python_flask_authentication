from basic_auth import app, server
from basic_auth.requires_authorization import requires_authorization
from flask import jsonify


@app.route('/api/secret')
@requires_authorization
def api_secret():
    return jsonify({'message': server.get_server_status()})
