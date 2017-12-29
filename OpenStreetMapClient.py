from urllib2 import Request, urlopen, URLError
import jsonpickle

def search(word):
    url = "http://nominatim.openstreetmap.org/search/"+word.replace(" ", "+")+"?format=jsonv2"
    request = Request(url)
    response = urlopen(request)
    nodeList = jsonpickle.decode(response.read())
    return nodeList

def reverse_search(lat,lon):
    url = "http://nominatim.openstreetmap.org/reverse?format=jsonv2&lat="+str(lat)+"&lon="+str(lon)
    request = Request(url)
    response = urlopen(request)
    node = jsonpickle.decode(response.read())
    return node


