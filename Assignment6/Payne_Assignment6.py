# Willie Payne
# 10/18
# Assignment 6 - Bayes Net Disease Predictor

import sys
import getopt

class Node(object):
	def __init__(self, name, probDist):
		self.name = name 
		self.probDist = probDist # Node's probability distribution
		self.edge = None # List of children
		self.parent = None # List of Parents

# Simply initializes and returns all of the nodes given the assignment
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

# Both parent nodes are known
def easyCombined(findNode, flag):
	return "Combined calculation with two known parent nodes not yet supported."

# Both child nodes are known
def easyCombined(findNode, flag):
	return "Combined calculation with two known child nodes not yet supported."

# Updated beliefs when one parent node and one child node is known to be true
def combined(findNode, parentNode, childNode, flag):
	# Easiest case
	if (findNode == parentNode) or (findNode == childNode):
		return abs(flag - 1)
	# Easier -  Parent nodes are independent so we can simply use diagnostic reasoning
	elif (findNode.name == "Smoker") or (findNode.name == "Pollution"):
		return diagnostic(findNode, childNode, flag)
	# Hard - Bayes Rule relying on earlier calculations
	else:
		if findNode.name == "Cancer":
			# P(C|D,S) = (P(D|C,S) * P(C|S))/P(D|S) = (P(D|C) * P(C|S))/P(D|S)
			val1 = predictive(childNode, findNode, 0)
			val2 = predictive(findNode, parentNode, 0)
			val3 = predictive(childNode, parentNode, 0)
			return abs(flag - (val1 * val2)/val3)
		# We are looking for one of the child nodes
		else:
			newCancerVal = combined(cancer, parentNode, childNode, 0) 
			result = (newCancerVal * findNode.probDist['T']) + ((1 - newCancerVal) * findNode.probDist['F'])
			return abs(flag - result)

# We know smoking is True, either pollution or smoking is also True
def intercausal(findNode, givenNode, flag):
	# Easiest Case
	if (findNode == givenNode) or findNode == cancer:
		return abs(flag - 1)
	# Causal Chain Rule Case - We know cancer so no need to care about its parents
	elif findNode.name == "XRay" or findNode.name == "Dyspnoea":
		return abs(flag - predictive(findNode, cancer, 0))
	# Hard Case - Causes (smoker and pollution) are conditionally dependent
	else:
		if givenNode.name == "Smoker":
			bayesValNum = (cancer.probDist["low"]["T"] * findNode.probDist["low"])
			bayesValDenom = ((cancer.probDist["low"]["T"] * findNode.probDist["low"]) + (cancer.probDist["high"]["T"] * (1 - findNode.probDist["low"])))
			bayesVal = bayesValNum/bayesValDenom
			return abs(flag - bayesVal)
		else:
			bayesValNum = (cancer.probDist["low"]["T"] * findNode.probDist["T"])
			bayesValDenom = ((cancer.probDist["low"]["T"] * findNode.probDist["T"]) + (cancer.probDist["low"]["F"] * (1 - findNode.probDist["T"])))
			bayesVal = bayesValNum/bayesValDenom
			return abs(flag - bayesVal)

def predictive(findNode, givenNode, flag):
	# Easiest Case
	if findNode == givenNode:
		return abs(flag - 1)
	# Easy Case - Knowing one node will not affect another independent node 
	elif (findNode.name == 'Pollution' and givenNode.name == 'Smoker') or (findNode.name == 'Pollution' and givenNode.name == 'Smoker'):
		if 'T' in findNode.probDist:
			return abs(flag - findNode.probDist['T'])
		else:
			return abs(flag - findNode.probDist['low']) # Again - table asks for pollution to be high
	# Easy Case
	elif givenNode.name == 'Cancer':
		return abs(flag - findNode.probDist['T'])
	# Harder Case
	elif findNode.name == 'Cancer':
		if givenNode.name == 'Smoker':
			val1 = cancer.probDist["low"]["T"] * pollution.probDist["low"]
			val2 = cancer.probDist["high"]["T"] * (1 - pollution.probDist["low"])
			return abs(flag - (val1 + val2))
		elif givenNode.name == 'Pollution':
			val1 = cancer.probDist["low"]["T"] * smoker.probDist["T"]
			val2 = cancer.probDist["low"]["F"] * (1 - smoker.probDist["T"])
			return abs(flag - (val1 + val2))
	# Harder Case - calculate by whether or not cancer occurs via new cancer value
	else:
		newCancerVal = predictive(cancer, givenNode, 0)
		result = (newCancerVal * findNode.probDist['T']) + ((1 - newCancerVal) * findNode.probDist['F'])
		return abs(flag - result)

