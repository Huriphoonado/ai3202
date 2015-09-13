# Willie Payne
# CSCI 3202 Assignment 2

# Implementation of A* Search

import sys
import copy

# Node class containing all information needed for A* search
# Initialized with an id, location, type, and weight all provided in World files
# Nodes are stored in nodeDict, a dictionary representing our graph
class Node(object):
	def __init__(self, id, location, type, weight):
		self.id = id # '[x,y]'
		self.location = location # [x,y]
		self.type = type # 0 = path, 1 = mountain, 2 = wall
		self.g = 0 # Distance to Start
		self.h = 0 # Heuristic
		self.f = 0 # g + h
		self.weight = weight # Becomes 10 if node is a mountain
		self.parent = None # parent node used for determining path

# Read in the map file to use and the heuristic type as commandline arguments
# If either are invalid - return false
def inputText():
	if len(sys.argv) != 3:
		print "Wrong number of arguments supplied (Input world followed by heuristic)"
		return (False, False)
	elif sys.argv[1] != "World1.txt" and sys.argv[1] != "World2.txt":
		print "Incorrect world supplied"
		return (False, False)
	elif sys.argv[2] != "Manhattan" and sys.argv[2] != "DiagonalShortcut":
		print "Incorrect heuristic supplied"
		return (False, False)
	else:
		return (sys.argv[1], sys.argv[2])

# Reads the file and returns the file as a string
def readFile(fileName):
	mapString = open(fileName, 'r')
	mapString = mapString.read()
	return mapString

# Reads the string and returns nodeDict, a dictionary of nodes
# 	The node's key is the string of its coordinate
# 	nodeDict is used to determine neighbor nodes, node types, and h value
# 	aStar algorithm copies nodes on its path from nodeDict
def stringToDict(mapString):
	xPos = 0
	yPos = 0
	rows = mapString.split('\n')
	newRows = []
	nodeDict = {}
	for row in rows:
		if row != '':
			newRows.append(row.split(' '))
	for c in newRows:
		xPos = 0
		for r in c:
			pathType = ''
			weighted = 0
			if r == '0':
				pathType = 'path'
			elif r == '1':
				pathType = 'mountain'
				weighted = 10
			else:
				pathType = 'wall'
			newNode = Node(str([xPos, yPos]),[xPos, yPos], pathType, weighted)
			nodeDict[newNode.id] = newNode
			xPos = xPos + 1
		yPos = yPos + 1

	return nodeDict

# Returns 10 times the distance from every node to the end node
def manhattanDistance(nodeDict, end):
	xPos,yPos = 0,0
	endX, endY = end.location

	for n in nodeDict:
		xPos,yPos = nodeDict[n].location
		nodeDict[n].h = (abs(endX - xPos) + abs(endY - yPos)) * 10 # Reduced to 5 yields better results

	return nodeDict

# Subtracts the cost of steps saved by taking a diagonal 
# From Game Programming Heuristics: http://theory.stanford.edu/%7Eamitp/GameProgramming/Heuristics.html
def diagonalShortcut(nodeDict, end):
	xPos, yPos = 0,0
	dx, dy = 0,0
	endX, endY = end.location
	amountSaved = 14 - (2 * 10) 

	for n in nodeDict:
		xPos,yPos = nodeDict[n].location
		dx = abs(endX - xPos)
		dy = abs(endY - yPos)
		nodeDict[n].h = (10 * (dx + dy)) + (amountSaved * min(dx, dy))

	return nodeDict

# Returns the node with the smallest f value in the opened list
def returnMinNode(opened):
	pos = 0
	currentMin = opened[0].f
	if len(opened) == 1:
		return opened[0]
	else:
		for n in range(len(opened)):
			if opened[n].f < currentMin:
				currentMin = opened[n].f
				pos = n
	return opened[pos]

# If node is in the closed list - Don't look at it (return False)
# Else, consider it - return True
def checkClosedList(currentNode, closed):
	for n in closed:
		if currentNode.id == n.id:
			return False
	else:
		return True

