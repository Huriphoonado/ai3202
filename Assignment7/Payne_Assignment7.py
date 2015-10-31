# Willie Payne
# Assignment 7 - Prior and Rejection Sampling

def initVars():
	samples = [0.82, 0.56, 0.08, 0.81, 0.34, 0.22, 0.37, 0.99, 0.55, 
	0.61, 0.31, 0.66, 0.28, 1.0, 0.95, 0.71, 0.14, 0.1, 1.0, 0.71, 
	0.1, 0.6, 0.64, 0.73, 0.39, 0.03, 0.99, 1.0, 0.97, 0.54, 0.8, 
	0.97, 0.07, 0.69, 0.43, 0.29, 0.61, 0.03, 0.13, 0.14, 0.13, 
	0.4, 0.94, 0.19, 0.6, 0.68, 0.36, 0.67, 0.12, 0.38, 0.42, 
	0.81, 0.0, 0.2, 0.85, 0.01, 0.55, 0.3, 0.3, 0.11, 0.83, 0.96, 
	0.41, 0.65, 0.29, 0.4, 0.54, 0.23, 0.74, 0.65, 0.38, 0.41, 0.82, 
	0.08, 0.39, 0.97, 0.95, 0.01, 0.62, 0.32, 0.56, 0.68, 0.32, 0.27, 
	0.77, 0.74, 0.79, 0.11, 0.29, 0.69, 0.99, 0.79, 0.21, 0.2, 0.43, 
	0.81, 0.9, 0.0, 0.91, 0.01]

	organized_samples = []
	for i in range(0, len(samples), 4):
		newList = [samples[i], samples[i+1], samples[i+2], samples[i+3]]
		organized_samples.append(newList)

	c = {"T": .5}
	s = {"T": .1, "F": .5}
	r = {"T": .8, "F": .2}
	w = {"T": {"T": .99, "F": .9}, "F": {"T": .9, "F": 0}} # w[S][R]

	return organized_samples, c, s, r, w

# Iterate through the list of numbers keeping track of the world state
# 	Order: C -> S -> R -> W
def priorSampling(samples, c, s, r, w):
	cCount, sCount, rCount, wCount = 0, 0, 0, 0
	cState, sState, rState, = "T", "T", "T"
	size = float(len(samples))
	worldStates = []

	for sample in samples:
		s1, s2, s3, s4 = sample[0], sample[1], sample[2], sample[3]
		# Cloudy
		if s1 <= c["T"]:
			cCount = cCount + 1.
			cState = "T"
		else:
			cState = "F"
		# Sprinkler
		if s2 <= s[cState]:
			sCount = sCount + 1.
			sState = "T"
		else:
			sState = "F"
		# Rainy
		if s3 <= r[cState]:
			rCount = rCount + 1.
			rState = "T"
		else:
			rState = "F"
		# Wet Grass
		if s4 <= w[sState][rState]:
			wCount = wCount + 1.
			wState = "T"
		else:
			wState = "F"
		
		worldStates.append([cState, sState, rState, wState])

	return worldStates

def solvePriorities(worldStates):
	size = float(len(worldStates))
	prob1, prob2, prob3, prob4 = 0., 0., 0., 0.
	prob2Count, prob3Count, prob4Count = 0., 0., 0.
	
	# Problem 1 - P(c = true)
	for state in worldStates:
		if state[0] == "T":
			prob1 = prob1 + 1

	# Problem 2 - P(c = true | rain = true)
	for state in worldStates:
		if state[2] == "T":
			prob2Count = prob2Count + 1
			if state[0] == "T":
				prob2 = prob2 + 1

	# Problem 3 - P(s=true|w=true)
	for state in worldStates:
		if state[3] == "T":
			prob3Count = prob3Count + 1
			if state[1] == "T":
				prob3 = prob3 + 1

	# Problem 4 - P(s=true|c=true,w=true)
	for state in worldStates:
		if state[0] == "T" and state[3] == "T":
			prob4Count = prob4Count + 1
			if state[1] == "T":
				prob4 = prob4 + 1

	return prob1/size, prob2/prob2Count, prob3/prob3Count, prob4/prob4Count

def main():
	samples, c, s, r, w = initVars()
	worldStates = priorSampling(samples, c, s, r, w)
	print solvePriorities(worldStates)


if __name__ == "__main__":
	main()