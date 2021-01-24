from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from database.database import DatabaseReference
from database.tours import Tours
from places.search_places import PlacesClient

app = Flask(__name__)
CORS(app, support_credentials=True)
db_ref = DatabaseReference()
tours = Tours(db_ref)
places_client = PlacesClient()


@app.route("/tours/create", methods=["POST"])
@cross_origin(supports_credentials=True)
def create_tour():
    global tours
    tour_info = request.json
    has_error, error_message = tours.check_has_error(tour_info)
    if has_error:
        return jsonify({'error': error_message}), 400

    tours.save_tour(waypoints=request.json)
    return "OK"


@app.route("/tours/available", methods=["GET"])
@cross_origin(supports_credentials=True)
def see_available_tours():
    global tours
    return jsonify(tours.get_available_tours())


@app.route("/tours/load", methods=["GET"])
@cross_origin(supports_credentials=True)
def load_tour():
    global tours
    desired_tour_id = request.args['tour_id']
    return jsonify(tours.get_tour(tour_id=desired_tour_id))


@app.route("/buildings/nearby", methods=["GET"])
def nearby_buildings():
    global places_client
    params = request.args
    lat = float(params["lat"])
    lng = float(params["lng"])

    if lat == 0 or lng == 0:
        return jsonify({'error': 'Invalid lat,lng'}), 400

    radius = int(params["radius"]) if "radius" in params else RadarClient.DEFAULT_SEARCH_RADIUS

    get_val = lambda v : params[v] if v in params else None
    places = places_client.get_places(lat,
                                      lng,
                                      categories=get_val("categories"),
                                      chains=get_val("chains"),
                                      groups=get_val("groups"),
                                      radius=radius)

    if places is None:
        return jsonify({'error': 'Missing one of chains, categories, or groups'}), 400
    else:
        return jsonify(places)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
