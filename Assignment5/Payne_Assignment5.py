# Willie Payne
# AI 3202 - Assignment 5

# Markhov Decision Processes

import sys

# Node class containing all information needed for MDP
# Initialized with an location, type, and reward all provided in World files
# Nodes are stored in nodeList, a dictionary representing our graph
class Node(object):
	def __init__(self, location, type, reward):
		self.location = location # [x,y]
		self.type = type # 0 = path, 1 = mountain, 2 = wall, 3 = Snake, 4 = barn, 5 = terminal
		self.reward = reward # Determined by Node Type
		self.utility = 0
		self.direction = '' # calulated by whichever direction yields the highest utility
		self.parent = None # Pointer to the Node of whichever direction yields the highest utility
		# Adjacent nodes are set after the world has been read in
		self.north = None
		self.south = None
		self.east = None
		self.west = None

	# Calculates the utility of the current node
	# 	If one of the adjacent nodes is None - we bounce back and use the utility of the current
	# 	node in our calculations
	def calculateUtility(self):
		y = 0.9 # discount factor

		# Terminal node remains at 50
		if self.type == 'terminal':
			self.utility = self.reward
			self.direction = 'Done'
			return self.utility

		# Determine what values to use in the calculation
		if self.north != None:
			northUtil = self.north.utility
		else:
			northUtil = self.utility
		if self.south != None:
			southUtil = self.south.utility
		else:
			southUtil = self.utility
		if self.east != None:
			eastUtil = self.east.utility
		else:
			eastUtil = self.utility
		if self.west != None:
			westUtil = self.west.utility
		else:
			westUtil = self.utility

		# Transition Model Calculations
		northOption = (0.8 * northUtil) + (0.1 * eastUtil) + (0.1 * westUtil)
		southOption = (0.8 * southUtil) + (0.1 * eastUtil) + (0.1 * westUtil)
		eastOption = (0.8 * eastUtil) + (0.1 * northUtil) + (0.1 * southUtil)
		westOption = (0.8 * westUtil) + (0.1 * northUtil) + (0.1 * southUtil)

		# Pick the highest calculated option
		# 	Array stores utility, direction, and parent node
		options = ([northOption, 'North', self.north], [southOption, 'South', self.south], 
			[eastOption, 'East', self.east], [westOption, 'West', self.west])
		bestOption = max(options)
		
		# Calculate equation via the provided utility
		self.utility = self.reward + (y * bestOption[0])
		self.direction = bestOption[1]
		self.parent = bestOption[2]

		return self.utility

# Read in the map file to use and e as commandline arguments
# If invalid or not supplied - return False
def inputText():
	if len(sys.argv) != 3:
		print "Wrong number of arguments supplied (Input E value)"
		return (False, False)
	elif sys.argv[1] != "World1MDP.txt":
		print "Incorrect world supplied"
		return (False, False)
	else:
		return (sys.argv[1], float(sys.argv[2]))

# Reads the file and returns the file as a string
def readFile(fileName):
	mapString = open(fileName, 'r')
	mapString = mapString.read()
	return mapString

# Reads the string and returns nodeList, a list of nodes
# 	The node's position in the list is a mapping of its coordinate nodeList[x][y]
# 	The starting point in the list is nodeList[0][0]
# 	nodeList is essentially our graph class
def stringToList(mapString):
	xPos = 0
	yPos = 7
	rows = mapString.split('\n')
	newRows = list()
	nodeList = []

	for k in range(10):
			nodeList.append([])
			for j in range(8):
				nodeList[k].append(None)

	for row in rows:
		if row != '':
			newRows.append(row.split(' '))
	for c in newRows:
		xPos = 0
		for r in c:
			pathType = ''
			reward = 0
			if r == '0':
				pathType = 'path'
			elif r == '1':
				pathType = 'mountain'
				reward = -1.0
			elif r == '2':
				pathType = 'wall'
			elif r == '3':
				pathType = 'snake'
				reward = -2.0
			elif r == '4':
				pathType = 'barn'
				reward = 1.0
			else:
				pathType = 'terminal'
				reward = 50.0
			newNode = Node([xPos, yPos], pathType, reward)
			nodeList[xPos][yPos] = newNode
			xPos = xPos + 1
		yPos = yPos - 1

	return nodeList

