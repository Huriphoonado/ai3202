# Willie Payne
# 10/18
# Assignment 6 - Bayes Net Disease Predictor

# Welcome to change the command line parser any way that we like (eg -p True)

class Node(object):
	def __init__(self, name, probDist):
		self.name = name
		self.probDist = probDist
		self.edge = None
		self.parent = None

# In order to make life easier, I am calling "low" for Pollution, "T"
def initVars():
	pollution = Node("Pollution", {"low": 0.9})
	smoker = Node("Smoker", {"T": 0.3})
	xray = Node("XRay", {"T": 0.9, "F": 0.2})
	dyspnoea = Node("Dyspnoea", {"T": 0.65, "F": 0.3})
	cancer = Node("Cancer", {"low": {"T": 0.03, "F":0.001}, "high": {"T": 0.05, "F":0.02}})
	pollution.edge = cancer
	smoker.edge = cancer
	cancer.parent = [pollution, smoker]
	cancer.edge = [xray, dyspnoea]
	xray.parent = cancer
	dyspnoea.parent = cancer

	return pollution, smoker, xray, dyspnoea, cancer

# Helper function to calculate marginal probability distribution of cancer
def cancerProb():
	val1 = cancer.probDist["low"]["T"] * smoker.probDist["T"] * pollution.probDist["low"]
	val2 = cancer.probDist["low"]["F"] * (1 - smoker.probDist["T"]) * pollution.probDist["low"]
	val3 = cancer.probDist["high"]["T"] * smoker.probDist["T"] * (1 - pollution.probDist["low"])
	val4 = cancer.probDist["high"]["F"] * (1 - smoker.probDist["T"]) * ((1 - pollution.probDist["low"]))
	return val1 + val2 + val3 + val4

# eg findNode is 
def diagnostic(findNode, givenNode):
	# easiest calculation
	if findNode == givenNode:
		return 1
	# harder calculation
	elif givenNode.name == 'Cancer' or findNode.name == 'Cancer':
		pass
	# hardest calculation - eg findNode is Pollution, givenNode is Dys
	else: 
		if findNode.name == 'Smoker':
			extraNode = pollution
			val1 = givenNode.probDist["T"] * cancer.probDist["low"]["T"] * findNode.probDist["T"] * extraNode.probDist["low"]
			val2 = givenNode.probDist["T"] * cancer.probDist["high"]["T"] * findNode.probDist["T"] * (1 - extraNode.probDist["low"])
			val3 = givenNode.probDist["F"] * (1 - cancer.probDist["low"]["T"]) * findNode.probDist["T"] * extraNode.probDist["low"]
			val4 = givenNode.probDist["F"] * (1 - cancer.probDist["high"]["T"]) * findNode.probDist["T"] * (1 - extraNode.probDist["low"])
			val5 = cancer.probDist["low"]["T"] * findNode.probDist["T"] * extraNode.probDist["low"]
			val6 = cancer.probDist["high"]["T"] * findNode.probDist["T"] * (1 - extraNode.probDist["low"])
			val7 = (1 - cancer.probDist["low"]["T"]) * findNode.probDist["T"] * extraNode.probDist["low"]
			val8 = (1 - cancer.probDist["high"]["T"]) * findNode.probDist["T"] * (1 - extraNode.probDist["low"])
			helperVal1 = (val1 + val2 + val3 + val4)/(val5 + val6 + val7 + val8)
			helperVal2 = margProb(givenNode)
			bayesVal = (helperVal1 * findNode.probDist["T"])/helperVal2
			return bayesVal
		else:
			# Example is looking for whether pollution is high
			extraNode = smoker
			val1 = givenNode.probDist["T"] * cancer.probDist["high"]["T"] * extraNode.probDist["T"] * (1 - findNode.probDist["low"])
			val2 = givenNode.probDist["T"] * cancer.probDist["high"]["F"] * (1 - extraNode.probDist["T"]) * (1 - findNode.probDist["low"])
			val3 = givenNode.probDist["F"] * (1 - cancer.probDist["high"]["T"]) * extraNode.probDist["T"] * (1 - findNode.probDist["low"])
			val4 = givenNode.probDist["F"] * (1 - cancer.probDist["high"]["F"]) * (1 - extraNode.probDist["T"]) * (1 - findNode.probDist["low"])
			val5 = cancer.probDist["high"]["T"] * extraNode.probDist["T"] * (1 - findNode.probDist["low"])
			val6 = cancer.probDist["high"]["F"] * (1 - extraNode.probDist["T"]) * (1 - findNode.probDist["low"])
			val7 = (1 - cancer.probDist["high"]["T"]) * extraNode.probDist["T"] * (1 - findNode.probDist["low"])
			val8 = (1 - cancer.probDist["high"]["F"]) * (1 - extraNode.probDist["T"]) * (1 - findNode.probDist["low"])
			helperVal1 = (val1 + val2 + val3 + val4)/(val5 + val6 + val7 + val8)
			helperVal2 = margProb(givenNode)
			print helperVal2
			bayesVal = (helperVal1 * (1 - findNode.probDist["low"]))/helperVal2
			return bayesVal

# Will calculate the marginal probability of any node that has been given
def margProb(findNode):
	if findNode.name == 'Dyspnoea' or findNode.name == 'XRay':
		cancerVal = cancerProb()
		return (findNode.probDist["T"] * cancerVal) + (findNode.probDist["F"] * (1 - cancerVal))
	elif findNode.name == 'Cancer':
		return cancerProb()
	elif findNode.name == 'Pollution':
		findNode.probDist["high"]
	else:
		findNode.probDist["T"]

def jointProb():
	pass


def inputs():
	pass

def main():
	global pollution, smoker, xray, dyspnoea, cancer
	pollution, smoker, xray, dyspnoea, cancer = initVars()
	print diagnostic(pollution, dyspnoea)

if __name__ == "__main__":
	main()