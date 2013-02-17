from PyQt4 import QtGui, QtCore
from WolfWriterNodeXML import *
from WolfWriterCommon import *
from WolfWriterWord import *
import re

class WWEncyclopedia (WWNodeFirstAbstract):
	xml_name="encyclopedia"
	dico_attributes={} 
	
	def __init__(self,filepath,book=None,new=False,parent_file=None,**kargs_if_creation):
		WWNodeFirstAbstract.__init__(self,filepath,new=new,parent_file=parent_file,**kargs_if_creation)	
		self.book=book
		
		self.word_set=WWWordSet()
		self.list_entry=[]
		for entry_node in self.xml_node.getDirectElementsByTagName(u"entry"):
			self.list_entry.append(WWEntry(xml_node=entry_node,parent=self))
			# self.add_fromNode(entry_node)
		self.fillingWordSet()
	
			
	def fillingWordSet(self):
		self.word_set=WWWordSet()
		for entry in self.list_entry:
			if entry.properName: # if it is a proper name we do not allow the word to be in a lower form
				id=WWWordTools.IND_FIRST_CAP|WWWordTools.IND_ALL_CAP
			else:
				id=WWWordTools.IND_LOWER|WWWordTools.IND_FIRST_CAP|WWWordTools.IND_ALL_CAP
			
			self.word_set.addWord(entry.name,id)
			for other_name in entry.other_names:
				self.word_set.addWord(other_name,id)
		
			
	def addEntry(self,name,type=None,desc=None,other_names=None):
		if type==None: type=""
		if other_names==None: other_names=[]
		if desc==None: desc=""
		entry=WWEntry(xml_node=None,parent=self,name=name,other_names=other_names,type=type,desc=desc)
		self.list_entry.append(entry)
		self.fillingWordSet()
		return entry

	# def addEntry_X(self,name=None,type=None,desc=None,other_names=None,parent=None):
		# if name==None: name=""
		# if type==None: type=""
		# if other_names==None: other_names=[]
		# if desc==None: desc=""
		
		# entry=WWEntry(xml_node=None,parent=self,name=name,other_names=other_names,type=type,desc=desc)
		# dialog=entry.attributeDialog_X(parent=parent)
		# res=dialog.exec_()
		# if res==1:
			# self.list_entry.append(entry)
			# self.fillingWordSet()
		
		# return bool(res)
	
	def removeEntry(self,entry):
		if not entry in self.list_entry:
			return False
		self.list_entry.remove(entry)
		self.fillingWordSet()
		return True

	# def removeEntryFromName_X(self,name,parent=None):
		# if not self.word_set.isIn(name):
			# return False
			
		# list_possible_entries=self.getEntriesWithName(name)
		# if len(list_possible_entries)>1:
			# dialog=QtGui.QInputDialog()
			# list_name=[l.name for l in list_possible_entries]
			# name_to_pop,res=dialog.getItem(parent,"Entry selection","Please chose the entry",list_name)
			# if not res: return False
			# to_pop=list_possible_entries[list_name.index(name_to_pop)]
		# else:
			# to_pop=list_possible_entries[0]
		
		# mess=QtGui.QMessageBox()
		# ans = mess.question(parent, "Confirmation",										\
				# u"Are you sure to remove the entry <"+to_pop.name+"> from the Ency ?",  \
				# QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		
		# if ans == QtGui.QMessageBox.No:
			# return False
		# self.list_entry.remove(to_pop)
		# self.fillingWordSet()
		# return True
			
				
		
	def accessEntryFromName_X(self,name,parent=None):
		if not self.word_set.isIn(name):
			return False
			
		list_possible_entries=self.getEntriesWithName(name)
		if len(list_possible_entries)>1:
			dialog=QtGui.QInputDialog()
			list_name=[l.name for l in list_possible_entries]
			name_to_pop,res=dialog.getItem(parent,"Entry selection","Please chose the entry",list_name)
			if not res: return False
			select_entry=list_possible_entries[list_name.index(name_to_pop)]
		else:
			select_entry=list_possible_entries[0]
		
		dialog=select_entry.attributeDialog_X(parent=parent)
		res=dialog.exec_()
		if res==1:
			self.fillingWordSet()
		return bool(res)
			
		
	def getEntriesWithName(self,name):
		print "name  :  ",unicode(name).encode('ascii','replace')		
		list_possible_entries=[]
		for entry in self.list_entry:
			print "HEHO !"
			if entry.compare(name):
				list_possible_entries.append(entry)
		return list_possible_entries
		
	def searchEntriesWithName(self,name):
		# to_search=name+u".*"
		to_search=u".*"+name+u".*"
		list_possible_entries=[]
		for entry in self.list_entry:
			if entry.search(to_search):
				list_possible_entries.append(entry)
		return list_possible_entries
		
		
	def hasEntry(self,data):
		if isinstance(data,WWEntry):
			if data in self.list_entry:
				return True
			else: return False
		else:
			if self.word_set.isIn(data):
				return True
			else: return False
		
	def xml_output(self,doc,parentNode):
		node=doc.createElement(self.xml_name)
		for entry in self.list_entry:
			entry.xml_output(doc,node)
		parentNode.appendChild(node)	

	def txt_output(self):
		res=u""
		res+=u"Encyclopedia \n\n"
		for entry in self.list_entry:
			res+=entry.txt_output()+u"\n\n"
		return res


		
