from urllib2 import Request, urlopen, URLError
import jsonpickle
API_KEY = "AIzaSyD4r0qGg8gCnKMmGPlgkdWd6MOTwWGDLaw"
GOOGLE_GEOCODING_BASE_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key="+API_KEY

def nearby_search(lat,lng,radius):
    url = GOOGLE_GEOCODING_BASE_URL+"&location="+str(lat)+","+str(lng)+"&radius="+str(radius)
    try:
        request = Request(url)
        response = jsonpickle.decode((urlopen(request)).read())
        if (response["status"] == 'OK'):
            return response["results"]
        else:
            return {}
    except  URLError:
        print("Request failed")
        return {}

def is_place_an_establishment(place):
    if "establishment" in place["types"]:
        return True
    return False

print(nearby_search(-7.233453,-39.409775 , 5)[1]["types"])