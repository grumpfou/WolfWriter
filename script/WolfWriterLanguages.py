"""
Part of the WolfWriter project. Written by Renaud Dessalles
Contains the class that deal with the typograpgy.
The WWLanguageAbstract class is the model class of all the language class below.
It must not be used directly, only subclass should be used.

There is two ways of correcting the typography of the user :
- by cheaking during the editing : every time the cursor moves (a char is inserted or
a the user moves the cursor), the software is cheaking if the chars around the place 
leaved by the cursor are correct, and correct them if necessary. The method used to do
so is correct_between_chars.
- after a word is written : to correct the previous word etc. The method used to do
so is wordCorrection.
The class can also contain some pluggin usefull in the language :
- the shortcuts_insert dict allow to insert specific text after a shortcut
- the shortcuts_correction_plugins dict allow to do a more complex modification of the 
text.

When creating a new Language class, it must contain :
- the encoding
- the name of the language (in the language)
- possibly the shortcuts_insert (a dictionary where the key is a tuple containing 
the sequence os the shortcut and the value is the string to insert.
_ a __init__ method with :
	a dictionary shortcuts_correction_plugins dict : 
		key : shortcuts_correction_plugins 
		value : the name of the pluggin method
- a reimplementation of the correct_between_chars method
- a possibly reimplementation of the wordCorrection method
- the possibly method menthion in the values of the shortcuts_correction_plugins
"""
from PyQt4 import QtGui, QtCore
from WolfWriterCommon import  CONSTANTS
from WolfWriterWord import WWWordTools, WWWordDico
from WolfWriterLanguagesRules import *

