# -*- coding: utf-8 -*-

import sys
import string
from PyQt4 import QtGui, QtCore
from WolfWriterCommon import *
from WolfWriterLanguages import *
from WolfWriterReadConfigFile import *
from WolfWriterHighlighter import *
from WolfWriterCharTable import *
# from WolfWriterEncyPage import *

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



class WWTextEdit(QtGui.QTextEdit):
	def __init__(self, parent=None,book=None,main_window=None):
		QtGui.QTextEdit.__init__(self,parent)
		self.font_size=CONSTANTS.TEXT_FONT_SIZE
		self.indent=CONSTANTS.TEXT_INDENT
		self.setTabChangesFocus (True)
		
		
		QtCore.QObject.connect(self,QtCore.SIGNAL("cursorPositionChanged()"),self.SLOT_cursorPositionChanged)
		self.old_cursor_position=self.textCursor().position()
		self.book=book
		self.main_window=main_window
		if CONSTANTS.WITH_HIGHLIGHTER:
			self.highlighter=WWHighlighter(self.document(),book=book)
		
		dico=Language.shortcuts_insert
		mapper = QtCore.QSignalMapper(self)
		for k in dico.keys():
			short=QtGui.QShortcut(QtGui.QKeySequence(*k),self)
			QtCore.QObject.connect(short,QtCore.SIGNAL("activated ()"), mapper, QtCore.SLOT("map()"))
			short.setContext(QtCore.Qt.WidgetShortcut)
			mapper.setMapping(short, dico[k])
		self.connect(mapper, QtCore.SIGNAL("mapped(const QString &)"), self.insertPlainText )
		
		dico=Language.shortcuts_correction_plugins
		self.dico_pluggins={}
		mapper = QtCore.QSignalMapper(self)
		for i,k in enumerate(dico.keys()):
			short=QtGui.QShortcut(QtGui.QKeySequence(*k),self)
			QtCore.QObject.connect(short,QtCore.SIGNAL("activated ()"), mapper, QtCore.SLOT("map()"))
			short.setContext(QtCore.Qt.WidgetShortcut)
			
			self.dico_pluggins[i]=dico[k]
			mapper.setMapping(short, i)
		
		
		self.actionLaunchCharWidgetTable=QtGui.QAction("&Special Characters",self)
		
		self.actionLaunchCharWidgetTable.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"character-set.png")))
		self.connect(self.actionLaunchCharWidgetTable, QtCore.SIGNAL("triggered()"), self.SLOT_launchCharWidgetTable)
		self.connect(mapper, QtCore.SIGNAL("mapped(int)"), self.SLOT_pluggins )
		
		
		
	def setText(self,text=None,book=None):
		if book==None: book=self.book
		if text==None: text=""

		# if CONSTANTS.JUSTIFY:
			# document.setDefaultTextOption(QtGui.QTextOption(QtCore.Qt.AlignJustify))
		# format_char=cursor.charFormat()
		# format_block=cursor.blockFormat()
		# format_char.setFont(QtGui.QFont(CONSTANTS.FONT,self.font_size))
		# if self.indent!=0:
			# format_block.setTextIndent (self.indent)
			# format_block.setLineHeight (CONSTANTS.LINE_HEIGHT, QtGui.QTextBlockFormat.ProportionalHeight)
			
		
		# cursor.setCharFormat(format_char)
		# cursor.setBlockFormat(format_block)
		
		document=QtGui.QTextDocument(self)
		cursor=QtGui.QTextCursor(document)
		cursor.insertText(text)
		cursor.setPosition(0)
		
		if CONSTANTS.RECHECK_TEXT_OPEN:
			Language.cheak_after_paste(cursor)
		
		self.blockSignals (True)
		self.setDocument(document)
		self.blockSignals (False)
		if CONSTANTS.WITH_HIGHLIGHTER:
			self.highlighter=WWHighlighter(self.document(),book=book)
		self.setTextCursor(cursor)	

		self.book=book
	
	############################## SLOTS #################################
			
	def SLOT_cursorPositionChanged(self):
		self.blockSignals (True)
		
		if self.old_cursor_position>=self.document().characterCount(): #if we were at the end of the 
			self.old_cursor_position=self.textCursor().position()
			self.blockSignals (False)
			return self.old_cursor_position
		
		if CONSTANTS.DO_TYPOGRAPHY:
			cursor=QtGui.QTextCursor(self.document())
			cursor.clearSelection()
			cursor.setPosition(self.old_cursor_position)
			res=Language.correct_between_chars(cursor)
			if res and self.main_window!=None:
				self.main_window.changeMessageStatusBar("Correction : "+res[0].title)
			
		if CONSTANTS.AUTO_CORRECTION:
			cursor=self.textCursor()
			last_char=Language.lastChar(cursor)
			if last_char in [u' ',u'\u00A0',u'\n',u';',u':',u'!',u'?',u',',u'.',u"'",u'-']:
				Language.afterWordWritten(cursor)
		
		self.blockSignals (False)
		self.old_cursor_position=self.textCursor().position()
		return self.old_cursor_position
	
	
	def SLOT_pluggins(self,iterator):
		function=self.dico_pluggins[iterator]
		function(cursor=self.textCursor())
		
	
	def contextMenuEvent(self,event):
		cursor = QtGui.QTextCursor(self.document())
		cursor = self.cursorForPosition(event.pos())
		self.setTextCursor(cursor)
		word,cur_tmp=Language.getWordUnderCursor(cursor,char_expection=[u'-'])
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
		print "mouseDoubleClickEvent"
		print "self.book  :  ",self.book
		if self.book!=None and self.parent()!=None:
			print 'aa'
			cursor = QtGui.QTextCursor(self.document())
			cursor = self.cursorForPosition(event.pos())
			self.setTextCursor(cursor)
			word,cur_tmp=Language.getWordUnderCursor(cursor,char_expection=[u'-'])
			if self.book.encyclopedia.word_set.isIn (word):
				print 'isin'
				
				list_possible_entries=self.book.encyclopedia.getEntriesWithName(word)
				if len(list_possible_entries)>1:
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
				else: "WASA"
				# self.highlighter.reload_word_set()
				# self.highlighter.rehighlight()
				# else :
					# QtGui.QTextEdit.mouseDoubleClickEvent(self,event)
			else:
				QtGui.QTextEdit.mouseDoubleClickEvent(self,event)
		
		
		
	def SLOT_launchCharWidgetTable(self):
			charWid=WWCharWidgetTable(linked_text_widget=self,parent=self,flags = QtCore.Qt.Tool)#, flag = QtCore.Qt.Dialog)
			rect=self.cursorRect()
			charWid.move(self.mapToGlobal (rect.bottomRight ()))
			charWid.show()
		
	####################################################################
	

	def insertFromMimeData(self,source ):
		self.blockSignals (True)		
		text=source.text()
		cursor=self.textCursor()
		cursor_pos=cursor.position()
		cursor.insertText(text)
		cursor.setPosition(cursor_pos)
		Language.cheak_after_paste(cursor,text.size()) 
		self.blockSignals (False)
	
	def  	resizeEvent (self,event):
		QtGui.QTextEdit.resizeEvent(self,event)
		self.blockSignals (True)
		if CONSTANTS.WITH_HIGHLIGHTER:
			self.highlighter.rehighlight()
		self.blockSignals (False)
		
	
	def afterCorrection(self,rule,pos):
		pass
		
