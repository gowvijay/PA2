#
import indexer
import gui 
import sys


if __name__ == '__main__':
    debugFlag = 0
    pdf_file_name, index_file_name = sys.argv[1:3]
    try:
        word_file_name = sys.argv[3]
    except:
        word_file_name = ''
    if debugFlag:
        print sys.argv
        print pdf_file_name, index_file_name, word_file_name
    if word_file_name:
        textFile, index_file_name = indexer.buildIndex(pdf_file_name, index_file_name, word_file_name)
    else:
		textFile = indexer.pdfToText(pdf_file_name)
    gui.showGUI(textFile, index_file_name)
