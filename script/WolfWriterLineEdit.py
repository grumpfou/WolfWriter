"""
Part of the WolfWriter project. Written by Renaud Dessalles
Contain a reimplementation of QtGui.QLineEdit to allow the call the char table and
to have the language shorcuts.
"""

from PyQt4 import QtGui, QtCore
from WolfWriterCommon import *
from WolfWriterLanguages import *
from WolfWriterCharTable import *

class WWLineEdit(QtGui.QLineEdit):
	def __init__(self,language_name=None,*args,**kargs):
		QtGui.QLineEdit.__init__(self,*args,**kargs)
		self.actionLaunchCharWidgetTable=QtGui.QAction("&Special Characters",self)		
		self.actionLaunchCharWidgetTable.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"character-set.png")))
		self.connect(self.actionLaunchCharWidgetTable, QtCore.SIGNAL("triggered()"), self.SLOT_launchCharWidgetTable)
		
		
		if language_name==None:
			self.language=WWLanguageDico[CONSTANTS.DFT_WRITING_LANGUAGE]()
		else :
			if not WWLanguageDico.has_key(language_name):
				self.language=WWLanguageDico[CONSTANTS.DFT_WRITING_LANGUAGE]()
				raise WWError("Do not have the typography for the language "+language_name)
			else:
				self.language=WWLanguageDico[language_name]()
		dico=self.language.shortcuts_insert
		mapper = QtCore.QSignalMapper(self)
		for k in dico.keys():
			short=QtGui.QShortcut(QtGui.QKeySequence(*k),self)
			QtCore.QObject.connect(short,QtCore.SIGNAL("activated ()"), mapper, QtCore.SLOT("map()"))
			short.setContext(QtCore.Qt.WidgetShortcut)
			mapper.setMapping(short, dico[k])
		self.connect(mapper, QtCore.SIGNAL("mapped(const QString &)"), self.insert )

	def contextMenuEvent(self,event):
		menu=self.createStandardContextMenu ()
		menu.addAction(self.actionLaunchCharWidgetTable)
		menu.exec_(event.globalPos())
	

	def SLOT_launchCharWidgetTable(self):
		charWid=WWCharWidgetTable(linked_text_widget=self,parent=self,flags = QtCore.Qt.Tool)#, flag = QtCore.Qt.Dialog)
		rect=self.cursorRect()
		charWid.move(self.mapToGlobal (rect.bottomRight ()))
		charWid.show()
			
if __name__ == '__main__':			
	import sys
	app = QtGui.QApplication(sys.argv)
	
	lineEdit=WWLineEdit()
	layout=QtGui.QHBoxLayout()
	layout.addWidget(lineEdit)
	# app.connect(button, QtCore.SIGNAL("clicked()"), toto)
	# app.connect(button, QtCore.SIGNAL("clicked()"), textedit.action)
	wid=QtGui.QWidget()
	wid.setLayout(layout)
	wid.show()
	sys.exit(app.exec_())