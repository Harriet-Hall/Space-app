from flask import Flask
from jinja2 import Environment, FileSystemLoader, select_autoescape

app = Flask(__name__)

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

@app.route("/")
def hello_world():
    template = env.get_template('index.html')
    return template.render()