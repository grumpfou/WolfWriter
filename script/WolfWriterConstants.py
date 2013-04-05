"""
Part of the WolfWriter project. Written by Renaud Dessalles
Contains a implementation of the WWConstants. This class deals with all the contants that are
used in the project. This function contain the default values of all theses functions. There
can be overwritten using a config file (see WolfWriterReadConfigFile.py)
WWConstants contain a dictionary with the following format
- the key is a string wich contain the name of the contant
- the value is a tuple of two elements:
	- the first element if the type of the constant :
		if it is alone then it meant that the constant is a simple value with the current type
		if it is include in a list, then the constant is a list of element of the current type
	- the second element is the default value of the constant
The WWConstants.overright function takes all the elements to change in the constant value.
For instance :
>>> CONSTANTS.overright(JUSTIFY=False,INDENT=40) # will change CONSTANTS.JUSTIFY to false
			# and CONSTANTS.INDENT to 40
"""
from WolfWriterError import WWError

class WWConstants:
	"""
	- JUSTIFY 				: if you want the text to be jsutify
	- SCENE_INDENT			: for the scene edit widget : to size of the indentation
	- TEXT_INDENT				: for the encyclopedia edit widget : to size of the indentation
	- SCENE_FONT_SIZE			: for the scene edit widget : to size of the font
	- TEXT_FONT_SIZE			: for the encyclopedia edit widget : to size of the font
	- FONT					: the name of the font in the edition widgets
	- LANGUAGE				: the language of the application (for now no effect)
	- DFT_WRITING_LANGUAGE	: by default when creating a new book, what language should we choose
	- DO_AUTO_CORRECTION		: if the software replace the word described in AUTO_CORRECTION
	- DO_TYPOGRAPHY			: if the software take care of the typography
	- AUTO_CORRECTION			: the list of the word and the word to replace
	- WITH_HIGHLIGHTER		: tels if the hilighter should be active
	- NAMEGEN_RANGE_LEN		: for the name generator : the range of the length
	- NAMEGEN_DFT_LEN			: for the name generator : the default length of the name to be created
	- NAMEGEN_RANGE_NUMBER	: for the name generator : the range of the number of names to be created
	- NAMEGEN_DFT_NUMBER		: for the name generator : the range of the number of names to be created
	- SEARCH_CONTXT_DIST		: for the search pannel : the size of the context in with is presented the result
	- MAX_ZFILL				: for the temporary file, the numbers of zeros into the files (limit the number of scenes)
	- EXTERNAL_SOFT_PATH		: the full path to an external software with which we edit the scene
	- LINE_HEIGHT				: the inter-line in the edit widgets
	- TIME_STATUS_MESSAGE		: the time it leaves a message into the status bar (put 0 if it is indefinitly)
	- RECHECK_TEXT_OPEN		: tels if we have to reacheck the typography of a text when reopening it
	- DELETE_TEMP_FILES		: tels if it deletes the temporary files, the ones that are created when dezipping the files
	- ENCY_TAB_APPLY			: tels if we apply the modifications made to a page of the encyclopedia when moving
	- DLT_OPEN_SAVE_SITE		: the path to the directory where we have to open the file ("~" if you want home)		
	"""
	def __init__(self,**kargs):
		# The syntax is as follow
		# value : [type,default_value]
		self.all_constants= {
			"JUSTIFY" 				: ( bool   		  , True  		),
			"SCENE_INDENT"			: ( int    		  , 50 			),
			"TEXT_INDENT"			: ( int    		  , 20 			),
			"SCENE_FONT_SIZE"		: ( int    		  , 16 			),
			"TEXT_FONT_SIZE"		: ( int    		  , 10 			),
			"FONT"					: ( unicode 	  , "Times" 	),
			"LANGUAGE"				: ( unicode 	  , "French"	),
			"DFT_WRITING_LANGUAGE"	: ( unicode 	  , "English"	),
			"DO_AUTO_CORRECTION"	: ( bool	      , True		),
			"DO_TYPOGRAPHY"			: ( bool	      , True		),
			"AUTO_CORRECTION"		: ( [unicode]     , []			),
			"WITH_HIGHLIGHTER"		: ( bool	      , True		),
			"NAMEGEN_RANGE_LEN"		: ( [int]		  ,	[0,100]		),
			"NAMEGEN_DFT_LEN"		: ( int			  ,	5			),
			"NAMEGEN_RANGE_NUMBER"	: ( [int]		  ,	[0,100]		),
			"NAMEGEN_DFT_NUMBER"	: ( int			  ,	10			),
			"SEARCH_CONTXT_DIST"	: ( int			  , 20			),
			"MAX_ZFILL"				: ( int			  ,	4			),
			"EXTERNAL_SOFT_PATH"	: ( unicode		  ,	""			),
			"LINE_HEIGHT"			: ( float		  , 100			),
			"TIME_STATUS_MESSAGE"	: ( int			  , 3000		),
			"RECHECK_TEXT_OPEN"		: ( bool		  , False		),
			"DELETE_TEMP_FILES"		: ( bool		  , True		),
			"ENCY_TAB_APPLY"		: ( bool		  , True		),
			"DLT_OPEN_SAVE_SITE"	: ( unicode		  , "~"			)
			}
		for key in self.all_constants.keys():
			self.__dict__[key]=self.all_constants[key][1]
			
		self.overright(**kargs)
	
	def overright(self,**kargs):
		for key in kargs.keys():
			if key not in self.all_constants.keys():
				raise WWError("The key "+key+" is unkown.")
				
			if isinstance(self.all_constants[key][0],list):
				if not isinstance(kargs[key],list):
					raise WWError("The argument "+str(kargs[key])+" should be a list.")
				try :
					self.__dict__[key]=[self.all_constants[key][0][0](v) for v in kargs[key]]
				except ValueError:
					raise WWError("The arguments contained in "+str(kargs[key])+" should be convertible in "+str(self.all_constants[key][0,0]))

			else:
				try :
					self.__dict__[key]=self.all_constants[key][0](kargs[key])
				except ValueError:
					raise WWError("The arguments contained in "+str(kargs[key])+" should be convertible in "+str(self.all_constants[key][0]))				
	
	def __str__(self,only_different_from_default=False):
		res=""
		for key in self.all_constants.keys():
			if only_different_from_default and self.__dict__[key]==self.all_constants[key][1]:
				pass
			else:
				res+=key+" : "+str(self.__dict__[key])+"\n"
		return res	