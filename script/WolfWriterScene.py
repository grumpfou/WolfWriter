"""
Part of the WolfWriter project. Written by Renaud Dessalles
Contains a re-implementation of the WWNodeFirstAbstract to deals with the scenes.
In the zipfile (.ww) there is every files of each of the scenes of the book. Theses files 
are under the format xml. WWScene is able to read this file and to build the object that 
will represent the scene in the software.
"""

import xml.dom.minidom as XML
import xml.parsers.expat as XML_Error
import codecs
import os
import re

from WolfWriterError import *
from WolfWriterCommon import *	
from WolfWriterNodeXML import *
from WolfWriterError import WWEvalError
		
class WWScene (WWNodeFirstAbstract):
	xml_name="scene"
	dico_attributes={"title":unicode}
	def __init__(self,pathway,new=False,parent=None,parent_file=None,**kargs_if_creation):
		# pathway : the path to the xml file of the scene
		# new is turn to True if the scene is just created and False if it is an existing 
		#	 file we are just oppening
		# parent should be the corresponding parent chapter of the scene.
		# parent_file should be the path to main.xml containing the structure of the file
		#	 from which the scene is a part of.
		# **kargs_if_creation contain all the attrite usfull when creating the scene at
		#	 first (it is in fact only the title
		WWNodeFirstAbstract.__init__(self,pathway,new=new,parent=parent,parent_file=parent_file,**kargs_if_creation)
		pathway=pathway.replace('/','\\') # TODO : it is only windows style
		d,f=os.path.split(pathway)
		self.filename=f
		self.dirname=d

		
		
		pathway=os.path.join(self.dirname,self.filename)
		if new:
			self.text=u""
			self.stats={"numberChars":0,"numberWords":0}
		else:
			self.read_text()
			self.doStats()
		
	def read_text(self):
		# Get the text contained in the "text" node and putting it in self.text
		nd=self.xml_node.getFirstElementsByTagName('text')
		if nd.hasChildNodes():
			self.text=nd.firstChild.nodeValue
		else:
			self.text=u""
		

	def doStats(self):
		# Is called when we want to make the statistics on the scene (number of words etc)
		numberChars=len(self.text)
		numberWords=len(self.text.split())
		self.stats={"numberChars":numberChars,"numberWords":numberWords}
		
		print "numberChars : ",numberChars
		print "numberWords : ",numberWords
	
	def xml_output(self,doc,parentNode):
		# It is called when we have to create the xml file. Adding the nodes to the 
		# parentNode given in entry.
		node=doc.createElement(self.xml_name)
		node.setAttribute("title",self.title)
		text_container=doc.createElement("text")
		text_node=doc.createTextNode(self.text)
		text_container.appendChild(text_node)
		node.appendChild(text_container)
		parentNode.appendChild(node)
		
	def output(self,scene_isSeparator=True,scene_separator='***\n',scene_titleSyntax="'Scene : '+self.number_in_brotherhood()+'\\n\\n'",\
					block_begin=None,block_end='\n',**kargs):
		# This function is called when exporting the file to another format (.html,
		# .txt, etc.).
		# - scene_isSeparator : is True if we just want to make a separation bewtween scene
		# - scene_separator : the string that should be the separation between scenes 
		# 		(usefull only if scene_isSeparator is True)
		# - scene_titleSyntax : string that is a python code. It will gives the form of the
		#		title in the exportation (usefull only if scene_isSeparator is False).
		# - block_begin : the string to add at the begining of each blocks
		# - block_end : the string to add at the end of each blocks
		
		to_add=u""
		if block_begin==None: block_begin=u""
		if scene_isSeparator:
			if scene_separator==None:
				scene_separator="\n"
			if self.number_in_brotherhood()>0:
				to_add+=scene_separator
				# to_add+=chapter_separator+'\n' # Attention : \\n is not allways the symbol of newline
				
		else:
			try :
				to_add = eval(scene_titleSyntax)
			except SyntaxError:
				raise WWEvalError(scene_titleSyntax)
				
		
		to_add+=block_begin+self.text.replace('\n',block_end+block_begin)+block_end #Todo
	
		return to_add		
				
		
		
	def getInfo(self,info):
		# Will give the information corresponding to the "info" attribute contains.
		if info=='title':
			try:
				number = self.parent.children.index(self) + 1
				res= "Sc "+str(number)
			except ValueError:
				res = "Sc ErrorNumber"
			if self.title!="":
				res+=" : "+self.title
			return res
		
		elif info=='numberWords':
			return self.stats["numberWords"]
		return 0
	
	def find(self,pattern,regexp=False,casse=False,entireword=False,contextdist=None):
		# Yield every instance of the given "pattern" in the scene text.
		# - regexp : True if the pattern is considered as a regular expression
		# - casse : True if the pattern is considered as casse sensitive
		# - entireword : True if we have to consider a entire word
		# - contextdist : the distant to take on both sides for the context of the instance
		# The method yield a list of 3 things :
		# - the iterator or the instance
		# - the constext in which it has been find
		# - the current scene
		# NOTE : some problems with words containing accentuate capitals.
		
		if contextdist==None:
			contextdist=CONSTANTS.SEARCH_CONTXT_DIST
		if not regexp:
			for c in [u'\\',u'.',u'^',u'$',u'*',u'+',u'?',u'{',u'}',u'[',u']',u'|',u'(',u')']:
				pattern=pattern.replace(c,u'\\'+c)
		if entireword:
			pattern=u'\\b'+pattern+u'\\b'
		args=[pattern,self.text]
		
		if not casse:
			args+=[ re.IGNORECASE ]
		
		for it in re.finditer(*args):
			context=self.text[max(0,it.start()-contextdist):min(len(self.text),it.end()+contextdist)]
			context=context.replace(u'\n',u' ')
			yield [it,context,self]
		

	
		
		
