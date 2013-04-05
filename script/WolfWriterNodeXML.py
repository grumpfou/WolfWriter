"""
Part of the WolfWriter project. Written by Renaud Dessalles
Contains classes relative to Nodes. It will allow to read the xml nodes contained in the 
ww zip file. They are abstract classes re-implemented in WWStructure, WWStory, 
WWChapter, WWScene, WWEncyclopedia, WWEntry etc.
"""
import os
import xml.dom.minidom as XML
import xml.parsers.expat as XML_Error

from WolfWriterError import *

class WWErrorXML (Exception):
    def __init__(self,raison):
        self.raison = raison
    
    def __str__(self):
        return self.raison
	
class WWNodeAbstract:
	xml_name=""
	dico_attributes={} #dictionary : (name:type)
	def __init__(self,xml_node=None,parent=None,children=None,**kargs_if_creation):
		"""
		This class represent a node in the middle or the end of the Tree of the xml.
		- xml_node : the XML node corresponding
		- parent : the parent structure corresponding to the parent xml node.
		- children : list of the children structures
		- **kargs_if_creation : in case of creation of a node (not readed in an XML 
				file), all these information will be added in the attributes (they 
				should represent an entry of dico_attributes).
		"""
		if children==None: children=[]
		self.list_atributes=[]
		self.parent		= parent
		self.children	= children
		self.xml_node	= xml_node
		self.list_revision=[]
		if xml_node==None:
			for i in kargs_if_creation.keys():
				if i not in self.dico_attributes.keys():
					raise WWError("During the creation of the node <"+self.xml_name+">, the argument <"+i+"> is not one the the argument of the Node")
			for y in kargs_if_creation.keys():
				self.list_atributes.append(y)
				self.__dict__[y]=kargs_if_creation[y]				
		else:
			self.read_attributes()
	
	def read_attributes(self):
		"""
		Will read the attributes contained in the XML node and will add them to the 
		structure if they have an entry in dico_attributes.
		"""
		if self.xml_node.attributes!=None:
			for y in self.xml_node.attributes.keys() :
				if y in self.dico_attributes.keys():
					self.list_atributes.append(y)
					self.__dict__[y]=self.dico_attributes[y](self.xml_node.getAttribute(y))
				else:
					raise WWErrorXML("The attribute <"+y+"> is not known for the node <"+self.xml_name+">")



	def xml_output(self):
		"""
		Function to re-implement to explain the production of the xml-output.
		"""
		raise NotImplementedError
	def output(self):
		"""
		This function is called when exporting the file to another format (.html,
		.txt, etc.).
		"""
		raise NotImplementedError
	
	def find(self,patern,**kargs):
		"""
		This function is called when searching some word in the class and in the 
		children.
		"""
		raise NotImplementedError
	

	def getInfo(self,info):
		"""
		This function ask for the corresponding information ask in "info", number of 
		words for instance.
		"""
		if info in self.list_atributes:
			return self.__dict__[info]
		else:
			return 0
	
	def getFirstNode(self):
		"""
		Will give the first node of the structure.
		"""
		if self.parent==None:
			raise WWError("We can not have a first node to a <"+self.xml_name+"> which has no parent.")
		return self.parent.getFirstNode()
	
	def number_in_brotherhood(self):
		"""
		Gives the place of the structure in the brotherhood.
		
		Example 
		-------
		
		If we are the node4 in the tree :
		
		seed __________ node0
		     |_________ node1
		     |_________ node2
		     |_________ node3
		     |_________ node4
		     |_________ node5
		     |_________ node6
		
		>>> node4.number_in_brotherhood()
		4
		"""
		if (self.parent!=None):
			return self.parent.children.index(self)
		return 0
		
	def insertChildren(self,position, list_objects):
		"""
		Will insert the objects contained in list_objects in the structure at the 
		given position :
		- position : shoud be 0<=position<=len(self.children) , the place where to 
		insert the objects.
		- list_objects : list of the object to insert.
		
		Example 
		-------
		If we are the node4 in the tree :
		
		seed __________ node0
		     |_________ node1
		     |_________ node2
		
		Then :
		
		>>> seed.insert(1,[node00,node01])
		
		will give :
				
		seed __________ node0
		     |_________ node00
		     |_________ node01
		     |_________ node1
		     |_________ node2
		"""
		assert 0<=position<=len(self.children)
		pos=position
		for obj in list_objects:
			
			self.children.insert(pos,obj)
			obj.parent=self
		
	def removeChildren(self,position, count):
		"""
		Will remove "count" children at the position "position".
		- position : should be 0<=position. The place were we begin to remove the 
				objects.
		- count : should be position+count<=len(self.children). The number of object 
				to remove.
				
		Example 
		-------
		
		If we have the tree
		
		seed __________ node0
		     |_________ node1
		     |_________ node2
		     |_________ node3
		     |_________ node4
		     |_________ node5
		     |_________ node6
			 
		Then the command :
		>>> seed.removeChildren(2,3)
		Will give :
		
		seed __________ node0
		     |_________ node1
		     |_________ node5
		     |_________ node6
		"""
		assert 0<=position 
		assert position+count<=len(self.children)
		removed=[]
		for i in range(count):
			rm=self.children.pop(position)
			removed.append(rm)
		return removed
			
	