class WWSceneEdit(WWTextEdit):
	def __init__(self,parent,scene=None,book=None,main_window=None):
		WWTextEdit.__init__(self,parent=parent,main_window=main_window,book=book)
		# self.font_size=CONSTANTS.SCENE_FONT_SIZE
		# self.indent=CONSTANTS.SCENE_INDENT
		self.scene=None
		self.book=None
		self.setScene(scene,book)
		
		
	def setText(self,text=None,book=None):
		# Reimplementation of setText to put the format of the Scene edit
		if book==None: book=self.book
		if text==None: text=""

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
			
		
		cursor.setCharFormat(format_char)
		cursor.setBlockFormat(format_block)
		
		cursor.insertText(text)
		cursor.setPosition(0)
		
		if CONSTANTS.RECHECK_TEXT_OPEN:
			Language.cheak_after_paste(cursor)
		
		self.blockSignals (True)
		self.setDocument(document)
		self.blockSignals (False)
		if CONSTANTS.WITH_HIGHLIGHTER:
			self.highlighter=WWHighlighter(self.document(),book=book)
		self.setTextCursor(cursor)	

		self.book=book	
	
	def uploadScene(self):
		# Is called when it change the active scene, it uploads the WWScene class, making statistics etc.
		if self.scene!=None:
			newText=unicode(self.toPlainText())

			self.scene.hasChanged=True
			
			self.scene.text=unicode(newText)
			self.scene.doStats()
			self.scene.parent.doStats()
			self.scene.parent.parent.doStats()
	
	def setScene(self,newscene,book=None):
		#set a new scene in the widget
		self.uploadScene()
		# self.emit(QtCore.SIGNAL("correction1 (  )"))
		# self.afterCorrection(0,0)
		
		self.scene=newscene

		if self.scene!=None:
			self.setText(self.scene.text,book=book)
		else:
			self.setText(book=book)
	
	# def afterCorrection(self,rule,pos):
		# self.main_window.SLOT_messageStatusBar(rule.title)
		
	# def getToolBar(self,parent=None):
		# actionCopy		= QtGui.QAction("Copy",self)
		# actionCopy.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"editcopy.png")))
		# self.connect(actionCopy, QtCore.SIGNAL("triggered()"), self.copy)
		
		# actionCut		= QtGui.QAction("Cut",self)
		# actionCut.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"editcut.png")))
		# self.connect(actionCut, QtCore.SIGNAL("triggered()"), self.cut)
		
		# actionPaste		= QtGui.QAction("Paste",self)
		# actionPaste.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"editpaste.png")))
		# self.connect(actionPaste, QtCore.SIGNAL("triggered()"), self.paste)
		
		# actionUndo		= QtGui.QAction("Undo",self)
		# actionUndo.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"editundo.png")))
		# self.connect(actionUndo, QtCore.SIGNAL("triggered()"), self.undo)
		
		# actionRedo		= QtGui.QAction("Redo",self)
		# actionRedo.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"editredo.png")))
		# self.connect(actionRedo, QtCore.SIGNAL("triggered()"), self.redo)
		
				
		# toolBar=QtGui.QToolBar ("ToolBar",parent)
		# toolBar.addAction(actionCopy)
		# toolBar.addAction(actionCut)		
		# toolBar.addAction(actionPaste)		
		# toolBar.addAction(actionUndo)		
		# toolBar.addAction(actionRedo)		
		# toolBar.addAction(self.actionLaunchCharWidgetTable)
		# return toolBar
			
	def getEditActions(self,parent=None):
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
		
		# actionRedo		= QtGui.QAction("Redo",self)
		# actionRedo.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"editredo.png")))
		# actionRedo.setShortcuts(QtGui.QKeySequence.Redo)
		# self.connect(actionRedo, QtCore.SIGNAL("triggered()"), self.redo)
		
		return [actionCopy,actionCut,actionPaste,actionUndo,actionRedo]
				
		# toolBar=QtGui.QToolBar ("ToolBar",parent)
		# toolBar.addAction(actionCopy)
		# toolBar.addAction(actionCut)		
		# toolBar.addAction(actionPaste)		
		# toolBar.addAction(actionUndo)		
		# toolBar.addAction(actionRedo)		
		# toolBar.addAction(self.actionLaunchCharWidgetTable)
		# return toolBar
			
		

		
if __name__ == '__main__':
	from WolfWriterBook import *
	from WolfWriterCharTable import *
	pp="C:\\Users\\Renaud\\Documents\\Programmation\\Python\\WolfWriter_Test\\TestPerso\\testa.zip"
	
	
	bk=WWBook(archivepath=pp)
	
	app = QtGui.QApplication(sys.argv)
	
	textedit = WWSceneEdit(parent=None,scene=bk.structure.story.list_chapters[0].children[0],book=bk)
	button= QtGui.QPushButton('ATGC')
	# button.setAction(textedit.action)
	
	# text_edit1=QtGui.QTextEdit()
	layout=QtGui.QHBoxLayout()
	layout.addWidget(textedit)
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