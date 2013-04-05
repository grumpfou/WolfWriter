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
	- every index is associate with the corresponding object (WWStory, WWChapter and 
	WWScene).
"""
from PyQt4 import QtGui, QtCore

import sys
import string
import os

from WolfWriterCommon	import *
from WolfWriterBook 	import *
from WolfWriterScene 	import *




class WWTreeView(QtGui.QTreeView):
	def __init__(self,story,parent=None,main_window=None):
		""" This class is a re-implementation of QTreeView which w<ill display the 
		structure of the story.
		- story : the WWScene to display (TODO : it would be better if it was a WWStructure
		- parent : the parent widget
		- main_window : the possible WWMainWindow that is above the WWTreeView (to know 
			what is the active scene etc.
		"""
		QtGui.QTreeView.__init__(self,parent)			
		self.main_window=main_window
		model=WWTreeModel(story,parent=self)
		self.setModel(model)
		self.setup_actions()
		self.setContextMenuPolicy( QtCore.Qt.ActionsContextMenu ) 
		# self.setStory(story)
		
	def setStory(self,story):
		self.model().story=story
		
	def setup_actions(self):
		"""
		This method is called at the very beinging to create the different actions.
		"""

		# actionAddChapter : add a chapter after the current row position
		self.actionAddChapter=QtGui.QAction("&Add Chapter after",self)
		self.actionAddChapter.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"add_chap.png")))
		self.addAction(self.actionAddChapter)
		self.connect(self.actionAddChapter, QtCore.SIGNAL("triggered()"), self.SLOT_addChapter )
		
		# actionAddChapterBefore : add a chapter before the current row position
		self.actionAddChapterBefore=QtGui.QAction("&Add Chapter before",self)
		self.addAction(self.actionAddChapterBefore)
		self.connect(self.actionAddChapterBefore, QtCore.SIGNAL("triggered()"), self.SLOT_addChapterBefore )

		# actionAddScene : add a chapter after the current row position
		self.actionAddScene=QtGui.QAction("&Add Scene after",self)
		self.actionAddScene.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"add_scene.png")))
		self.addAction(self.actionAddScene)
		self.connect(self.actionAddScene, QtCore.SIGNAL("triggered()"), self.SLOT_addScene )
		
		# actionAddSceneBefore : add a chapter before the current row position
		self.actionAddSceneBefore=QtGui.QAction("&Add Scene before",self)
		self.addAction(self.actionAddSceneBefore)
		self.connect(self.actionAddSceneBefore, QtCore.SIGNAL("triggered()"), self.SLOT_addSceneBefore )
		
		# actionMoveObjectUp: move the chapter/scene above 
		# (if we move a scene which is at the begining of the chapter, we move it at the 
		# end of the previous chapter.)
		self.actionMoveObjectUp=QtGui.QAction("&Move object up",self)
		self.actionMoveObjectUp.setShortcuts(QtGui.QKeySequence("Ctrl+Up"))
		self.actionMoveObjectUp.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"1uparrow.png")))
		self.addAction(self.actionMoveObjectUp)
		self.connect(self.actionMoveObjectUp, QtCore.SIGNAL("triggered()"), self.SLOT_actionMoveObjectUp )

		# actionMoveObjectDown: move the chapter/scene below 
		# (if we move a scene which is at the end of the chapter, we move it at the 
		# begining of the next chapter.)
		self.actionMoveObjectDown=QtGui.QAction("&Move object down",self)
		self.actionMoveObjectDown.setShortcuts(QtGui.QKeySequence("Ctrl+Down"))
		self.actionMoveObjectDown.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"1downarrow.png")))
		self.addAction(self.actionMoveObjectDown)
		self.connect(self.actionMoveObjectDown, QtCore.SIGNAL("triggered()"), self.SLOT_actionMoveObjectDown )

		# actionChangeTitleObject: change chapter/scene's title
		self.actionChangeTitleObject=QtGui.QAction("&Change object's title",self)
		self.addAction(self.actionChangeTitleObject)
		self.actionChangeTitleObject.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"applixware.png")))
		self.connect(self.actionChangeTitleObject, QtCore.SIGNAL("triggered()"), self.SLOT_changeTitleObject )		
		
		# actionRemoveObject: remove chapter/scene. (Do not do anything if it is the last 
		# scene of a chapter or the last chapter of a story.)
		self.actionRemoveObject=QtGui.QAction("&Remove the selected object",self)
		self.actionRemoveObject.setIcon(QtGui.QIcon(os.path.join(abs_path_icon,"del_object.png")))
		self.actionRemoveObject.setShortcuts(QtGui.QKeySequence.Delete)
		self.addAction(self.actionRemoveObject)
		self.connect(self.actionRemoveObject, QtCore.SIGNAL("triggered()"), self.SLOT_removeObject )
		
		# if an object is activated, it calls the SLOT_activated
		self.connect(self, QtCore.SIGNAL("activated (const QModelIndex & )"), self.SLOT_activated )
		
		
	
	# def mouseDoubleClickEvent(self,event):
		# #prevent or roll/deroll the chaper
		# QtGui.QAbstractItemView.mouseDoubleClickEvent(self,event)
	
	
	
	############### SLOTS ###############
	def SLOT_addChapter(self,place=0,with_activation=True):
		"""Add a chapter and it's first scene relatively to the row of the current index.
		place : the position where to insert the chapter in the story relative to the row 
			of the current index. (0 : just after, -1 : just before)
		with_activation : if we have to change the active scene of 
			self.main_window.sceneEdit to the newly created WWScene ?
		"""
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
		
			
		# Get the titles
		chap_title = QtGui.QInputDialog.getText(self, "New Chapter", "What is the title of the new chapter?")
		if not chap_title[1]:
			return False
		scne_title = QtGui.QInputDialog.getText(self, "First Scene", "What is the title of the first scene of the chapter?")
		if not scne_title[1]:
			return False
		
		# If no title given, we take the default one
		if unicode(scne_title[0])!=u'':
			new_scene=self.model().story.parent.create_new_scene(title=scne_title[0])
		else :
			new_scene=self.model().story.parent.create_new_scene()
			
		if unicode(chap_title[1])!=u'':
			new_chapter=WWChapter(xml_node=None,
					parent=self.model().story,
					title= chap_title[0] 
					)
		else:
			new_chapter=WWChapter(xml_node=None,
					parent=self.model().story,
					)
			
		# We insert the newly created Chapter and Scene
		self.model().insertRows(row,1,index,list_objects=[new_chapter])
		index=self.model().index(row,0,index)
		self.model().insertRows(0,1,index,list_objects=[new_scene])
		self.SLOT_emitChanged()
		if with_activation:
			index=self.model().index(0,0,index)
			self.setCurrentIndex(index)
			self.SLOT_activated(index)
		return True

	def SLOT_addChapterBefore(self,*args,**kargs):
		"""Insert a chapter just before the row of the current index"""
		self.SLOT_addChapter(place=-1,*args,**kargs)
		
		
	def SLOT_addScene(self,place=0,with_activation=True):
		"""Add a scene relatively to the row of the current index.
		place : the position where to insert the scene in the story relative to the row 
			of the current index. (0 : just after, -1 : just before)
		with_activation : if we have to change the active scene of 
			self.main_window.sceneEdit to the newly created WWScene ?
		"""
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
		if scne_title[1]:
			if unicode(scne_title[0])!=u'': new_scene=self.model().story.parent.create_new_scene(title=scne_title[0])
			else : new_scene=self.model().story.parent.create_new_scene()
			
			self.model().insertRows(row,1,index.parent(),list_objects=[new_scene])
			self.SLOT_emitChanged()
			if with_activation:
				index=self.model().index(row,0,index.parent())
				self.setCurrentIndex(index)
				self.SLOT_activated(index)

	def SLOT_addSceneBefore(self):
		"""Insert a scene just before the row of the current index"""
		self.SLOT_addScene(place=-1)
		
	def SLOT_actionMoveObjectUp(self):
		"""Move the object at the current index just above.
		If the object is the first scene of a middle chapter, it will move it at the last 
		place of the previous chapter.
		It the object is the first chapter or the first scene of the first chapter, it 
		does nothing.
		"""
		index=self.selectionModel().currentIndex()
		row=index.row()
		dist=index.distanceToRoot()
		siblingsCount=len(self.model().getItem(index.parent()).children)
		
		object=(self.model().getItem(index))
		new_index=False
		if 0<dist<DEPTH_SCENE and row>0: #We move a chapter or a scene
			self.model().moveRows(pos_init=row,pos_end=row-1, rows=1,parent_init=index.parent(),parent_end=None)
		elif dist==DEPTH_SCENE-1 and row==0: #We move a scene in the upper chapter
			index_end=self.selectionModel().currentIndex()
			index_end=self.model().prevIndex(index_end)
			while index_end.isValid() and index_end.distanceToRoot()!=DEPTH_SCENE-1:
				if index_end.distanceToRoot()==0:
					return False #We are at the end of the tree
				index_end=self.model().prevIndex(index_end)
			if not index_end.isValid():
				return False	#We are at the end of the tree	
			if siblingsCount==1:  #If it was the last scene in the chapter		
				#we ask if we have to delete the chapter
				ans = QtGui.QMessageBox.question(self, "Delete Message", \
					"You will delete the chapter "+object.parent.title,QtGui.QMessageBox.Yes \
					| QtGui.QMessageBox.No)
				if not ans==QtGui.QMessageBox.Yes:
					return False
				to_delete_index=index.parent()
				
			pos_end=self.model().getItem(index_end).number_in_brotherhood()+1 #the place where we should place the scene
			self.model().moveRows(pos_init=row,pos_end=pos_end, rows=1,\
				parent_init=index.parent(),parent_end=index_end.parent())
			if siblingsCount==1:
				#we delete the empty chapter
				self.SLOT_removeObject(index=to_delete_index,with_activation=False,with_confirm_msg=False)
				
		self.SLOT_emitChanged()
		return True
	
			
	def SLOT_actionMoveObjectDown(self):
		"""Move the object at the current index just bellow.
		If the object is the last scene of a middle chapter, it will move it at the first 
		place of the next chapter.
		It the object is the last chapter or the last scene of the last chapter, it 
		does nothing.
		"""		
		index=self.selectionModel().currentIndex()
		row=index.row()
		dist=index.distanceToRoot()

		siblingsCount=len(self.model().getItem(index.parent()).children)
		
		object=(self.model().getItem(index))

		if 0<=dist<DEPTH_SCENE and row<siblingsCount-1: #We move a chapter or a scene
			self.model().moveRows(pos_init=row,pos_end=row+1, rows=1,parent_init=index.parent(),parent_end=None)
		elif dist==DEPTH_SCENE-1 and row==siblingsCount-1: #We move a scene in the downer chapter
			index_end=self.selectionModel().currentIndex()
			index_end=self.model().nextIndex(index_end)
			while index_end.isValid() and index_end.distanceToRoot()!=DEPTH_SCENE-1:
				if index_end.distanceToRoot()==0:
					return False #We are at the end of the tree
				index_end=self.model().nextIndex(index_end)
			if not index_end.isValid():
				return False		
			if siblingsCount==1:#If it was the last scene in the chapter		
				#we ask if we have to delete the chapter				
				ans = QtGui.QMessageBox.question(self, "Delete Message", \
					"You will delete the chapter "+object.parent.title,QtGui.QMessageBox.Yes \
					| QtGui.QMessageBox.No)
				if not ans==QtGui.QMessageBox.Yes:
					return False
				to_delete_index=index.parent()
				
			self.model().moveRows(pos_init=row,pos_end=0, rows=1,\
				parent_init=index.parent(),parent_end=index_end.parent())
			if siblingsCount==1:
				#we delete the empty chapter
				self.SLOT_removeObject(index=to_delete_index,with_activation=False,with_confirm_msg=False)
		
		self.SLOT_emitChanged()
		return True
			
	
		
	def SLOT_removeObject(self,index=None,with_activation=True,with_confirm_msg=True):
		"""Remove the object at a given index.
		index : the index of the object to remove (if none, then we take the current index)
		with_activation : change the active scene in self.main_window if we delete it
		with_confirm_msg : ask for a confirmation before making deletion
		"""
		if index==None :index=self.selectionModel().currentIndex()
		row=index.row()
		dist=index.distanceToRoot()
		
		object=self.model().getItem(index)
		
		if dist<1: 
			return False
		elif len(self.model().getItem(index.parent()).children)==1 : #if we are the only child
			# we try to delete the parent
			self.setCurrentIndex (index.parent())
			
			return self.SLOT_removeObject()	

		if with_confirm_msg:
			ans = QtGui.QMessageBox.question(self, "Delete Message", "Do you really want to delete the "+object.xml_name+' '+object.title,\
						QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
			
			if not ans==QtGui.QMessageBox.Yes:
				return False
		index_parent=index.parent()
		self.model().removeRows(index.row(),1,index.parent())
		self.SLOT_emitChanged()
		
		if with_activation and \
				(self.main_window.sceneEdit.scene==object or self.main_window.sceneEdit.scene in object.children):
			#if the active scene has been deleted
			object_parent=self.model().getItem(index.parent())
			number_children=len(object_parent.children)
			index=self.model().index(min(row,number_children-1),0,index_parent) #we take the more close index to the delted object
			dist=index.distanceToRoot()
			while dist<DEPTH_SCENE-1: #if it is not a scene, we o thurther in the tree
				index=self.model().index(0,0,index)
				dist=index.distanceToRoot()
				
			self.setCurrentIndex(index)
			self.SLOT_activated(index)			
			return True
		else : 
			return False
				
				
		
	def SLOT_activated (self,index) :
		"""Method that emit the signal "objectActivated" and the object of the activated 
		index."""
		item=self.model().getItem(index)
		
		self.emit(QtCore.SIGNAL("objectActivated (PyQt_PyObject)"),  item)
			

	def SLOT_emitChanged(self):
		"""Method that emit the signal "changed" to inform WolfWriter that someting has 
		been changed in the structure of the book."""
		self.emit(QtCore.SIGNAL("changed ()"))
	
	def SLOT_changeTitleObject(self):
		"""Method that will allow to change the Chapter/Scene title."""
		index=self.selectionModel().currentIndex()
		item=self.model().getItem(index)
		if isinstance(item,WWScene):
			question="What is the new scene's title?"
		elif isinstance(item,WWChapter):
			question="What is the new chapter's title?"
		newname=QtGui.QInputDialog.getText(self, "New title", question,text=item.title)
		if newname[1]:
			item.title=unicode(newname[0])
			self.SLOT_emitChanged()

		
		
	#####################################
	def activateNextScene(self,start_index=None):
		"""Will emit an "activated" signal on the index corresponding to the first scene comming after start_index.
		- start_index : the index to start with, if None, it takes the current index.
		If the index is the one of a chapter, it gives the first of its scene.
		If the index is the one of the last scene of a middle chapter, it gives the first 
			scene of the next chapter.
		If the index is the one of the last scene of the last chapter, it does nothing.
		"""
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
		"""Will emit an "activated" signal on the index corresponding to the first scene comming before start_index.
		- start_index : the index to start with, if None, it takes the current index.
		If the index is the one of a chapter, it gives the last of its scene.
		If the index is the one of the first scene of a middle chapter, it gives the last 
			scene of the previous chapter.
		If the index is the one of the first scene of the first chapter, it does nothing.
		"""		
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
		"""Will give the index of a given object."""				
		if item==self.model().story:
			return self.rootIndex ()
		else:
			parentItem=item.parent
			parentIndex=self.getIndex(parentItem)
			index=self.model().index(item.number_in_brotherhood(),0,parentIndex)
			return index
			
		
		
		
	def getToolBar(self,parent):
		"""Give the toolbar with all the actions"""
		toolBar=QtGui.QToolBar ("ToolBar",parent)
		toolBar.addAction(self.actionAddChapter)
		toolBar.addAction(self.actionAddScene)
		toolBar.addAction(self.actionRemoveObject)		
		toolBar.addAction(self.actionMoveObjectDown)		
		toolBar.addAction(self.actionMoveObjectUp)		
		return toolBar
		

class WWTreeModel (QtCore.QAbstractItemModel):
	def __init__(self,story,headers=None,parent=None):
		""" A quite classic re-implementation of the QAbstractItemModel
		- story : the WWStory instance, it will represent the root of the tree
			Note: Choose the WWStructure should be more coherent
		- headers : list of the informations asked to be displayed
		- parent: the WWTreeView
		"""
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
		if rows==len(parentItem.children): last=position + rows #to deal with complicated behaviour of beginRemoveRows
		else: last=position + rows - 1                          #to deal with complicated behaviour of beginRemoveRows
		self.beginRemoveRows(parent, position, position + rows - 1)
		removed = parentItem.removeChildren(position, rows)
		self.endRemoveRows()

		return removed
		
	def moveRows (self, pos_init, pos_end, rows,parent_init, parent_end=None):
		if parent_end==None : 
			parent_end=parent_init
			
			if pos_init<=pos_end:
				pos_end_qt=pos_end+1 #to deal with complicated behaviour of beginMoveRows
			else:
				pos_end_qt=pos_end #to deal with complicated behaviour of beginMoveRows
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
		"""Function that return the given object (WWStory, WWChapter or WWScene) at the 
		given index"""
		if (index.isValid()) :
			item = index.internalPointer()
			if (item) :
				return item
		
		return self.story
		

			
	def nextIndex(self,index,with_children=True):
		"""
		This function get the next index that comes after the one in entry:
		If it has a child, it will gives the first child (excepect if with_children is
		false)
		Otherwise, it gives the next sibling
		If there is no sibling, it gives the parents' next brother
		If the index is the last one, then it return an invalid index
		Example :
		
			S___1___11
			 |   |__12
			 |
			 |__2___21
			     |__22
		
		>>> WWTreeModel.nextIndex(index_of_21,with_children=True)
		    index_of_22 #the next sibling of 21 (because, 21 has no child)
		>>> WWTreeModel.nextIndex(index_of_21,with_children=False)
		    index_of_22 #the next sibling of 21
		>>> WWTreeModel.nextIndex(index_of_12,with_children=True)
		    index_of_1 #the parent of 12 (because, 12 has no child)
		>>> WWTreeModel.nextIndex(index_of_12,with_children=False)
		    index_of_1 #the parent of 12		
		>>> WWTreeModel.nextIndex(index_of_1,with_children=True)
		    index_of_11 #the first child of 1
		>>> WWTreeModel.nextIndex(index_of_1,with_children=False)
		    index_of_2 #the next sibling of 1
		>>> WWTreeModel.nextIndex(index_of_2,with_children=False)
		    index_of_S #the seed		
		"""
		if with_children and self.rowCount(index)>0:   #if the node has children, we give the first child
			return self.index(0,index.column(),index)
		
		parent_index=self.parent(index)
		if parent_index.distanceToRoot()==0 and index.row()==self.rowCount(parent_index)-1:
				#if we are at the last children of the seed, we return the seed
			return parent_index
			
		if self.rowCount(self.parent(index))-index.row()>1:   #if the node has a next brother, we give the next brother
			index_tmp=self.index(index.row()+1,index.column(),parent_index)
			return index_tmp
		
		return self.nextIndex(parent_index,with_children=False) # we search for the next index after the parent one
		
	def prevIndex(self,index,with_children=True):
		"""
		This function get the previous index that comes before the one in entry:
		If it has a child, it will gives the last child (excepect if with_children is false)
		Otherwise, it gives the previous sibling
		If there is no sibling, it gives the parents' previous brother
		If the index is the first one, then it return an invalid index	
		Example :
		
			S___1___11
			 |   |__12
			 |
			 |__2___21
			     |__22
		
		>>> WWTreeModel.prevIndex(index_of_22,with_children=True)
		   index_of_21 #the previous sibling of 22 (because, 22 has no child)
		>>> WWTreeModel.prevIndex(index_of_22,with_children=False)
		   index_of_21 #the previous sibling of 22
		>>> WWTreeModel.prevIndex(index_of_21,with_children=True)
		   index_of_2 #the parent of 21 (because, 21 has no child)
		>>> WWTreeModel.prevIndex(index_of_21,with_children=False)
		   index_of_2 #the parent of 21
		>>> WWTreeModel.prevIndex(index_of_2,with_children=True)
		   index_of_22 #the last child of 2
		>>> WWTreeModel.prevIndex(index_of_2,with_children=False)
		   index_of_1 #the previous sibling of 2
		>>> WWTreeModel.prevIndex(index_of_1,with_children=False)
		   index_of_S #the seed		
		"""
		if with_children and self.rowCount(index)>0:  #if the node has children, we give the last child
			return self.index(self.rowCount(index)-1,index.column(),index)
		
		parent_index=self.parent(index)
		if parent_index.distanceToRoot()==0 and index.row()==0:
			# if we are a the first child of the seed, we return the seed
			return parent_index #we return the seed of the tree
			
		if index.row()>0:   #if the node has a previous brother, we give the previous brother
			index_tmp=self.index(index.row()-1,index.column(),parent_index)
			return index_tmp
		
		return self.prevIndex(parent_index,with_children=False) # we search for the next index before the parent one
			
	
	
		
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
	