# Willie Payne
# CSCI 3202 Assignment 2

class Node(object):
	def __init__(self, location, type):
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
	mapFile = raw_input("Please provide a world (World1.txt or World2.txt): ")
	if mapFile != "World1.txt" and mapFile != "World2.txt":
		print "Invalid Input"
		return (False,False)
	hType = raw_input("Please provide a heuristic (Manhattan): ")
	if hType != "Manhattan":
		print "Invalid Input"
		return (False,False)
	return (mapFile, hType)

# Reads the file and returns the file as a string
def readFile(fileName):
	mapString = open(fileName, 'r')
	mapString = mapString.read()
	return mapString

def buildGraph(mapString):
	xPos = 0
	yPos = 0
	rows = mapString.split('\n')
	newRows = []
	nodeList = []
	
	for row in rows:
		if row != '':
			newRows.append(row.split(' '))
	for c in newRows:
		xPos = 0
		for r in c:
			pathType = ''
			print r
			if r == '0':
				pathType = 'path'
			elif r == '1':
				pathType = 'mountain'
			else:
				pathType = 'wall'
			newNode = Node([xPos, yPos], pathType)
			nodeList.append(newNode)
			xPos = xPos + 1
		yPos = yPos + 1
	return nodeList


	
# Horizontal and Vertical Moves cost 10
# Diagonal Moves cost 14
# Mountains cost an extra 10
def Manhattan_Distance(N):
	pass

if __name__ == "__main__":
	mapFile, hType = inputText()
	if mapFile != False:
		mapString = readFile(mapFile)
		buildGraph(mapString)