# Assignment 8
# Willie Payne

import sys

# Create a dict with actual letter and then counts for how many times the actual
# letter appears and how many times the incorrect letters appear.
# Then go back through and calculate the probabilities and store them within each dict
# 	I think that these are the emission probabilities

class Letter(object):
	def __init__(self, letter):
		self.letter = letter # letter is the actual state letter
		self.observed = {} # dict containing counts of actual letters typed
		self.emmissions = {} # dict containing emmission probabilities
		self.nextLetters = {} # dict containing counts of letters observed after current letter
		self.transitions = {} # dict containing transition probabilities

	# Once we observe a letter, add it to the observed or nextLetters dict or add to its count
	def increment(self, observedLetter, correctDict):
		if observedLetter in correctDict:
			correctDict[observedLetter] = correctDict[observedLetter] + 1.
		else:
			correctDict[observedLetter] = 1.

	# Update the emisstions dict to contain probabilities for all observed letters
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
	def calcTransitions(self):
		statesNum = len(self.observed)
		totalStates =  0.

		for nextLetter in self.nextLetters:
			totalStates = totalStates + self.nextLetters[nextLetter]

		for nextLetter in self.nextLetters:
			print nextLetter
			self.transitions[nextLetter] = (1 + self.nextLetters[nextLetter])/(statesNum + totalStates)

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

# Iterates through all of the letters and calculates emmissions
def calcAllEmissions(letters):
	for l in letters:
		letters[l].calcEmissions()

	return letters

def calcAllTransitions(letters):
	for l in letters:
		letters[l].calcTransitions()

	return letters

# Simply Iterates through all of the letters and prints emmissions tables
def printAllEmissions(letters):
	for l in letters:
		print "State %s: Observations" % l,
		for i in letters[l].emmissions:
			print "(%s: %.3f)" % (i, letters[l].emmissions[i]),
		print ""

def printAllTransitions(letters):
	for l in letters:
		print "State %s: Transitions" % l,
		for i in letters[l].transitions:
			print "(%s: %.3f)" % (i, letters[l].transitions[i]),
		print ""

def main():
	letterList = readFile()
	if letterList == False:
		return False

	letters = createLetters()
	letters = countObservations(letters, letterList)
	letters = calcAllEmissions(letters)
	letters = countTransitions(letters, letterList)
	letters = calcAllTransitions(letters)

	print "-----------------Emissions Probabilities-----------------"
	printAllEmissions(letters)
	print "-----------------Transition Probabilities-----------------"
	printAllTransitions(letters)

if __name__ == '__main__':
	main()