

from PyQt4 import QtGui, QtCore
from WolfWriterCommon import *
from WolfWriterBook import *
from WolfWriterScene import *
# from WolfWriterChapterScene import *
import sys
import string
import os

"""
Part of the WolfWriter project. Written by Renaud Dessalles
This file contain three classes which are involved in the graphical representation of the
 structure of the book.
 It is comunicating with the WWStory, WWChapters and WWScene (in the WolfWriterBook.py and 
 WolfWriterScene.py) objects and show them as a tree.
- WWTreeView is a QTreeView subclass: 
	- Its actions it allows to add, move and remove the chapters and the scenes of the book.
	- It is emeting the signal objectActivated when an object is emetted with the 
	corresponding scene/chapter/story in argument. The Signal is recieved and interpreted 
	by the main Window.
	- it is emeting the signal changed when the structure has been changed.
- WWTreeModel is the QAbstractItemModel used by WWTreeView.
	- the __init__ function is asking for the header. It is a list of the data we want to
	show. The information of an object (scene/chapter/story) is obtained via the method
	getInfo of WWStory, WWChapters and WWScene classes.
	- every index is associate with the corresponding item (WWTreeItem) of its line via 
	the method getItem.
- WWTreeItem represent a single item in the tree (mainly, it know its parent, and its 	
	children) and is associate with a WWStory, WWChapters and WWScene object.

Note : WWTreeItem is quite redondant with the WWStory, WWChapters and WWScene classes.
I plan to merge this class with the WWStory, WWChapters and WWScene in a further
 version of WolfWriter.
"""