# Takes in a list of nodes and sets each node's adjacent nodes to be correct pointers
# 	Remains None if the adjacent node is a wall or is outside the bounds of the map
def calcAdjNodes(nodeList):
	xBound = 10
	yBound = 8

	for x in range(10):
		for y in range(8):
			current = nodeList[x][y]
			if current.type != 'wall':
				if x + 1 < xBound and nodeList[x+1][y].type != 'wall':
					current.east = nodeList[x+1][y]
				if x - 1 >= 0 and nodeList[x-1][y].type != 'wall':
					current.west = nodeList[x-1][y]
				if y + 1 < yBound and nodeList[x][y+1].type != 'wall':
					current.north = nodeList[x][y+1]
				if y - 1 >= 0 and nodeList[x][y-1].type != 'wall':
					current.south = nodeList[x][y-1]
	return nodeList

# Iterate through the loop and keep track of the biggest delta value
# 	Continue until biggest delta is greater than minChange
def ValueIteration(nodeList, minChange):
	maxChangeInCycle = minChange + 1
	iterate = 0
	while maxChangeInCycle > minChange:
		maxChangeInCycle = 0
		iterate = iterate + 1
		#print iterate
		for y in range(7, -1, -1):
				for x in range(9, -1, -1):
					if nodeList[x][y].type != 'wall':
						oldUtil = nodeList[x][y].utility
						newUtil = nodeList[x][y].calculateUtility()
						currentChange = abs(oldUtil - newUtil)
						if currentChange > maxChangeInCycle:
							maxChangeInCycle = currentChange

	return nodeList

# Simply prints all the values in the map arranged in nice columns
# 	Helps in practice to gather all the utilities and directions
def printVals(nodeList):
	nodeListFormatted = []

	for k in range(8):
		nodeListFormatted.append([])
		for j in range(10):
			nodeListFormatted[k].append(None)

	for y in range(8):
		for x in range(10):
			if nodeList[x][y].type != 'wall':
				nodeListFormatted[7-y][x] = str(nodeList[x][y].direction)
			else:
				nodeListFormatted[7-y][x] = 'Wall'

	col_width = max(len(word) for row in nodeListFormatted for word in row) + 2
	for row in nodeListFormatted:
		print "".join(word.ljust(col_width) for word in row)

# Prints the path taken from a node to its parent nodes to the terminal
# 	Prevents an infinite loop that can occur if two nodes point at each other
def printPath(currentNode, lastNode):
	if currentNode.type == 'terminal':
		print "Final Location:", currentNode.location[0], currentNode.location[1], "Reward:", '%.3f' % currentNode.utility
		return
	elif currentNode.parent == lastNode:
		print "The path ends here as two nodes are each other's best direction."
		print "There is either an error, or the algorithm has found a local max"
		print "Final Location:", currentNode.location[0], currentNode.location[1], "Utility:", '%.3f' % currentNode.utility
		return
	else:
		print "Location:", currentNode.location[0], currentNode.location[1], "Utility:", '%.3f' % currentNode.utility
		return printPath(currentNode.parent, lastNode)

def main():
	mapFile, eVal = inputText()
	if mapFile != False and eVal != False:
		minChange = (eVal * .1)/.9
		mapString = readFile(mapFile)
		nodeList = stringToList(mapString)
		nodeList = calcAdjNodes(nodeList)
		nodeList = ValueIteration(nodeList, minChange)
		printPath(nodeList[0][0], None)

if __name__ == "__main__":
	main()