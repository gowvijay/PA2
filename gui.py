

import indexer
import curses, sys, os
import pprint
pp = pprint.pprint

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
	
	topWin = None
	bottomWin = None
	
	topPad = None
	bottomPad = None
	
	pdfPadNum = None
	indexPadNum = None
	
	activeWin = None
	cursor = {}
	scrn = None
	row = 0
	col = 0
	
gb = gl = globals()

#wr = curses.wrapper.wrapper()
def initScreen():
	gl.scrn = curses.initscr()
	size = getSecondWindowCorner()
	gl.topWin = gl.scrn.subwin(size[0]-1, size[1]-1, 0+1,0)
	gl.bottomWin = gl.scrn.subwin(size[0]-1, size[1]-1, size[0]+1,0)
	curses.noecho()
	curses.cbreak()
	curses.start_color()
	gl.scrn.keypad(1)
	gb.scrn.clear()
	gl.scrn.refresh()
	gl.row = 0
	gl.column = 0
	
def initPdfAndIndex():
	'''http://docs.python.org/library/curses.html#curses.window.overlay
	window.overlay(destwin[, sminrow, smincol, dminrow, dmincol, dmaxrow, dmaxcol])
		Overlay the window on top of destwin. The windows need not be the same size, 
		only the overlapping region is copied. This copy is non-destructive, which 
		means that the current background character does not overwrite the old contents of destwin.
		To get fine-grained control over the copied region, the second form of overlay() 
		can be used. sminrow and smincol are the upper-left coordinates of the source window, 
		and the other variables mark a rectangle in the destination window.
	'''
	try:
		padDict = gl.padsList[0]
		pad = padDict['pad']
		padDict['scrollPadCoor'] = (0,0)
		gl.topPadNum = 0
		pad.overlay(gl.topWin)
		gl.topWin.move(0, 0)
		gl.topWin.cursyncup()
		gl.topWin.refresh()
		gl.activeWin = gl.topWin
		
		padDict = gl.padsList[1]
		pad = padDict['pad']
		padDict['scrollPadCoor'] = (0,0)
		dsize = pad.getmaxyx()
		dy, dx = dsize 
		ssize = gl.bottomWin.getmaxyx()
		sy, sx = ssize
		pad.overlay(gl.bottomWin, 0, 0, 0, 0, sy-1, min(dx-1, sx-1))
		'''window.hline([y, x], ch, n)
    Display a horizontal line starting at (y, x) with length n consisting of the character ch.'''
		
		#gl.scrn.hline('-', 5)
		
		gl.bottomPadNum = 1
		gl.bottomWin.refresh()
		#gl.topWin.overlay(pad)
		#gl.scrn.refresh()
	except:
		gl.error['initPdfAndIndex'] = dsize, ssize, (sy-1, dx-1)
		raise
		
def scrollPad(win='', lines=1, cols=0):
	'''
	http://docs.python.org/library/curses.html#curses.window.mvderwin
	'''
	try:
		if not win:
			win = gl.activeWin
		if win == gl.topWin:
			padnum = gl.topPadNum
		else:
			padnum = gl.bottomPadNum
		padDict = gl.padsList[padnum]
		pad = padDict['pad']
		coor = padDict['scrollPadCoor']
		newY, newX = coor
		newY, newX = max(newY+lines, 0), max(newX +cols, 0)
		padDict['scrollPadCoor'] = (newY, newX)
		dsize = pad.getmaxyx()
		dy, dx = dsize 
		ssize = win.getmaxyx()
		sy, sx = ssize
		gl.error['scrollPad1'] = newY, newX , (min(newY, dy-sy), min(newX, max(dx-sx, 0)), 0, 0, sy-1, min(dx-1, sx-1)), (dy-sy, dx-sx)
		win.clear()
		pad.overlay(win, min(newY, max(dy-sy, 0)), min(newX, max(dx-sx, 0)), 0, 0, min(sy-1, dy-1), min(dx-1, sx-1))
		win.refresh()
		return
	except:
		gl.error['scrollPad0'] = win, newY, newX, 0, 0, sy-1, dx-1
		raise
	#gl.padsList[0]['pad'].mvderwin(2, 3)
	#gl.topWin.mvderwin(2, 3)
	
def restoreScreen():
	curses.nocbreak()
	curses.echo()
	gl.scrn.keypad(0)
	curses.endwin()
	
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
	try:
		gl.padsList = [{} for j in pagesList]
		for padNum, page in enumerate(pagesList):
			pad, pageLines = createNewPad(page)
			fillInPad(pad, pageLines)
			addPadToPadList(pad, pageLines, padNum)
	except:
		gl.error['createNewPad'] = pad, padNum, page, pageLines
		gl.error['gl.padsList'] = gl.padsList
		raise
	  
padsKeys = ['pad', 'pageLines', 'coor', 'cursorPos', 'bottom' ]
		
