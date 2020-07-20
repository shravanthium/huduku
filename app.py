from flask import request, jsonify, Flask
from core.huduku import Huduku

config = {
    "DEBUG": True,
}

app = Flask(__name__)

app.config.from_mapping(config)


@app.route("/")
def index():
    return "<br/><h3>HUDUKU</h3><p>Semantic Document Search Engine.</p>"


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    K = int(request.args.get("K"))
    hd = Huduku()
    return jsonify(hd.search(K, query))


@app.route("/list", methods=["GET"])
def list():
    query_list = eval(request.args.get("queries"))
    K = int(request.args.get("K"))
    hd = Huduku()
    return jsonify(hd.bulk_search(K, query_list))
