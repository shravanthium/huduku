from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<br/><h3>HUDUKU</h3><p>Semantic Document Search Engine.</p>"