class WWTreeView(QtGui.QTreeView):
	def __init__(self,story,parent=None):
		QtGui.QTreeView.__init__(self,parent)			
		model=WWTreeModel(story,parent=self)
		self.setModel(model)
		self.setup_actions()
		self.setContextMenuPolicy( QtCore.Qt.ActionsContextMenu ) 
		# self.setStory(story)
		
	def setStory(self,story):
		self.model().story=story
		
	def setup_actions(self):
		# self.actionRemoveRow=QtGui.QAction("&Remove row",self)
		# self.connect(self.actionRemoveRow, QtCore.SIGNAL("triggered()"), self.SLOT_removeRow )
		
		# self.actionInsertRow=QtGui.QAction("&Insert row",self)
		# self.connect(self.actionInsertRow, QtCore.SIGNAL("triggered()"), self.SLOT_insertRow )
		
		self.actionAddChapter=QtGui.QAction("&Add Chapter after",self)
		self.actionAddChapter.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"add_chap.png")))
		self.addAction(self.actionAddChapter)
		self.connect(self.actionAddChapter, QtCore.SIGNAL("triggered()"), self.SLOT_addChapter )
		
		self.actionAddChapterBefore=QtGui.QAction("&Add Chapter before",self)
		# self.actionAddChapter.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"add_chap.png")))
		self.addAction(self.actionAddChapterBefore)
		self.connect(self.actionAddChapterBefore, QtCore.SIGNAL("triggered()"), self.SLOT_addChapterBefore )

		self.actionAddScene=QtGui.QAction("&Add Scene after",self)
		self.actionAddScene.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"add_scene.png")))
		self.addAction(self.actionAddScene)
		self.connect(self.actionAddScene, QtCore.SIGNAL("triggered()"), self.SLOT_addScene )
		
		self.actionAddSceneBefore=QtGui.QAction("&Add Scene before",self)
		# self.actionAddSceneBefore.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"add_scene.png")))
		self.addAction(self.actionAddSceneBefore)
		self.connect(self.actionAddSceneBefore, QtCore.SIGNAL("triggered()"), self.SLOT_addSceneBefore )
		
		
		self.actionMoveObjectUp=QtGui.QAction("&Move object up",self)
		self.actionMoveObjectUp.setShortcuts(QtGui.QKeySequence("Ctrl+Up"))
		self.actionMoveObjectUp.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"1uparrow.png")))
		self.addAction(self.actionMoveObjectUp)
		self.connect(self.actionMoveObjectUp, QtCore.SIGNAL("triggered()"), self.SLOT_actionMoveObjectUp )

		self.actionMoveObjectDown=QtGui.QAction("&Move object down",self)
		self.actionMoveObjectDown.setShortcuts(QtGui.QKeySequence("Ctrl+Down"))
		self.actionMoveObjectDown.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"1downarrow.png")))
		self.addAction(self.actionMoveObjectDown)
		self.connect(self.actionMoveObjectDown, QtCore.SIGNAL("triggered()"), self.SLOT_actionMoveObjectDown )

		self.actionChangeTitleObject=QtGui.QAction("&Change object's title",self)
		self.addAction(self.actionChangeTitleObject)
		self.actionChangeTitleObject.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"applixware.png")))
		self.connect(self.actionChangeTitleObject, QtCore.SIGNAL("triggered()"), self.SLOT_changeTitleObject )		
		
		self.actionRemoveObject=QtGui.QAction("&Remove the selected object",self)
		self.actionRemoveObject.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"del_object.png")))
		self.actionRemoveObject.setShortcuts(QtGui.QKeySequence.Delete)
		self.addAction(self.actionRemoveObject)
		self.connect(self.actionRemoveObject, QtCore.SIGNAL("triggered()"), self.SLOT_removeObject )
		
		# self.actionRefresh=QtGui.QAction("&Refresh the informations",self)
		# self.actionRefresh.setShortcuts(QtGui.QKeySequence.Refresh)
		# self.connect(self.actionRefresh, QtCore.SIGNAL("triggered()"), self.SLOT_actionRefresh)
		
		self.connect(self, QtCore.SIGNAL("activated (const QModelIndex & )"), self.SLOT_activated )
		
		
		# self.actionTest=QtGui.QAction("&Test",self)
		# self.connect(self.actionTest, QtCore.SIGNAL("triggered()"), self.SLOT_test )
	
	def mouseDoubleClickEvent(self,event):
		#prevent or roll/deroll the chaper
		QtGui.QAbstractItemView.mouseDoubleClickEvent(self,event)
	
	
	
	############### SLOTS ###############
	# def SLOT_removeRow(self):
		# index=self.selectionModel().currentIndex()
		# self.model().removeRows(index.row(),1,index.parent())
	# def SLOT_insertRow(self):
		# index=self.selectionModel().currentIndex()
		# self.model().insertRows(index.row(),1,index.parent())
	def SLOT_test(self):
		print 'test'		
	def SLOT_addChapter(self,place=0):
		index=self.selectionModel().currentIndex()
		dist=index.distanceToRoot()
		
		if 0<dist<DEPTH_SCENE-1:
			row=index.row()+1+place
			index=index.parent()
		elif dist==0:
			row=0
		else :
			index=index.parent()
			row=index.row()+1+place
			index=index.parent()
		
			
			
		chap_title = QtGui.QInputDialog.getText(self, "Nouveau Chapitre", "Quel est le titre du nouveau chapitre ?")
		scne_title = QtGui.QInputDialog.getText(self, "Premiere Scene", "Quel est le titre de la premiere scene ?")
		
		if scne_title[1]: new_scene=self.model().story.parent.create_new_scene(title=scne_title[0])
		else : new_scene=self.model().story.parent.create_new_scene()
			
		if chap_title[1]:
			new_chapter=WWChapter(xml_node=None,
					parent=self.model().story,
					title= chap_title[0] 
					)
		else:
			new_chapter=WWChapter(xml_node=None,
					parent=self.model().story,
					)
			
		
		self.model().insertRows(row,1,index,list_objects=[new_chapter])
		index=self.model().index(row,0,index)
		self.model().insertRows(0,1,index,list_objects=[new_scene])
		self.SLOT_emitChanged()

	def SLOT_addChapterBefore(self):
		self.SLOT_addChapter(place=-1)
		
		
	def SLOT_addScene(self,place=0):
	
		index=self.selectionModel().currentIndex()
		dist=index.distanceToRoot()
	
		if dist==DEPTH_SCENE-1:
			row=index.row()+1+place
		else:
			while dist<DEPTH_SCENE-1:
				index=index.child(0,0)
				dist+=1
			row=0
		
		
		scne_title = QtGui.QInputDialog.getText(self, "Nouvelle Secne", "Quel est le titre de la premiere scene ?")
		if scne_title[1]: new_scene=self.model().story.parent.create_new_scene(title=scne_title[0])
		else : new_scene=self.model().story.parent.create_new_scene()
		
		self.model().insertRows(row,1,index.parent(),list_objects=[new_scene])
		# itemScene=itemScenes[0]		
		
		# columnDataScene=[new_scene.getInfo(i) for i in self.model().headers]
		self.SLOT_emitChanged()
		# for i,column in enumerate(columnDataScene):
			# itemScene.setData(i, column)

	def SLOT_addSceneBefore(self):
		self.SLOT_addScene(place=-1)
	def SLOT_actionMoveObjectUp(self):
		index=self.selectionModel().currentIndex()
		row=index.row()
		dist=index.distanceToRoot()
		
		
		object=(self.model().getItem(index))
		new_index=False
		if 0<dist<DEPTH_SCENE and row>0: #We move a chapter or a scene
			self.model().moveRows(pos_init=row,pos_end=row-1, rows=1,parent_init=index.parent(),parent_end=None)
			self.SLOT_emitChanged()
		elif dist==DEPTH_SCENE-1 and row==0: #We move a scene in the upper chapter
			##### TO CORRECT ###########
			# parent=self.model().getItem(index).parent()
			# print "parent.childCount() AVANT :  ",parent.childCount()
			# parent_place=parent.number_in_brotherhood()
			# if parent_place>0:
				# assert object.xml_name=="scene"
				# index_parent_end=index.parent().sibling(parent_place-1,0)
				# parent_end=self.model().getItem(index_parent_end)
				# object_parent_end=parent_end.object
				
				# newPlace=parent_end.childCount()
				
				
				# self.model().moveRows(pos_init=row,pos_end=newPlace, rows=1,parent_init=index.parent(),parent_end=index_parent_end)
				# object.parent.moveScene(initPlace=row, newPlace=newPlace,otherChapter=parent_end.object)	
				# new_index=self.model().index(parent_end.childCount()-1,index.column(),parent=index_parent_end)
				
			# print "parent.childCount() APRES :  ",parent.childCount()
			##### TO CORRECT ###########
			pass
			
	def SLOT_actionMoveObjectDown(self):
		index=self.selectionModel().currentIndex()
		row=index.row()
		dist=index.distanceToRoot()

		siblingsCount=len(self.model().getItem(index.parent()).children)
		
		object=(self.model().getItem(index))
		new_index=False
		if 0<=dist<DEPTH_SCENE and row<siblingsCount-1: #We move a chapter or a scene
			self.model().moveRows(pos_init=row,pos_end=row+1, rows=1,parent_init=index.parent(),parent_end=None)
			self.SLOT_emitChanged()
		elif dist==DEPTH_SCENE-1 and row==siblingsCount-1: #We move a scene in the downer chapter
			pass
				
			
	
		
	def SLOT_removeObject(self):
		index=self.selectionModel().currentIndex()
		row=index.row()
		dist=index.distanceToRoot()
		
		object=self.model().getItem(index)
		
		if dist<1: 
			return False
		elif len(self.model().getItem(index.parent()).children)==1 : #if we are the only child
			# we try to delete the parent
			self.setCurrentIndex (index.parent())
			
			return self.SLOT_removeObject()	

		ans = QtGui.QMessageBox.question(self, "Delete Message", "Do you really want to delete the "+object.xml_name, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No);
		
		if ans==QtGui.QMessageBox.Yes:
			self.model().removeRows(index.row(),1,index.parent())
			self.SLOT_emitChanged()
			return True
		else : 
			return False
				
				
		
	def SLOT_activated (self,index) :
		item=self.model().getItem(index)
		
		self.emit(QtCore.SIGNAL("objectActivated (PyQt_PyObject)"),  item)
			

	def SLOT_emitChanged(self):
		self.emit(QtCore.SIGNAL("changed ()"))
	
	def SLOT_changeTitleObject(self):
		index=self.selectionModel().currentIndex()
		item=self.model().getItem(index)
		if isinstance(item,WWScene):
			question="What is the new scene's title?"
		elif isinstance(item,WWChapter):
			question="What is the new chapter's title?"
		newname=QtGui.QInputDialog.getText(self, "New title", question)
		if newname[1]:
			item.changeTitle(unicode(newname[0]))
			self.SLOT_emitChanged()

	# def SLOT_actionRefresh(self):
		# self.model().refresh_all()
		
		
	#####################################
	def activateNextScene(self,start_index=None):
		if start_index==None:
			index=self.selectionModel().currentIndex()
		else:
			index=start_index
		index=self.model().nextIndex(index)
		while index.isValid() and index.distanceToRoot()!=DEPTH_SCENE-1:
			index=self.model().nextIndex(index)
		if not index.isValid():
			return False
		
		self.setCurrentIndex(index)
		self.emit(QtCore.SIGNAL("activated(const QModelIndex & )"),  index)
		
	def activatePrevScene(self,start_index=None):
		if start_index==None:
			index=self.selectionModel().currentIndex()
		else:
			index=start_index
		index=self.model().prevIndex(index)
		while index.isValid() and index.distanceToRoot()!=DEPTH_SCENE-1:
			index=self.model().prevIndex(index)
		if not index.isValid():
			return False
		
		self.setCurrentIndex(index)
		self.emit(QtCore.SIGNAL("activated(const QModelIndex & )"),  index)
		
		
	def getIndex(self,item):
		if item==self.model().story:
			return self.rootIndex ()
		else:
			parentItem=item.parent
			parentIndex=self.getIndex(parentItem)
			index=self.model().index(item.number_in_brotherhood(),0,parentIndex)
			return index
			
		
		
		
	def getToolBar(self,parent):
		toolBar=QtGui.QToolBar ("ToolBar",parent)
		toolBar.addAction(self.actionAddChapter)
		toolBar.addAction(self.actionAddScene)
		toolBar.addAction(self.actionRemoveObject)		
		toolBar.addAction(self.actionMoveObjectDown)		
		toolBar.addAction(self.actionMoveObjectUp)		
		return toolBar
		