class WWLanguageAbstract:
	name=u''
	encoding=''
	shortcuts_insert={}
	def __init__(self):
		### We are creating the autocorrection:
		self.dicoWords=WWWordDico(data_list=CONSTANTS.AUTO_CORRECTION)
		self.shortcuts_correction={	}
		self.rules=[]
		
	
	def correct_between_chars(self,cursor):
		last_char=self.lastChar(cursor)
		next_char=self.nextChar(cursor)
		for rule in self.rules:
			res=rule.correct(last_char,next_char,cursor)
			if res :
				return (rule,cursor.position())
		
		return False
		
	def lastChar(self,cursor,n=1):
		if cursor.atBlockStart():
			return u'\n'		
		else :
			cur_tmp=QtGui.QTextCursor(cursor)
			cur_tmp.clearSelection()
			for i in range(n-1):
				cur_tmp.movePosition(QtGui.QTextCursor.Left,QtGui.QTextCursor.MoveAnchor)
				if cur_tmp.atBlockStart():
					return '\n'		
			cur_tmp.movePosition (QtGui.QTextCursor.Left,QtGui.QTextCursor.KeepAnchor)
			return cur_tmp.selectedText ()

	def nextChar(self,cursor,n=1):
		if cursor.atBlockEnd():
			return u'\n'		
		else :
			cur_tmp=QtGui.QTextCursor(cursor)
			cur_tmp.clearSelection()
			for i in range(n-1):
				cur_tmp.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.MoveAnchor)
				if cur_tmp.atBlockEnd():
					return u'\n'				
			cur_tmp.movePosition (QtGui.QTextCursor.Right,QtGui.QTextCursor.KeepAnchor,n=n)
			return cur_tmp.selectedText ()
			
	def getWordUnderCursor(self,cursor,char_expection=None):
		if char_expection==None : char_expection=[]
		cur_start=QtGui.QTextCursor(cursor)
		cur_start.clearSelection()
		cur_end=QtGui.QTextCursor(cursor)
		cur_end.clearSelection()
		
		regexp=QtCore.QRegExp("\\b")
		
		cur_start=cur_start.document().find(regexp,cur_start,QtGui.QTextDocument.FindBackward)
		while self.lastChar( cur_start ) in char_expection:
			print 'klm'
			cur_start.movePosition(QtGui.QTextCursor.Left,QtGui.QTextCursor.MoveAnchor)
			cur_start=cur_start.document().find(regexp,cur_start,QtGui.QTextDocument.FindBackward)
		cur_end=cur_end.document().find(regexp,cur_end)
		# print "self.nextChar( cur_end )  :  ", unicode(self.nextChar( cur_end )).encode('ascii','replace')
		# print "self.lastChar( cur_end )  :  ", unicode(self.lastChar( cur_end )).encode('ascii','replace')
		while self.nextChar( cur_end ) in char_expection:
			print 'jkl'
			cur_end.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.MoveAnchor,n=2)
			cur_end=cur_end.document().find(regexp,cur_end)
		
		n=cur_end.position()-cur_start.position()
		cur_start.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.KeepAnchor,n=n)
		return cur_start.selectedText(),cur_start
		
	def cheak(self,qdoc):
		cursor=QTextCursor(qdoc)
		res=False
		res_tmp=self.correct_between_chars(cursor)
		res=res or res_tmp
		while cursor.movePosition(QtGui.QTextCursor.Right):
			res_tmp=self.correct_between_chars(cursor)
			res=res or res_tmp
		return res	

	def cheak_after_paste(self,cursor,nb_ite=-1):
		i=0
		res=False
		res_tmp=self.correct_between_chars(cursor)
		res=res or res_tmp		
		while cursor.movePosition(QtGui.QTextCursor.Right) and i!=nb_ite:
			res_tmp=self.correct_between_chars(cursor)
			res=res or res_tmp
			i+=1
		return res
	
	def afterWordWritten(self,cursor):
		cur_tmp=QtGui.QTextCursor(cursor)
		cur_tmp.clearSelection()
		if cur_tmp.movePosition (QtGui.QTextCursor.Left,QtGui.QTextCursor.MoveAnchor,1):
			# cur_tmp.select(QtGui.QTextCursor.WordUnderCursor)
			# word=cur_tmp.selectedText ()
			word,cur_tmp=self.getWordUnderCursor(cur_tmp)
			replace=False
			
			#We replace things due to the language : 'oe' as a elision for instance
			word_replace=self.wordCorrection(word)
			if word_replace:
				word=word_replace
				replace=True
				
			#We replace things due to the language user settings : 'gvt' --> 'government'
			word_replace=self.dicoWords.get(word)
			if word_replace:
				word=word_replace
				replace=True
				
			if replace:
				cur_tmp.insertText(word)

	def wordCorrection(self):
		raise False
		
	

	
