from json import dump
import time
from os import getenv, environ
import requests
from flask import Flask, render_template, request
from modules import url_creator
from week_days import Week

application = app = Flask(__name__)
home_page = "home_page.html"
forcast_page = "forecast.html"


@app.route('/')
def index():
    """open the home page"""
    return render_template(home_page, success="True", color=f"{getenv('BG_COLOR')}")


@app.route('/weather', methods=["GET"])
def weather():
    """open page with data from api request"""
    global response, this_week
    response = this_week = None
    location = request.args.get('location')
    url_api = url_creator.get_url(location)
    try:
        # api req for weather data
        response = requests.get(url_api).json()
        this_week = Week(response)
        # saves the data to PV
        filename = f"{response['address']}_{time.strftime('%d-%m-%Y_%H-%M-%S')}"
        with open(f"/search_history/{filename}.json", "w") as forcast:
            dump(response, forcast)

    except (Exception):
        # route to homepage with fail alert
        return render_template(home_page, success="False", color=f"{getenv('BG_COLOR')}")

    else:
        # route to forcast webpage
        return render_template(forcast_page, place=response['resolvedAddress'], week=this_week)


if __name__ == "__main__":
    app.run(port=5051)
