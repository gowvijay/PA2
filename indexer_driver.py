#
import indexer
import gui 
import sys

class testGlobals:
	testWordFile = 'words_testFile.txt'
	testPdfFile = 'pdfTestFile.pdf'
	testIndexFile = 'testIndexFile.txt'
	debug = 1

test = testGlobals()
debug = test.debug
	

if __name__ == '__main__':
    try:
        pdf_file_name, index_file_name = sys.argv[1:3]
    except:
        pdf_file_name = test.testPdfFile
        index_file_name = test.testIndexFile
    try:
        word_file_name = sys.argv[3]
    except:
        word_file_name = ''
    if debug:
        print sys.argv
        print pdf_file_name, index_file_name, word_file_name
        raw_input(word_file_name)
    if word_file_name:
        textFile, index_file_name = indexer.buildIndex(pdf_file_name, index_file_name, word_file_name)
    else:
		textFile = indexer.pdfToText(pdf_file_name)
    gui.showGUI(textFile, index_file_name)