# Diagnostic reasoning based off of Table 2.2
# 	Works in some extra cases, but not all 
def diagnostic(findNode, givenNode, flag):
	# easiest calculation
	if findNode == givenNode:
		return abs(flag - 1)
	
	# harder calculations using Bayes Rule
	elif givenNode.name == 'Cancer' or findNode.name == 'Cancer':
		if findNode.name == 'Cancer': # we know either dyspnoia or xray
			bayesVal = (givenNode.probDist['T'] * cancerProb())/margProb(givenNode)
			return abs(flag - bayesVal)
		# Used in the Intercausal Table
		elif findNode.name == 'Pollution':
			helperVal =  predictive(cancer, findNode, 0)
			bayesVal =  (helperVal * findNode.probDist['low']) / cancerProb()
			return abs(flag - bayesVal)
		else:
			helperVal =  predictive(cancer, findNode, 0)
			bayesVal =  (helperVal * findNode.probDist['T']) / cancerProb()
			return abs(flag - bayesVal)

	# harder calculation  using joint probabilities
	elif findNode.name == 'XRay' or findNode.name == 'Dyspnoea':
		newCancerVal = diagnostic(cancer, givenNode, 0)
		result = (newCancerVal * findNode.probDist['T']) + ((1 - newCancerVal) * findNode.probDist['F'])
		return abs(flag - result)
	
	# hardest calculation - eg findNode is Pollution, givenNode is Dyspnoia
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
			bayesVal = (helperVal1 * (abs(flag - findNode.probDist["T"])))/helperVal2
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
			bayesVal = (helperVal1 * (abs(flag - findNode.probDist["low"])))/helperVal2 # pollution = high
			return bayesVal

# Will calculate the marginal probability of any node that has been given
def margProb(findNode):
	if findNode.name == 'Dyspnoea' or findNode.name == 'XRay':
		cancerVal = cancerProb()
		return (findNode.probDist["T"] * cancerVal) + (findNode.probDist["F"] * (1 - cancerVal))
	elif findNode.name == 'Cancer':
		return cancerProb()
	elif findNode.name == 'Pollution':
		return findNode.probDist["low"]
	else:
		return findNode.probDist["T"]

# Not fully implemented - will calculate joint probabilities given the assignment guidelines
def jointProb(input):
	if input == "psc":
		return (pollution.probDist["low"] * smoker.probDist["T"] * cancer.probDist["low"]["T"])
	elif input == "~p~s~c":
		return ((1 - pollution.probDist["low"]) * (1 - smoker.probDist["T"]) * cancer.probDist["high"]["F"])
	else:
		val1 = (pollution.probDist["low"] * smoker.probDist["T"] * cancer.probDist["low"]["T"])
		val2 = (pollution.probDist["low"] * (1 - smoker.probDist["T"]) * cancer.probDist["low"]["F"])
		val3 = ((1 - pollution.probDist["low"]) * smoker.probDist["T"] * cancer.probDist["high"]["T"])
		val4 = ((1 - pollution.probDist["low"]) * (1 - smoker.probDist["T"]) * cancer.probDist["high"]["F"])
		return (val1, val2, val3, val4)

# Simply sets the probability distribution value of the node given to the prior
def setPrior(findNode, prior):
	if "low" in findNode.probDist:
		findNode.probDist["low"] = prior
		return prior
	else:
		findNode.probDist["T"] = prior
		return prior

# Given an inputted letter - will return a node and if necessary a flagf
# 	Used for marginal probability and conditional probability
def returnNode(nodeLetter):
	if nodeLetter == 'P':
		return pollution
	elif nodeLetter == 'S':
		return smoker
	elif nodeLetter == 'C':
		return cancer
	elif nodeLetter == 'D':
		return dyspnoea
	elif nodeLetter == 'X':
		return xray
	elif nodeLetter == 'p':
		return (pollution, 0)
	elif nodeLetter == 's':
		return (smoker, 0)
	elif nodeLetter == 'c':
		return (cancer, 0)
	elif nodeLetter == 'd':
		return (dyspnoea, 0)
	elif nodeLetter == 'x':
		return (xray, 0)
	elif nodeLetter == '~p':
		return (pollution, 1)
	elif nodeLetter == '~s':
		return (smoker, 1)
	elif nodeLetter == '~c':
		return (cancer, 1)
	elif nodeLetter == '~d':
		return (dyspnoea, 1)
	elif nodeLetter == '~x':
		return (xray, 1)

