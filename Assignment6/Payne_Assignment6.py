# Willie Payne
# 10/18
# Assignment 6 - Bayes Net Disease Predictor

import getopt

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

def jointProb():
	pass

def inputs():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
        # print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)
	for o, a in opts:
		if o in ("-p"):
			print "flag", o
			print "args", a
			print a[0]
			print float(a[1:])
			#setting the prior here works if the Bayes net is already built
			#setPrior(a[0], float(a[1:])
		elif o in ("-m"):
			print "flag", o
			print "args", a
			print type(a)
			#calcMarginal(a)
		elif o in ("-g"):
			print "flag", o
			print "args", a
			print type(a)
			'''you may want to parse a here and pass the left of |
			and right of | as arguments to calcConditional
			'''
			p = a.find("|")
			print a[:p]
			print a[p+1:]
			#calcConditional(a[:p], a[p+1:])
		elif o in ("-j"):
			print "flag", o
			print "args", a
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
	tests(0.3)

if __name__ == "__main__":
	main()