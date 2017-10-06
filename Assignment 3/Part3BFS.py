from PIL import Image, ImageDraw, ImageFont
from heapq import heappush, heappop



class Tile:		#tile class for every tile generated
	xPos = 0
	yPos = 0
	g = 0
	h = 0
	f = 0
	cost = 0
	parent = None

	def __init__(self, x, y, parent, cost):		#initialize parent and coordinates
		self.xPos = x
		self.yPos = y
		self.parent = parent
		self.cost = cost

	def __cmp__(self, rhs):		#overload cmp operator, compares only f value
		if rhs == None: return False
		if self.f > rhs.f: return 1
		if self.f == rhs.f: return 0
		if self.f < rhs.f: return -1

	def __eq__(self, rhs):		##overload == operator to compare x and y coordinates
		if rhs == None: return False
		if self.xPos == rhs.xPos and self.yPos == rhs.yPos: return True
		return False

	def manhattanDist(self, end):		#calculates manhattan dist from self to given tile
		#calculates |x_2 - x_1| + |y_2 - y_1|
		return abs(self.xPos - end.xPos) + abs(self.yPos - end.yPos)


class Board:
	x, y = 0,0								#initialize variables to save board size
	board = []								#initialize board for saving input file

	def __init__(self, filename):

		file = open(filename, 'r')			#open boardfile
		for line in file:					#iterate trought file
			l = list(line[:-1])				#make string into list & removing the last \n
			if self.x == 0: self.x = len(l)	#if x is not set it is set to the length of input list
			if 'A' in l:					#if there is an element in input list with value A save as startTile
				self.startTile =Tile(l.index('A'),(len(self.board)), None, 0)
			if 'B' in l:					#if there is element in input list with value B save as endTile
				self.endTile = Tile(l.index('B'),(len(self.board)), None, 0)
			self.board.append(l)			#append the input list to board when finished investigating it
			self.y+=1						#increment y for every input list



	def bfs(self):
		c, o = [], []						#initialize closed and open lists

		#give startTile right h and f value, and append to open list
		self.startTile.h = self.startTile.manhattanDist(self.endTile)
		self.startTile.f = self.startTile.h + self.startTile.g
		o.append(self.startTile)

		while o:							#while there is elements in open-list		
			x = o.pop(0)						#pop the best element(smallest f) from 
			if x in c: continue				#if element is already closed continue
			c.append(x)						#push element into closed list

			#if we are at endTile we are finished, return good values
			if x == self.endTile: return x, True, o, c
			succ = self.genSucc(x)			#find successors to x
			for s in succ:					#for all successors
				if s in c: continue			#if already closed continue 
				g = x.g + s.cost			#calculate value of g for successor	

				#if s not opened or has better value than already existing opened s
				if s not in o or g < o[o.index(s)].g:
					s.g = g 				#update g and calculate new h
					s.h = s.manhattanDist(self.endTile)
					s.f = s.g + s.h 		#update h
					if s not in o:			#if not opened push into heap at right place
						o.append(s)
		return None, False					#if we didn't reach endTile return false


	def genSucc(self, current):
		succ = []							#initialize successor list
		x, y = current.xPos, current.yPos	#get current coordinates

		#array for iterate over successors
		array = [(x-1, y), (x+1,y), (x, y-1), (x, y+1)]
		for x_,y_ in array:					#iterate through all sucessor coordinates

			#if inside board get cost associated with tile and append to successor list
			if 0 <= x_ < self.x and 0 <= y_ < self.y: 
				if self.board[y_][x_] == '#': continue 
				cost = self.getCost(self.board[y_][x_])
				succ.append(Tile(x_, y_, current, cost))
		return succ

	def reconstructPath(self, current):
		#reconstruct path by starting at a current tile
		path = [(current.xPos, current.yPos)]

		while current.parent:  #and working your way backwards trought parents until there is none
			path.append((current.parent.xPos,current.parent.yPos))
			current = current.parent
		return path

	def getColor(self, symbol):
		#returns color value based on which symbol
		if symbol == "A":
			return (255,0,0)
		elif symbol == "B":
			return (64,128,64)
		elif symbol == "w":
			return (0,0,255)
		elif symbol == "m":
			return (128,128,128)
		elif symbol == "f":
			return (0,102,51)
		elif symbol == "g":
			return (51,255,51)
		elif symbol == "r":
			return (204,102,0)
		elif symbol == "#":
			return (0,0,0)

	def getCost(self, symbol):
		#returns cost based on input symbol
		if symbol == "w":
			return 100
		elif symbol == "m":
			return 50
		elif symbol == "f":
			return 10
		elif symbol == "g":
			return 5
		elif symbol == "r":
			return 1
		elif symbol == "B" or symbol == "A" or symbol =="." or symbol == "#":
			return 1

	def printBoardGraphics(self, path, opened, closed):
		img = Image.new("RGB", (70*self.x, 70*self.y), "white")			#draw background image with 70*x by 70*y resolution
		idraw = ImageDraw.Draw(img)										#make possible to draw
		for x in range(0, len(self.board)):								#iterate trough all elements in board
			for y in range(0, len(self.board[0])):						
				c = self.getColor(self.board[x][y])						#get color of current element
				#draw 70x70 rectangle with right color and a black outline
				idraw.rectangle([(y*70,x*70),(y*70+70,x*70+70)], fill=c, outline=(0,0,0))

				#if coordinate is in path draw smaller square on top to show path
				if (y,x) in path:
					c = (107,97,255)
					idraw.rectangle([(y*70+20,x*70+20),(y*70+50,x*70+50)], fill=c, outline=(0,0,0))
				elif (y,x) in closed:
					c = (0,0,0)
					font = ImageFont.truetype("arial.ttf", size=40)
					idraw.text([y*70+20,x*70+20],"X", c, font)
				elif (y,x) in opened:
					c = (0,0,0)
					font = ImageFont.truetype("arial.ttf", size=100)
					idraw.text([y*70+15,x*70+5],"*", c, font)

		img.save("pictures/bfs board-1-4.png")										#save board	


def main(): 
	#make board, run bfs and save graphics
	a = Board("boards/board-1-4.txt")
	current, success, opened, closed = a.bfs()
	o, c = [], []
	if success:
		path = a.reconstructPath(current)
		for element in opened:
			o.append((element.xPos, element.yPos))
		for element in closed:
			c.append((element.xPos, element.yPos))
		a.printBoardGraphics(path, o, c)

if __name__ == "__main__":
    main()