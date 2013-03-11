from WolfWriterError import WWError
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

class WWConstants:
	def __init__(self,**kargs):
		# The syntax is as follow
		# value : [type,default_value]
		self.all_constants= {
			"JUSTIFY" 				: ( bool   		  , True  		),
			"INDENT"				: ( int    		  , 50 			),
			"SIZE"					: ( int    		  , 16 			),
			"FONT"					: ( unicode 	  , "Times" 	),
			"COLOR"					: ( unicode 	  , "red"		),
			"BACKGROUND_COLOR"		: ( unicode 	  , "white"		),
			"LANGUAGE"				: ( unicode 	  , "French"	),
			"ZOOM"					: ( int			  , 0			),
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
			"RECHECK_SCENE_OPEN"	: ( bool		  , False		),
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
	
	def __str__(self):
		res=""
		for key in self.all_constants.keys():
			res+=key+" : "+str(self.__dict__[key])+"\n"
		return res	