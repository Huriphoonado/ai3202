# Assignment 8
# Willie Payne

# Run by calling the data files as commandline arguments For example:
# $ python Payne_Assignment8.py "typos20.data" "types20Testdata"

import sys
from math import log10

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
	# 	All other letters since they are impossible will be given a value of 0
	def calcEmissions(self):
		statesNum = len(self.observed) # possible states
		totalStates =  0. # Count of all observed states

		# Calculate total number of times letter has appeared
		for observedLetter in self.observed:
			totalStates = totalStates + self.observed[observedLetter]

		for observedLetter in self.observed:
			# Laplace Smoothed Estimate
			self.emmissions[observedLetter] = (1 + self.observed[observedLetter])/(statesNum + totalStates)

		# Set really small so virtually impossible, but still able to take the logarithm
		for l in range(97,123):
			if chr(l) not in self.emmissions:
				self.emmissions[chr(l)] = 0.0001
		if "_" not in self.emmissions:
			self.emmissions["_"] = 0.0001

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
	if len(sys.argv) != 3:
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

# Viterbi Code Goes Here

def readTestFile():
	fileName = sys.argv[2]
	testStates = []
	testObservations = []
	letterString = open(fileName, 'r')
	letterString = letterString.read()
	rows = letterString.split("\n")
	for row in rows:
		if len(row) == 3:
			sp = row.split(' ')
			testStates.append(sp[0])
			testObservations.append(sp[1])
	return testStates, testObservations

# I used the wikipedia page on Viterbi as a resource
# 	https://en.wikipedia.org/wiki/Viterbi_algorithm
def viterbi(letters, obs):
	vit = [{}] 
	path = {}
	
	# Initialize case zero for all states
	# Use logarithms to prevent underflow errors
		# 	If not used, every character after a point will be thought to be 'z'
	for letter in letters:
		vit[0][letter] = log10(letters[letter].initialState) + log10(letters[letter].emmissions[obs[0]])
		path[letter] = [letter]

	# Iterate through the rest of the observation
	# For each possible state at each time, keep track of 
	# what its path and probability would be
	for l in range(1, len(obs)):
		vit.append({})
		newPath = {}
		for s in letters:
			# (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
			(prob, state) = max((vit[l-1][s0] + log10(letters[s0].transitions[s]) + log10(letters[s].emmissions[obs[l]]), s0) for s0 in letters)
			vit[l][s] = prob # keep track of each possible letter's greatest probability
			# New path is the path up to the most probable state
			newPath[s] = path[state] + [s]
		
		# We don't care about older paths, only the current one
		path = newPath

	# Determine the the most probable last letter
	n = len(obs) - 1
	(prob, state) = max((vit[n][s], s) for s in letters)
	
	return path[state]

def checkResults(testStates, testObservations, finalPath):
	size = len(finalPath)
	correctObs = 0.
	correctVit = 0.
	finalOutput = "States | Observations | Viterbi" + "\n" + "----------------------------" + "\n"
	for i in range(size):
		finalOutput = finalOutput + ' | '.join([testStates[i], testObservations[i], finalPath[i], "\n"])
		if testObservations[i] == testStates[i]:
			correctObs = correctObs + 1
		if finalPath[i] == testStates[i]:
			correctVit = correctVit + 1
	correctObs = 1 - (correctObs/size)
	correctVit = 1 - (correctVit/size)
	print "Observations Error Rate: %f" % correctObs
	print "Viterbi Error Rate: %f" % correctVit
	print finalOutput
	return correctVit


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

	# Calculate HMM
	letters = createLetters()
	letters = countObservations(letters, letterList)
	letters = calcAllEmissions(letters)
	letters = countTransitions(letters, letterList)
	letters = calcAllTransitions(letters)
	letters = countOccurences(letters, letterList)
	letters = calcAllInitialStateDist(letters)
	
	# Viterbi
	testStates, testObservations = readTestFile()
	finalPath = viterbi(letters, testObservations)
	checkResults(testStates, testObservations, finalPath)

	'''
	print "-----------------Emissions Probabilities-----------------"
	printAllEmissions(letters)
	print "-----------------Transition Probabilities-----------------"
	printAllTransitions(letters)
	print "----------------Initial State Distribution----------------"
	printAllInitStateDist(letters)
	'''


if __name__ == '__main__':
	main()