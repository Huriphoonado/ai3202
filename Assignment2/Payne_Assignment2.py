# Willie Payne
# CSCI 3202 Assignment 2

class Node(object):
	def __init__(self, location):
		self.location = location
		self.distanceToStart = 0
		self.heuristic = 0
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

def readFile(fileName):
	pass
	
# Horizontal and Vertical Moves cost 10
# Diagonal Moves cost 14
# Mountains cost an extra 10
def Manhattan_Distance(N):
	pass

if __name__ == "__main__":
	mapFile, hType = inputText()
	if mapFile != False:
		readFile(mapFile)
		myNode = Node([0, 0])