from PyQt4 import QtGui, QtCore
from WolfWriterTextEdit import *
# import WolfWriterTextEdit

class WWEncyMainPage(QtGui.QWidget):
	def __init__(self,encyclopedia,parent,parent_panel=None):
		QtGui.QWidget.__init__(self,parent=parent)
		self.encyclopedia=encyclopedia
		self.parent_panel=parent_panel

		self.search_line = QtGui.QLineEdit ()
		find_button = QtGui.QPushButton("&Find")
		self.listWidget=QtGui.QListWidget()
		
		main_layout=QtGui.QFormLayout()
		main_layout.addRow(self.search_line,find_button)
		main_layout.addRow(self.listWidget)
		
		self.connect(find_button, QtCore.SIGNAL("clicked()"), self.SLOT_search)
		self.connect(self.search_line, QtCore.SIGNAL('returnPressed  ()'), self.SLOT_search)
		self.connect(self.listWidget,QtCore.SIGNAL('itemActivated ( QListWidgetItem *  )'), self.SLOT_activated)
		# self.connect(self.listWidget,QtCore.SIGNAL('itemDoubleClicked ( QListWidgetItem * item ) '), self.SLOT_activated)
		
		self.setLayout(main_layout)
		self.SLOT_search()
	
	################## SLOTS #######################	
	def SLOT_search(self):
		name=unicode(self.search_line.text())
		if name.strip()==u"":
			self.list_entries=self.encyclopedia.list_entry
		else:
			print "cououc"
			self.list_entries=self.encyclopedia.searchEntriesWithName(name)
			print "self.list_entries  :  ",self.list_entries
		self.listWidget.clear()
		self.list_names_entry=[]
		for entry in self.list_entries:
			res=entry.get_name_with_other_names()
			self.list_names_entry.append(res)
		for name in self.list_names_entry:
			self.listWidget.addItem(name)
	
	def SLOT_activated(self,item):
		index=self.list_names_entry.index(unicode(item.text()))
		entry=self.list_entries[index]
		self.parent().addPage(WWEncyPage(entry=entry,parent=self.parent(),parent_panel=self.parent_panel))
		
	################################################
	
class WWEncyPage(QtGui.QWidget):
	def __init__(self,entry,parent=None,parent_panel=None):
		QtGui.QWidget.__init__(self,parent=parent)	
		self.entry=entry
		self.parent_panel=parent_panel
		self.start()
		
	def start(self):
		self.name_choose = QtGui.QLineEdit ()
		self.name_choose.setText (self.entry.name)
		
		self.type_choose	= QtGui.QLineEdit ()
		self.type_choose.setText (self.entry.type)
		
		self.other_names_choose	= QtGui.QLineEdit ()
		other_names_str=""
		for n in self.entry.other_names:
			other_names_str+=n+' '
		self.other_names_choose.setText (other_names_str)
		
		self.is_proper_name = QtGui.QCheckBox()
		if self.entry.properName:
			self.is_proper_name.setCheckState (QtCore.Qt.Checked)
		# (self, parent=None,book=None,main_window=None):
		self.desc_choose	= WWTextEdit (book=self.parent_panel.encyclopedia.book,main_window=self.parent_panel.main_window)
		self.desc_choose.setText(self.entry.desc)
		
		layout_info=QtGui.QFormLayout()
		layout_info.addRow("&Name : ",self.name_choose)
		layout_info.addRow("&Other Names : ",self.other_names_choose)
		layout_info.addRow("Proper Name : ",self.is_proper_name)
		layout_info.addRow("&Type : ",self.type_choose)
		layout_info.addRow("&Description : ",self.desc_choose)
		
		layout_button=QtGui.QHBoxLayout ()
		apply = QtGui.QPushButton("&Apply")
		cancel = QtGui.QPushButton("&Cancel")
		layout_button.addWidget(apply)
		layout_button.addWidget(cancel)
		
		layout_main=QtGui.QVBoxLayout ()
		layout_main.addLayout(layout_info)
		layout_main.addLayout(layout_button)
		
		self.setLayout(layout_main)

		
		self.connect(cancel, QtCore.SIGNAL("clicked()"), self.start)
		self.connect(apply, QtCore.SIGNAL("clicked()"), self.apply)
		print "COucou"

	def apply(self):
		self.entry.name=unicode(self.name_choose.text())
		self.entry.type=unicode(self.type_choose.text())
		self.entry.desc=unicode(self.desc_choose.toPlainText())
		self.entry.other_names=unicode(self.other_names_choose.text()).split()
		self.entry.properName=self.is_proper_name.isChecked()
		
		if self.parent_panel!=None:
			self.parent_panel.encyclopedia.fillingWordSet()
			self.parent_panel.main_window.textEdit.highlighter.reload_word_set()
			self.parent_panel.main_window.textEdit.highlighter.rehighlight()
		self.SLOT_emitChanged()
	
	def SLOT_emitChanged(self):
		self.emit(QtCore.SIGNAL("changed ()"))
				
	