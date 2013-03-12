import xml.dom.minidom as XML
import xml.parsers.expat as XML_Error
import os.path
import random
from WolfWriterCommon import *
from WolfWriterScene import *
from WolfWriterNodeXML import *
from WolfWriterEncyclopedia import *
from WolfWriterLineEdit import *

import zipfile
import codecs







class WWBook:
	# def __init__(self,dirname=None):
		# self.list_files=os.listdir(dirname)
		# assert "main.xml" in self.list_files
		
		# filepath=os.path.join(dirname,"main.xml")
		# print "filepath : ",filepath
		# if dirname!=None:
			# self.structure=WWStructure(filepath=filepath,book=self,parent_file=None)
		
		
	def __init__(self,archivepath=None):
	
		self.archivepath=archivepath
		self.list_files=[]
		self.list_archives=[]
		
		self.dezip()
		# self.list_files=os.listdir(dirname)
		
		assert TMP_FILE_MARK+"main.xml" in self.list_files
		assert TMP_FILE_MARK+"encyclopedia.xml" in self.list_files
		dirname,f=os.path.split(self.archivepath)
		filepath_structure=os.path.join(dirname,TMP_FILE_MARK+"main.xml")
		filepath_encyclopedia=os.path.join(dirname,TMP_FILE_MARK+"encyclopedia.xml")

		if archivepath!=None:
			self.structure=WWStructure(filepath=filepath_structure,book=self,parent_file=None)
			self.encyclopedia=WWEncyclopedia(filepath=filepath_encyclopedia,book=self,parent_file=None)
		
		
		
		
		# self.story_node=root.getFirstElementsByTagName(WWStory.xml_name)
		
		# assert os.path.isfile(filepath)
		# self.filepath=filepath
		# # self.dezip() decoment when need
		# # assert self.is_correct()
		# d,f=os.path.split(self.filepath)
		
		# self.book_xml_file=XML.parse(os.path.join(d,TMP_FILE_MARK+MAIN_FILE_NAME))
		# root = xml_file.documentElement
		# self.story=root.getFirstElementsByTagName('story')
		# # self.story=root.getFirstElementsByTagName('encyclopedia') ###TODO
		
	def dezip(self):
		d,f=os.path.split(self.archivepath)
		print "d  :  ",d
		print "f  :  ",f
		
		zfile = zipfile.ZipFile(self.archivepath, 'r')
		try:
			for i in zfile.namelist():  ## On parcourt l'ensemble des fichiers de l'archive
				data = zfile.read(i)                   ## lecture du fichier compresse
				try:
					dir_arch,fil_arch=os.path.split(i)
					print "i  :  ",i
					print "dir_arch,fil_arch  :  ",dir_arch,fil_arch
					if dir_arch=='':
						j=TMP_FILE_MARK+fil_arch
						self.list_files.append(j)
						fp = open(os.path.join(d,j), "wb")  ## creation en local du nouveau fichier
						fp.write(data)                         ## ajout des donnees du fichier compresse dans le fichier local
						
					else:
						pass #for now we do not decompress the archives
						# j=os.path.join(dir_arch,TMP_FILE_MARK+fil_arch)

					print "j  :  ",j
						

				except BaseException, e:
					raise e
				finally:
					fp.close()
		finally:
			zfile.close()
	
	def rezip(self,filepath=None):
		if filepath!=None:
			dirname,filename=os.path.split(filepath)
		else:
			dirname,filename=os.path.split(self.archivepath)
		zfile = zipfile.ZipFile(os.path.join(dirname,filename), 'w')
		
		
		new_list_names=set(self.list_files)
		new_list_names.union([TMP_FILE_MARK+fname for fname in self.structure.list_associate_files])
		try:
			for f in new_list_names:
				dir_arch,fil_arch=os.path.split(f)
				if dir_arch=='':
					ff=fil_arch[len(TMP_FILE_MARK):]
				else:
					ff=os.path.join(dir_arch,fil_arch[len(TMP_FILE_MARK):])			
				
				pathway=os.path.join(dirname,f)
				zfile.write(pathway,arcname=ff)
		finally:
			zfile.close()
		self.list_files=list(new_list_names)
	
	def del_files(self,dirname=None):
		if dirname==None:
			dirname,f=os.path.split(self.archivepath)
		for i in self.list_files:
			try:
				os.remove(os.path.join(dirname,i))
			except:
				# print "struggle to supress ",i
				pass

			
	def save_book(self,filepath=None):
		if filepath!=None:
			dirname=None
		else:
			dirname,f=os.path.split(self.archivepath)
			
		self.structure.save_xml(dirname=dirname)
		self.structure.save_associate_files(dirname=dirname)
		self.encyclopedia.save_xml(dirname=dirname)
		self.upload_revision()
		self.rezip(filepath)
		
		
	def save_txt(self,filename):
		res=self.structure.txt_output()
		fichier = codecs.open(filename, encoding='utf-8', mode='w')
		try :
			fichier.write(res)
		finally:
			fichier.close()
	
	def upload_revision(self):
		pass
	
	def metadataLayout_X(self,parent=None):
		author_choose = WWLineEdit ()
		author_choose.setText (self.structure.author)
		
		projectname_choose	= WWLineEdit ()
		projectname_choose.setText (self.structure.project_name)
		
		storytitle_choose	= WWLineEdit ()
		storytitle_choose.setText (self.structure.story.title)
		
		layout_info=QtGui.QFormLayout()
		layout_info.addRow("&Author : ",author_choose)
		layout_info.addRow("&ProjectName : ",projectname_choose)
		layout_info.addRow("&StoryTitle : ",storytitle_choose)
		
		return (layout_info, author_choose,projectname_choose,storytitle_choose)	
	
	def metadataDialog_X(self,parent=None):
		layout_info, author_choose,projectname_choose,storytitle_choose=self.metadataLayout_X()
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
			self.structure.author=unicode(author_choose.text())
			self.structure.project_name=unicode(projectname_choose.text())
			self.structure.story.title=unicode(storytitle_choose.text())
			dialog.accept()
			
		
		dialog.connect(quitter, QtCore.SIGNAL("clicked()"), dialog, QtCore.SLOT("close()"))
		dialog.connect(generer, QtCore.SIGNAL("clicked()"), generateEntry)
		
		return dialog
		
	def save_archive(self,name=None):
		if name == None:
			name=str(WWDate())
		
		dirpath,f=os.path.split(self.archivepath)
			
		dir_archive_path=os.path.join(dirpath,name)
		os.mkdir(dir_archive_path)
		self.structure.save_xml(dirname=dir_archive_path)
		self.structure.save_associate_files(dirname=dir_archive_path)
		self.encyclopedia.save_xml(dirname=dir_archive_path)
		
		new_list_names=[os.path.join(name,TMP_FILE_MARK+fname) for fname in self.structure.list_associate_files]+\
							[os.path.join(name,TMP_FILE_MARK+'encyclopedia.xml'),os.path.join(name,TMP_FILE_MARK+'main.xml')]
		self.list_files=list(set(self.list_files+new_list_names))
		self.list_archives.append(name)
		
	# def xml_output(self,doc,parentNode):
		
		# node=doc.createElement('structure')
		# # self.encyclopedia.xml_output(doc,parentNode)
		# self.story.xml_output(doc,node)
		# parentNode.appendChild(node)
	# # def rezip(self):
		
