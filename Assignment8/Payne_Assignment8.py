# Assignment 8
# Willie Payne

# Create a dict with actual letter and then counts for how many times the actual
# letter appears and how many times the incorrect letters appear.
# Then go back through and calculate the probabilities and store them within each dict
# 	I think that these are the emission probabilities

class letter(object):
	def __init__(self, letter):
		self.letter = letter # letter is the actual state letter
		self.observed = {}
		self.emmissions = {}

	# Once we observe a letter add it to the observed dict or add to its count
	def increment(self, observedLetter):
		if observedLetter in self.observed:
			self.observed[observedLetter] = self.observed[observedLetter]

	# Update the emisstions dict to contain probabilities for all observed letters
	def calcEmissions(self):
		statesNum = len(self.observed) # possible states
		totalStates = 0

		# Calculate total number of times letter has appeared
		for observedLetter in self.observed:
			totalStates = totalStates + self.observed[observedLetter]

		for observedLetter in self.observed:
			# Laplace Smoothed Estimate
			self.emmissions[observedLetter] = (1 + self.observed[observedLetter])/(statesNum + totalStates)

# Read in the data file and return a list of all the outputs
def readFile(fileName):
	pass
# Returns a dictionary with counts based on state and output
def countStates(valList):
	pass

def main():
	pass

if __name__ == '__main__':
	main()