class WWLanguageFrench (WWLanguageAbstract):
	encoding='utf-8'
	name=u'Fran\u00E7ais'
	shortcuts_insert={
			(QtCore.Qt.CTRL+QtCore.Qt.Key_7		,QtCore.Qt.SHIFT+QtCore.Qt.Key_A)	:u"\u00C0",
			(QtCore.Qt.CTRL+QtCore.Qt.Key_Comma	,QtCore.Qt.SHIFT+QtCore.Qt.Key_C)	:u"\u00C7",
			(QtCore.Qt.CTRL+QtCore.Qt.Key_4		,QtCore.Qt.SHIFT+QtCore.Qt.Key_E)	:u"\u00C9",
			(QtCore.Qt.CTRL+QtCore.Qt.Key_7		,QtCore.Qt.SHIFT+QtCore.Qt.Key_E)	:u"\u00C8"}
	
	
	def __init__(self):
		WWLanguageAbstract.__init__(self)
		self.shortcuts_correction_plugins={
			(QtCore.Qt.CTRL+QtCore.Qt.Key_D,)	: self.dialog_correction}
		self.rules=[	WWRuleFrench0001(language=self),
						WWRuleFrench0002(language=self),
						WWRuleFrench0003(language=self),
						WWRuleFrench0004(language=self),
						WWRuleFrench0005(language=self),
						WWRuleFrench0006(language=self),
						WWRuleFrench0007(language=self),
						WWRuleFrench0008(language=self),
						WWRuleFrench0009(language=self),
						WWRuleFrench0010(language=self),
						WWRuleFrench0011(language=self),
						WWRuleFrench0012(language=self),
						WWRuleFrench0013(language=self)]

	"""
	def correct_between_chars(self,cursor):
		last_char=self.lastChar(cursor)
		next_char=self.nextChar(cursor)
		res=False
		
		if last_char==u' ' and next_char in [u' ',u'\n']:
			cursor.deletePreviousChar()
			res=True
		elif last_char==u'\u00A0' and next_char in [u'\u00A0',' ']:
			cursor.deleteChar()
		
		elif last_char==u'\n' and next_char in [u' ',u'\n']:
			cursor.deleteChar()
			res=True
		elif next_char in [u';',u':',u'!',u'?',u'\u00BB']:
			if last_char==' ': 
				cursor.deletePreviousChar()
				cursor.insertText(u'\u00A0')
				res=True
			elif last_char!=u'\u00A0': 
				cursor.insertText(u'\u00A0')
				res=True
		elif last_char==u'\u00AB':
			if next_char==' ': 
				cursor.deleteChar()
				cursor.insertText(u'\u00A0')
			elif next_char!=u'\u00A0':
				cursor.insertText(u'\u00A0')
			
		elif last_char==u'\u00A0' and (next_char not in [u';',u':',u'!',u'?',u'\u00BB']): 
			last_last_char=self.lastChar(cursor,n=2)
			if last_last_char!=u'\u00AB': # we cheak it caused by an oppening "guillemet"
				cursor.deletePreviousChar()
				cursor.insertText(u' ')
				res=True
		
		elif last_char in [u' ', u'\u00A0'] and next_char in [u'.',u',']:
			cursor.deletePreviousChar()
			res=True
		
		elif last_char in [u';',u':'] and (next_char not in [u'\n',u' ']):
			if next_char== u'\u00A0':
				cursor.deleteChar()
				res=True
		elif last_char==u"'":
			cursor.deletePreviousChar()
			cursor.insertText(u'\u2019')

		elif next_char==u'"':
			if last_char in [u' ',u'\n',u'\u00A0']:
				cursor.deleteChar()
				cursor.insertText(u'\u00AB\u00A0')
			else :
				cursor.deleteChar()
				cursor.insertText(u'\u00A0\u00BB')
			res=True
			
			
		elif last_char==u'"':
			if next_char==u' ':
				cursor.deletePreviousChar()
				cursor.insertText(u'\u00A0\u00BB')
			else :
				cursor.deletePreviousChar()
				cursor.insertText(u'\u00AB\u00A0')
			res=True
		
		elif last_char==u'.' and next_char==u'.':
			
			if self.lastChar(cursor,n=2)==u'.':
				cursor.deleteChar()
				cursor.deletePreviousChar()
				cursor.deletePreviousChar()
				cursor.insertText(u'\u2026')
				res=True
				
		elif last_char==u'\u2014' and next_char!=u'\u00A0':
			if next_char==' ': 
				cursor.deleteChar()
				cursor.insertText(u'\u00A0')
				res=True
			elif next_char!=u'\u00A0': 
				cursor.insertText(u'\u00A0')
				res=True
		return res

		"""
	def wordCorrection(self,word):
		word=unicode(word)
		id=WWWordTools.whatID(word)
		word=word.lower()
		if word=='--':
			return u"\u2014"
		if word.find(u'oe')!=-1:
			word=word.replace(u'oe',u'\u0153')
			word=WWWordTools.toID(word,id)
			return word
		
		else:
			return False

	def dialog_correction(self,cursor):
		for block in cursor.yieldBlockInSelection():
			cur_tmp=QtGui.QTextCursor(block)
			next_char=self.nextChar(cur_tmp)
			if next_char==u'\u2014':
				cur_tmp.deleteChar()
			else:
				cur_tmp.insertText(u'\u2014')
			self.correct_between_chars(cur_tmp)
			
	
			
	
Language=WWLanguageFrench()