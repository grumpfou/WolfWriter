"""
Part of the WolfWriter project. Written by Renaud Dessalles
Contains a reimplementation of the QTextEdit that respect the typography of Language
- WWTextEdit is a basic wrtier that repect the typology.
	- __init__ is charging the shortcuts of the Language (contained in 
		afterWordWritten and shortcuts_correction_plugins dict of Language)
	- the SLOT_cursorPositionChanged calls the Language's correct_between_chars method
		to correct what has been just written, and afterWordWritten method if a word
		had just been written.
	- the contextMenuEvent has been rewritten in order to allow to add or remove a 
		word in the encyclopedia of the book.
	- the mouseDoubleClickEvent has been rewritten in order to allow to acces to an
		entry of the encyclopedia of the book.
	- insertFromMimeData method cheak the typography of what has been paste

- WWSceneEdit is WWTextEdit sub-class that is more specific on modifying a scene:
	- uploadScene method allow to put the text of the widget in the WWScene's text.
	- setScene method is oppening the scene in the widget (and correct the typography)
"""

from PyQt4 import QtGui, QtCore

import sys
import string

from WolfWriterCommon 			import *
from WolfWriterLanguages 		import *
from WolfWriterReadConfigFile 	import *
from WolfWriterHighlighter 		import *
from WolfWriterCharTable 		import *
from WolfWriterError 			import *


	


