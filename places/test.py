from search_places import PlacesClient

client = PlacesClient()
places = client.get_places(41.904485, -87.634791, categories="food-beverage")
print(places)