import requests


class YelpClient:

    API_KEY = "REDACTED"

    def __init__(self):
        self.headers = {'Authorization': 'Bearer {}'.format(YelpClient.API_KEY)}

    @staticmethod
    def relevant_json(js):
        if 'error' in js:
            return None

        return {
            'review_count': js['review_count'],
            'phone_number': js['phone'],
            'rating': js['rating'],
            'address': ', '.join(js['location']['display_address']),
            'description': ', '.join([cat['title'] for cat in js['categories']])
        }

    def get_reviews(self, yelp_id):
        url = "https://api.yelp.com/v3/businesses/{}".format(yelp_id)
        resp = requests.get(url, headers=self.headers)
        js = resp.json()
        relevant_data = YelpClient.relevant_json(js)
        return relevant_data
