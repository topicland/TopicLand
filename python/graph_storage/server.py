#!/usr/bin/env python3

import os
import sys
import logging
import argparse
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
import pymysql.cursors

import model

logger = logging.getLogger("openmldb_server")

app = Flask(__name__,
            template_folder="./dist/",
            static_folder="./dist",
            static_url_path="")
cors = CORS(app, resources=r'/*')

app.config['CORS_HEADERS'] = 'Content-Type'

# Define parameters
parser = argparse.ArgumentParser()
parser.add_argument(
    "--host",
    default=os.environ.get("HOST", "0.0.0.0"),
    help="The host of the server(eg. 0.0.0.0)")
parser.add_argument(
    "--port",
    default=int(os.environ.get("PORT", "7788")),
    help="The port of the server(eg. 7788)",
    type=int)
parser.add_argument(
    "--debug",
    default=bool(os.environ.get("DEBUG", "false")),
    help="Enable debug for flask or not(eg. true)",
    type=bool)

args = parser.parse_args(sys.argv[1:])
for arg in vars(args):
    logger.info("{}: {}".format(arg, getattr(args, arg)))

db_config = model.DbConfig("localhost", "root", "wawa316", "cyberpunk_edgerunner")
graph = model.Graph()
#graph.load_from_db(db_config)

"""
@app.route('/')
@cross_origin()
def index():
    return render_template("index.html")
"""

@app.route('/api/<db>/nodes', methods=['GET'])
@cross_origin()
def get_nodes(db):
    num = request.args.get('num', default = -1, type = int)
    result = {"nodes": graph.get_nodes_for_frontend(db_config, num)}
    return jsonify(result)

@app.route('/api/<db>/edges', methods=['GET'])
@cross_origin()
def get_edges(db):
    result = {"edges": graph.get_edges_for_frontend(db_config)}
    return jsonify(result)

@app.route('/api/<db>/groups', methods=['GET'])
@cross_origin()
def get_groups(db):
    print(graph.groups)
    result = {"groups": graph.groups}
    return jsonify(result)    

def main():
  # Start web browser if possible
  # webbrowser.open("http://{}:{}".format(args.host, args.port))

  # TODO: debug config does not work
  app.run(host=args.host,
          port=args.port,
          threaded=True,
          debug=args.debug)

if __name__ == "__main__":
  main()