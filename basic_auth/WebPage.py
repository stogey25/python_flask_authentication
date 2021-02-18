import os

from basic_auth import app, server
from basic_auth.requires_authorization import requires_authorization
from flask import render_template, redirect, abort, send_file, request


@app.route('/')
@requires_authorization
def index():
    return render_template('index.html', message=server.get_server_status())


@app.route('/resetButton')
@requires_authorization
def button():
    new_status = server.reset_server()
    return redirect('/')


@app.route('/files', methods=['GET', 'POST'])
@requires_authorization
def files():

    # Joining the base and the requested path
    abs_path = os.path.abspath(app.config['BACKUP_DIR'])

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', path=abs_path, files=files)


@app.route('/files/<path:path>')
@requires_authorization
def download(path):
    return send_file(os.path.join(app.config['BACKUP_DIR'], path))
