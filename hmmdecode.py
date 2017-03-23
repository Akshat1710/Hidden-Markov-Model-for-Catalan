import time
import sys
import copy

def getHMMModel():
	global tagInfo, trainingFile, startTagTransitionProbabilitiesDictionary, tagTransitionProbabilitiesDictionary, tagEmissionProbabilitiesDictionary
	file = open(trainingFile, 'r')
	lineNumber = 0
	for eachLine in file:
		lineNumber += 1
		if lineNumber == 1:
			startTagTransitionProbabilitiesDictionary = eval(eachLine)
		elif lineNumber == 2:
			tagTransitionProbabilitiesDictionary = eval(eachLine)
		elif lineNumber == 3:
			tagEmissionProbabilitiesDictionary = eval(eachLine)
		else: 
			tagInfo = eval(eachLine)

def checkSeenWord(currentWord):
	global tagEmissionProbabilitiesDictionary, tagInfo
	flag = False
	nextPossibleTags = list()
	for eachTag in tagEmissionProbabilitiesDictionary.keys():
		if currentWord in tagEmissionProbabilitiesDictionary[eachTag]:
			flag = True
			nextPossibleTags.append(eachTag)
	if not flag:
		nextPossibleTags = copy.deepcopy(tagInfo)
	return nextPossibleTags, flag

def getPreviousMaximumTransitionProbability(backpointerDictionary, state, currentTag):
	maxProb = float("-inf")
	for eachList in backpointerDictionary[state-1][currentTag]:
		#print eachList
		prob = eachList[0]
		if prob > maxProb:
			maxProb = prob
			maxProbTag = eachList[1]
	#print maxProb
	return maxProb

def writeOutput(result):
	file = open('hmmoutput.txt', 'a')
	for i in reversed(result):
		file.write(i)
	file.write("\n")
	file.close()

def getMostLikelyTagForEachWord(backpointerDictionary, state, currentLine):
	maxProb = float("-inf")
	currentMaxProbTag = ''
	previousMaxProbTag = ''
	for eachTag in backpointerDictionary[state].keys():
		for eachList in backpointerDictionary[state][eachTag]:
			prob = eachList[0]
			if prob >= maxProb:
				maxProb = prob
				currentMaxProbTag = eachTag
				previousMaxProbTag = eachList[1]
	#print "Current Max Prob Tag- ", currentMaxProbTag, " Previous Max Prob Tag- ", previousMaxProbTag
	state -= 1
	result = list()
	result.append(str(currentLine[state]+"/"+currentMaxProbTag) + " ")
	#file.write(str(currentLine[state]+"/"+currentMaxProbTag) + " ")
	while state != 0:
		currentMaxProbTag = previousMaxProbTag
		for eachList in backpointerDictionary[state][previousMaxProbTag]:
			prob = eachList[0]
			if prob >= maxProb:
				maxProb = prob
				'''currentMaxProbTag = previousMaxProbTag'''
				previousMaxProbTag = eachList[1]
		'''previousMaxProbTag = previousProbTag'''
		#print "Current Max Prob Tag- ", currentMaxProbTag, " Previous Max Prob Tag- ", previousMaxProbTag
		state -= 1
		result.append(str(currentLine[state]+"/"+currentMaxProbTag)+ " ")
		#file.write(str(currentLine[state]+"/"+currentMaxProbTag) + " ")
	writeOutput(result)
	
def getTag(testingFile):
	global startTagTransitionProbabilitiesDictionary, tagTransitionProbabilitiesDictionary, tagEmissionProbabilitiesDictionary
	file = open(testingFile, 'r')
	for eachLine in file:
		#print '------------------------------------------------------------------------------------------------'
		state = 0
		previousTag = 'q0'
		eachLine = eachLine.rstrip().split(' ')
		backpointerDictionary = dict()
		for eachWord in eachLine:
			state += 1
			backpointerDictionary[state] = dict()
			if state == 1:
				nextPossibleTagsQueue, seen = checkSeenWord(eachWord)
				#print "Next Possible Tags- ", nextPossibleTagsQueue
				previousTag = ''
				for eachTag in nextPossibleTagsQueue:
					backpointerDictionary[state][eachTag] = list()
					transitionProbability = startTagTransitionProbabilitiesDictionary[eachTag]
					if seen:
						emissionProbability = tagEmissionProbabilitiesDictionary[eachTag][eachWord]
					else:
						emissionProbability = 1
					#print transitionProbability, emissionProbability
					probability = float(transitionProbability * emissionProbability)
					'''
					tempList = ['Current Total Probability', 'Previous Tag']
					'''
					tempList = [probability, previousTag]
					#print state, eachTag, tempList
					backpointerDictionary[state][eachTag].append(tempList)

			else:
				#print nextPossibleTagsQueue
				while nextPossibleTagsQueue:
					previousTag = nextPossibleTagsQueue.pop(0)
					queue, seen = checkSeenWord(eachWord)
					#print "Next Possible Tags- ", queue
					for eachPossibleTag in queue:
						if eachPossibleTag not in backpointerDictionary[state]:
							backpointerDictionary[state][eachPossibleTag] = list()
						currentTag = eachPossibleTag
						transitionProbability = tagTransitionProbabilitiesDictionary[previousTag+'->'+currentTag]
						if seen:
							emissionProbability = tagEmissionProbabilitiesDictionary[currentTag][eachWord]
						else:
							emissionProbability = 1
						previousTransitionProbability = getPreviousMaximumTransitionProbability(backpointerDictionary, state, previousTag)
						probability = float(previousTransitionProbability * transitionProbability * emissionProbability)
						tempList = [probability, previousTag]
						#print state, eachPossibleTag, tempList
						backpointerDictionary[state][eachPossibleTag].append(tempList)
				nextPossibleTagsQueue = copy.deepcopy(queue)
		
		#print eachLine, backpointerDictionary, state
		getMostLikelyTagForEachWord(backpointerDictionary, state, eachLine)


startTime = time.time()
'''
Global Variables
'''
trainingFile = 'hmmmodel.txt'
startTagTransitionProbabilitiesDictionary = dict()
tagTransitionProbabilitiesDictionary = dict()
tagEmissionProbabilitiesDictionary = dict()
backpointerDictionary = dict()
tagInfo = list()
getHMMModel()
getTag(sys.argv[1])

'''
Printing goes here
'''
'''
print "\nstartTagTransitionProbabilitiesDictionary- ", startTagTransitionProbabilitiesDictionary
print "\ntagTransitionProbabilitiesDictionary- ", tagTransitionProbabilitiesDictionary
print "\ntagEmissionProbabilitiesDictionary- ", tagEmissionProbabilitiesDictionary
'''
endTime = time.time()
