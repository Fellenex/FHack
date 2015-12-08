#Written by Chris Keeler, December 8th, 2015

#TODO:
#	Interactive script allowing the user to enter the likenesses of the choices as they become discovered.
#	Beautify the string output
#	Generate a path tree for each possible discovered likeness, to show what should happen from the start, regardless of game feedback

import numpy as np

#Parameters:
#	_a: A string
#	_b: A string
#
#Return value:
#	likeness: an integer, representing how many characters are shared in a and b
#
def likeness(_a,_b):
	if not(len(_a)==len(_b)):
		return -1
	else:
		likeness=0
		for i in range(len(_a)):
			if _a[i]==_b[i]:
				likeness+=1
	return likeness

#Parameters:
#	_strings: A list of strinsg for which to create string likenesses for each other
#
#Return value:
#	likenesses: a 2-d list of string likenesses for each string
#
def stringLikenesses(_strings):
	likenesses = []
	for s in _strings:
		thisList = []
		for t in _strings:
			thisList.append(likeness(s,t))
		likenesses.append(thisList)

	return likenesses

#Parameters:
#	_likenesses: A 2-d list of string likenesses for each string
#	_len: The length of each word
#
#Return Value:
#	likenessCount: a 2-d list of string likeness densities for each string
#
def stringLikenessDensities(_likenesses, _len):
	likenessCount = []

	for s in _likenesses:
		count = [0]*(_len+1)
		for l in range(0,len(s)):

			#print str(s[l])+" gettin' a boost!"
			count[s[l]] += 1

		likenessCount.append(count)

	return likenessCount

#Parameters:
#	_densities: A 2-d list of string likeness densities for each string
#
#Return Value:
#	evenness: A list of integers representing the evenness of each likeness density list
#
def calculateEvenness(_densities):
	evenness = []
	for d in _densities:
		s = np.std(d)
		m = np.mean(d)

		evenness.append(s)

	return evenness


#Parameters:
#	_strings: A list of strings for which we must print output
#	_n: The length of each string
#
#Return Value:
#	None
#
def stringsToString(_strings, _n):
	likenesses = stringLikenesses(_strings)
	likenessCount = stringLikenessDensities(likenesses, _n)
	evenness = calculateEvenness(likenessCount)

	print "String\tLikeness Count\t\tEvenness"
	for i in range(len(_strings)):
		print _strings[i]+"\t"+str(likenessCount[i])+"\t\t"+str(evenness[i])

	print "Best: "+str(bestChoice(_strings))

#After checking some specific string and receiving a likeness for it, we can eliminate the strings which do not match this.
#
#Parameters:
#	_strings: A list of strings to alter
#	_guessedString: The string for which we know a likeness
#	_knownLikeness: The likeness between _chosenString and the goal string
#
#Return Value:
#	possibles: A list of strings with _knownLikeness to 
#
def removeImpossibles(_strings, _guessedString, _knownLikeness):
	possibles = []
	for s in _strings:

		if s == _guessedString:
			#ignore it
			continue

		elif likeness(s, _guessedString) == _knownLikeness:
			possibles.append(s)

	return possibles

#Parameters:
#	_strings: A list of strings for which we must find the best choice
#
#Return Value:
#	bestWord: A string, to be used as the first choice.
def bestChoice(_strings):
	likenesses = stringLikenesses(_strings)
	likenessCount = stringLikenessDensities(likenesses, len(_strings[0]))
	evenness = calculateEvenness(likenessCount)

	bestWord = _strings[evenness.index(min(evenness))]
	return bestWord

#Opens a text file named "words.txt" located in the same directory as this script.
	#Assumes that the text file has one word per line
#
def main():
	with open('words.txt','r') as f:
		words = f.read().rstrip('\n').split()

	n = len(words)

	stringsToString(words,len(words[0]))

main()