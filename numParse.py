#Function numParse takes in a string and the index of a numeric digit. 
#The return value is the whole number in the string, i.e with all the other digits that consecutively surround it. 

def numParse(line, index):
    #if the value pointed to by index is not a digit, then return -1. 
    if not line[index].isdigit():
        return -1 
    num = ''
    lowerBound = index
    upperBound = index
    #For the first half of the string ending with index
    h1 = line[0:index]
    for i in reversed(h1):
        if not i.isdigit():
            break 
        lowerBound = lowerBound - 1
    h2 = line[(index+1):len(line)] 
    for j in h2:
        if not j.isdigit():
            break
        upperBound = upperBound + 1
    num = int(line[lowerBound:(upperBound+1)])    
    return num
#Tests:
#Just change around the indices to test out!
#print  numParse('This number, 4938, is unordinary.', 7)
#print  numParse('Whole bunch of numbers: 2345, 98234902, 23940238, 33, 1 ', 54)
 
