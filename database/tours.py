
class Tours:

    def __init__(self, db_ref):
        self.db_ref = db_ref

    def _validate_stop(self, stop):
        expected_fields = ["stop_number", "name", "lat", "lng", "address", "user_comment"]
        for field in expected_fields:
            if field not in stop:
                return False

        return True

    # Returns bool, str (has_error, error_message)
    def check_has_error(self, tour_data):
        expected_fields = ["tour_description", "tour_name", "user_id", "stops"]
        for field in expected_fields:
            if field not in tour_data:
                error_message = "Request is missing field {}".format(field)
                return True, error_message

        if len(tour_data["stops"]) < 1:
            return True, "Request must have at least one stop on the tour."

        for i, stop in enumerate(tour_data["stops"]):
            if not self._validate_stop(stop):
                return True, "Stop #{} on tour has invalid format.".format(i)

        return False, ""

    def save_tour(self, waypoints):
        keys = ["tours"]
        user_tour_keys = self.db_ref.keys_at_path(keys)
        tour_id = 0 if user_tour_keys is None else str(len(user_tour_keys))
        keys.append(str(tour_id))
        self.db_ref.save_json_data(keys, waypoints)

    def get_available_tours(self):
        tour_refs = self.db_ref.load_json_data(["tours"])
        available_tours = []
        for tour in tour_refs.each():
            tour = \
                {
                    'description': tour.val()['tour_description'],
                    'name': tour.val()['tour_name'],
                    'id': tour.key()
                }
            available_tours.append(tour)

        return available_tours

    def get_tour(self, tour_id):
        return self.db_ref.load_json_data(["tours", tour_id]).val()
