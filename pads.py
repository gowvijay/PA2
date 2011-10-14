

  
#help on pads: 			http://docs.python.org/library/curses.html#curses.newpad
#curses programming: 	http://docs.python.org/howto/curses.html#windows-and-pads
# Example:
#pad = curses.newpad(100, 100)
##  These loops fill the pad with letters; this is
## explained in the next section
#for y in range(0, 100):
    #for x in range(0, 100):
        #try: pad.addch(y,x, ord('a') + (x*x+y*y) % 26 )
        #except curses.error: pass
##  Displays a section of the pad in the middle of the screen
#pad.refresh( 0,0, 5,5, 20,75)



class globals:
	pass
 
 
class pad:
  
	def __init__(self, pageLines=[]):
		self.rowsTotal = len(pageLines)
		self.colsTotal = max(map(len, pageLines))
		self.curRow = 0
		self.curCol = 0
		
	