class WWTextEdit(QtGui.QTextEdit):
	def __init__(self, parent=None,book=None,main_window=None):
		"""
		- parent : the parent widget
		- main_window : the WWMainWindow above (to deal with its status bar)
		- book : the given WWBook
		Note : for testing reasons, this class should work even if the book and the 
		main_window	is not specified.
		"""
		QtGui.QTextEdit.__init__(self,parent)
		self.book=book
		self.main_window=main_window
		# self.font_size=CONSTANTS.TEXT_FONT_SIZE
		# self.indent=CONSTANTS.TEXT_INDENT
		self.setTabChangesFocus (True)
		
		
		QtCore.QObject.connect(self,QtCore.SIGNAL("cursorPositionChanged()"),self.SLOT_cursorPositionChanged)
		
		self.old_cursor_position=self.textCursor().position() #we will remember the old position of the cursor in order to make typography corrections when it will move
		
		if book!=None:
			self.changeLanguage(book.structure.language)
		else : self.changeLanguage(None)
		# create the highlighter if necessary
		print "CONSTANTS.WITH_HIGHLIGHTER  :  ",CONSTANTS.WITH_HIGHLIGHTER
		if CONSTANTS.WITH_HIGHLIGHTER:
			self.highlighter=WWHighlighter(self.document(),book=book)
		
		
		# Creating the action actionLaunchCharWidgetTable (it will display the char
		# table).
		self.actionLaunchCharWidgetTable=QtGui.QAction("&Special Characters",self)
		self.actionLaunchCharWidgetTable.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"character-set.png")))
		self.connect(self.actionLaunchCharWidgetTable, QtCore.SIGNAL("triggered()"), self.SLOT_launchCharWidgetTable)
		
		shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Z"), self)
		self.connect(shortcut, QtCore.SIGNAL("activated()"), self.undo)
		
		
		
	def setText(self,text=None,book=None):
		"""This method will set the text contained in text (when changing the active scene for instance.
		- text : the text to insert (if None then it will insert u"")
		- book : the book of the scene, if it is None, we keep the previous one
		"""
		if book==None: book=self.book
		if text==None: text=""
		# We change the language if necessary
		if book!=None :
			if self.language.name!=book.structure.language:
				self.changeLanguage(book.structure.language)
		
		# Creating the new document and inserting the text in it
		document=QtGui.QTextDocument(self)
		cursor=QtGui.QTextCursor(document)
		cursor.insertText(text)
		cursor.setPosition(0)
		
		# Recheck the document typography if necessary
		if CONSTANTS.RECHECK_TEXT_OPEN:
			self.language.cheak_after_paste(cursor)
		
		# Adding the document to as document of the WWTextEdit
		self.blockSignals (True)
		if CONSTANTS.WITH_HIGHLIGHTER:
			newHighlight=WWHighlighter(document,book=book)
		self.setDocument(document)
		
		if CONSTANTS.WITH_HIGHLIGHTER:
			self.highlighter=newHighlight
		# if CONSTANTS.WITH_HIGHLIGHTER:
			# self.highlighter.book=book
			# self.highlighter.reload_word_set()
			# self.highlighter.setDocument(self.document())
		# if CONSTANTS.WITH_HIGHLIGHTER:
			# self.highlighter.rehighlight()
		self.document().clearUndoRedoStacks() # It will empty the history (no "undo" before)
		
		self.blockSignals (False)
		self.setTextCursor(cursor)	

		self.book=book
	
	############################## SLOTS #################################
			
	def SLOT_cursorPositionChanged(self):
		"""Method that is called when the cursor position has just changed."""
		self.blockSignals (True) #allow the method to move the cursor in the method 
									# without calling itself one again.
		
		if self.old_cursor_position>=self.document().characterCount():
			# If we were at the end of the document and suppress the end, it does 
			# then nothing.
			self.old_cursor_position=self.textCursor().position()
			self.blockSignals (False)
			return self.old_cursor_position
		
		if CONSTANTS.DO_TYPOGRAPHY:
			# We check the typography at the site we just left
			cursor=QtGui.QTextCursor(self.document())
			cursor.clearSelection()
			cursor.setPosition(self.old_cursor_position)
			res=self.language.correct_between_chars(cursor)
			if res and self.main_window!=None:
				self.main_window.changeMessageStatusBar("Correction : "+res[0].title)
				
			
		if CONSTANTS.AUTO_CORRECTION:
			# If we have just written a word (by a space, or a ponctuation) it makes 
			# the auto-correction of the word.
			cursor=self.textCursor()
			last_char=self.language.lastChar(cursor)
			if last_char in [u' ',u'\u00A0',u'\n',u';',u':',u'!',u'?',u',',u'.',u"'",u'-']:
				self.language.afterWordWritten(cursor)
		
		self.blockSignals (False)
		self.old_cursor_position=self.textCursor().position() #update the cursor position
		return self.old_cursor_position
	
	
	def SLOT_pluggins(self,iterator):
		"""Launch the pluggin corresponding to the iterator"""
		function=self.dico_pluggins[iterator]
		function(cursor=self.textCursor())
		
	
	def contextMenuEvent(self,event):
		"""A re-implementation of the contextmenu, will add some actions
		- actionRemoveWordEncyclopedia : remove the word under cursor from the 
			encyclopedia.
		- actionAddWordEncyclopedia : add the word under cursor to the encyclopedia.
		- self.actionLaunchCharWidgetTable : launch the char table
		"""
		cursor = QtGui.QTextCursor(self.document())
		cursor = self.cursorForPosition(event.pos())
		self.setTextCursor(cursor)
		word,cur_tmp=self.language.getWordUnderCursor(cursor,char_exception=[u'-'])
		# cursor.select(QtGui.QTextCursor.WordUnderCursor)
		# word=cursor.selectedText ()
		def addWord():
			res=self.main_window.ency_panel.SLOT_actionNew(word)
			if res:
				self.highlighter.reload_word_set()
				self.highlighter.rehighlight()
		def removeWord():
			res= self.main_window.ency_panel.SLOT_actionDelete(word)
			if res:
				self.highlighter.reload_word_set()
				self.highlighter.rehighlight()
		
	
		menu=self.createStandardContextMenu()
		if self.book!=None and CONSTANTS.WITH_HIGHLIGHTER:
			if self.book.encyclopedia.word_set.isIn (word):
				actionRemoveWordEncyclopedia=QtGui.QAction("&Remove the word from Ency",self)
				self.connect(actionRemoveWordEncyclopedia, QtCore.SIGNAL("triggered()"), removeWord)
				menu.addAction(actionRemoveWordEncyclopedia)
			else:				
				actionAddWordEncyclopedia=QtGui.QAction("&Add the word to Ency",self)
				self.connect(actionAddWordEncyclopedia, QtCore.SIGNAL("triggered()"), addWord)
				menu.addAction(actionAddWordEncyclopedia)
				
				
				menu.addAction(self.actionLaunchCharWidgetTable)
			
		menu.exec_(event.globalPos())
		

	def mouseDoubleClickEvent(self,event):
		"""A re-implementation of the mouseDoubleClickEvent, if the word under cursor 
		is a possible entry in the encyclopedia, it will show it in the EncyPannel.
		"""
		if self.book!=None and self.parent()!=None:
			cursor = self.cursorForPosition(event.pos())
			self.setTextCursor(cursor)
			word,cur_tmp=self.language.getWordUnderCursor(cursor,char_exception=[u'-'])
			if self.book.encyclopedia.word_set.isIn (word):
				list_possible_entries=self.book.encyclopedia.getEntriesWithName(word)
				if len(list_possible_entries)>1:
					# If there is more than one possible entry, the user have to choose
					dialog=QtGui.QInputDialog()
					list_name=[e.get_name_with_other_names() for e in list_possible_entries]
					name_to_pop,res=dialog.getItem(self,"Entry selection","Please chose the entry",list_name)
					if not res:
						QtGui.QTextEdit.mouseDoubleClickEvent(self,event)
						return False
					select_entry=list_possible_entries[list_name.index(name_to_pop)]
				else:
					select_entry=list_possible_entries[0]
				
				if self.main_window!=None:
					self.main_window.ency_panel.addPageFromEntry(select_entry,self.main_window.ency_panel)
					self.main_window.tab_widget.setCurrentWidget(self.main_window.ency_panel)
				else: pass
				# self.highlighter.reload_word_set()
				# self.highlighter.rehighlight()
				# else :
					# QtGui.QTextEdit.mouseDoubleClickEvent(self,event)
			else:
				QtGui.QTextEdit.mouseDoubleClickEvent(self,event)
		
		
		
	def SLOT_launchCharWidgetTable(self):
		"""Slot that is called when we have to display the char table"""
		charWid=WWCharWidgetTable(linked_text_widget=self,parent=self,flags = QtCore.Qt.Tool)#, flag = QtCore.Qt.Dialog)
		rect=self.cursorRect()
		charWid.move(self.mapToGlobal (rect.bottomRight ()))
		charWid.show()
	
	def SLOT_recheckTypography(self):
		"""Quick method that check and correct all the typography of the text.
		TODO : some summuary window of all the corrections.
		"""
		cursor=self.textCursor()
		cursor.setPosition(0)
		self.language.cheak_after_paste(cursor)
		
	
	####################################################################
	

	def insertFromMimeData(self,source ):
		"""A re-implementation of insertFromMimeData. We have to check the typography 
		of what we have just paste.
		TODO : some summuary window of all the corrections.
		"""
		self.blockSignals (True)
		text=source.text()
		text.replace(QtCore.QString("\t"), QtCore.QString(" "))
		cursor=self.textCursor()
		cursor_pos=cursor.position()
		cursor.insertText(text)
		cursor.setPosition(cursor_pos)
		if CONSTANTS.DO_TYPOGRAPHY:
			self.language.cheak_after_paste(cursor,text.size()) 
		self.blockSignals (False)
	
	
	
	def afterCorrection(self,rule,pos):
		"""?????????????"""
		pass
		
	def changeLanguage(self,language_name=None):
		
		
		# fill self.language according to the language of the book
		if language_name==None:
			self.language=WWLanguageDico[CONSTANTS.DFT_WRITING_LANGUAGE]()
		else :
			if not WWLanguageDico.has_key(language_name):
				self.language=WWLanguageDico[CONSTANTS.DFT_WRITING_LANGUAGE]()
				raise WWError("Do not have the typography for the language "+self.book.structure.language)
			else:
				self.language=WWLanguageDico[language_name]()		
				
				
		# add the language insert shortcuts to the class 
		dico=self.language.shortcuts_insert
		mapper = QtCore.QSignalMapper(self)
		for k in dico.keys():
			short=QtGui.QShortcut(QtGui.QKeySequence(*k),self)
			QtCore.QObject.connect(short,QtCore.SIGNAL("activated ()"), mapper, QtCore.SLOT("map()"))
			short.setContext(QtCore.Qt.WidgetShortcut)
			mapper.setMapping(short, dico[k])
		self.connect(mapper, QtCore.SIGNAL("mapped(const QString &)"), self.insertPlainText )
		
		# add the language pluggins to the class 
		dico=self.language.shortcuts_correction_plugins
		self.dico_pluggins={}
		mapper = QtCore.QSignalMapper(self)
		for i,k in enumerate(dico.keys()):
			short=QtGui.QShortcut(QtGui.QKeySequence(*k),self)
			QtCore.QObject.connect(short,QtCore.SIGNAL("activated ()"), mapper, QtCore.SLOT("map()"))
			short.setContext(QtCore.Qt.WidgetShortcut)
			
			self.dico_pluggins[i]=dico[k]
			mapper.setMapping(short, i)		
		self.connect(mapper, QtCore.SIGNAL("mapped(int)"), self.SLOT_pluggins )
	
	def undo(self):
		"""
		This method do the usual undo, except in the case it has there has be a typography correction, in which
		case it comes back to the state before the events that trigger the correction:
		exemple:
		"Hello,<space>you!"       
			-----     suppress coma     ----->       "Hello<space>you!"
			-----     another space     ----->       "Hello<space><space>you!"       
			----- typography correction ----->       "Hello<space>you!"
			-----        Ctrl-Z         ----->       "Hello,<space>you!"
		
		"""
		print "undo"
		self.blockSignals (True)
		if CONSTANTS.DO_TYPOGRAPHY:
			i=1
			do_again=True
			while do_again and i<CONSTANTS.LIM_RECURSIV_UNDO:
				for j in range(i):
					QtGui.QTextEdit.undo(self)
				cursor=self.textCursor()
				cursor.clearSelection()
				do_again=self.language.correct_between_chars(cursor)
				i+=1
			self.blockSignals (False)
			self.old_cursor_position=self.textCursor().position() #update the cursor position
		else:
			QtGui.QTextEdit.undo(self)
		
	


	def keyPressEvent(self,event):
		"""
		This action grab the Undo KeySequence to execute the special function self.undo .
		"""
		if (event.matches(QtGui.QKeySequence.Undo)):
				self.undo()
		else:
			QtGui.QTextEdit.keyPressEvent(self,event)
       
		