class WWNodeFirstAbstract (WWNodeAbstract):
	
	def __init__(self,filepath,new=False,parent_file=None,parent=None,**kargs_if_creation):
		
		"""
		This class represent a node in the root of the tree of the xml file (like WWStructure, WWEncyclopedia and WWScene).
		- filepath : the path of the xml node.
		- new : is True if it is a new file.
		- parent_file : the name of the xml file corresponding to the structure where 
				it is called. (for instance, for a scene, we will hav the path to 
				main.xml)
		- parent : in the WolfWriter structure, what is the parent (caution, even if a 
			WWScene is a WWNodeFirstAbstract, it has as parent the WWChapter).
		- **kargs_if_creation : in case of creation of a node (not readed in an XML 
				file), all these information will be added in the attributes (they 
				should represent an entry of dico_attributes).
		"""
		self.parent_file=parent_file
		d,f=os.path.split(filepath)
		self.filename=f
		self.dirname=d
		if new:
			WWNodeAbstract.__init__(self,xml_node=None,parent=parent,**kargs_if_creation)
			self.hasChanged=True
		else:
			if not os.path.isfile(filepath):
				raise WWError("The file "+filepath+" does not exist")
			xml_node=XML.parse(filepath)
			xml_node_local=xml_node.getFirstElementsByTagName(self.xml_name)
			WWNodeAbstract.__init__(self,xml_node=xml_node_local,parent=parent,**kargs_if_creation)
			self.hasChanged=False
			
	def getFirstNode(self):
		"""
		When it is called it returns himself. It is at the top of the XML tree.
		"""
		return self
	
	def save_xml(self,dirname=None,filename=None,passNotChanged=True,prename=None):
		"""
		Will save as an xml file all the structure in a file :
		- dirname : where to save the file (if None we take the one when initiating 
				the instance.
		- filename : the name of the file (if None we take the one when initiating the 
				instance.
		- passNotChanged : if True then it will the saving if nothing have changed.
		- prename : to add to before the the filename (a temporary file mark for 
				instance.)		
		"""
		if ( passNotChanged) or (self.hasChanged):
			if dirname!=None:
				self.dirname=dirname
			if filename!=None:
				self.filename=filename
			if prename==None:
				prename=""
			
			
			doc = XML.Document()
			self.xml_output(doc,doc)
			try:
				path=os.path.join(self.dirname,prename+self.filename)
				file=open(path,"w")
				# doc.domConfig.setParameter('format-pretty-print', True)
				file.write(doc.toPrettyWithText().encode('utf-8'))
			except Exception, e:
				print e
			finally:
				file.close()

				

