#search() function searches a list of strings for a range of similar words. #All the strings are ended by a newline character. The values to be returned#are the rows and columns the words are located, along with the length of   the located word. Return them in a list of tuples,                          i.e [(2, 17, 5), (5, 9, 4)] 
import string 
def search(lines, toFind):

#toFind needs to be cleaned up. Find the first instance of a space, and cut the string off from there. Store in cleaned. i.e call/calls/called/calling
#individual words will be stored in targets. 
    output = []

   # cleaned = toFind[0:toFind.index(' ')]
    cleaned = toFind[0: find(toFind, ' ')]

    targets = [''] 
    index = 0
    for s in cleaned:
        if s.isalpha():
            targets[index].append(s)
        else:
            index = index + 1 

#Now we will search for each word, within each line. If it is found, we will store the list (row, column, length) within the list to be returned. 
    r = 0
    for l in lines:
        for t in targets:
            line = l      
            while not find(line ,t) == -1:
                col = find(l, t)
                row = r
                if not col == -1:
                    output.append((r, col, len(t)))
                l = l[col+len(t): len(l)]
            l = line 
        r = r + 1 

    return output 

#Test code below. 
a = ["hi, I am a robot.", "I can do many things other robots can't do", "For instance, no other robot can run as many programs as I can."]
b = ['robot  r ']

search (a, b)


                     