# Calculates adjacent nodes  when provided a currentNode
# 	Returns two lists - horizontal/vertical nodes and diagonal nodes
# 	Does not return walls or nodes in the closed list
def returnAdjacentNodes(nodeDict, currentNode, closed):
	xPos,yPos = currentNode.location
	nNodes = []
	dNodes = []
	nNodeKeys = [str([xPos + 1,yPos]), str([xPos - 1,yPos]), str([xPos,yPos + 1]), str([xPos,yPos - 1])]
	dNodeKeys = [str([xPos + 1,yPos + 1]), str([xPos + 1,yPos - 1]), str([xPos - 1,yPos + 1]), str([xPos -1 ,yPos - 1])]
	for n in nNodeKeys:
		if n in nodeDict:
			if nodeDict[n].type != 'wall':
				if checkClosedList(nodeDict[n], closed):
					nNodes.append(nodeDict[n].id)
	for n in dNodeKeys:
		if n in nodeDict:
			if nodeDict[n].type != 'wall':
				if checkClosedList(nodeDict[n], closed):
					dNodes.append(nodeDict[n].id)
	return nNodes, dNodes

# Searches through the list of opened nodes
# 	If node is in list: check if it has a lower g value and replace if necessary
# 	Otherwise, append it to the list
def replaceIfLower(opened, currentNode):
	for n in opened:
		if n.id == currentNode.id:
			if n.g > currentNode.g:
				n.g = currentNode.g
				n.parent = currentNode.parent
			break
	else:
		opened.append(currentNode)
	return opened

# Traces the solution node's parents all the way back to the start
def trackSolution(endNode, traveledList):
	while endNode != None:
		traveledList.insert(0,endNode.location)
		endNode = endNode.parent
	return traveledList

# A* Search - called with nodeDict initialized to selected heuristic
# 	Horizontal and Vertical Moves cost 10, Diagonal Moves cost 14
# 	Mountains cost an extra 10
def aStar(nodeDict, start, end):
	opened = []
	closed = []
	traveledList = []
	opened.append(start)
	nodesEvaluated = 0

	while len(opened) > 0:
		currentNode = returnMinNode(opened)
		opened.remove(currentNode)
		if currentNode.location != end.location:
			closed.append(currentNode)
			nNodes, dNodes = returnAdjacentNodes(nodeDict, currentNode, closed)
			for n in nNodes: # Horiz/Vert = totalDist + Weight + 10
				newNode = copy.copy(nodeDict[n])
				newNode.g = currentNode.g + newNode.weight + 10
				newNode.f = newNode.g + newNode.h
				newNode.parent = currentNode
				opened = replaceIfLower(opened, newNode)
			for n in dNodes: # Diag = totalDist + Weight + 14
				newNode = copy.copy(nodeDict[n])
				newNode.g = currentNode.g + newNode.weight + 14
				newNode.f = newNode.g + newNode.h
				newNode.parent = currentNode
				opened = replaceIfLower(opened, newNode)
		else: # We have reached the solution so let's retrace our steps!
			traveledList = trackSolution(currentNode, traveledList)
			nodesEvaluated = len(closed) + len(opened)
			
			print 'Cost:', currentNode.g
			print 'Total Nodes Evaluated:', nodesEvaluated
			print len(traveledList), 'Nodes Visited on Path (With Starting Point as x: 0, y: 0):'
			for n in traveledList:
				print n[0], 7 - n[1]
			
			return True

if __name__ == "__main__":
	mapFile, hType = inputText()
	
	if mapFile != False:
		start = str([0,7]) # Start and end are same on both worlds
		end = str([9,0])
		mapString = readFile(mapFile) # Convert world file to string
		nodeDict = stringToDict(mapString) # Convert string to dictionary of nodes
		
		if hType == 'Manhattan': # set nodeDict to Manhattan heuristic and call A*
			nodeDict = manhattanDistance(nodeDict, nodeDict[end])
			aStar(nodeDict, nodeDict[start], nodeDict[end])

		else: # set nodeDict to Diagonal Shortcut heuristic and call A*
			nodeDict = diagonalShortcut(nodeDict, nodeDict[end])
			aStar(nodeDict, nodeDict[start], nodeDict[end])

