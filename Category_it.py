import nltk
import os
import random
from nltk.stem.lancaster import LancasterStemmer
# word stemmer
stemmer = LancasterStemmer()

# nltk.download()

# 7 classes of training data
training_data = []
file = open('./storage/categorytestset.txt', mode='r')
lines = file.readlines()
for line in lines:
    c,s = line.split("\t")
    # print("c:",c,"s:",s, end="")
    training_data.append({"class":c, "sentence":s})

file.close()

print ("%s sentences of training data" % len(training_data))

# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    # prepare a list of words within each class
    class_words[c] = []

# loop through each sentence in our training data
for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1

            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])

# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
# print ("Corpus words and counts: %s \n" % corpus_words)
# also we have all words in each class
# print ("Class words: %s" % class_words)

# calculate a score for a given class
def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with same weight
            score += 1
            
            if show_details:
                print ("   match: %s" % stemmer.stem(word.lower() ))
    return score

    # we can now calculate a score for a new sentence
sentence = "sentence: two children are playing on golf field"

# now we can find the class with the highest score
for c in class_words.keys():
    print ("Class: %s  Score: %s \n" % (c, calculate_class_score(sentence, c)))

# calculate a score for a given class taking into account word commonality
def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1/corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score

# we can now calculate a score for a new sentence
sentence = "sentence: two children are playing on golf field"

# now we can find the class with the highest score
for c in class_words.keys():
    print ("Class: %s  Score: %s \n" % (c, calculate_class_score(sentence, c)))

# return the class with highest score for sentence
def classify(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score(sentence, c, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score

    return high_class, high_score

##################################################################
##################################################################



def recommendTags(sen):
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    # print("Files in %r: %s" % (cwd, files))

    category = [[], [], [], [], [], [], [], []]

    # readline_all.py
    #f = open('C://Users/JIWON/Desktop/taglist/fashion.txt', 'r')

    # store crawling result into category List
    for i in range(1,9):
        filename = "./taglist/"
        filename += str(i) + ".txt"
        f = open(filename)
        while True:
            line = f.readline()
            if not line: break
            #print(line[1:])
            category[i-1].append(line[1:-1])

        f.close()

    # #category[0].append()
    # print(category)
    # print(c_result)
    dic = {'holiday':0,'beauty':1, 'couple':2, 'fashion':3, 'pets':4, 'food':5, 'travel':6, 'fitness':7 }
    c_result = classify(sen)[0]
    index = dic[c_result]

    return c_result, random.sample(category[index], 5)
# index

###########################최종 출력###########################
##############################################################
# sen = "two children are playing on golf field"
# c_result = classify(sen)[0]

# index = dic[c_result]
# randomList = random.sample(category[index], 3)

# print("sentence: " + sen)
# print("category: " + c_result)
# print(randomList)
##############################################################
##############################################################