class WWSceneEdit(WWTextEdit):
	def __init__(self,parent,scene=None,book=None,main_window=None):
		"""A re-implementation of WWTextEdit that will specifically dedicated to the 
		given scene. It will have specific font and font_size.
		"""
		WWTextEdit.__init__(self,parent=parent,main_window=main_window,book=book)
		# self.font_size=CONSTANTS.SCENE_FONT_SIZE
		# self.indent=CONSTANTS.SCENE_INDENT
		self.scene=None
		self.book=None
		self.setScene(scene,book)
		
		
	def setText(self,text=None,book=None):
		""" Reimplementation of setText to put the format of the Scene edit 
		(with justification, font size, font etc.)
		"""
		
		
		if book==None: book=self.book
		if text==None: text=""
			
		# Changing the language to the one of the book :
		if book!=None :
			if self.language.name!=book.structure.language:
				self.changeLanguage(book.structure.language)
		
		# Creating the new QTextDocument
		document=QtGui.QTextDocument(self)
		
		if CONSTANTS.JUSTIFY:
			document.setDefaultTextOption(QtGui.QTextOption(QtCore.Qt.AlignJustify))
		cursor=QtGui.QTextCursor(document)
		format_char=cursor.charFormat()
		format_block=cursor.blockFormat()
		format_char.setFont(QtGui.QFont(CONSTANTS.FONT,CONSTANTS.SCENE_FONT_SIZE))
		if CONSTANTS.SCENE_INDENT!=0:
			format_block.setTextIndent (CONSTANTS.SCENE_INDENT)
			format_block.setLineHeight (CONSTANTS.LINE_HEIGHT, QtGui.QTextBlockFormat.ProportionalHeight)
			
		# Putting the cursor at the good format
		cursor.setCharFormat(format_char)
		cursor.setBlockFormat(format_block)
		
		cursor.insertText(text)
		cursor.setPosition(0)
		
		# Recheck and correct if necessary the document
		if CONSTANTS.RECHECK_TEXT_OPEN:
			self.language.cheak_after_paste(cursor)
		
		# Put the document as the document of the class
		self.blockSignals (True)
		if CONSTANTS.WITH_HIGHLIGHTER:
			newHighlight=WWHighlighter(document,book=book)
		self.setDocument(document)
		
		if CONSTANTS.WITH_HIGHLIGHTER:
			self.highlighter=newHighlight
			
		self.document().clearUndoRedoStacks() # It will empty the history (no "undo" before)
		self.blockSignals (False)
		
		self.setTextCursor(cursor)	

		self.book=book	
	
	def uploadScene(self):
		"""Is called when it change the active scene, it uploads the WWScene class, making statistics etc."""
		if self.scene!=None:
			newText=unicode(self.toPlainText())

			self.scene.hasChanged=True
			
			self.scene.text=unicode(newText)
			self.scene.doStats()
			self.scene.parent.doStats()
			self.scene.parent.parent.doStats()
	
	def setScene(self,newscene,book=None):
		""" set a new scene in the widget"""
		self.uploadScene() #"saving" the old scene
		# self.emit(QtCore.SIGNAL("correction1 (  )"))
		# self.afterCorrection(0,0)
		
		self.scene=newscene
		
		# Inserting the text of the new scene
		if self.scene!=None:
			
			self.setText(self.scene.text,book=book)
		else:
			self.setText(book=book)
		
	def getEditActions(self,parent=None):
		""" Create and get all the edtion acction (copy/paste/...)"""
		actionCopy		= QtGui.QAction("Copy",self)
		actionCopy.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"editcopy.png")))
		actionCopy.setShortcuts(QtGui.QKeySequence.Copy)
		self.connect(actionCopy, QtCore.SIGNAL("triggered()"), self.copy)
		
		actionCut		= QtGui.QAction("Cut",self)
		actionCut.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"editcut.png")))
		actionCut.setShortcuts(QtGui.QKeySequence.Cut)
		self.connect(actionCut, QtCore.SIGNAL("triggered()"), self.cut)
		
		actionPaste		= QtGui.QAction("Paste",self)
		actionPaste.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"editpaste.png")))
		actionPaste.setShortcuts(QtGui.QKeySequence.Paste)
		self.connect(actionPaste, QtCore.SIGNAL("triggered()"), self.paste)
		
		actionUndo		= QtGui.QAction("Undo",self)
		actionUndo.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"editundo.png")))
		actionUndo.setShortcuts(QtGui.QKeySequence.Undo)
		self.connect(actionUndo, QtCore.SIGNAL("triggered()"), self.undo)
		
		actionRedo		= QtGui.QAction("Redo",self)
		actionRedo.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"editredo.png")))
		actionRedo.setShortcuts(QtGui.QKeySequence.Redo)
		self.connect(actionRedo, QtCore.SIGNAL("triggered()"), self.redo)
		
		
		return [actionCopy,actionCut,actionPaste,actionUndo,actionRedo]
		

		
