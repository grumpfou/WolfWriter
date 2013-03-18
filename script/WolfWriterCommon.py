import xml.dom.minidom as XML
import xml.parsers.expat as XML_Error
import datetime
import os
import sys
# import string
import re
from PyQt4 import QtCore,QtGui

"""
Part of the WolfWriter project. Written by Renaud Dessalles
This file contain some simple function that might be use in all the source files.
It is a Melding pot of all kind of functions and constants
"""

# Here we create the CONTANTS instance.
from WolfWriterConstants import *
CONSTANTS = WWConstants()

from WolfWriterReadConfigFile import *


TMP_FILE_MARK='~'			# It is prefix of an temporary file
MAIN_FILE_NAME='main.xml'   # The wich of the zip file that contains the 
							# main structure of the project
DEPTH_SCENE=3               # The Depth of the Scene :
							# for now DepthStory = 1, DepthChapter = 2, DepthChapter = 3 
VERSIONXML_WW="0.9"         # The version of the zip files


SPACE_SIMILAR=[u' ',u'\n',u'\u00A0'] # All the char that are similar to a space

#path to the softwares options files relitively from the place of WolfWriterMainWindow.py
rel_path_constants_file	= "..\\config\\config.txt"	# path to the configuration file
rel_path_new_book		= "..\\config\\NewBook.zip"		# path to a default book
rel_path_icon			= "..\\icon\\"						# path to the icons directory

#calculing the absolute to the softwares options files
abs_path_WWMainWindow,tmp= os.path.split(sys.argv[0])
abs_path_constants_file	= os.path.join(abs_path_WWMainWindow,rel_path_constants_file)
abs_path_new_book		= os.path.join(abs_path_WWMainWindow,rel_path_new_book		)
abs_path_icon			= os.path.join(abs_path_WWMainWindow,rel_path_icon			)

WWReadConfigFile(os.path.join(sys.argv[0],abs_path_constants_file),CONSTANTS) # overload the CONTANTS attribute by the 
												# config_file's information.





def WWRomanNumber(number):
	"""Function that from a int return a string of the correspondant number in Roman numerals.
	Works for evry number from 1 to 4999"""
	
	if number>4999 or number<1:
		raise OverflowError("The should be between 1 and 4999")
	numerals = { 1 : "I", 4 : "IV", 5 : "V", 9 : "IX", 10 : "X", 40 : "XL",
				50 : "L", 90 : "XC", 100 : "C", 400 : "CD", 500 : "D", 900 : "CM", 1000 : "M" }
	result = ""
	for value, numeral in sorted(numerals.items(), reverse=True):
		while number >= value:
			result += numeral
			number -= value
	return result

# A spetial function that just return the same thing.
def WWIdentity(object):
	return object

# This class deals with the dates in the format YYYYMMDDHHMinMinSS
# >>> WWDate() #create the date from the current time
# >>> WWDate("20121115111213") #create the date correspondig to
#		#the 15 november 2012, at 11 hours 11 minutes and 11 sec
class WWDate:
	def __init__(self,obj=None):
		if obj==None: 
			date=datetime.datetime.now()
			obj=date.strftime("%Y%m%d%H%M%S")	
		# obj=str(obj)
		if len(obj)!=14:
			raise WWErrorXML("The date <"+obj+"> is not correct, it has a lenght of "+unicode(len(obj)))
		
		self.year	=int(obj[:4]    )
		self.mounth	=int(obj[4:6]   )
		self.day	=int(obj[6:8]   )
		self.hour	=int(obj[8:10]  )
		self.min	=int(obj[10:12] )
		self.sec	=int(obj[12:]   )
		self.assert_valid()
	
	def assert_valid(self):
		assert 0<self.mounth <=12
		assert 0<self.day <=31
		assert 0<=self.hour <24
		assert 0<=self.min <60
		assert 0<=self.sec <60
		
	
	def __str__(self):
		res = str(self.year).zfill(4)+ str(self.mounth).zfill(2)+ str(self.day).zfill(2)+ \
					str(self.hour).zfill(2)+ str(self.min).zfill(2)+ str(self.sec).zfill(2)
		return res

		
		
# These functions are added to the XML.Node structure :
def getDirectElementsByTagName_WW(self,name):
	# allows from a name to yield every elements with a specific tag name
	node=self.firstChild
	while node!=None:
		if node.nodeType==XML.Node.ELEMENT_NODE and node.tagName==name:
			yield node
		node=node.nextSibling
