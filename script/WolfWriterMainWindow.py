from PyQt4 import QtGui, QtCore

import os
import codecs
import subprocess
import sys

from WolfWriterTreeView import *
from WolfWriterTextEdit import *
from WolfWriterBook import *
from WolfWriterTabWidget import *
from WolfWriterCommon import *


"""
Part of the WolfWriter project. Written by Renaud Dessalles
Contains a reimplementation of the QMainWindow. It contains all the elements of the
graphical interface of the software.
the main window is divided in tree vertacal parts :
- the left layout shows the structure of the book as a tree. Mainly, it is a widget contained in
	the WolfWriterTreeView.py file.
- the center layout is concerning the scene which has been activated in the tree. It is mainly the
	widget WWSceneEdit in the WolfWritterTextEdit.py file
- the right layout is cvontaining all the help to the writting : the encyclopedia, a search engine,
	a name generator etc. It will be describe in the file WolfWriterTabWidget.py file.

The setup_ method of the WWMainWindow class are quite straightforward. They are called back to the 
initiation of the class.
Every action has its own slot and are discribed in the setup_actions method.
"""



class WWMainWindow(QtGui.QMainWindow):
	def __init__(self,book):
		QtGui.QMainWindow.__init__(self,parent=None)
		### Setups graphical objects ###
		self.setup_actions()
		self.book=book
		self.setup_menuBar()
		self.setup_mainLayout()
		
		self.setup_connections()
		
		self.reload_pannels()
		
		
		# self.sceneActive=None
		
	def setup_actions(self):
		# Action of openning a new book
		self.actionNewBook			= QtGui.QAction("&New book",self)
		self.actionNewBook.setShortcuts(QtGui.QKeySequence.New)
		
		# Action of openning a old book
		self.actionOpenBook			= QtGui.QAction("&Open book",self)
		self.actionOpenBook.setShortcuts(QtGui.QKeySequence.Open)
		
		# Action of saving the book as
		self.actionSaveAsBook		= QtGui.QAction("Save book &as",self)
		self.actionSaveAsBook.setShortcuts(QtGui.QKeySequence.SaveAs)
		
		# Action of saving the book 
		self.actionSaveBook			= QtGui.QAction("&Save book",self)
		self.actionSaveBook.setShortcuts(QtGui.QKeySequence.Save)
		
		# Action of saving an archive of the book.
		# an archive is a version of the book save into the main book file.
		# in further version of the software, it will allow to make some stats, reloading old version etc.
		# for now, it is not really usefull
		self.actionSaveArchive		= QtGui.QAction("&Save archive",self)

		# Action of exporting the book in another format (only .txt for now)
		self.actionExportBook		= QtGui.QAction("&Export book",self)
		# Action of Changing the metadata (author, title etc.)
		self.actionChangeMetadata	= QtGui.QAction("&Change metadata",self)

		# Action of adding a chapter to the structure
		self.actionAddChapter		= QtGui.QAction("&Add a new Chapter",self)
		# Action of deleting a chapter
		self.actionDeleteChapter    = QtGui.QAction("&Delete the active Chapter",self)
		# Action of adding a scene
		self.actionAddScene         = QtGui.QAction("&Add a new Scene",self)
		# Action of deleting a scene
		self.actionDeleteScene      = QtGui.QAction("&Delete the active Scene",self)
		
		# Action of charging anothter config file #!Not stable!#
		self.actionOpenConfig		= QtGui.QAction("&Open Config File",self)
		
		# Action of opening the scene with another software (mine is called antidote)
		self.actionSendToAntidote	= QtGui.QAction("&Send the Scene to antidote",self)
		
		
	def setup_connections(self):
		self.connect(self.actionNewBook			, QtCore.SIGNAL("triggered()"), self.SLOT_actionNewBook)
		self.connect(self.actionOpenBook		, QtCore.SIGNAL("triggered()"), self.SLOT_actionOpenBook)
		self.connect(self.treeView				, QtCore.SIGNAL("objectActivated( PyQt_PyObject )"),self.SLOT_objectActivated)
		self.connect(self.actionSaveAsBook		, QtCore.SIGNAL("triggered()"), self.SLOT_actionSaveAsBook)
		self.connect(self.actionSaveBook		, QtCore.SIGNAL("triggered()"), self.SLOT_actionSaveBook)
		self.connect(self.actionSaveArchive		, QtCore.SIGNAL("triggered()"), self.SLOT_actionSaveArchive)
		self.connect(self.actionExportBook		, QtCore.SIGNAL("triggered()"), self.SLOT_actionExportBook)
		self.connect(self.actionChangeMetadata	, QtCore.SIGNAL("triggered()"), self.SLOT_actionChangeMetadata)
		self.connect(self.lineEditScene			, QtCore.SIGNAL('returnPressed()'), self.SLOT_changeSceneTitle)
		self.connect(self.actionOpenConfig		, QtCore.SIGNAL('triggered()'), self.SLOT_actionOpenConfig)
		self.connect(self.actionAddChapter		, QtCore.SIGNAL('triggered()'), self.SLOT_actionAddChapter)
		self.connect(self.actionDeleteChapter	, QtCore.SIGNAL('triggered()'), self.SLOT_actionDeleteChapter)
		self.connect(self.actionAddScene		, QtCore.SIGNAL('triggered()'), self.SLOT_actionAddScene)
		self.connect(self.actionDeleteScene		, QtCore.SIGNAL('triggered()'), self.SLOT_actionDeleteScene)
		self.connect(self.actionSendToAntidote	, QtCore.SIGNAL('triggered()'), self.SLOT_actionSendToAntidote)
		
		self.connect(self.buttonPrevScene	, QtCore.SIGNAL('clicked()'), self.SLOT_buttonPrevScene)
		self.connect(self.buttonNextScene	, QtCore.SIGNAL('clicked()'), self.SLOT_buttonNextScene)
		
		
		self.connect(self.treeView,QtCore.SIGNAL('changed  ()'), self.SLOT_somethingChanged)
		self.connect(self.textEdit,QtCore.SIGNAL('textChanged ()'), self.SLOT_somethingChanged)
		self.connect(self.tab_widget,QtCore.SIGNAL('changed  ()'), self.SLOT_somethingChanged)

	def setup_mainLayout(self):
		def setup_leftLayout(widget):
			self.leftLayout=QtGui.QVBoxLayout(widget)
			self.treeView=WWTreeView(story=self.book.structure.story,parent=self)
			toolBar=self.treeView.getToolBar(self)
			self.leftLayout.addWidget( toolBar )
			self.leftLayout.addWidget( self.treeView )
			self.leftLayout.setSizeConstraint (QtGui.QLayout.SetMaximumSize)
			widget.setLayout ( self.leftLayout )
			# policy=QtGui.QSizePolicy (  )
			# policy.setHorizontalPolicy(QtGui.QSizePolicy.Fixed)
			# widget.setSizePolicy(policy)
		def setup_centerLayout(widget):
			self.centerLayout=QtGui.QVBoxLayout(widget)
			# self.lineEditChapter=QtGui.QLineEdit(self)
			self.lineEditScene=QtGui.QLineEdit(self)
			self.textEdit=WWSceneEdit(parent=self,main_window=self)
			
			bottom_widget=QtGui.QWidget()
			layout_bottom=QtGui.QHBoxLayout()
			self.buttonPrevScene = QtGui.QPushButton("&Previous Scene")
			self.buttonPrevScene.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"back.png")))
			self.buttonNextScene = QtGui.QPushButton("&Next Scene")
			self.buttonNextScene.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"forward.png")))
			layout_bottom.addWidget(self.buttonPrevScene)
			layout_bottom.addWidget(self.buttonNextScene)
			bottom_widget.setLayout(layout_bottom)
			
			# self.rightLayout.addWidget( self.lineEditChapter )
			self.centerLayout.addWidget( self.lineEditScene )
			self.centerLayout.addWidget( self.textEdit )
			self.centerLayout.addWidget( bottom_widget )
			widget.setLayout ( self.centerLayout )
			# policy=QtGui.QSizePolicy (  )
			# policy.setHorizontalPolicy(QtGui.QSizePolicy.Maximum)
			# widget.setSizePolicy(policy)
		def setup_rightLayout(widget):
			self.ency_panel=WWEncyPanel(encyclopedia=self.book.encyclopedia,main_window=self)
			self.search_panel=WWSearchPanel(self.book,main_window=self)
			self.name_generator_panel=WWNameGeneratorPannel(main_window=self)
			self.tab_widget=WWTabWidget(list_panels=[
								self.ency_panel,
								self.search_panel,
								self.name_generator_panel,
								]) #TODO when recharged book
			self.rightLayout=QtGui.QVBoxLayout(widget)
			self.rightLayout.addWidget( self.tab_widget )
			widget.setLayout ( self.rightLayout )
			
		
		
		self.splitter 	= QtGui.QSplitter(self)
		lWidget		= QtGui.QWidget(self)
		cWidget		= QtGui.QWidget(self)
		rWidget		= QtGui.QWidget(self)
		self.splitter.addWidget	(lWidget)
		self.splitter.addWidget	(cWidget)
		self.splitter.addWidget	(rWidget)
		setup_leftLayout		(lWidget)
		setup_centerLayout		(cWidget)
		setup_rightLayout		(rWidget)
		self.setCentralWidget (self.splitter)

		
		
		total=self.geometry().width() 
		self.splitter.setSizes ( [0.2*total,0.6*total,0.2*total] )
		

		
		
		
	def setup_menuBar(self):
		menuFile=self.menuBar().addMenu ( "File" )
		menuChapter=self.menuBar().addMenu ( "Chapter" )
		menuScene=self.menuBar().addMenu ( "Scene" )
		menuOptions=self.menuBar().addMenu ( "Options" )
		menuAbout=self.menuBar().addMenu ( "About" )
		def setup_book():
			menuFile.addAction(self.actionNewBook)
			menuFile.addAction(self.actionOpenBook)
			menuFile.addAction(self.actionSaveBook)
			self.actionSaveBook.setEnabled(False)
			menuFile.addAction(self.actionSaveAsBook)
			menuFile.addAction(self.actionSaveArchive)
			menuFile.addAction(self.actionExportBook)
			menuFile.addAction(self.actionChangeMetadata)
		def setup_chapter():
			menuChapter.addAction(self.actionAddChapter   )
			menuChapter.addAction(self.actionDeleteChapter)
			
		def setup_scene():
			menuScene.addAction(self.actionAddScene)
			menuScene.addAction(self.actionDeleteScene)
			menuScene.addAction(self.actionSendToAntidote)
		def setup_options():
			menuOptions.addAction(self.actionOpenConfig)
		def setup_about():	
			pass
	
		setup_book()
		setup_chapter()
		setup_scene()
		setup_options()
		
		
		
	################### SLOTS ###################
	
	
	
	def SLOT_actionNewBook(self): 
		if self.actionSaveBook.isEnabled ():# if the current book has unsaved changes
			res=self.doSaveDialog()
			
			if (res != QtGui.QMessageBox.Yes) and (res != QtGui.QMessageBox.No):
				return False
		
		self.book=WWBook(archivepath=abs_path_new_book) # we load the empty book file
		self.book.archivepath=None					# we put it's archivepath to None (allow the software to ask 
													# 							where to save at the first saving)
		self.setWindowTitle ( unicode("WolfWriter : ")+ self.book.structure.project_name)

		self.reload_pannels()
		return True
	
	
	def SLOT_actionOpenBook(self): 
		if self.actionSaveBook.isEnabled ():
			res=self.doSaveDialog()
			if (res != QtGui.QMessageBox.Yes) and (res != QtGui.QMessageBox.No):
				return False
		dialog= QtGui.QFileDialog(self)
		
		filename = dialog.	getOpenFileName(self,"Select a archive",self.get_default_opening_saving_site())
		if filename:
			filename=unicode(filename)
			self.book=WWBook(archivepath=filename)
			# self.treeView.setStory(self.book.structure.story)
			self.reload_pannels()
			return True
			
		return False
	
	def SLOT_actionSaveAsBook(self):
		dialog= QtGui.QFileDialog(self)
		filepath = dialog.getSaveFileName(self,"Select a archive where to save",self.get_default_opening_saving_site())
		if filepath:
			self.textEdit.uploadScene()
			filepath=unicode(filepath)
			self.book.save_book(filepath=filepath)
			self.book.archivepath=filepath
	
	def SLOT_actionSaveBook(self):
		if self.book.archivepath==None: #if the book has never been saved
			self.SLOT_actionSaveAsBook()
			
		else:
			self.textEdit.uploadScene()
			self.book.save_book()
			self.actionSaveBook.setEnabled(False)
			self.setWindowTitle ( unicode("WolfWriter : ")+ self.book.structure.project_name)
	
	def SLOT_actionSaveArchive(self):
		# An archive is put in the zip file under the directory containg the date in the format
		# YYYYMMDDHHMMSS. It allows the user to keep an old version of it's work.
		self.textEdit.uploadScene()
		self.book.save_archive()
	
		
	def SLOT_actionExportBook(self):
		# Slot that export the book under another format (for now only txt)
		dialog= QtGui.QFileDialog(self)
		filename = dialog.getSaveFileName(self,"Select a directory where to save",self.get_default_opening_saving_site()) #only txt for now
		if filename:
			self.textEdit.uploadScene()
			self.book.save_txt(filename)
				
		
	def SLOT_objectActivated(self,object):
		# this Slot is called when an object in the tree is activated :
		# - if it is a chapter or the story, it allows to change the title
		# - if it is the scene it is openning it in the WWSceneEdit
		if isinstance(object,WWScene):
			self.lineEditScene.setText(object.title)
			self.textEdit.setScene(object,self.book)
		elif isinstance(object,WWChapter):
			newname=QtGui.QInputDialog.getText(self, "Nouveau titre de chapitre", "Quel est le nouveau titre du chapitre ?")
			if newname[1]:
				object.changeTitle(unicode(newname[0]))
				## TODO refresh the tree
				self.SLOT_somethingChanged()
		elif isinstance(object,WWStory):
			newname=QtGui.QInputDialog.getText(self, "Nouveau titre de chapitre", "Quel est le nouveau titre de l'histoire ?")
			if newname[1]:
				object.changeTitle(unicode(newname[0]))
				## TODO refresh the tree
				self.SLOT_somethingChanged()
	
	def SLOT_changeSceneTitle(self):
		# is called when Enter is pressed in the lineEditScene : 
		# it changes the title of the scene
		if self.textEdit.scene!=None:
			newTitle=unicode(self.lineEditScene.text())	
			if newTitle!=self.textEdit.scene.title:
				self.textEdit.scene.title=newTitle
				# self.treeView.SLOT_actionRefresh()
				## TODO refresh the tree
				self.SLOT_somethingChanged()
		
	def SLOT_actionChangeMetadata(self):
		# The metadata are the author, the name of the project etc.
		dialog=self.book.metadataDialog_X(parent=self)
		res=dialog.exec_()
		self.SLOT_somethingChanged()
		
			
	def SLOT_actionAddChapter(self):
		self.treeView.SLOT_addChapter()
		self.SLOT_somethingChanged()
	def SLOT_actionDeleteChapter    (self):
		index=self.treeView.selectionModel().currentIndex()
		dist=index.distanceToRoot()
		while dist==DEPTH_SCENE:
			index=index.parent()
			dist=index.distanceToRoot()
		self.treeView.setCurrentIndex(index)
		self.treeView.SLOT_removeObject()
		self.SLOT_somethingChanged()
	def SLOT_actionAddScene         (self):
		self.treeView.SLOT_addScene()
		self.SLOT_somethingChanged()
	def SLOT_actionDeleteScene      (self):
		### TODO ###
		pass
	def SLOT_actionSendToAntidote (self):
		# Send the scene to another software (mine is called Antidote and accept only a certain type of encoding).
		path=CONSTANTS.EXTERNAL_SOFT_PATH
		if path=="":
			QtGui.QMessageBox.information(self, "Antidote Sender", "Sorry, there is no path to the Antidote software in the configuration file.")
			return False
		if self.textEdit.scene!=None:
			self.textEdit.uploadScene()
			text=self.textEdit.scene.txt_output()
			i=0
			while TMP_FILE_MARK+"tmp"+str(i).zfill(CONSTANTS.MAX_ZFILL)+'.txt' in os.listdir('.'):
				i+=1
			name=TMP_FILE_MARK+"tmp"+str(i).zfill(CONSTANTS.MAX_ZFILL)+'.txt'
			fichier = codecs.open(name, encoding='utf-8-sig', mode='w')
			try :
				fichier.write(text)
			finally:
				fichier.close()
			s=subprocess.call(path+' '+os.path.abspath(name))
			
			res = QtGui.QMessageBox.question(self, "Antidote Sender", "Have you finished to correct the file", QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
 
			if (res == QtGui.QMessageBox.Yes) :
				fichier = codecs.open(name, encoding='utf-8-sig', mode='rb')
				try :
					text=fichier.read()
					self.textEdit.setText(text)
					self.textEdit.uploadScene()
				finally:
					fichier.close()
		
	def SLOT_actionOpenConfig(self):
		dialog= QtGui.QFileDialog(self)
		
		filename = dialog.getOpenFileName(self,"Select a config file",self.get_default_opening_saving_site())
		if filename:
			filename=unicode(filename)
			try:
				WWReadConfigFile(pathway=filename)
				self.path_configFile=filename
				self.textEdit.putDefaultText()
			except Exception,e:
				raise e
			return True
		return False
	
	def SLOT_somethingChanged(self):
		# the SLOT_somethingChanged is mainly called if anything has been changed without saving
		# it is putting a star at the end of the window's name and enabeling the save button
		self.actionSaveBook.setEnabled(True)
		self.setWindowTitle ( unicode("WolfWriter : ")+ self.book.structure.project_name+ "*")
	
	def SLOT_buttonPrevScene(self):
		self.treeView.activatePrevScene()
	def SLOT_buttonNextScene(self):
		self.treeView.activateNextScene()
			

	#############################################
	
	def closeEvent(self, event):
		# cheak if we have changed something without saving
		if self.actionSaveBook.isEnabled ():
			res=self.doSaveDialog()
			if (res == QtGui.QMessageBox.Yes) or (res == QtGui.QMessageBox.No):
				event.accept()
			else:
				event.ignore()
		else:
			event.accept()

	def doSaveDialog(self):
		# is called when we try to close a book with modification which have not been saved
		res=QtGui.QMessageBox.question(self, "Modification", "Do you want to save the modifications",\
					QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
		if (res == QtGui.QMessageBox.Yes):
			self.SLOT_actionSaveBook()
			
		return res
	
	def reload_pannels(self):
		# When opening a new book, reload all the pannels  and put the last scene in the TextEditWidget
		self.treeView.setStory(self.book.structure.story)
		self.treeView.expandAll()		
		last_scene=self.book.structure.story.children[-1].children[-1]
		last_index=self.treeView.model().createIndex(last_scene.number_in_brotherhood(),0,last_scene)
		
		assert isinstance(last_scene,WWScene), 'The object is not a scene'
		self.treeView.setCurrentIndex (last_index)
		self.treeView.SLOT_activated(last_index)
		
		self.ency_panel.startEncyclopedia(self.book.encyclopedia)
		self.search_panel.book=self.book
		
		self.setWindowTitle ( unicode("WolfWriter : ")+ self.book.structure.project_name)
		self.actionSaveBook.setEnabled(False)

		
	def get_default_opening_saving_site(self):
		# When open a file dialog, in which directory the dialog window should begin :
		if self.book.archivepath== None:
			return os.path.expanduser(CONSTANTS.DLT_OPEN_SAVE_SITE)
		else :
			res,tmp=os.path.split(self.book.archivepath)
			return res
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	if len(sys.argv)>1:
		bk=WWBook(archivepath=sys.argv[1])
	else:
		bk=WWBook(archivepath=abs_path_new_book)
		bk.archivepath=None
		
		
	# pp="C:/Users/Renaud/Documents/Programmation/Python/Writing_help/WolfWriter/Test/testa.zip"
	
	mainWindow = WWMainWindow(bk)
	mainWindow.show()

	sys.exit(app.exec_())