class WWStructure (WWNodeFirstAbstract):
	xml_name="structure"
	dico_attributes={"project_name":unicode,"author":unicode,"creation_date":int,"versionXML_WW":unicode} 
	
	def __init__(self,filepath,book=None,parent_file=None,**kargs_if_creation):
		if book==None:
			WWNodeFirstAbstract.__init__(self,filepath,new=True,parent_file=parent_file,**kargs_if_creation)	
			self.book=WWBook() #TODO
			assert self.versionXML_WW==VERSIONXML_WW
		else:
			WWNodeFirstAbstract.__init__(self,filepath,new=False,parent_file=parent_file,**kargs_if_creation)	
			self.book=book
			
		# TODO
		# self.encyclopedia_node=root.getFirstElementsByTagName(WWEncyclopedia.xml_name)
		# self.encyclopedia=WWEncyclopedia(xml_node=self.encyclopedia_node,parent=self)
		# TODO
		self.list_associate_files=[]
		
		story_node=self.xml_node.getFirstElementsByTagName(WWStory.xml_name)

		self.story=WWStory(xml_node=story_node,parent=self)
		
		
	def xml_output(self,doc,parentNode):
		node=doc.createElement(self.xml_name)
		# TODO
		# self.encyclopedia.xml_output(doc,node) 
		# TODO
		for i in self.list_atributes: node.setAttribute(i,unicode(self.__dict__[i]))
		self.story.xml_output(doc,node)
		parentNode.appendChild(node)	

	def txt_output(self):
		res=u""
		res+=self.story.title
		res+=u"Author : "+self.author+u"\n\n"
		res+=self.story.txt_output()
		return res
		
	def save_associate_files(self,dirname=None):
		if dirname==None:
			dirname=self.dirname
		else :
			self.dirname=dirname
		for ch in self.story.list_chapters:
			ch.saveScenes(dirname=dirname)
		# TODO for the encyclopedia	# TODO

	def find(self,patern,**kargs):
		for word in self.story.find(patern,**kargs):
			yield word
			
	def create_new_scene(self,title="Untitled"):

		newname="Scene0000.xml"
		for i in range(1,10000):
			print "self.getFirstNode().list_associate_files  :  ",self.getFirstNode().list_associate_files
			if newname not in self.getFirstNode().list_associate_files:
				break
			else :
				newname="Scene"+str(i).zfill(CONSTANTS.MAX_ZFILL)+".xml"
				

			
			
		filepath=os.path.join(self.getFirstNode().dirname,TMP_FILE_MARK+newname)
		self.getFirstNode().book.list_files+=[TMP_FILE_MARK+newname]
		newScene=WWScene(pathway=filepath,new=True,parent=None,parent_file=self.getFirstNode(),title=title)
		
		return newScene

			
