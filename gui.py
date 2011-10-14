

import indexer
import curses, sys, os

#print curses

#help(curses.wrapper)
#help on pads: 			http://docs.python.org/library/curses.html#curses.newpad
#curses programming: 	http://docs.python.org/howto/curses.html#windows-and-pads


def testGame():
	'''the game on the professor's book. page 139.'''
	gl.boxrows = 5
	gl.boxcols = 5
	while True:
		c = gl.scrn.getch()
		c = chr(c)
		if c == 'q': break
		draw(c)
		
def draw(chr):
	# paint chr at current position, overwriting what was there; if it?s
	# the last row, also change colors; if instead of color we had
	# wanted, say, reverse video, we would specify curses.A_REVERSE instead of
	# curses.color_pair(1)
	if gb.row == gb.boxrows-1:
		gb.scrn.addch(gb.row,gb.col,chr,curses.color_pair(1))
	else:
		gb.scrn.addch(gb.row,gb.col,chr)
	# implement the change
	gb.scrn.refresh()
	# move down one row
	gb.row += 1
	# if at bottom, go to top of next column
	if gb.row == gb.boxrows:
		gb.row = 0
		gb.col += 1
		# if in last column, go back to first column
		if gb.col == gb.boxcols: 
			gb.col = 0



class globals:
	error = {}
	pagesList = []
	padsList = []  #maybe a more complicated version of a list. probably a list of {}
	pdfPad = None
	indexPad = None
	scrn = None
	row = 0
	col = 0
	
gb = gl = globals()

#wr = curses.wrapper.wrapper()
def initScreen():
	gl.scrn = curses.initscr()
	curses.noecho
	curses.cbreak()
	curses.start_color()
	gl.scrn.keypad(1)
	gb.scrn.clear()
	gl.scrn.refresh()
	gl.row = 0
	gl.column = 0
	
def restoreScreen():
	curses.nocbreak()
	curses.echo()
	curses.endwin()
	gl.scrn.keypad(0)
	
	
def grabPages(textFile):
	gl.pagesList = indexer.preparePdfPages(textFile)
	return gl.pagesList
	
def grabCurrScreenSize():
	'''returns the height and width of the window'''
	#print 'asdfa'
	size =  gl.scrn.getmaxyx()
	return size
	pass
	  
def getSecondWindowCorner():
	'''Returns where the second window should be.
	the height of the main window / 2, and column 0.
	
	The first window should always be displayed at (0,0)
	'''
	height, width = grabCurrScreenSize()
	return height/2, width
	
def createNewPads(pagesList):
	gl.padsList = [{} for j in pagesList]
	for padNum, page in pagesList:
		pad, pageLines = createNewPad(page)
		fillInPad(pad, pageLines)
		addPadToPadList(pad, padNum, pageLines)
		
padsKeys = ['pad', 'pageLines', 'coor', ]
		
def addPadToPadList(pad, pageLines, padNum=-1):
	tempPad = {'pad': pad, 'pageLines': pageLines}
	if padNum == -1:
		padNum = len(gl.padsList)
		gl.padsList.append(tempPad)
		#return padNum
	else:
		gl.padsList[padNum]['pad'] = pad
		gl.padsList[padNum]['pageLines'] = pageLines
	return padNum
	
def displayNewPad(page, bottom = False):
	pad, pageLines = createNewPad(page)
	fillInPad(pad, pageLines)
	padNum = addPadToPadList(pad, pageLines)
	displayPad(padNum, bottom)
	return pad, pageLines
	
def createNewPad(pageStr):
	pageLines = pageStr.split(os.linesep)
	nlines = len(pageLines)
	ncols = max(map(len, pageLines))
	pad = curses.newpad(nlines, ncols)
	return pad, pageLines
	
def fillInPad(pad, pageLines):
	for j, line in enumerate(pageLines):
		pad.addstr(j, 0, line)
		
def addPad_Coordinates(padNum, (padCornerY, padCornerX, winStart_Y, winStart_X, winEnd_Y, winEnd_X) = (0,0,0,0,0,0), bottom=False):
	gl.padsList[padNum]['coor'] = (padCornerY, padCornerX, winStart_Y, winStart_X, winEnd_Y, winEnd_X)
	gl.padsList[padNum]['bottom'] = bottom
	
def getPad_Coordinates(padNum):
	try: 
		return gl.padsList[padNum]['coor']
	except:
		return (0,0,0,0,0,0)
		
def displayPad(padNum, bottom=False, padCorner = (0,0) ):
	pad = gl.padsList[padNum]['pad']
	y, x = 0, 0
	midy, midx = getSecondWindowCorner()
	winY, winX = grabCurrScreenSize()
	#pad.refresh(y, x, 0, 0, 10, 30)
	try:
		if not bottom:
			coords = (padCorner[0], padCorner[1], 1, 0, midy-1, midx-1)
			#pad.refresh(padCorner[0], padCorner[1], 1, 0, midy-1, midx-1)
		else:
			coords = (padCorner[0], padCorner[1], midy+1, 0, winY-1, winX-1)
		pad.refresh(*coords)
		addPad_Coordinates(padNum, coords, bottom)
		
	except :
		gl.error['bottom ='] = bottom
		gl.error['args on 0'] = (padCorner[0], padCorner[1], 0, 0, midy-1, midx-1)
		gl.error['args on 1'] = (padCorner[0], padCorner[1], midy-1, midx, winY-1, winX-1)
		raise
	#pad.refresh(padRowNum, padColNum, windowYcoord, windowXcoord, windowY_ENDcoor, windowX_ENDcoor)
	#pad.refresh(0, 0, 0, 0, 23, 79)
	#pad.refresh(0, 0, y, 0, winY - 1, winX-1)
	gl.scrn.refresh()
	
def movePad(padNum, lines=1, columns=0):
	'''
	window.scroll([lines=1])
	  Scroll the screen or scrolling region upward by lines lines.
    window.hline([y, x], ch, n)
	  Display a horizontal line starting at (y, x) with length n consisting of the character ch.
'''
	padDict = gl.padsList[padNum]
	pad = padDict['pad']
	coor = padDict['coor']
	bottom = padDict['bottom']
	#padCorner = coor[:2]
	newY = coor[0] + lines
	if newY < 0:
		newY = 0
	newX = coor[1] + columns
	if newX < 0:
		newX = 0
	displayPad(padNum, bottom, padCorner = (newY, newX))
	#pad.scroll()
	pass
	
#keyboardActions = {
					#'o':switchWindow, 
					#'u':moveUp, 'd':moveDown,
					#'l':moveRight, 'r':moveLeft, 
					#'v':viewNext, 
					#'q':quit, 
				  #}
	
def checkUserInput():
	c = gl.scrn.getch()
	c = chr(c)
	if c == 'q': raise
	
def main():
	try:
		initScreen()
		size =  (grabCurrScreenSize(), grabCurrScreenSize())
		initializeTesting()
		gl.scrn.getch()
		#testGame()
		#restoreScreen()
	except Exception as err:
		print type(err)
		print err.args
		print err
		
		raise
	finally :
		restoreScreen()
		print size
		print gl.error
		#raise
	
def initializeTesting():
	pages = indexer.preparePdfPages(indexer.test.testPdfFile)
	gl.pagesList = pages
	displayNewPad(pages[0])
	displayNewPad(pages[1], 1)
	for i in range(3):
	#while True:
		checkUserInput()
		movePad(0, 1, i)
		movePad(1, 1, i)
	
	
#print __name__
if __name__ == '__main__':
	
	main()
	
	
	
	
	
	
	
	
	
	
	
	