class WWTreeModel (QtCore.QAbstractItemModel):
	def __init__(self,story,headers=None,parent=None):
		QtCore.QAbstractItemModel.__init__(self,parent=parent)
		if headers==None:
			headers=["title","numberWords"]
		
		self.story=story # WWStory
		self.headers=headers

	def data(self,index,role= QtCore.Qt.DisplayRole ):
		if (not index.isValid()):
			return QtCore.QVariant()
		if (role != QtCore.Qt.DisplayRole ):
			return QtCore.QVariant()
		item=self.getItem(index)
		return item.getInfo(self.headers[index.column()])
	
	def headerData(self,section, orientation, role = QtCore.Qt.DisplayRole):
		if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
			return self.story.getInfo(self.headers[section]) 
		return QtCore.QVariant()
	
	def index(self,row,column,parent=None):
		if parent==None :	
			parent=QtCore.QModelIndex()
		if (parent.isValid() and parent.column() != 0):
			return QtCore.QModelIndex()
			
		parentItem = self.getItem(parent)
		try:
			childItem = parentItem.children[row]
		except IndexError,e:
			return QtCore.QModelIndex()
		if (childItem):
			return self.createIndex(row, column, childItem)
		else :
			return QtCore.QModelIndex()
		
	def parent(self,index):
		if (not index.isValid()):
			return QtCore.QModelIndex()

		childItem = self.getItem(index)
		parentItem = childItem.parent

		if (parentItem == self.story):
			return QtCore.QModelIndex()
	
	
		
		return self.createIndex(parentItem.number_in_brotherhood(), 0, parentItem)
		
	def rowCount(self,parent=None):
		if parent==None :				
			parent=QtCore.QModelIndex()
		parentItem = self.getItem(parent)
		return len(parentItem.children)
	
	def columnCount(self,parent=None):
		if parent==None :				
			parent=QtCore.QModelIndex()
		return len(self.headers)
	
	def flags(self,index):
		if (not index.isValid()):
			return 0
		return  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
	
	def insertRows(self,position,rows,parent = None , list_objects=None):
			
		if parent==None :				
			parent=QtCore.QModelIndex()	
		parentItem = self.getItem(parent)

		self.beginInsertRows(parent, position, position + rows - 1)
		items = parentItem.insertChildren(position, list_objects=list_objects)
		self.endInsertRows()

		return items
		
	def removeRows(self,position, rows,parent = None):
		if parent==None :				
			parent=QtCore.QModelIndex()	
		parentItem = self.getItem(parent)
		
		# ## removes childrens' children
		# for r in range(position,position+rows):
			# childIndex = parent.child(r,0)
			# childItem = self.getItem(childIndex)
			# if len(childItem.children)!=0:
				# print "WWWWW"
				# # self.removeRows(0,len(childItem.children),childIndex)
		
		## removes children
		if rows==len(parentItem.children): last=position + rows 
		else: last=position + rows - 1
		self.beginRemoveRows(parent, position, position + rows - 1)
		removed = parentItem.removeChildren(position, rows)
		self.endRemoveRows()

		return removed
		
	def moveRows (self, pos_init, pos_end, rows,parent_init, parent_end=None):
		if parent_end==None : 
			parent_end=parent_init
			
			if pos_init<=pos_end:
				pos_end_qt=pos_end+1
			else:
				pos_end_qt=pos_end
		else:
			pos_end_qt=pos_end
	
			
		self.beginMoveRows( parent_init , pos_init , pos_init+rows-1, 
							parent_end, pos_end_qt )
		parentInitItem = self.getItem(parent_init)
		parentEndItem = self.getItem(parent_end)
		moved = parentInitItem.removeChildren(pos_init, rows)
		parentEndItem.insertChildren(pos_end, moved)
		self.endMoveRows ()
			
	def getItem(self,index):
		if (index.isValid()) :
			item = index.internalPointer()
			if (item) :
				return item
		
		return self.story
		

			
	def nextIndex(self,index,with_children=True):
		# This function get the next index that comes after the one in entry:
		# If it has a child, it will gives the first child (excepect if with_children is false)
		# Otherwise, it gives the next sibbling
		# If there is no sibling, it gives the parents' next brother
		# If the index is the last one, then it return an invalid index		
		if with_children and self.rowCount(index)>0:   #if the node has children, we give the first child
			return self.index(0,index.column(),index)
		
		parent_index=self.parent(index)
		if not parent_index.isValid():
			return parent_index
			
		if self.rowCount(self.parent(index))-index.row()>1:   #if the node has a next brother, we give the next brother
			index_tmp=self.index(index.row()+1,index.column(),parent_index)
			return index_tmp
		
		return self.nextIndex(parent_index,with_children=False) # we search for the next index after the parent one
		
	def prevIndex(self,index,with_children=True):
		# This function get the previous index that comes after the one in entry:
		# If it has a child, it will gives the last child (excepect if with_children is false)
		# Otherwise, it gives the previous sibbling
		# If there is no sibling, it gives the parents' previous brother
		# If the index is the first one, then it return an invalid index	
		# if index.distanceToRoot()==0:
			# return QtCore.QModelIndex()
		
		if with_children and self.rowCount(index)>0:   #if the node has children, we give the last child
			return self.index(self.rowCount(index)-1,index.column(),index)
		
		parent_index=self.parent(index)
		if not parent_index.isValid():
			return parent_index
			
		if index.row()>0:   #if the node has a previous brother, we give the previous brother
			index_tmp=self.index(index.row()-1,index.column(),parent_index)
			return index_tmp
		
		return self.prevIndex(parent_index,with_children=False) # we search for the next index after the parent one
			
	
	
		
