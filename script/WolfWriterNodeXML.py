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
		if self.xml_node.attributes!=None:
			for y in self.xml_node.attributes.keys() :
				if y in self.dico_attributes.keys():
					self.list_atributes.append(y)
					self.__dict__[y]=self.dico_attributes[y](self.xml_node.getAttribute(y))
				else:
					raise WWErrorXML("The attribute <"+y+"> is not known for the node <"+self.xml_name+">")



	def xml_output(self):
		raise NotImplementedError
	def txt_output(self):
		raise NotImplementedError
	
	def find(self,patern,**kargs):
		raise NotImplementedError
	

	def getInfo(self,info):
		if info in self.list_atributes:
			return self.__dict__[info]
		else:
			return 0
	
	def getFirstNode(self):
		if self.parent==None:
			raise WWError("We can not have a first node to a <"+self.xml_name+"> which has no parent.")
		return self.parent.getFirstNode()
	
	def number_in_brotherhood(self):
		if (self.parent!=None):
			return self.parent.children.index(self)
		return 0
		
	def insertChildren(self,position, list_objects):
		print "list_objects  :  ",list_objects
		assert 0<=position<=len(self.children)
		pos=position
		for obj in list_objects:
			
			self.children.insert(pos,obj)
			obj.parent=self
		
	def removeChildren(self,position, count):
		assert 0<=position 
		assert position+count<=len(self.children)
		removed=[]
		for i in range(count):
			rm=self.children.pop(position)
			removed.append(rm)
		return removed
			
	


class WWNodeFirstAbstract (WWNodeAbstract):
	
	def __init__(self,filepath,new=False,parent_file=None,parent=None,**kargs_if_creation):
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
		return self
	
	def save_xml(self,dirname=None,filename=None,passNotChanged=True,prename=None):
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

				

