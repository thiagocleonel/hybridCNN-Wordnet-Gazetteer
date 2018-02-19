import HybridIdentifier as hybrid_identifier
import GooglePlacesClient as gpc
import sys #For command-line arguments parsing
import os.path #For check if lat-lon textfile exists

hybridCNN_categories = 0
latlon_textfile_path = ''
default_radius = 100 #100 meters as default radius for GooglePlaces

#None arguments
if(len(sys.argv) == 1):
    print 'Usage: python ' +sys.argv[1]+ ' (lat-lon textfile) (images_dir(optional))'
    sys.exit()

#Only lat-lon textfile given as argument; Check if file exists
if(len(sys.argv) == 2):
    given_path = sys.argv[1]
    if(not (os.path.isfile(given_path))):
        print "Lat-lon textfile doesn't exist"
        sys.exit()
    #hybridCNN_categories = hybrid_identifier.execute(nCategory=5)    
    latlon_textfile_path = given_path

#Lat-lon textfile AND images directory path given as arguments
if(len(sys.argv) == 3):
    given_latlon_path = sys.argv[1]
    given_imagesdir_path = sys.argv[2]
    if(not(os.path.isfile(given_latlon_path))):
        print "Lat-lon textfile doesn't exist" 
        sys.exit()
    latlon_textfile_path = given_latlon_path
    if(not (os.path.isdir(given_imagesdir_path))):
        print "Image(s) directory doesn't exists"
        sys.exit()
    hybridCNN_categories = hybrid_identifier.execute(given_imagesdir_path,5) #Gets the top-nCategory for each image present in DEFAULT_DIR 

#Import Lat and lon coordinates
src_file = open(latlon_textfile_path, 'r')
coordinates = []
gpc_categories = []
for line in src_file:
    pair = [float(x.strip()) for x in line.split(',')]
    coordinates.append(pair)
    categories = gpc.listCategories(pair[0],pair[1],default_radius,5)
    gpc_categories.append(categories)
print gpc_categories








