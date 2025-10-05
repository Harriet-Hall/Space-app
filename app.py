from flask import Flask, request
from jinja2 import Environment, FileSystemLoader, select_autoescape
import requests
import math

app = Flask(__name__)

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

# response = requests.get("https://ssd-api.jpl.nasa.gov/sentry.api")
# asteroid_dict = response.json()
# asteroids = asteroid_dict["data"]
# print(asteroids[1]["fullname"])

def get_asteroid(asteroids, asteroid_name):
    for asteroid in asteroids:
        if asteroid["fullname"] == asteroid_name:
            return asteroid
        else:
            continue



def compute_crater_radius(asteroid):
    constant = 0.55
    gravity = 9.8
    asteroid_density = 3000
    earth_density = 2700
    print(asteroid["diameter"])
    if not asteroid["diameter"]:
        asteroid_diameter = asteroid["diameter"]
    else:
        asteroid_diameter = 10
    if not asteroid["v_inf"]:
        impact_velocity = asteroid["v_inf"]
    else:
        impact_velocity = 30
    crater_diameter = constant * (gravity **-0.22) *(asteroid_density/earth_density)**0.3*float(asteroid_diameter)**0.78*float(impact_velocity)**0.44
    crater_radius = crater_diameter / 2
    return crater_radius

@app.route("/", methods=["GET","POST"])
def hello_world():
    if request.method == 'GET':
        if request.args.get("asteroid"):
            asteroid_name = request.args.get("asteroid")
            print(asteroid_name)

            response = requests.get("https://ssd-api.jpl.nasa.gov/sentry.api")
            asteroid_dict = response.json()
            asteroids = asteroid_dict["data"][:10]

            asteroid = get_asteroid(asteroids, asteroid_name)
            radius = compute_crater_radius(asteroid) * 1000

            template = env.get_template('index.html')
            return template.render(asteroids=asteroids, radius=radius)

    response = requests.get("https://ssd-api.jpl.nasa.gov/sentry.api")
    asteroid_dict = response.json()
    asteroids = asteroid_dict["data"][:10]

    template = env.get_template('index.html')
    return template.render(asteroids=asteroids)
        

# @app.route("/asteroid?asteroid=<asteroid_name>")
# def asteroid_name():
#     asteroid_name = request.args.get('asteroid')
#     return f"<p>{asteroid_name}</p>"
    