if __name__ == '__main__':
	class MainWindow ( QtGui.QMainWindow):
		def __init__(self, story,parent=None):
			QtGui.QMainWindow.__init__(self,parent)
			
			self.view=WWTreeView(story,parent=self)
			self.setCentralWidget(self.view)
			self.toolBar=self.addToolBar("ToolBar")
			self.toolBar.addAction(self.view.actionAddChapter)
			self.toolBar.addAction(self.view.actionAddScene)
			self.toolBar.addAction(self.view.actionRemoveObject)
			self.toolBar.addAction(self.view.actionMoveObjectDown)
			self.toolBar.addAction(self.view.actionMoveObjectUp)


	import WolfWriterBook
	app = QtGui.QApplication(sys.argv)
	
	
	pp=pp="C:\\Users\\Renaud\\Documents\\Programmation\\Python\\WolfWriter_Test\\TestPerso\\testa.zip"
	# xml_file=XML.parse(pp)
	# root = xml_file.documentElement
	# n=root.getFirstElementsByTagName('story')
	bk=WolfWriterBook.WWBook(pp)
	
	print "##################"
	for ch in bk.structure.story.children:
		print "ch.children  :  ",ch.children
		# print "ch.list_scenes  :  ",ch.list_scenes
	print "##################"
	mainWindow = MainWindow(bk.structure.story)
	mainWindow.show()
	sys.exit(app.exec_())		
	# ch=WolfWriterBook.WWChapter(pp)	
	