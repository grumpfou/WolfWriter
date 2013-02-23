from WolfWriterBook import *
from WolfWriterEncyclopedia import *
from WolfWriterCommon import *
from WolfWriterEncyPage import *

import sys
import random
from PyQt4 import QtGui, QtCore


class WWTabWidget( QtGui.QTabWidget):
	def __init__(self,list_panels=None,*args,**kargs):
		QtGui.QTabWidget.__init__(self,*args,**kargs)
		self.list_panels=list_panels
		for panel in self.list_panels:
			self.addTab(panel,panel.name)
			self.connect(panel,QtCore.SIGNAL("changed()"),self.SLOT_emitChanged)

	def getPanelByType(self,type):
		list_res=[]
		for panel in self.list_panels:
			if isintance(panel,type):
				list_res.append(panel)
		return list_res
		
	def SLOT_emitChanged(self):
		self.emit(QtCore.SIGNAL("changed ()"))

class WWNameGeneratorPannel( QtGui.QWidget):
	def __init__(self,main_window=None,*args,**kargs):
		self.name=u"Name generator"
		QtGui.QWidget.__init__(self,*args,**kargs)
		self.main_window=main_window
		
		self.lenght_spinbox=QtGui.QSpinBox()
		self.lenght_spinbox.setRange(CONSTANTS.NAMEGEN_RANGE_LEN[0],CONSTANTS.NAMEGEN_RANGE_LEN[1])
		self.lenght_spinbox.setValue(CONSTANTS.NAMEGEN_DFT_LEN)
		
		self.number_spinbox=QtGui.QSpinBox()
		self.number_spinbox.setRange(CONSTANTS.NAMEGEN_RANGE_NUMBER[0],CONSTANTS.NAMEGEN_RANGE_NUMBER[1])
		self.number_spinbox.setValue(CONSTANTS.NAMEGEN_DFT_NUMBER)
		
		generate_button = QtGui.QPushButton("&Generate")
		generate_button.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"run.png")))
		self.connect(generate_button, QtCore.SIGNAL("clicked()"), self.SLOT_generate)
		
		self.listWidget=QtGui.QListWidget()
		
		
		main_layout=QtGui.QFormLayout()
		main_layout.addRow(u"Lenght of the Words",self.lenght_spinbox)
		main_layout.addRow(u"Number of the Words",self.number_spinbox)
		main_layout.addRow(generate_button)
		main_layout.addRow(self.listWidget)
		
		self. setLayout ( main_layout )
		
	
	def SLOT_generate(self):
		vowel=['a','e','i','o','u','ei','ai','y']
		consonant=['z','r','t','p','q','s','d','f','g','h','k','l','m','w','x','c','v','b','n','ch','th','gh']
		def name_generator(i=5):
			name=''
			begin=random.choice(range(2)) ## if begin==0, then it will ebgin with a vowel, else it will begin with a consonant
			for j in range(i):
				if j%2==begin:
					name=name+random.choice(vowel)
				else:
					name=name+random.choice(consonant)
			return name
		self.listWidget.clear()
		for n in range(int(self.number_spinbox.value())):
			name=name_generator(i=int(self.lenght_spinbox.value()))
			self.listWidget.addItem(name.capitalize())
		
