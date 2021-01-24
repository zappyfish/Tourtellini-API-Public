from places.radar_search import RadarClient
from places.yelp import YelpClient


class PlacesClient:

    DEFAULT_SEARCH_RADIUS = 1000

    def __init__(self):
        self.radar_client = RadarClient()
        self.yelp_client = YelpClient()

    def get_places(self, lat, lng, categories=None, chains=None, groups=None, radius=DEFAULT_SEARCH_RADIUS, limit=250):
        places = self.radar_client.get_places(lat, lng, categories, chains, groups, radius, limit)
        for place in places:
            if 'yelpId' in place:
                yelp_review = self.yelp_client.get_reviews(place['yelpId'])
                if yelp_review is not None:
                    place['yelp_review'] = yelp_review

        return places
