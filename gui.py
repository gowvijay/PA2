

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
	pagesList = []
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
	gb.scrn.clear()
	gl.scrn.refresh()
	gl.row = 0
	gl.column = 0
	
def restoreScreen():
	curses.nocbreak()
	curses.echo()
	curses.endwin()
	
def grabPages(textFile):
	gl.pagesList = indexer.preparePdfPages(textFile)
	return gl.pagesList
	
def grabCurrScreenSize():
	'''returns the height and width of the window'''
	#print 'asdfa'
	return gl.scrn.getmaxyx()
	pass
	  
def getSecondWindowCorner():
	'''Returns where the second window should be.
	the height of the main window / 2, and column 0.
	
	The first window should always be displayed at (0,0)
	'''
	height, col = grabCurrScreenSize()
	return height/2, col
	
	
def displayNewPad(page):
	pad, pageLines = createNewPad(page)
	fillInPad(pad, pageLines)
	displayPad(pad)
	
def createNewPad(page):
	pageLines = page.split(os.linesep)
	nlines = len(lines)
	ncols = max(map(len, lines))
	pad = curses.newpad(nlines, ncols)
	return pad, pageLines
	
def fillInPad(pad, pageLines):
	for j, line in enumerate(pageLines):
		pad.addstr(j, 0, line)
		
def displayPad(pad, bottom=False):
	y, x = 0, 0
	if bottom:
		y, x = getSecondWindowCorner()
	winY, winX = grabCurrScreenSize()
	pad.refresh(y, x, 0, 0, winY/2, winX)
	
	
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
		size =  grabCurrScreenSize()
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
		#raise
	
#print __name__
if __name__ == '__main__':
	main()
	
	
	
	
	
	
	
	
	
	
	
	