class WWStory (WWNodeAbstract):
	xml_name="story"
	dico_attributes={"title":unicode,"date":unicode} 

	
	def __init__(self,xml_node,parent=None):
		WWNodeAbstract.__init__(self,xml_node,parent=parent)
		self.list_chapters=[]
		self.children=self.list_chapters
		self.make_list_chapters()
		self.doStats()
		
	def make_list_chapters(self):
		for n in self.xml_node.getDirectElementsByTagName(WWChapter.xml_name):
			ch=WWChapter(n,self)
			self.list_chapters.append(ch)
	
	
	def addChapter(self,place=-1,title="UntitledChapter",title_first_scene="UntitledScene"):
		raise NotImplementedError
		if place==-1:
			place=len(self.list_chapters)
		assert 0<=place<=len(self.list_chapters)
		new_chapter=WWChapter(xml_node=None,
				parent=self,
				title_first_scene=title_first_scene,
				title=title 
				)
		self.list_chapters.insert(place,new_chapter)
		return new_chapter

		
		
		
	def deleteChapter(self,place):
		raise NotImplementedError
		assert 0<=place<len(self.list_chapters)
		# self.add_revision("deleteChapter",place=place)
		self.list_chapters.pop(place)
		
	def moveChapter(self,initPlace,newPlace):
		assert 0<=initPlace<len(self.list_chapters)
		assert 0<=newPlace<len(self.list_chapters)
		# self.add_revision("moveChapter",initPlace=initPlace,newPlace=newPlace)
		tmp_chapter=self.list_chapters.pop(initPlace)
		self.list_chapters.insert(newPlace,tmp_chapter)
		
		
	def changeTitle(self,newTitle,origin="local"):
		self.title=newTitle

	def xml_output(self,doc,parentNode):
		node=doc.createElement(self.xml_name)
		for sc in self.list_chapters:
			sc.xml_output(doc,node)
		for i in self.list_atributes: node.setAttribute(i,unicode(self.__dict__[i]))
		parentNode.appendChild(node)
		
	def txt_output(self,chapter_number='romain',scene_sep=u'***'):
		res=u''
		for i,ch in enumerate(self.list_chapters):
			res+=u"Chapitre "+WWRomanNumber(i+1)+u"\n\n"
			number_scenes=len(ch.children)
			for j,sc in enumerate(ch.children):
				res+=sc.txt_output()
				if j<number_scenes-1:
					res+=u"\n\n"+scene_sep+u"\n\n"
		return res
			
	def doStats(self):
		numberChars=0
		numberWords=0
		for ch in self.list_chapters:
			numberChars+=ch.stats["numberChars"]
			numberWords+=ch.stats["numberWords"]
			# print "numberChars : ",numberChars
			# print "numberWords : ",numberWords
		self.stats={"numberChars":numberChars,"numberWords":numberWords}			
			
	def getInfo(self,info):
		if info=='numberWords':
			return self.stats["numberWords"]
		else:
			return WWNodeAbstract.getInfo(self,info)
	
	def find(self,patern,**kargs):
		for ch in self.list_chapters:
			for word in ch.find(patern,**kargs):
				yield word+[self]

