import nltk
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from build_load import get_f_names
import cPickle
import time


def increment_last_number(s):
    for i in range(len(s)-1, -1, -1):
        if s[i] == ' ':
            return s[0:i+1] + str(int(s[i+1:len(s)]) + 1)
        
def save_word_fileid():
    cPickle.dump(word_fileid,open("word_fileid.dat",'w'), cPickle.HIGHEST_PROTOCOL)

def load_word_fileid():
    return cPickle.load(open("word_fileid.dat",'r'))

def save_word_freq():
    cPickle.dump(word_freq,open("word_freq.dat",'w'), cPickle.HIGHEST_PROTOCOL)

def load_word_freq():
    return cPickle.load(open("word_freq.dat",'r'))

word_fileid = {}
word_freq = {}
stemmer = PorterStemmer()
dirname = "/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/"
f_names = get_f_names()
stopset = set(stopwords.words('english'))

start_time = time.time()

for f_name in f_names:
    with open(dirname + f_name,'r') as f:
        text = re.sub(r"[\W]", " ", f.read())
        tokens = nltk.word_tokenize(text.lower())
        file_id = str(f_names.index(f_name))
        for token in tokens:
            if token not in stopset:
                word = stemmer.stem(token)
                if word in word_freq: #seen word
                    if file_id in word_fileid[word].split(): #seen word, seen file
                        word_freq[word] = increment_last_number(word_freq[word])
                    else: #seen word, new file
                        word_fileid[word] += ' ' + file_id
                        word_freq[word] += ' 1'
                else: #new word
                    word_freq[word] = ' 1'
                    word_fileid[word] = ' ' + file_id

save_word_fileid()
save_word_freq()
# print word_fileid
# print word_freq

duration = time.time() - start_time
print("--- %s seconds ---" % (duration))

    