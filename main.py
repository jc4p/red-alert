from flask import Flask, request, jsonify
from models import *
import time

HUE_MIN = 46920 # blue
HUE_MAX = 65280 # red
LIGHTS = [4, 5]
l = LightGateway()
l.on(LIGHTS)
l.brightness(LIGHTS, 200)

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return "Hi!"

@app.route("/beat", methods=["POST"])
def beat():
    rate = request.form.get("rate", "")
    if not rate:
        raise InvalidRequestError("No rate")
    hr_scale = get_scalar(float(rate))
    hue = get_hue(hr_scale)
    l.update(LIGHTS, hue)
    return "Updated to {}".format(hue)

def get_scalar(rate):
    HR_LOW = 55.0
    HR_HIGH = 180.0
    if rate < HR_LOW:
        return 0.0
    if rate > HR_HIGH:
        return 1.0

    return (rate - HR_LOW) / (HR_HIGH - HR_LOW)

def get_hue(hr_scale):
    return int(HUE_MIN + ((HUE_MAX - HUE_MIN) * hr_scale))

def should_strobe(hr_scale):
    return hr_scale > 0.70

class InvalidRequestError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidRequestError)
def handle_invalid_request_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0")