class WWSearchPanel( QtGui.QWidget):
	def __init__(self,book,main_window=None,*args,**kargs):
		self.name=u"Search"
		QtGui.QWidget.__init__(self,*args,**kargs)
		self.book=book
		self.main_window=main_window
		
		# self.actionSearch=QtGui.QAction("Search",self)
		# self.actionSearch.setIcon(QtGui.QIcon(os.path.join(empl_icon,"find.png")))
		# self.connect(self.actionSearch, QtCore.SIGNAL('triggered  ()'), self.SLOT_actionSearch)
		

	
		
		self.search_line	= QtGui.QLineEdit ()
		
		self.casse_checkbox = QtGui.QCheckBox()
		self.regexp_checkbox = QtGui.QCheckBox()
		self.entireword_checkbox = QtGui.QCheckBox()
		
		self.listWidget=QtGui.QListWidget()
		find_button = QtGui.QPushButton("&Find")
		find_button.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"find.png")))
		
		
		main_layout=QtGui.QFormLayout()
		main_layout.addRow(self.search_line,find_button)
		main_layout.addRow(u"Casse sensitive",self.casse_checkbox)
		main_layout.addRow(u"Regular expression",self.regexp_checkbox)
		main_layout.addRow(u"Entire word",self.entireword_checkbox)
		main_layout.addRow(self.listWidget)
		
		self. setLayout ( main_layout )
		
		self.connect(find_button, QtCore.SIGNAL("clicked()"), self.SLOT_search)
		self.connect(self.search_line, QtCore.SIGNAL('returnPressed  ()'), self.SLOT_search)
		self.connect(self.listWidget,QtCore.SIGNAL('itemActivated ( QListWidgetItem *  )'), self.SLOT_activated)
		
		self.results_list=[]
	
	def SLOT_search(self):
		if self.main_window!=None:
			self.main_window.sceneEdit.uploadScene()
		pattern=unicode(self.search_line.text())
		if pattern==u"": return False
		regexp=self.regexp_checkbox.isChecked()
		casse=self.casse_checkbox.isChecked()
		entireword=self.entireword_checkbox.isChecked()
		self.results_list=list(self.book.structure.find(pattern,regexp=regexp,casse=casse,entireword=entireword))
		self.display_results_list()
		return True

	def SLOT_activated(self,item):
		if self.main_window==None:
			return False
		result=self.results_list[self.listWidget.row(item)]
		self.main_window.SLOT_objectActivated(result[2])
		cursor=QtGui.QTextCursor(self.main_window.sceneEdit.document())
		cursor.setPosition(result[0].start())
		cursor.setPosition(result[0].end(),QtGui.QTextCursor.KeepAnchor)
		
		self.main_window.sceneEdit.setTextCursor(cursor)
		self.main_window.sceneEdit.setFocus ()
		return True
	
	def display_results_list(self):
		self.listWidget.clear()
		for res in self.results_list:
			to_add=	u"..."+res[1]+u"... " + \
					u" Chapter : "+ res[3].title +\
					u" Scene : "+ res[2].title
			self.listWidget.addItem(to_add)
			