class WWChapter (WWNodeAbstract):
	xml_name="chapter"	
	dico_attributes={"title":unicode} #dictionary : (name:type)

	def __init__(self,xml_node=None,parent=None,**kargs_if_creation):
		
		
		self.children_names = []
		self.children = []
		self.children=self.children
		if xml_node!=None:
			WWNodeAbstract.__init__(self,xml_node,parent)
			self.read_scenes()
			self.doStats()
		else:
			# title_first_scene=kargs_if_creation.pop("title_first_scene")
			WWNodeAbstract.__init__(self,xml_node=None,parent=parent,**kargs_if_creation)	
			# self.addScene(title=title_first_scene)
			self.stats={"numberChars":0,"numberWords":0}
			
	def read_scenes(self):
		for link_node in self.xml_node.getDirectElementsByTagName("scene_link"):
			link=link_node.getAttribute('value')
			# title=link_node.getAttribute('title')
			filepath=os.path.join(self.getFirstNode().dirname,TMP_FILE_MARK+link)
			self.children.append(WWScene(pathway=filepath,parent=self,parent_file=self.getFirstNode()))
			
			self.getFirstNode().list_associate_files.append(link)
			self.children_names.append(link)###########TODO
	

	
	
		
	
	def deleteScene(self,place=-1):
		raise NotImplementedError
		if place==-1: place=len(self.children)-1
		assert 0<=place<len(self.children)
		name=self.children_names.pop(place)
		self.children.pop(place)
		self.getFirstNode().list_associate_files.remove(name)

	def moveScene (self,initPlace,newPlace,otherChapter=None):
		raise NotImplementedError
		if otherChapter==None:
			otherChapter=self
			assert 0<=initPlace<len(self.children)
			assert 0<=newPlace<len(otherChapter.children)
		else :
			assert isinstance(otherChapter,WWChapter)
			assert 0<=initPlace<len(self.children)
			assert 0<=newPlace<=len(otherChapter.children)
		tmp_sc=self.children.pop(initPlace)
		tmp_sc_name=self.children_names.pop(initPlace)
		
		otherChapter.children.insert(newPlace,tmp_sc)
		otherChapter.children_names.insert(newPlace,tmp_sc_name)


	def insertChildren(self,position, list_objects):
		WWNodeAbstract.insertChildren(self,position, list_objects)
		self.cheak_children_names()
	def removeChildren(self,position, count):
		removed = WWNodeAbstract.removeChildren(self,position, count)
		self.cheak_children_names()
		return removed
		
	
	def cheak_children_names(self):
		new_children_names=[]
		for sc in self.children:
			tmp,link=os.path.split(sc.filename)
			link=link[len(TMP_FILE_MARK):] #we remove the TMP_FILE_MARK from the link
			new_children_names.append(link)
		self.children_names=new_children_names
		
	def changeTitle(self,newTitle,origin="local"):
		self.title=newTitle
	
	
		
	def xml_output(self,doc,parentNode):
		node=doc.createElement(self.xml_name)
		# for rev in self.list_revision:
			# rev.xml_output(doc,node)
		for i,sc in enumerate(self.children_names):
			node_scene_link=doc.createElement("scene_link")
			node_scene_link.setAttribute("value",sc)
			node_scene_link.setAttribute("title",
				self.children[i].title)
			node.appendChild(node_scene_link)
		for i in self.list_atributes: node.setAttribute(i,unicode(self.__dict__[i]))
		parentNode.appendChild(node)
	
	def doStats(self):
		numberChars=0
		numberWords=0
		for sc in self.children:
			numberChars+=sc.stats["numberChars"]
			numberWords+=sc.stats["numberWords"]
			# print self.title+"numberChars : ",numberChars
			# print self.title+"numberWords : ",numberWords
		self.stats={"numberChars":numberChars,"numberWords":numberWords}
			
	def saveScenes(self,dirname):
		for i in range(len(self.children_names)):
			self.saveScene(place=i,dirname=dirname)
	def saveScene(self,place,dirname=None):
		assert 0<=place<len(self.children)
		if dirname==None : dirpath=self.getFirstNode().dirname
		self.children[place].save_xml(dirname=dirname,filename=TMP_FILE_MARK+self.children_names[place])
	
	def getInfo(self,info):
		if info=='numberWords':
			return self.stats["numberWords"]
		elif info=='title':
			try:
				number = self.parent.list_chapters.index(self) + 1
				res= "Ch "+WWRomanNumber(number)
			except ValueError:
				res = "Ch ErrorNumber"
			if self.title!="":
				res+=" : "+self.title
			return res
		
		else:
			return WWNodeAbstract.getInfo(self,info)
			
	def find(self,patern,**kargs):
		for sc in self.children:
			for word in sc.find(patern,**kargs):
				yield word+[self]

if __name__ == '__main__':
	pp="C:/Users/Renaud/Documents/Programmation/Python/Writing_help/WolfWriter/Test/testa.zip"
	bk=WWBook(pp)
	
	doc = XML.Document()
	bk.structure.xml_output(doc,doc)
	print doc.toprettyxml()	
	print (bk.structure.txt_output()).encode('ascii','replace')
	
	# pp="C:\Users\Renaud\Documents\Python\Writing_help\WolfWriter\Test\masterpiece.xml"
	# xml_file=XML.parse(pp)
	# root = xml_file.documentElement
	# n=root.getFirstElementsByTagName('story')
	# sh=WWStory(xml_node=n,path=pp)
	