def getFirstElementsByTagName_WW(self,name):
	# allows from a name to have the first element with a specific tag name
	node=self.firstChild
	while node!=None:
		if node.nodeType==XML.Node.ELEMENT_NODE and node.tagName==name:
			return node
		node=node.nextSibling
	return None
def hasDirectElementsByTagName_WW(self,name,number=None):
	# return true if it has the corresponding element with the correct tag name
	node=self.firstChild
	i=0
	while node!=None:
		if node.nodeType==XML.Node.ELEMENT_NODE and node.tagName==name:
			if number==None:
				return True
				break
			i=i+1
		node=node.nextSibling
	if number!=None and i==number:
		return True
	return False
	
def toPrettyWithText_WW(self):
	# allows to have a string representation of the XML structure that has the text node
	# just between the including nodes : Before we had
	# >>> ...
	# >>> 	<text>
	# >>> 		SomeText
	# >>> 	</text>
	# >>> ...
	# And with this function :
	# >>> ...
	# >>> 	<text>SomeText</text>
	# >>> ...
	uglyXml = self.toprettyxml(indent='  ')
	text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)    
	prettyXml = text_re.sub('>\g<1></', uglyXml)
	return prettyXml
# We add these functions to the XML.Node struture. 
XML.Node.hasDirectElementsByTagName=hasDirectElementsByTagName_WW
XML.Node.getFirstElementsByTagName=getFirstElementsByTagName_WW
XML.Node.getDirectElementsByTagName=getDirectElementsByTagName_WW
XML.Node.toPrettyWithText=toPrettyWithText_WW


# Simple function added to the struture QModelIndex that allows to have to distance to the root
def distanceToRoot_WW(self):
	index=QtCore.QModelIndex(self)
	i=0
	while index!=QtCore.QModelIndex():
		index=index.parent()
		i+=1
	return i
QtCore.QModelIndex.distanceToRoot=distanceToRoot_WW


# class WWRevision:
	# ###TODO Faire la meme methode que pour node abstract
	# xml_name="rev"
	# def __init__(self,xml_node=None,dico=None,**kargs_if_creation):
		# self.list_value=[]
		# if xml_node==None:
			# self.date	= WWDate()
			# for y in kargs_if_creation.keys():
				# self.list_value.append(y)
				# self.__dict__[y]=kargs_if_creation[y]
		# else : 
			# if not xml_node.hasAttribute('name'):
			# # if not xml_node.hasDirectElementsByTagName('name'):
				# raise WWErrorXML("The revision node has no attribute <name>.")
			# # if not xml_node.hasDirectElementsByTagName('date'):
			# if not xml_node.hasAttribute('date'):
				# raise WWErrorXML("The revision node has no attribute <date>.")
				
			
			# self.name	= xml_node.getAttribute('name')
			# self.date	= WWDate(xml_node.getAttribute('date'))
			
			# keyss=xml_node.attributes.keys()[:]
			# keyss.remove('name')
			# keyss.remove('date')
			
			# for y in keyss:
				# assert y in dico.keys()
				# self.list_value.append(y)
				# self.__dict__[y]=dico[y](xml_node.getAttribute(y))
				
			
	# def xml_output(self,doc,parentNode):
		# node=doc.createElement(self.xml_name)
		# node.setAttribute("name", self.name)
		# for i in self.list_value[::-1]: node.setAttribute(i,unicode(self.__dict__[i]))
		# node.setAttribute("date", unicode(self.date))		
		# parentNode.appendChild(node)

	
# class WWWordTools:
	# IND_LOWER=1
	# IND_FIRST_CAP=2
	# IND_ALL_CAP=4
	
	# @staticmethod
	# def whatID(word):
		# if len(word)==0:
			# return False
		# elif word.isupper():
			# if len(word)==1:
				# return WWWordTools.IND_FIRST_CAP
			# else:
				# return WWWordTools.IND_ALL_CAP
		# elif word[0].isupper():
			# return WWWordTools.IND_FIRST_CAP
		# else:
			# return WWWordTools.IND_LOWER

	# @staticmethod
	# def toID(word,id):
		# word=unicode(word)
		# if id==WWWordTools.IND_FIRST_CAP:
			# word=string.capwords(word,sep=u'-')

				
		# elif id==WWWordTools.IND_ALL_CAP:
			# word=word.upper()
		# return word
	
    # # whatID = staticmethod(whatID)
    # # toID = staticmethod(toID)