class WWEncyPanel (QtGui.QWidget):
	def __init__(self,encyclopedia,main_window=None,*args,**kargs):
		self.name=u"Ency Navigator"
		QtGui.QWidget.__init__(self,*args,**kargs)
		self.main_window=main_window
		
			
	
		self.actionPrevious=QtGui.QAction("&Previous Page",self)
		self.actionPrevious.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"back.png")))
		self.connect(self.actionPrevious, QtCore.SIGNAL('triggered  ()'), self.SLOT_actionPrevious)
		
		self.actionHome=QtGui.QAction("&Research Page",self)
		self.actionHome.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"gohome.png")))
		self.connect(self.actionHome, QtCore.SIGNAL('triggered  ()'), self.SLOT_actionHome)
		
		self.actionNext=QtGui.QAction("&Next Page",self)
		self.actionNext.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"forward.png")))
		self.connect(self.actionNext, QtCore.SIGNAL('triggered  ()'), self.SLOT_actionNext)
		
		self.actionNew=QtGui.QAction("&New Page",self)
		self.actionNew.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"edit_add.png")))
		self.connect(self.actionNew, QtCore.SIGNAL('triggered  ()'), self.SLOT_actionNew)
		
		self.actionDelete=QtGui.QAction("&Delete Page",self)
		self.actionDelete.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"edit_remove.png")))
		self.connect(self.actionDelete, QtCore.SIGNAL('triggered  ()'), self.SLOT_actionDelete)
		
		
		
		self.mainLayout=QtGui.QVBoxLayout()
		self.toolBar=QtGui.QToolBar("Navigator's Toolbar")
		self.toolBar.addAction(self.actionPrevious)
		self.toolBar.addAction(self.actionHome)
		self.toolBar.addAction(self.actionNext)
		self.toolBar.addAction(self.actionNew)
		self.toolBar.addAction(self.actionDelete)
		self.mainLayout.addWidget( self.toolBar )
		
		self.iterator=None
		self.startEncyclopedia(encyclopedia)
		self. 	setLayout ( self.mainLayout )
		
	
	def startEncyclopedia(self,new_encyclopedia):
		if self.iterator!=None: #If there was allready a widget
			# We remove the previous widget
			wid_to_remove=self.list_pages[self.iterator]
			wid_to_remove.close()
			# self.mainLayout.addWidget(self.list_pages[iterator])
			
		# We add the new WWEncyMainPage
		self.list_pages=[WWEncyMainPage(new_encyclopedia,parent=self,parent_panel=self)]
		self.encyclopedia=new_encyclopedia
		self.mainLayout.addWidget(self.list_pages[0])
		self.list_pages[0].show()
		self.iterator=0
		self.cheakButton()
	
	def previousPage(self,nb_times=1):
		if self.iterator-nb_times<0:
			return False
		
		return self.displayPage(self.iterator-nb_times)

	def nextPage(self,nb_times=1):
		if self.iterator+nb_times>=len(self.list_pages):
			return False
		return self.displayPage(self.iterator+nb_times)
	
	def displayPage(self,iterator=-1):
		iterator=iterator%len(self.list_pages)
		
		# We remove the previous widget
		wid_to_remove=self.list_pages[self.iterator]
		wid_to_remove.close()
		# We display the new page
		self.mainLayout.addWidget(self.list_pages[iterator])
		self.list_pages[iterator].show()
		self.iterator=iterator
		self.cheakButton()
	
	def cheakButton(self):
		if self.iterator==0:
			self.actionPrevious.setEnabled (False)
		else:
			self.actionPrevious.setEnabled (True)
			
		if self.iterator==len(self.list_pages)-1:
			self.actionNext.setEnabled (False)
		else:
			self.actionNext.setEnabled (True)
		
		if isinstance(self.list_pages[self.iterator],WWEncyPage):
			self.actionDelete.setEnabled (True)
		else:
			self.actionDelete.setEnabled (False)
		
		# self.show()
	
	def addPage(self,page):
		self.list_pages=self.list_pages[:self.iterator+1]
		self.list_pages.append(page)
		page.parent_panel=self
		self.connect(page,QtCore.SIGNAL("changed()"),self.SLOT_emitChanged)
		# self.iterator+=1
		self.displayPage()
	def addPageFromEntry(self,entry,*args,**kargs):
		page=WWEncyPage(entry,parent_panel=self,*args,**kargs)
		self.addPage(page)
	
	#################### SLOTS #####################
	def SLOT_actionPrevious(self):
		self.previousPage()
	def SLOT_actionHome(self):
		print 'goHome'
		tmp=WWEncyMainPage(self.encyclopedia,parent=self,parent_panel=self)
		print "tmp  :  ",tmp
		self.addPage(tmp)
		# self.addPage(WWEncyMainPage(self.encyclopedia,parent=self))
	def SLOT_actionNext(self):
		self.nextPage()
	
	def SLOT_actionNew(self,word=None):
		if word==None:word=u""
		res=QtGui.QInputDialog.getText(self, u"New entry", "New entrie's name :",text=word)
		if res[1]:
			entry=self.encyclopedia.addEntry(name=unicode(res[0]))
			page=WWEncyPage(entry,parent_panel=self)
			self.addPage(page)
		self.SLOT_emitChanged()
	def SLOT_actionDelete(self,word=None):
	# def removeEntryFromName_X(self,name,parent=None):
		if word!=None:	
			if not self.encyclopedia.word_set.isIn(word):
				return False
				
			list_possible_entries=self.encyclopedia.getEntriesWithName(word)
			if len(list_possible_entries)>1:
				dialog=QtGui.QInputDialog(parent=self)
				list_name=[l.get_name_with_other_names() for l in list_possible_entries]
				name_to_pop,res=dialog.getItem(parent,"Entry selection","Please chose the entry",list_name)
				if not res: return False
				entry=list_possible_entries[list_name.index(name_to_pop)]
			else:
				entry=list_possible_entries[0]
		else:
			assert isinstance(self.list_pages[self.iterator],WWEncyPage)
			entry=self.list_pages[self.iterator].entry
		
		mess=QtGui.QMessageBox()
		ans = mess.question(self, "Confirmation",										\
				u"Are you sure to remove the entry <"+entry.get_name_with_other_names()+"> from the Ency ?",  \
				QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		
		if ans == QtGui.QMessageBox.No:
			return False
		self.encyclopedia.removeEntry(entry)
		self.SLOT_emitChanged()
		return True
		
		
	def SLOT_emitChanged(self):
		self.emit(QtCore.SIGNAL("changed ()"))
		
	################################################

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	pp="C:/Users/Renaud/Documents/Programmation/Python/Writing_help/WolfWriter/Test/testa.zip"
	bk=WWBook(pp)
	encyNavigator=WWEncyPanel(encyclopedia=bk.encyclopedia)
	searchPanel=WWSearchPanel(bk)
	namegenPanel=WWNameGeneratorPannel(bk)
	tabWidget=WWTabWidget(list_panels=[encyNavigator,searchPanel,namegenPanel])
	tabWidget.show()
	sys.exit(app.exec_())
	# doc = XML.Document()
	# en.xml_output(doc,doc)
	
	# print (doc.toprettyxml()).encode('ascii','replace')		
	# print "##############################################"
	# print (doc.toPrettyWithText()).encode('ascii','replace')