"""
Part of the WolfWriter project. Written by Renaud Dessalles
Contains the WWExportAbstract class and its reimplementations of the QMainWindow. The classes will
allow the software to export the given book to several possible formats.
Each reimplementation of WWExportAbstract should contain :
- the extension (for instance 'txt' for .txt exportations).
- options_dft which is the default dictionary of the Export calss to gives in the WWStructure.output function
"""
import copy
import codecs
import os


class WWExportAbstract:
	extension=None
	options_dft={}
	def __init__(self,book):
		self.book=book
		self.options=copy.copy(self.options_dft)
	
	def preview(self,options):
		raise NotImplementedError
	
	def convert(self):
		return self.book.structure.output(**self.options)
	
	def save(self,filename):
		
		res=self.convert()
		fichier = codecs.open(filename, encoding='utf-8', mode='w')
		path,ext=os.path.splitext(filename)
		assert ext[1:]==self.extension
		try :
			fichier.write(res)
		finally:
			fichier.close()
		
class WWExportTxt (WWExportAbstract):
	extension='txt'
	options_dft=dict(
		structure_withTitle		=	True,
		structure_titleSyntax	=	"self.story.title+'\\n\\n'",
		structure_withAuthor	=	True,
		structure_authorSyntax	=	"'Author : '+self.author+'\\n\\n'",
		chapter_isSeparator		=	False,
		# chapter_separator		=	'***\n',
		chapter_titleSyntax		=	"'\\nChapter '+WWRomanNumber(self.number_in_brotherhood()+1)+' : '+self.title+'\\n\\n'",
		scene_isSeparator		=	True,
		scene_separator			=	'\n***\n\n'
		# scene_titleSyntax		=	"'Scene : '+self.number_in_brotherhood()+'\\n\\n'"
				)
		

		
		
		
class WWExportHtml (WWExportAbstract):
	extension='html'
	options_dft=dict(
		structure_beforeSyntax	=	u""" '<?xml version="1.0" encoding="UTF-8"?>\\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">\\n<head>\\n  <title>'+self.story.title+ '</title>  \\n  <link rel="stylesheet" href="style.css" type="text/css"/>\\n  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\\n  <meta name="Author" content="' +self.author+'"/>\\n</head>\\n<body>\\n'""",		
		structure_afterSyntax	=	u"'\\t</body>\\n</html>'",
		structure_withTitle		=	True,
		structure_titleSyntax	=	"'<h1>'+self.story.title+'</h1>\\n\\n'",
		structure_withAuthor	=	True,
		structure_authorSyntax	=	"'<p>Author : '+self.author+'</p>\\n\\n'",
		chapter_isSeparator		=	False,
		# chapter_separator		=	'***\n',
		chapter_titleSyntax		=	"'<h2>Chapter '+WWRomanNumber(self.number_in_brotherhood()+1)+' : '+self.title+'</h2>\\n'",
		scene_isSeparator		=	True,
		scene_separator			=	'<p><br>***<br></p>\n',
		# scene_titleSyntax		=	"'Scene : '+self.number_in_brotherhood()+'\\n\\n'",
		block_begin				=	'<p>',
		block_end				=	'</p>\n'
				)

		
	# def convert(self):
		
		# after_body=u"\t</body>\n</html>"

	# def convert(self):
		# raise self.book.output()

WWExportList=[WWExportTxt,WWExportHtml]

if __name__ == '__main__':
	from WolfWriterBook import *
	# from WolfWriterCharTable import *
	pp="C:\\Users\\Renaud\\Documents\\Programmation\\Python\\WolfWriter_Test\\TestPerso\\testa.zip"
	
	
	bk=WWBook(zippath=pp)

	export=WWExportHtml(bk)
	print export.convert().encode('ascii','replace')
	
	# sys.exit(textedit.exec_())