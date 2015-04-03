#!/usr/local/bin/python2.7
# encoding: utf-8
'''
inverted_index_generator -- shortdesc
 
inverted_index_generator is a description
 
It defines classes_and_methods
 
@author:     user_name
 
@copyright:  2015 organization_name. All rights reserved.
 
@license:    license
 
@contact:    user_email
@deffield    updated: Updated
'''
 
import os
from my_parser import *
import cPickle
 
def get_filtered_words(text):
    text = text.lower() 
    text = re.sub(r'[^a-z0-9 ]',' ',text)
    text = text.split()
    return [w for w in text if not w in stopwords.words('english')]

# Stemming.
# Return | A list of stemmed words.
def stemming(text):    
    stemmer = PorterStemmer()
    stemmed_words = []
    for word in text:
        stemmed_words.append(stemmer.stem(word))
    return stemmed_words
# Generate inverted index using one word index strategy.
def generate_inverted_index_one_word_strategy(text,file_name,inverted_index):
    for word in text:
        if not inverted_index.has_key(word):
            inverted_index[word] = {}
            inverted_index[word][file_name] = 1
        else:
            if not inverted_index[word].has_key(file_name):
                inverted_index[word][file_name] = 1
            else:
                inverted_index[word][file_name] = inverted_index[word][file_name] + 1
 
 
# Generate inverted index.
def generate_inverted_index(generator1,text,file_name,inverted_index):
    generator1(text,file_name,inverted_index)
     
# Export inverted index.
def export_inverted_index(obj, file_name):
    with open(file_name, 'wb') as file:
        cPickle.dump(obj, file, protocol = cPickle.HIGHEST_PROTOCOL)
        
        
# Get the file names of all blogs.    
file_names = [file_name for file_name in os.listdir('/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/') if file_name[-4:] == '.txt']
 
         
# Generate inverted index by reading all files.
inverted_index = {}
for file_name in file_names:
    with open('/Users/ruichen/Documents/COMP90042/proj1/proj1data/blogs/'+ file_name,'r') as file:
        text = file.read()
        filtered_words = get_filtered_words(text)
        stemmed_words = stemming(filtered_words)
        generate_inverted_index(generate_inverted_index_one_word_strategy, stemmed_words,file_name,inverted_index)
        
export_inverted_index(inverted_index, 'inverted_index')
print 'Success!!'