# Determines the type of evidence we have and calls the correct calculation function
def conditionalProb(findNode, flag, givenNodeList):
	# No Evidence
	if len(givenNodeList) == 0:
		return abs(flag - margProb(findNode))
	# One Piece of Evidence
	elif len(givenNodeList) == 1:
		givenNode = givenNodeList[0]
		# Predictive
		if givenNode.name == "Pollution" or givenNode.name == "Smoker":
			return predictive(findNode, givenNode, flag)
		# Diagnostic
		elif givenNode.name == "Dyspnoea" or givenNode.name == "XRay":
			return diagnostic(findNode, givenNode, flag)
		# Intercausal
		else:
			if findNode.name == "Pollution" or findNode.name == "Smoker":
				return diagnostic(findNode, givenNode, flag)
			else:
				return predictive(findNode, givenNode, flag)
	else:
		# Intercausal (May not support intercausal where a child node is known)
		if givenNodeList[0].name == "Cancer":
			return intercausal(findNode, givenNodeList[1], flag)
		elif givenNodeList[1].name == "Cancer":
			return intercausal(findNode, givenNodeList[0], flag)
		# Combined - Determine the type of combination
		elif givenNodeList[0].name == "Smoker" or givenNodeList[0].name == "Pollution":
			if givenNodeList[1].name == "Smoker" or givenNodeList[1].name == "Pollution":
				return easyCombined(findNode, flag)
			elif givenNodeList[1].name == "Dyspnoea" or givenNodeList[1].name == "XRay":
				return combined(findNode, givenNodeList[0], givenNodeList[1], flag)
		else:
			if givenNodeList[1].name == "Smoker" or givenNodeList[1].name == "Pollution":
				return combined(findNode, givenNodeList[1], givenNodeList[0], flag)
			else:
				return hardCombined(findNode, flag)

def inputs():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
        # print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)
	for o, a in opts:
		if o in ("-p"):
			if type(returnNode(a)) == tuple:
				findNode = returnNode(a)[0]
			else:
				findNode = returnNode(a[0])
			setPrior(findNode, float(a[1:]))
		
		elif o in ("-m"):
			if type(returnNode(a)) == tuple:
				print margProb(returnNode(a)[0])
			else:
				print margProb(returnNode(a))
		
		elif o in ("-g"):
			p = a.find("|")
			if type(returnNode(a[:p])) == tuple:
				findNode, flag = returnNode(a[:p])
			else:
				findNode, flag = (returnNode(a[:p]), 0)
			givenNodeList = []
			if len(a[p+1:]) == 1:
				givenNodeList.append(returnNode(a[p+1]))
			elif len(a[p+1:]) == 2:
				givenNodeList.append(returnNode(a[p+1]))
				givenNodeList.append(returnNode(a[p+2]))
			elif len(a[p+1:]) > 2:
				print "Ignoring last value(s)"
				givenNodeList.append(returnNode(a[p+1]))
				givenNodeList.append(returnNode(a[p+2]))
			print conditionalProb(findNode, flag, givenNodeList)

		elif o in ("-j"):
			print jointProb(a)
		else:
			assert False, "unhandled option"

def tests(smokerVal):

	smoker.probDist["T"] = smokerVal

	# Column 1
	print('--------Column 1--------')
	print 1 - margProb(pollution)
	print margProb(smoker)
	print margProb(cancer)
	print margProb(xray)
	print margProb(dyspnoea)

	# Column 2
	print('--------Column 2--------')
	print diagnostic(pollution, dyspnoea, 1)
	print diagnostic(smoker, dyspnoea, 0)
	print diagnostic(cancer, dyspnoea, 0)
	print diagnostic(xray, dyspnoea, 0)
	print diagnostic(dyspnoea, dyspnoea, 0)
	
	# Column 3
	print('--------Column 3--------')
	print predictive(pollution, smoker, 1)
	print predictive(smoker, smoker, 0)
	print predictive(cancer, smoker, 0)
	print predictive(xray, smoker, 0)
	print predictive(dyspnoea, smoker, 0)

	# Column 4
	print('--------Column 4--------')
	print diagnostic(pollution, cancer, 1)
	print diagnostic(smoker, cancer, 0)
	print diagnostic(cancer, cancer, 0)
	print predictive(xray, cancer, 0)
	print predictive(dyspnoea, cancer, 0)

	# Column 5
	print('--------Column 5--------')
	print intercausal(pollution, smoker, 1)
	print intercausal(smoker, smoker, 0)
	print intercausal(cancer, smoker, 0)
	print intercausal(xray, smoker, 0)
	print intercausal(dyspnoea, smoker, 0)

	# Column 6
	print('--------Column 6--------')
	print combined(pollution, smoker, dyspnoea, 1)
	print combined(smoker, smoker, dyspnoea, 0)
	print combined(cancer, smoker, dyspnoea, 0)
	print combined(xray, smoker, dyspnoea, 0)
	print combined(dyspnoea, smoker, dyspnoea, 0)

def main():
	global pollution, smoker, xray, dyspnoea, cancer
	pollution, smoker, xray, dyspnoea, cancer = initVars()
	#tests(0.3)
	inputs()

if __name__ == "__main__":
	main()