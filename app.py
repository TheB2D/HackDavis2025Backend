# app.py
import os
from flask import Flask, request, jsonify  # type: ignore
from dotenv import load_dotenv  # type: ignore

# load environment variables from .env
load_dotenv()

# Helper modules
from oc_gleif import lookup_company
from oc_nominatim import geocode_company, geocode_address
from sea_routes import estimate_sea_route  # type: ignore
from parcel import track_parcel

import barcode
import insight_finder

app = Flask(__name__)

@app.route("/barcode", methods=["GET"])
def get_company():
    # Query parameters
    barcode_number = request.args.get("barcode_number")

    item_id = barcode.get_barcode_title(barcode_number)

    return jsonify({"item_description": item_id})

@app.route("/insights", methods=["GET"])
def insight():

    query = request.args.get("company")

    response = insight_finder.get_insights(query)

    return jsonify(response)


if __name__ == "__main__":
    host  = os.getenv("HOST", "127.0.0.1")
    port  = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)