'''Import Libraries'''
import sys
import time

def initialiseTransitionProbabilities():
	global tagInfo
	for i in range(0, len(tagInfo)):
		for j in range(0, len(tagInfo)):
			key = tagInfo[i]+"->"+tagInfo[j]
			tagTransitionProbabilitiesDictionary[key] = 0

def getTransitionProbabilities(trainingFile):
	global tagTransitionProbabilitiesDictionary, tagInfo
	initialiseTransitionProbabilities()
	file = open(trainingFile, 'r')
	for eachLine in file:
		eachWordTag = eachLine.rstrip().split(' ')
		for i in range(0, len(eachWordTag) - 1):
			tag_i = eachWordTag[i][len(eachWordTag[i]) - 2: len(eachWordTag[i])]
			tag_j = eachWordTag[i+1][len(eachWordTag[i+1]) - 2: len(eachWordTag[i+1])]
			key = tag_i + "->" + tag_j
			if tag_i not in tagTransitionCountDictionary:
				tagTransitionCountDictionary[tag_i] = 1
			else:
				tagTransitionCountDictionary[tag_i] += 1
			if key not in tagTransitionProbabilitiesDictionary:
				tagTransitionProbabilitiesDictionary[key] = 1
			else:
				tagTransitionProbabilitiesDictionary[key] += 1
	#print tagTransitionProbabilitiesDictionary 
	for key in tagTransitionProbabilitiesDictionary.keys():
		tag_i = key.split('->')[0]
		tagTransitionProbabilitiesDictionary[key] = float(tagTransitionProbabilitiesDictionary[key] + 1) / float(tagTransitionCountDictionary[tag_i] + len(tagInfo))

def getStartTransitionProbabilities():	
	global tagInfo, startTagCountDictionary, startTagTransitionProbabilitiesDictionary, sentenceCount
	for eachTag in tagInfo:
		if eachTag in startTagCountDictionary:
			startTagTransitionProbabilitiesDictionary[eachTag] = float(startTagCountDictionary[eachTag] + 1) / float(sentenceCount + len(tagInfo))
		else:
			startTagTransitionProbabilitiesDictionary[eachTag] = float(1) / float(sentenceCount + len(tagInfo))
	
def getStartTagCount(currentWord_Tag):
	global startTagCountDictionary, tagInfo
	tag = currentWord_Tag[len(currentWord_Tag) - 2: len(currentWord_Tag)]
	if tag not in startTagCountDictionary:
		startTagCountDictionary[tag] = 1
	else:
		startTagCountDictionary[tag] = startTagCountDictionary[tag] + 1

def getTagInfo(currentWordTag):
	global tagInfo
	for i in range(0, len(currentWordTag)):
		word = currentWordTag[i][0: len(currentWordTag[i]) - 3]
		tag = currentWordTag[i][len(currentWordTag[i]) - 2: len(currentWordTag[i])]
		if tag not in tagCountDictionary:
			tagCountDictionary[tag] = 1
		else:
			tagCountDictionary[tag] += 1
		if tag not in tagInfo:
			tagInfo.append(tag)
		if tag not in tagEmissionProbabilitiesDictionary:
			tagEmissionProbabilitiesDictionary[tag] = dict()
		#else:
		if word not in tagEmissionProbabilitiesDictionary[tag]:
			tagEmissionProbabilitiesDictionary[tag][word] = 1
		else:
			tagEmissionProbabilitiesDictionary[tag][word] += 1

def getTrainingData(trainingFile):
	global sentenceCount
	file = open(trainingFile, 'r')
	for eachLine in file:
		sentenceCount += 1
		word_Tag = eachLine.rstrip().split(' ')
		getStartTagCount(word_Tag[0])
		getTagInfo(word_Tag)

def getEmissionProbabilities():
	global tagCountDictionary, tagEmissionProbabilitiesDictionary
	for key in tagEmissionProbabilitiesDictionary.keys():
		for subKey in tagEmissionProbabilitiesDictionary[key]:
			tagEmissionProbabilitiesDictionary[key][subKey] = (tagEmissionProbabilitiesDictionary[key][subKey] * 1.0) / tagCountDictionary[key]

def setHMMModel():
	file = open('hmmmodel.txt', 'w')

	file.write(str(startTagTransitionProbabilitiesDictionary)+"\n")
	file.write(str(tagTransitionProbabilitiesDictionary)+"\n")
	file.write(str(tagEmissionProbabilitiesDictionary)+"\n")
	file.write(str(tagInfo)+"\n")
	file.close()

startTime = time.time()
'''
Global Variables
'''
sentenceCount = 0
tagInfo = list()
startTagCountDictionary = dict()
startTagTransitionProbabilitiesDictionary = dict()
tagTransitionCountDictionary = dict()
tagCountDictionary = dict()
tagTransitionProbabilitiesDictionary = dict()

tagEmissionProbabilitiesDictionary = dict()
'''
Fetch Training File
'''
trainingFile = sys.argv[1]
getTrainingData(trainingFile)
getStartTransitionProbabilities()
getTransitionProbabilities(trainingFile)
getEmissionProbabilities()

setHMMModel()
endTime = time.time()

'''
Print Statements
'''
'''
print "Tag Info- ", tagInfo
print "Tag Count- ", tagCountDictionary
print "\nTagTransitionCountDictionary- ", tagTransitionCountDictionary
print "\nTagTransitionProbabilitiesDictionary- ", tagTransitionProbabilitiesDictionary
print "\nTagEmissionProbabilitiesDictionary- ", tagEmissionProbabilitiesDictionary
print "\nSentence Count- ", sentenceCount
count = 0
for i in startTagCountDictionary.keys():
	count += startTagCountDictionary[i]
print "Start Tag Count Dictionary- ", startTagCountDictionary
print "Start Tag Count- ", count
print "Start Tag Transition Probabilities- ",
for i in startTagTransitionProbabilitiesDictionary.keys():
	print i, "- ", startTagTransitionProbabilitiesDictionary[i]
'''
print "Execution Time- ", (endTime - startTime)