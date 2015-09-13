# Willie Payne
# CSCI 3202 Assignment 2

import sys
import copy

class Node(object):
	def __init__(self, id, location, type, weight):
		self.id = id
		self.location = location
		self.type = type # path, mountain, wall
		self.g = 0 # Distance to Start
		self.h = 0 # Heuristic
		self.f = 0 # g + h
		self.weight = weight # Becomes 10 if node is a mountain
		self.parent = None

# Read in the map file to use and the heuristic type
# If either are invalid - return false
def inputText():
	if len(sys.argv) != 3:
		print "Wrong number of arguments supplied (Input world followed by heuristic)"
		return (False, False)
	elif sys.argv[1] != "World1.txt" and sys.argv[1] != "World2.txt":
		print "Incorrect world supplied"
		return (False, False)
	elif sys.argv[2] != "Manhattan":
		print "Incorrect heuristic supplied"
		return (False, False)
	else:
		return (sys.argv[1], sys.argv[2])

# Reads the file and returns the file as a string
def readFile(fileName):
	mapString = open(fileName, 'r')
	mapString = mapString.read()
	return mapString

def stringToList(mapString):
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
		nodeDict[n].h = (abs(endX - xPos) + abs(endY - yPos)) * 10

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
# Else consider it - return True
def checkClosedList(currentNode, closed):
	for n in closed:
		if currentNode.id == n.id:
			return False
	else:
		return True

# Calculates adjacent nodes  when provided a currentNode
# 	Returns two lists - horizontal/vertical and diagonal
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
			print n.id, n.parent.id, n.g, currentNode.id, currentNode.parent.id, currentNode.g
			if n.g > currentNode.g:
				n.g = currentNode.g
				n.parent = currentNode.parent
			break
	else:
		opened.append(currentNode)
	return opened

def trackSolution(endNode, traveledList):
	while endNode != None:
		traveledList.insert(0,endNode.location)
		endNode = endNode.parent
	return traveledList

# Horizontal and Vertical Moves cost 10
# Diagonal Moves cost 14
# Mountains cost an extra 10
def aStar(nodeDict, start, end):
	opened = []
	closed = []
	traveledList = []
	opened.append(start)

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
			print 'Cost:', currentNode.g
			print 'Number of Moves:', len(traveledList) - 1
			print 'Nodes Visited (With Starting Point as x: 0, y: 0):'
			for n in traveledList:
				print n[0], 7 - n[1]
			
			return True

if __name__ == "__main__":
	mapFile, hType = inputText()
	
	if mapFile != False:
		'''if mapFile == 'World1.txt':
			start = str([0,6]) # Starting/Ending points for World 1
			end = str([9,0])
		else:
			start = str([0,7]) # Starting/Ending points for World 2
			end = str([9,0])'''
		start = str([0,7])
		end = str([9,0])
		mapString = readFile(mapFile) # Convert world file to string
		nodeDict = stringToList(mapString) # Convert string to dictionary of nodes
		
		if hType == 'Manhattan':
			nodeDict = manhattanDistance(nodeDict, nodeDict[end])
			aStar(nodeDict, nodeDict[start], nodeDict[end])