def addPadToPadList(pad, pageLines, padNum=-1):
	tempPad = {'pad': pad, 'pageLines': pageLines, 'cursorPos':(0,0)}
	#gl.error['addPad, tempPad'] = tempPad
	#pad.move(0,0)
	#pad.syncok(1)
	if padNum == -1:
		padNum = len(gl.padsList)
		gl.padsList.append({})
		#return padNum
	gl.padsList[padNum].update(tempPad.items())
	##gl.error['addPad, gl.padsList'] = gl.padsList
	
		#gl.padsList[padNum]['pageLines'] = pageLines
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
  
def mouse_getPos(win=''):
	#padDict = gl.padsList[padNum]
	#pad = padDict['pad']
	if not win:
		win = gl.activeWin
	return win.getyx()
	
def mouse_movePos(win = '', lines=1, columns=0):
	try:
		if not win:
			win = gl.activeWin
		
		#coor = mouse_getPos(win)
		#coor = 0,0
		if win == gl.topWin:
			padNum = gl.topPadNum
		else:
			padNum = gl.bottomPadNum
			
		padDict = gl.padsList[padNum]
		try:
			coor = padDict['cursorPos']
		except:
			coor = (0,0)
		
		pad = padDict['pad']
		sy, sx = pad.getmaxyx()
		dy, dx = win.getmaxyx()
		newY = min( max(coor[0] + lines, 0), dy-1, sy-1 )
		newX = min( max(coor[1] + columns, 0), dx-1, sx-1 )
		padDict['cursorPos'] = (newY, newX)
		win.move(newY, newX)
		#win.move(5,5)
		win.cursyncup()
		gl.scrn.refresh()
		gl.error['move cursor1'] = (lines, columns, newY, newX, coor, (sy, sx ), (dy, dx) )
	except:
		gl.error['move cursor0'] = (lines, columns, newY, newX, coor)
		raise

def switchWindow():
	if gl.activeWin == gl.topWin:
		gl.activeWin = gl.bottomWin
	else:
		gl.activeWin = gl.topWin
	gl.activeWin.refresh()
	
def moveUp():
	try:
		mouse_movePos(lines=-1)
	except:
		scrollPad(lines=-1)
		
def moveDown():
	try:
		mouse_movePos(lines=1)
	except:
		scrollPad(lines=1)
		
def moveRight():
	try:
		mouse_movePos(lines=0, cols=-1)
	except:
		scrollPad(lines=0, cols=-1)
		
def moveLeft():
	try:
		mouse_movePos(lines=0, cols=1)
	except:
		scrollPad(lines=0, cols=1)
		
def viewNext():
	
	pass
  
def quit():
	restoreScreen()
	raise
		
keyboardActions = {
					'o':switchWindow, 
					'u':moveUp, 'd':moveDown,
					'r':moveRight, 'l':moveLeft, 
					'v':viewNext, 
					'q':quit, 
				  }

	
def checkUserInput():
	c = gl.scrn.getch()
	c = chr(c)
	if c == 'q': raise
	try:
		keyboardActions[c]()
	except:
		gl.error['checkUserInput'] = c
	
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
		#print size
		pp( gl.error )
		#raise
	
def initializeTesting():
	pages = indexer.preparePdfPages(indexer.test.testPdfFile)
	gl.pagesList = pages
	
	createNewPads(pages)
	initPdfAndIndex()
	#scrollPad()
	
	#displayNewPad(pages[0])
	#displayNewPad(pages[1], 1)
	for i in range(1000):
	##while True:
		checkUserInput()
		#scrollPad(lines = 5, cols=2)
		#switchWindow()
		#mouse_movePos(lines=10, columns=20)
	scrollPad(lines = -30, cols=-30)
		##movePad(0, 1, i**2)
		##movePad(1, 1, i**2)
		#mouse_movePos(0)
	#movePad(0, -100, -100)
	#movePad(1, -100, -100)
	#gl.scrn.vline('|', 24)
	gl.scrn.syncok(1)
	#gl.error['curses.setsyx(y, x)'] = curses.setsyx(5, 6)
	#gl.scrn.syncup()
	gl.error['curses.getsyx()'] = curses.getsyx()
	gl.error['gl.activeWin.getyx()'] = gl.activeWin.getyx()
	gl.error['gl.topWin.getyx()'] = gl.topWin.getyx()
	gl.error['gl.bottomWin.getyx()'] = gl.bottomWin.getyx()
	gl.error['window.getyx()'] = gl.scrn.getyx()
	gl.error['pad0.getyx()'] = gl.padsList[0]['pad'].getyx()
	gl.error['pad1.getyx()'] = gl.padsList[1]['pad'].getyx()
	gl.error['window.getyx()'] = gl.scrn.getyx()
	checkUserInput()
	
	
#print __name__
if __name__ == '__main__':
	
	main()
	
	
	
	
	
	
	
	
	
	
	
	