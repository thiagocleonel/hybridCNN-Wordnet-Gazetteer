from urllib2 import Request, urlopen, URLError
import jsonpickle
API_KEY = "AIzaSyD4r0qGg8gCnKMmGPlgkdWd6MOTwWGDLaw"
GOOGLE_GEOCODING_BASE_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key="+API_KEY

#radius = diameter in meters  
def nearbySearch(lat,lng,radius):
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

def isPlaceAnEstablishment(place_types):
    if "establishment" in place_types:
        return True
    return False

def listCategories(lat,lon,radius,nCategory): 
    #Gets the top-nCategory from each of the nearby places inside the given radius in Km
    return_hash = {}
    response_array = nearbySearch(lat,lon,radius)
    for place_hash in response_array:
        encoded_types = [place_type.encode('UTF-8') for place_type in place_hash['types']]
        if(isPlaceAnEstablishment(encoded_types)):
            return_hash[place_hash['name'].encode('UTF-8')] = encoded_types
    return return_hash      

