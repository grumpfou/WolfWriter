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
		nd=self.xml_node.getFirstElementsByTagName('text')
		if nd.hasChildNodes():
			self.text=nd.firstChild.nodeValue
		else:
			self.text=u""
		

	def doStats(self):
		numberChars=len(self.text)
		numberWords=len(self.text.split())
		self.stats={"numberChars":numberChars,"numberWords":numberWords}
		
		print "numberChars : ",numberChars
		print "numberWords : ",numberWords
	
	def xml_output(self,doc,parentNode):
		node=doc.createElement(self.xml_name)
		node.setAttribute("title",self.title)
		text_container=doc.createElement("text")
		text_node=doc.createTextNode(self.text)
		text_container.appendChild(text_node)
		node.appendChild(text_container)
		parentNode.appendChild(node)
		
	def output(self,scene_isSeparator=True,scene_separator='***\n',scene_titleSyntax="'Scene : '+self.number_in_brotherhood()+'\\n\\n'",\
					block_begin=None,block_end='\n',**kargs):
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
		if contextdist==None:
			contextdist=CONSTANTS.SEARCH_CONTXT_DIST
			print 'rr'
		#return [res,context,scene[,chapter[,story]]]
		if not regexp:
			for c in [u'\\',u'.',u'^',u'$',u'*',u'+',u'?',u'{',u'}',u'[',u']',u'|',u'(',u')']:
				pattern=pattern.replace(c,u'\\'+c)
		if entireword:
			print "entireword  :  ",entireword
			pattern=u'\\b'+pattern+u'\\b'
		args=[pattern,self.text]
		
		if not casse:
			args+=[ re.IGNORECASE ]
		
		for it in re.finditer(*args):
			print "max(0,it.start()-contextdist):min(len(self.text),it.end()+contextdist)  :  \n\t\t",max(0,it.start()-contextdist),min(len(self.text),it.end()+contextdist)
			context=self.text[max(0,it.start()-contextdist):min(len(self.text),it.end()+contextdist)]
			context=context.replace(u'\n',u' ')
			print "context  :  ",context.encode('ascii','replace')
			yield [it,context,self]
		

	
		
		
