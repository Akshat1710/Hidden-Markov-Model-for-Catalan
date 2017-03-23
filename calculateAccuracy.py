import sys
import itertools

def getFiles(givenTaggedOutputFile, generatedTaggedOutputFile):
	correctData = 0
	totalData = 0
	fileGiven = open(givenTaggedOutputFile, 'r')
	fileGenerated = open(generatedTaggedOutputFile, 'r')
	file = open('incorrectTags.txt', 'a')
	lineNumber = 0
	for eachLineInGivenTaggedOutputFile, eachLineInGeneratedTaggedOutputFile in itertools.izip(fileGiven, fileGenerated):
		eachLineInGivenTaggedOutputFile = eachLineInGivenTaggedOutputFile.split(' ')
		eachLineInGeneratedTaggedOutputFile = eachLineInGeneratedTaggedOutputFile.split(' ')
		lineNumber += 1
		for x, y in itertools.izip(eachLineInGivenTaggedOutputFile, eachLineInGeneratedTaggedOutputFile):
			if x == y:
				correctData += 1
			else:
				file.write(y+"\n")
			totalData += 1
	file.close()
	print correctData, totalData
	return float((correctData * 1.0)/ totalData)

def getAnswer():
	file = open('incorrectTags.txt', 'r')
	count = 0
	for eachLine in file:
		count += 1
	return count
	
print getFiles(sys.argv[1], sys.argv[2])
print getAnswer()