# class WWWordSet:
	# def __init__(self,data_list=None):
		# self.dico={}
		# if data_list!=None:
			
			# self.input_from_list(data_list)
	
	# def addWord(self,word_entry,id=None):
		# word_entry=unicode(word_entry).lower()
		# if id==None:
			# id=WWWordTools.IND_LOWER|WWWordTools.IND_FIRST_CAP|WWWordTools.IND_ALL_CAP
		
		# self.dico[word_entry]=id
	
	
	
	# def removeWord(self,word):
		# word=unicode(word).lower()
		# if self.dico.has_key(word):
			# self.dico.remove(word)
			# return True
		# else:
			# return False
	
	# def yieldSet(self):
		# list_id=[WWWordTools.IND_LOWER,WWWordTools.IND_FIRST_CAP,WWWordTools.IND_ALL_CAP]
		# for word,id in self.dico.items():
			# for id_tmp in list_id:
				# if id_tmp&id>0:
					# yield WWWordTools.toID(word,id_tmp)

		
	
	# def isIn(self,word):
		# word=unicode(word)
		# word_tmp=unicode(word).lower()
		# coresp=self.dico.get(word_tmp,False)
		# if not coresp: return False
		# id=WWWordTools.whatID(word)
		# if (id&coresp)>0:
			# return True
	# def input_from_list(self,data_list):
		# for data in data_list:
			# id=WWWordTools.whatID(data)
			# self.addWord(data,id)
	
	# # def get(self,word):
		# # word=unicode(word)
		# # word_tmp=unicode(word).lower()
		# # coresp=self.dico.get(word_tmp,False)
		# # if not coresp: return False
		# # id=WWWordTools.whatID(word)
		# # if id|coresp[1]>0:
			
			# # return WWWordTools.toID(coresp[0],id)
		# # else: return False
	
		
	
	
# class WWWordDico:
	# def __init__(self,data_list=None):
		# self.dico={}
		# if data_list!=None:
			
			# self.input_from_CONSTANTS(data_list)
	
	# def addWord(self,word_entry,word_out,id=None):
		# word_entry=unicode(word_entry)
		# word_out=unicode(word_out)
		# if id==None:
			# id=WWWordTools.IND_LOWER|WWWordTools.IND_FIRST_CAP|WWWordTools.IND_ALL_CAP
		
		# self.dico[word_entry]=(word_out,id)
	
	# def get(self,word):
		# word=unicode(word)
		# word_tmp=unicode(word).lower()
		# coresp=self.dico.get(word_tmp,False)
		# if not coresp: return False
		# id=WWWordTools.whatID(word)
		# if id|coresp[1]>0:
			
			# return WWWordTools.toID(coresp[0],id)
		# else: return False
	
	# def input_from_CONSTANTS(self,data_list):
		# for data in data_list:
			# # print "data : ",data.encode('ascii','replace')
			# data_tmp=data.strip()
			# i=data_tmp.find(' ')
			# if i!= -1:
				# k=data_tmp[:i]
				# v=data_tmp[i:].strip()
				# self.addWord(k,v)
	
	# def output_for_CONSTANTS(self):
		# data_list=[]
		# for k in self.dico.keys():
			# data_list.append(k+' '+self.dico[k])

		# return data_list

# add a simple function to the QCheckBox that return the checked state of the CheckBox
def isChecked_WW(self):
	# assert not self.isTristate
	assert not self.isTristate()
	if self.checkState () == QtCore.Qt.Checked:
		return True
	else :
		return False
QtGui.QCheckBox.isChecked=isChecked_WW
		
# Tells if the string contains only figure
def has_only_figures(obj):
	fig=[str(i) for i in range(10)]
	for i in range(len(obj)):
		if i not in fig:
			return False
	return True

def yieldBlockInSelection_WW(self):
	pos1=self.selectionStart()
	pos2=self.selectionEnd ()
	
	startCursor=QtGui.QTextCursor(self)
	endCursor=QtGui.QTextCursor(self)
	startCursor.setPosition(pos1)
	endCursor  .setPosition(pos2)

	bl=startCursor.block()
	bl_end=endCursor.block()
	yield bl
	while bl!=bl_end:
		bl=bl.next()
		yield bl
QtGui.QTextCursor.yieldBlockInSelection=yieldBlockInSelection_WW
