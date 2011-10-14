'''
words would be a dictionary built as:
    {'word/variant/variant': [index1, ind2, ind3], ... }
variants will be a dictionary containing all words and variants as keys
and the keys to the corresponding key in words as values:
    {'variant': 'word/variant/variant', word: 'word/variant/variant',...}
'''
import pprint, string, os, subprocess, shlex
pp = pprint.pprint

class globals:
    words = {}
    variants = {}
    pdfPages = []
    specialChar = '\x0c'
    translationTable = string.maketrans(string.punctuation, ' '*32)
    unixCmd = 'pdftotext'  # Usage: pdftotext [options] <PDF-file> [<text-file>]
    pdfFname = '.libreoffice/3/user/gallery/pdfTestFile.pdf'
    txtFname = ''

    @classmethod
    def printGl(self):
        pp(self.words)

    def __str__(self):
        rows = []
        for key, value in self.words.items():
            indexes = ','.join([str(j) for j in value])
            rows.append( ' '.join([key, indexes]) )
        rows.sort()
        return '\n'.join(rows)
    
    
gl = globals()

def buildIndex(pdf_file_name, index_file_name, word_file_name):
	'''main workflow function for this module'''
	prepareWords(word_file_name)
	textFile = pdfToText(pdf_file_name)
	indexPDF(textFile)
	if not debug:
		writeIndexFile(index_file_name)
	return textFile, index_file_name

def prepareWords(word_file_name):
    with open(word_file_name) as f:
        for line in f.readlines():
            wordAndVar = line.strip()
            gl.words[wordAndVar] = []
            for variant in wordAndVar.split('/'):
                gl.variants[variant] = wordAndVar

def pdfToText(pdf_file_name):
    gl.pdfFname = pdf_file_name
    gl.txtFname = os.path.splitext( pdf_file_name )[0] + '.txt'
    try:
        commandString = ' '.join([gl.unixCmd, gl.pdfFname])
        commandList = shlex.split(commandString)
        subprocess.Popen(commandList)
        assert os.path.isfile(gl.txtFname)
    except:
        print "Couldn't covert the pdf to text"
        raise
    return gl.txtFname
    pass

def indexPDF(pdf_file_name):
    preparePdfPages(pdf_file_name)
    parseAndIndexContent()

def filterChars(c):
    return (c in string.ascii_letters and c not in string.punctuation or c in string.whitespace or c == gl.specialChar)
        
def preparePdfPages(pdf_file_name):
	with open(pdf_file_name) as f:
		pdfContent = f.read()
	pdfContent = pdfContent.lower()
	pdfContent = pdfContent.translate(gl.translationTable)    
	pdfContent = filter(filterChars, pdfContent)
	gl.pdfPages = pdfContent.split(gl.specialChar)[:-1]
	return gl.pdfPages


def parseAndIndexContent():
    for pageNum, page in enumerate(gl.pdfPages):
        for word in page.split():
            addWord(word, pageNum) 

def addWord(word, pageNum):
    key = ''
    if word not in gl.variants:
        gl.variants[word] = word
        gl.words[word] = [pageNum]
        key = word
    else:
        key = gl.variants[word]
        if pageNum not in gl.words[key]:
            gl.words[key].append(pageNum)

def writeIndexFile(index_file_name):
    with open(index_file_name, 'w') as f:
        f.write(str(gl))
    
class testGlobals:
	testWordFile = 'words_testFile.txt'
	testPdfFile = 'pdfTestFile.txt'
	debug = 1
	
test = testGlobals()
debug = test.debug
	
#print __name__
if __name__ == '__main__':
    prepareWords('words_testFile.txt')
    indexPDF('pdfTestFile.txt')
    pass
