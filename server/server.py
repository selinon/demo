import os
import json
from flask import Flask, send_from_directory, abort, Response, jsonify, request, redirect
from werkzeug.utils import secure_filename
from .serverFlowInfo import ServerFlowInfo, YAML_FILES_DIR, CONFIG_PY_PATH

import sys

GRAPH_DIR = os.path.join(YAML_FILES_DIR, 'graphs')
UPLOAD_DIR = 'uploads'


app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/js/<file>', defaults={'subdir': 'js'})
@app.route('/img/<file>', defaults={'subdir': 'img'})
@app.route('/fonts/<file>', defaults={'subdir': 'fonts'})
@app.route('/css/<file>', defaults={'subdir': 'css'})
def static_files(subdir, file):
    return send_from_directory(os.path.join(app.static_folder, subdir), file)


@app.route('/html/<file>')
def html(file):
    if file == 'flows.html':
        return ServerFlowInfo.render_flow_template()
    else:
        return send_from_directory(app.static_folder, file)


@app.route('/graph/<flow>')
def flow_graph(flow):
    return send_from_directory(GRAPH_DIR, flow)


@app.route('/config-file/<path:file>')
def system_conf(file):
    if file != "nodes.yaml" and file != "nodes.yml":
        file = os.path.split(file)

        if len(file) != 2 or file[0] != 'flows':
            abort(404)

        return send_from_directory(os.path.join(YAML_FILES_DIR, 'flows'), file[1])
    else:
        return send_from_directory(YAML_FILES_DIR, file)


@app.route('/config-files')
def config_files():
    nodes_yml, flows = ServerFlowInfo.get_config_files()
    # remove config/ directory prefix
    ret = {
        'nodes': os.path.join(*(nodes_yml.split(os.path.sep)[1:])),
        'flows': [os.path.join(*(flow_yml.split(os.path.sep)[1:])) for flow_yml in flows]
    }
    return jsonify(ret)


@app.route('/run/<flow_name>', methods=['POST'])
def run(flow_name):
    try:
        if request.form['args']:
            args = json.loads(request.form['args'])
        else:
            args = None
        dispatcher_id = ServerFlowInfo.run(flow_name, args)
        return jsonify({'dispatcher_id': dispatcher_id})
    except Exception as exc:
        return jsonify({'error': str(exc)})


@app.route('/config.py')
def config_py():
    if not os.path.isfile(CONFIG_PY_PATH):
        abort(404)

    with open(CONFIG_PY_PATH, 'r') as f:
        content = f.read()

    return Response(content, mimetype='text/x-python')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or not request.files['file']:
        return jsonify({'error': 'No file in request'})
    file = request.files['file']
    # if a user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No file in request'})
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_DIR, filename)
        file.save(file_path)
        try:
            ServerFlowInfo.from_archive(file_path)
        except Exception as exc:
            return jsonify({'error': str(exc)})
        finally:
            os.remove(file_path)
        return redirect("/#flows")
    else:
        return jsonify({'error': 'No file in request'})
