"""
Part of the WolfWriter project. Written by Renaud Dessalles.
Contains a re-implementation of the QSyntaxHighlighter that will be used by 
WWTextEdit and WWSceneEdit. Its function for now, is to highlight the word that are 
an entry of the Encyclopedia.
In future it will also underline words for spelling correction.
"""

from PyQt4 import QtGui, QtCore

from WolfWriterCommon 	import *
from WolfWriterWord 	import *

class WWHighlighter (QtGui.QSyntaxHighlighter):
	def __init__(self,parent,book=None):
		QtGui.QSyntaxHighlighter.__init__(self,parent)
		self.format=QtGui.QTextCharFormat()
		self.format.setFontWeight(QtGui.QFont.Bold)
		self.format.setForeground(QtCore.Qt.darkMagenta)
		self.book=book
		self.reload_word_set()
	
	def reload_word_set(self):
		""" Reload all the words that are contained in the encyclopedia. """
		if self.book==None:
			self.word_set=WWWordSet([u'Marie',u'Pierre']) #just for the tests
		else:
			print "coucou1"
			self.word_set=self.book.encyclopedia.word_set
	
	def highlightBlock(self, text):
		""" The re-implmentation of highlightBlock, for every word of the *
		Encyclopedia, we change the format of every of its instance in the block."""
		for word in self.word_set.yieldSet():
			pattern = u"\\b"+word+u"\\b"

			expression=QtCore.QRegExp (pattern)
			# int index = text.indexOf(expression)
			index=text.indexOf(expression)
			while index>=0:
				self.setFormat(index,len(word),self.format)
				index = text.indexOf(word, index + len(word))
	
	
	
	
	
if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	class MainWindow ( QtGui.QMainWindow):
		def __init__(self, parent=None):
			QtGui.QMainWindow.__init__(self,parent)
			self.editor=QtGui.QTextEdit()
			self.setCentralWidget(self.editor)
	mainWindow = MainWindow()
	highlighter=WWHighlighter(mainWindow.editor.document())
	mainWindow.show()
			
	
	sys.exit(app.exec_())