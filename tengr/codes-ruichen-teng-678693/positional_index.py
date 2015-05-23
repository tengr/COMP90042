import nltk
import re
import os
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords   
import cPickle

posdic = {}
stemmer = PorterStemmer()
dirname = "/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/"
filenames = [f for f in os.listdir(dirname) if os.path.isfile(dirname + f) and os.path.getsize(dirname + f) > 0 ]
stopset = set(stopwords.words('english'))
 
for filename in filenames:
    with open(dirname + filename,'r') as f:
        text = re.sub(r"[\W]", " ", f.read())
        tokens = nltk.word_tokenize(text.lower())
        for i in xrange(len(tokens)):
            word = stemmer.stem(tokens[i].decode('utf8', 'ignore'))
            if word in posdic:
                if filename in posdic[word]:
                    posdic[word][filename].append(i)
                else:
                    posdic[word][filename] = [i]
            else: 
                posdic[word] = {}
                posdic[word][filename] = [i]
cPickle.dump(posdic,open("posdic.dat",'w'), cPickle.HIGHEST_PROTOCOL)
# posdic = cPickle.load(open("posdic.dat","r"))

