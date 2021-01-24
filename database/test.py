from database import DatabaseReference
from tours import Tours


db_ref = DatabaseReference()
tours = Tours(db_ref)

data = {'description': 'tour!!', 'tour_name': 'yay'}

tours.save_tour(data)