from nltk.corpus import wordnet as wn

min_acceptable_relatedness = 80.0


def fast_nouns_similarity(word1,word2):
    synset1 = wn.synset(word1+".n.01")
    synset2 = wn.synset(word2+".n.01")
    return synset1.wup_similarity(synset2)
    

def nouns_similarity(word1,word2):
    result = float(0)
    synsets_word1 = wn.synsets(word1, pos=wn.NOUN)
    synsets_word2 = wn.synsets(word2, pos=wn.NOUN)
    for synset1 in synsets_word1:
        #if not (str(synset1.name()).startswith(word1)):
          #  continue
        for synset2 in synsets_word2:
            #if not (str(synset2.name()).startswith(word2)):
            #    continue
            relatedness = synset1.wup_similarity(synset2)
            print "relatednwss btw " + str(synset1.name()) + " and " + str(synset2.name())+": " + str(relatedness)
	    if (relatedness > result):
	        result = relatedness;
    print result
    return result

def is_nouns_related(word1,word2):
    if(nouns_similarity(word1,word2)*100 > min_acceptable_relatedness):
        return True
    return False

    