if __name__ == '__main__':
	from WolfWriterBook import *
	from WolfWriterCharTable import *
	pp="C:\\Users\\Renaud\\Documents\\Programmation\\Python\\WolfWriter_Test\\TestPerso\\testa.zip"
	pp="C:\\Users\\Renaud\\Documents\\Programmation\\Python\\WolfWriter_Test\\BigBug\\book1.ww"
	

	
	
	bk=WWBook(zippath=pp)
	
	app = QtGui.QApplication(sys.argv)
	
	secenedit = WWSceneEdit(parent=None,scene=bk.structure.story.list_chapters[0].children[0],book=bk)
	textedit = WWTextEdit(parent=None,book=bk)
	textedit.setText(bk.structure.story.list_chapters[0].children[0].text)
	simpletextedit = QtGui.QTextEdit(parent=None)
	simpletextedit.setText(bk.structure.story.list_chapters[0].children[0].text)
	button= QtGui.QPushButton('ATGC')
	# button.setAction(textedit.action)
	
	
	# text_edit1=QtGui.QTextEdit()
	layout=QtGui.QHBoxLayout()
	layout.addWidget(secenedit)
	layout.addWidget(textedit)
	layout.addWidget(simpletextedit)
	layout.addWidget(button)
	

	def toto():
		# dialog=QtGui.QDialog(parent=textedit)
		# layout=QtGui.QVBoxLayout()
		# layout.addWidget(WWCharWidgetTable(linked_text_widget=textedit))
		# dialog.setLayout(layout)
		# # dialog.show()
		# charWid=WWCharWidgetTable(linked_text_widget=textedit,parent=textedit,flags = QtCore.Qt.Tool)#, flag = QtCore.Qt.Dialog)
		# rect=textedit.cursorRect()
		# rect1=textedit.geometry()
		# print "rect1.topLeft()  :  ",rect1.topLeft()
		# print "rect.bottomRight ()  :  ",rect.bottomRight ()
		# # charWid.exec_(textedit.mapToGlobal (rect.bottomRight ()))
		# charWid.move(textedit.mapToGlobal (rect.bottomRight ()))
		# charWid.show()
		tb=textedit.getToolBar(textedit)
		tb.show()
		
	app.connect(button, QtCore.SIGNAL("clicked()"), toto)
	# app.connect(button, QtCore.SIGNAL("clicked()"), textedit.action)
	wid=QtGui.QWidget()
	wid.setLayout(layout)
	main_window=QtGui.QMainWindow()
	main_window.setCentralWidget(wid)

	main_window.show()
	sys.exit(app.exec_())
	# sys.exit(textedit.exec_())