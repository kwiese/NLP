#Author: Kyle Wiese
#Programming Assignment 4 (Naive Bayes Implementation)

import nltk
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords as sw
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier as nb
from nltk.classify import SklearnClassifier
from sklearn.svm import SVC
import string
import random

#Get Feature Set
def document_features(document, word_features):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

#Cross-Validate
#test_set_section is from 1 to 10
def getTrainingSet(features, test_set_section):
	training_set = []
	if(test_set_section > 1):
		for i in xrange(0, ((test_set_section - 1) * 200), 200):
			training_set += features[i:i+200]
		if(test_set_section < 10):
			for i in xrange(((test_set_section) * 200), 2000, 200):
				training_set += features[i:i+200]
	else:
		for i in xrange(((test_set_section) * 200), 2000, 200):
				training_set += features[i:i+200]
	return(training_set)

def getTestSet(features, test_set_section):
	return(features[((test_set_section - 1) * 200):(test_set_section * 200)])

def main():
	#Get all words in all 2000 documents
	all_documents = [(list(movie_reviews.words(fileid)), category)
					for category in movie_reviews.categories()
					for fileid in movie_reviews.fileids(category)]

	#shuffle words
	random.shuffle(all_documents)

	#Get all words used in the negative reviews
	neg_documents = [list(movie_reviews.words(fileid)) 
					for category in movie_reviews.categories()
					for fileid in movie_reviews.fileids(category)
					if category == "neg"]
	#Get all words used in the positive reviews
	pos_documents = [list(movie_reviews.words(fileid)) 
					for category in movie_reviews.categories()
					for fileid in movie_reviews.fileids(category)
					if category == "pos"]

	neg_rev_words = []
	for i in range(len(neg_documents)):
		for j in range(len(neg_documents[i])):
			neg_rev_words.append(neg_documents[i][j])

	#find all words that arent common or punctuation
	stop_words = sw.words("english")
	all_words = FreqDist(w.lower() for w in neg_rev_words 
				if w.lower() not in string.punctuation 
				and w.lower() not in stop_words)

	#grab first 3000 of the remaining words
	word_features = all_words.most_common(3000)
	neg_features = []
	for comb in word_features:
		neg_features.append(comb[0])
	#get featuresets
	featuresets = [(document_features(d, neg_features), c) for (d,c) in all_documents]
	total_percent = 0.0
	for i in xrange(1,11):
		print("Test Set Section: %d" % i)

		#train and test the data using sklearn
		train_set = getTrainingSet(featuresets, i)
		test_set = getTestSet(featuresets, i)
		classifier = nltk.NaiveBayesClassifier.train(train_set)
		percent = nltk.classify.accuracy(classifier, test_set)
		print percent
		total_percent += percent
		print("----------------------------------------------------------------------")
	print("Average = %0.2f" % (total_percent/float(10)))


if __name__ == "__main__":
	main()