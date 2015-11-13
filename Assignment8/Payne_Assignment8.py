# Assignment 8
# Willie Payne

# Run by calling the data file as a commandline argument For example:
# $ python Payne_Assignment8.py "typos20.data"

import sys

# X[t] representing letter states
class Letter(object):
	def __init__(self, letter):
		self.letter = letter # letter is the actual state letter
		self.occurences = 0. # count of times that the letter state appears in the data
		self.initialState = 0. # Amount of times letter appears divided by total letters
		
		self.observed = {} # dict containing counts of actual letters typed
		self.emmissions = {} # dict containing emmission probabilities

		# Initialize these to contain all of the letters
		self.nextLetters = {} # dict containing counts of letters observed after current letter
		self.transitions = {} # dict containing transition probabilities

		for l in range(97,123):
			self.nextLetters[chr(l)] = 0.
		self.nextLetters["_"] = 0.

	# Once we observe a letter, add it to the observed or nextLetters dict or add to its count
	def increment(self, observedLetter, correctDict):
		if observedLetter in correctDict:
			correctDict[observedLetter] = correctDict[observedLetter] + 1.
		else:
			correctDict[observedLetter] = 1.

	# Update the emisstions dict to contain probabilities for all observed letters
	# Emissions Probabilities only have observed values local to them
	def calcEmissions(self):
		statesNum = len(self.observed) # possible states
		totalStates =  0. # Count of all observed states

		# Calculate total number of times letter has appeared
		for observedLetter in self.observed:
			totalStates = totalStates + self.observed[observedLetter]

		for observedLetter in self.observed:
			# Laplace Smoothed Estimate
			self.emmissions[observedLetter] = (1 + self.observed[observedLetter])/(statesNum + totalStates)

	# Update the transitions dict to contain probabilities for all next letters
	# With transitions - there is the chance for any letter, though it some are very very small
	def calcTransitions(self):
		statesNum = len(self.nextLetters) # Should be 27
		totalStates =  0.

		for nextLetter in self.nextLetters:
			totalStates = totalStates + self.nextLetters[nextLetter]

		for nextLetter in self.nextLetters:
			self.transitions[nextLetter] = (1 + self.nextLetters[nextLetter])/(statesNum + totalStates)

	def addToCount(self):
		self.occurences = self.occurences + 1.

# Read in the data file and return a list of all the outputs
# 	return letterList -> letterList[position][0 = state | 1 = observed]
def readFile():
	if len(sys.argv) != 2:
		print "Wrong number of arguments supplied"
		return False
	else:
		fileName = sys.argv[1]
		letterList = []
		letterString = open(fileName, 'r')
		letterString = letterString.read()
		rows = letterString.split("\n")
		for row in rows:
			sp = row.split(' ')
			if len(sp) == 2:
				letterList.append([sp[0], sp[1]])
		return letterList

# Returns a dict of all 26 letters attached to letter objects
def createLetters():
	letters = dict()
	for l in range(97,123):
		newLetter = Letter(chr(l))
		letters[chr(l)] = newLetter
	newLetter = Letter("_")
	letters["_"] = newLetter
	return letters

# -------------------------------------------------------------

# Iterate through all of the text file
# 	With each state - count the number of observations
def countObservations(letters, letterList):
	for i in letterList:
		state, observation, = i[0], i[1]
		letters[state].increment(observation, letters[state].observed)
	return letters

# Iterate through all of the text file
# 	With each state - count the number of nextStates
def countTransitions(letters, letterList):
	for i in range(len(letterList) - 1):
		state, nextState, = letterList[i][0], letterList[i+1][0]
		letters[state].increment(nextState, letters[state].nextLetters)
	return letters

# Iterate through all of the text file and count the number of times each
# letter appears - Used for initial state distribution
def countOccurences(letters, letterList):
	for i in letterList:
		state = i[0]
		letters[state].addToCount()
	return letters

# -------------------------------------------------------------

# Iterates through all of the letters and calculates emmissions
def calcAllEmissions(letters):
	for l in letters:
		letters[l].calcEmissions()

	return letters

def calcAllTransitions(letters):
	for l in letters:
		letters[l].calcTransitions()

	return letters

def calcAllInitialStateDist(letters):
	total = 0.
	for i in letters:
		total = total + letters[i].occurences
	for i in letters:
		letters[i].initialState = letters[i].occurences/total

	return letters

# -------------------------------------------------------------

# Simply Iterates through all of the letters and prints emmissions tables
def printAllEmissions(letters):
	for l in letters:
		print "-----State %s Observations-----" % l
		for i in letters[l].emmissions:
			print "P(%s|%s) = %.3f" % (i, l, letters[l].emmissions[i])
		print ""

def printAllTransitions(letters):
	for l in letters:
		print "-----State %s: Transitions-----" % l
		for i in letters[l].transitions:
			print "P(%s|%s) = %.3f" % (i, l, letters[l].transitions[i])
		print ""

def printAllInitStateDist(letters):
	total = 0.
	for l in letters:
		total = total + letters[l].initialState
		print "P(%s) = %.5f" % (l, letters[l].initialState)
	print "Total: %.5f" % total

# -------------------------------------------------------------

def main():
	letterList = readFile()
	if letterList == False:
		return False

	letters = createLetters()
	letters = countObservations(letters, letterList)
	letters = calcAllEmissions(letters)
	letters = countTransitions(letters, letterList)
	letters = calcAllTransitions(letters)
	letters = countOccurences(letters, letterList)
	letters = calcAllInitialStateDist(letters)

	print "-----------------Emissions Probabilities-----------------"
	printAllEmissions(letters)
	print "-----------------Transition Probabilities-----------------"
	printAllTransitions(letters)
	print "----------------Initial State Distribution----------------"
	printAllInitStateDist(letters)

if __name__ == '__main__':
	main()