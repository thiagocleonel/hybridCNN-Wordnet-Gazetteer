CAFFE_ROOT = '/home/thiago/caffezao/'
#IMAGE_PATH = '/home/thiago/Downloads/21273001_878718632279943_1207216092928458353_o.jpg'
IMAGES_DIR = '/home/thiago/images_ia/toAnalyze/'
CSV_LABELS_PATH = CAFFE_ROOT + 'models/hybrid_cnn/categoryIndex_hybridCNN.csv'
OUTPUT_FILE = '/home/thiago/tcc-output.txt'
SYNSET_WORDS_PATH = '/home/thiago/caffe/data/ilsvrc12/synset_words.txt'

import sys
import caffe
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def configureTools():

    plt.rcParams['figure.figsize'] = (10,10)
    plt.rcParams['image.interpolation'] = 'nearest'
    plt.rcParams['image.cmap'] = 'gray'

def importCaffe():

    sys.path.insert(0, CAFFE_ROOT+'python')


#Setup Caffe and instantiates net
def setupCaffe():
    caffe.set_mode_cpu()

def getNet():
    model_def = CAFFE_ROOT + 'models/hybrid_cnn/hybridCNN_deploy.prototxt'
    model_weights = CAFFE_ROOT + 'models/hybrid_cnn/hybridCNN_iter_700000.caffemodel'
    net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)
    return net

def loadAndConfigureMean():
    mu = np.load(CAFFE_ROOT + 'models/hybrid_cnn/hybridCNN_mean.npy')
    mu = mu.mean(1).mean(1)
    print 'mean-subtracted values:', zip('BGR', mu)
    return mu

def createTransformer(net, mean):
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', mean)
    transformer.set_raw_scale('data',255)
    transformer.set_channel_swap('data',(2,1,0))
    return transformer

def transform_images(transformer):
    result_hash = {}
    for filename in os.listdir(IMAGES_DIR):
        image = caffe.io.load_image(os.path.join(IMAGES_DIR+filename))
        transformed_image = transformer.preprocess('data',image)
        result_hash[IMAGES_DIR+filename] = transformed_image
    return result_hash

def predictClass(net, transformed_image):

    net.blobs['data'].reshape(50,        # batch size
                          3,         # 3-channel (BGR) images
                          227, 227)  # image size is 227x227
    net.blobs['data'].data[...] = transformed_image

    output = net.forward()
    output_prob = output['prob'][0] # the output probability vector for the first image in the batch
    #print 'predicted class is:', output_prob.argmax()
    return output_prob

def outputClassLabel(output_prob):
    labels = np.loadtxt(CSV_LABELS_PATH, str, delimiter='\t')
    #print 'output label:', labels[output_prob.argmax()]
    top_inds = output_prob.argsort()[::-1][:5]  # reverse sort and take five largest items
    #print 'probabilities and labels:'
    #print zip(output_prob[top_inds], labels[top_inds])
    return zip(output_prob[top_inds], labels[top_inds])
    #labels[output_prob.argmax()]

def openGoogleAndSearch(term):
    url = "https://www.google.com/search?q={}".format(term)
    webbrowser.open(url)

def stamp(label, image_path, y):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("LiberationMono-Bold.ttf", int(img.size[1]*0.025))
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((0, y*int(img.size[0]*0.025)),label,(140,140,140),font=font)
    img.save(image_path)

def findSynsetWord(word):
    synsetWordsFile = open(SYNSET_WORDS_PATH, "r")
    while True:
        line = synsetWordsFile.readline()
        if not line: break
        if word in line: return line
    return 'synset word not found'




if __name__ == '__main__':
    configureTools()
    importCaffe()
    setupCaffe()
    net = getNet()
    mean = loadAndConfigureMean()
    transformer = createTransformer(net, mean)
    transformed_images = transform_images(transformer)
    for image_path, image in transformed_images.iteritems():
        output_file = open(OUTPUT_FILE , 'a')
        #Magic happens at next line =)
        output_prob=predictClass(net,image)
        labels = outputClassLabel(output_prob)
        print "ARQUIVO: ", image_path, "\n ",labels, "\n"
        output_file.write("ARQUIVO: " + image_path + "\n " + str(labels) + "\n")
        for i in range(0,len(labels)):
            probability = labels[i][0]
            word_code = labels[i][1].split()[0]
            print "WordCode: " + word_code
            if "/" in word_code:
                #Places CNN codes are self-described, so they don't need any handling
                stamp_text = str(probability) + " " + word_code
            else:
                #ImageNet codes need some search on the synset_words.txt file to find the name of the class
                stamp_text = str(probability) + " " + str((findSynsetWord(word_code)).split()[1])
            stamp(stamp_text,image_path,i)



    #openGoogleAndSearch(label)


