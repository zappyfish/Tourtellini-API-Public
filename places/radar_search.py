from radar import RadarClient as _RadarClient


class RadarClient:

    SECRET_KEY = "REDACTED"

    def __init__(self):
        self.radar = _RadarClient(RadarClient.SECRET_KEY)

    def get_places(self, lat, lng, categories, chains, groups, radius, limit):
        if categories is None and chains is None and groups is None:
            print("Error: no valid search term received.")
            return None

        places = self.radar.search.places([lat, lng],
                                          chains=chains,
                                          categories=categories,
                                          groups=groups,
                                          radius=radius,
                                          limit=limit)

        return [place.raw_json for place in places]