class WWEntry (WWNodeAbstract):
	xml_name="entry"	
	dico_attributes={"name":unicode , "type":unicode , "properName":bool} #dictionary : (name:type)
	def __init__(self,xml_node=None,parent=None,**kargs_if_creation):
		if xml_node!=None:
			WWNodeAbstract.__init__(self,xml_node,parent)
			self.read_entry()
		else:
			if kargs_if_creation.has_key("other_names"):
				self.other_names=kargs_if_creation.pop("other_names")
			if kargs_if_creation.has_key("desc"):
				self.desc=kargs_if_creation.pop("desc")
			if not kargs_if_creation.has_key("type"):
				kargs_if_creation["type"]="Undified"
			WWNodeAbstract.__init__(self,xml_node=None,parent=parent,**kargs_if_creation)
			# self.parent.word_set.addWord(self.name,WWWordTools.IND_FIRST_CAP)
			# for other_name in self.other_names:
				# self.parent.word_set.addWord(other_name,WWWordTools.IND_FIRST_CAP)
		if not self.__dict__.has_key("properName"):
			print "sdhfhsdkj"
			if WWWordTools.whatID(self.name)==WWWordTools.IND_FIRST_CAP:
				self.properName=True
			else:
				self.properName=False
				
		
	
	def attributeLayout_X(self,parent=None):
		
		name_choose = QtGui.QLineEdit ()
		name_choose.setText (self.name)
		
		type_choose	= QtGui.QLineEdit ()
		type_choose.setText (self.type)
		
		other_names_choose	= QtGui.QLineEdit ()
		other_names_str=""
		for n in self.other_names:
			other_names_str+=n+' '
		other_names_choose.setText (other_names_str)
		
		desc_choose	= QtGui.QTextEdit ()
		desc_choose.setText(self.desc)
		
		layout_info=QtGui.QFormLayout()
		layout_info.addRow("&Name : ",name_choose)
		layout_info.addRow("&Other Names : ",other_names_choose)
		layout_info.addRow("&Type : ",type_choose)
		layout_info.addRow("&Description : ",desc_choose)
		
		return (layout_info, name_choose,type_choose,other_names_choose,desc_choose)
		
		
		
	def attributeDialog_X(self,parent=None):
	
		layout_info, name_choose,type_choose,other_names_choose,desc_choose=self.attributeLayout_X()
		layout_button=QtGui.QHBoxLayout ()
		generer = QtGui.QPushButton("&Generate")
		quitter = QtGui.QPushButton("&Quit")
		layout_button.addWidget(generer)
		layout_button.addWidget(quitter)
		
		
		layout_main=QtGui.QVBoxLayout ()
		layout_main.addLayout(layout_info)
		layout_main.addLayout(layout_button)
		
		dialog=QtGui.QDialog()
		dialog.setModal(True)
		dialog.setLayout(layout_main)

		def generateEntry():
			self.name=unicode(name_choose.text())
			self.type=unicode(type_choose.text())
			self.desc=unicode(desc_choose.toPlainText())
			self.other_names=unicode(other_names_choose.text()).split()
			dialog.accept()
			
		
		dialog.connect(quitter, QtCore.SIGNAL("clicked()"), dialog, QtCore.SLOT("close()"))
		dialog.connect(generer, QtCore.SIGNAL("clicked()"), generateEntry)
		
		return dialog
	
	
	def read_entry(self):
		self.desc=u""
		self.other_names=[]
					
		for other_node in self.xml_node.getDirectElementsByTagName(u"other"):
			other_name=other_node.getAttribute(u"value")
			self.other_names.append(other_name)
			# self.parent.word_set.addWord(other_name,WWWordTools.IND_FIRST_CAP)
	
		desc_node=self.xml_node.getFirstElementsByTagName("desc")
		if desc_node:
			self.desc=desc_node.firstChild.nodeValue
		
			
	def xml_output(self,doc,parentNode):
		node=doc.createElement(self.xml_name)
		if len(self.other_names)>0:
			for other_name in self.other_names:
				node_other=doc.createElement("other")
				node_other.setAttribute("value",other_name)
				node.appendChild(node_other)
		if self.desc!=u"":
			desc_container=doc.createElement("desc")
			desc_node=doc.createTextNode(self.desc)
			desc_container.appendChild(desc_node)
			node.appendChild(desc_container)

		for i in self.list_atributes:
			node.setAttribute(i,unicode(self.__dict__[i]))
		parentNode.appendChild(node)


	def txt_output(self):
		res=self.get_name_with_other_names()
		if self.desc!=u"":
			res+=u': \n'+self.desc
	
		return res
	
	def compare(self,name):
		name_tmp=unicode(name)
		tmp_list=[self.name]+self.other_names
		for i in tmp_list:
			if name_tmp.lower()==i.lower():
				return True
		
				### TO CHANGE IN THE CAPS Version###
				# id_name = WWWordTools.whatID(self.name)
				# if id_name
		return False
		
	def search(self,to_search):
		print "to_search  :  ",to_search
		name_tmp=unicode(to_search)
		tmp_list=[self.name]+self.other_names
		for i in tmp_list:
			if re.search(to_search.lower(),i.lower())!=None:
				return True
		
				### TO CHANGE IN THE CAPS Version###
				# id_name = WWWordTools.whatID(self.name)
				# if id_name
		return False
	def get_name_with_other_names(self):
		res=u""
		res+=self.name
		if len(self.other_names)>0:
			res+=u' ('
			for name in self.other_names[:-1]:
				res+=u' '+name+u', '
			res+=u' '+self.other_names[-1]+u' '
			
			res+=u')'	
		return res
		
			
if __name__ == '__main__':
	pp="C:/Users/Renaud/Documents/Programmation/Python/Writing_help/WolfWriter/Test/encyclopedia.xml"
	en=WWEncyclopedia(pp)
	
	
	doc = XML.Document()
	en.xml_output(doc,doc)
	
	print (doc.toprettyxml()).encode('ascii','replace')		
	print "##############################################"
	print (doc.toPrettyWithText()).encode('ascii','replace')		
	
	# print (en.txt_output()).encode('ascii','replace')			
	# print unicode(en.word_set.dico).encode('ascii','replace')			
			

			