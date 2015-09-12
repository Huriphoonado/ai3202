# Willie Payne
# CSCI 3202 Assignment 2

import sys

class Node(object):
	def __init__(self, id, location, type):
		self.id = id
		self.location = location
		self.adjacentNodes = []
		self.type = type # path, mountain, wall
		self.g = 0 # Distance to Start
		self.h = 0 # 
		self.f = 0
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
	nodeList = []
	nodeDict = {}
	for row in rows:
		if row != '':
			newRows.append(row.split(' '))
	for c in newRows:
		xPos = 0
		for r in c:
			pathType = ''
			if r == '0':
				pathType = 'path'
			elif r == '1':
				pathType = 'mountain'
			else:
				pathType = 'wall'
			newNode = Node(str([xPos, yPos]),[xPos, yPos], pathType)
			nodeDict[newNode.id] = newNode
			xPos = xPos + 1
		yPos = yPos + 1

	return nodeDict

# Calculates adjacent nodes  when provided a currentNode
# 	Returns two lists - horizontal/vertical and diagonal
# 	Does not return walls
def returnAdjacentNodes(nodeDict, currentNode):
	xPos,yPos = currentNode.location
	nNodes = []
	dNodes = []
	nNodeKeys = [str([xPos + 1,yPos]), str([xPos - 1,yPos]), str([xPos,yPos + 1]), str([xPos,yPos - 1])]
	dNodeKeys = [str([xPos + 1,yPos + 1]), str([xPos + 1,yPos - 1]), str([xPos - 1,yPos + 1]), str([xPos -1 ,yPos - 1])]
	for n in nNodeKeys:
		if n in nodeDict:
			if nodeDict[n].type != 'wall':
				nNodes.append(nodeDict[n])
	for n in dNodeKeys:
		if n in nodeDict:
			if nodeDict[n].type != 'wall':
				dNodes.append(nodeDict[n])
	return nNodes, dNodes

# Horizontal and Vertical Moves cost 10
# Diagonal Moves cost 14
# Mountains cost an extra 10
def Manhattan_Distance(N):
	pass

if __name__ == "__main__":
	mapFile, hType = inputText()
	if mapFile != False:
		mapString = readFile(mapFile)
		nodeDict = stringToList(mapString)
		returnAdjacentNodes(nodeDict, nodeDict[str([0,6])])
