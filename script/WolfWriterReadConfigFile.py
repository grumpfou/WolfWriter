"""
Part of the WolfWriter project. Written by Renaud Dessalles.
Contain the WWReadConfigFile class that will read the config.txt file to overwrite the 
constants that are contained in the file.
This python file is called from WolfWriterCommon.py to create the object CONSTANTS. It 
is this object which is used in all over the program.
"""

import string
import codecs

from WolfWriterError import WWError

class WWConfigFileError (WWError):
	def __init__(self,raison,line=False,file=False):
		"""Special Error function for the config file (is normaly able to gives the 
		line of the error in the config file, but it is approximative ^^"""
		self.raison	= raison
		self.line	= line
		self.file	= file
		print self
	def __str__(self):
		res=""
		if self.file :
			res+="In file "+self.file+" : "
		if self.line:
			res+="To line "+str(self.line)+" : "
		
		res+=self.raison
		
		return res.encode('ascii','replace')
		

class WWReadConfigFile:
	comment_sign='#' #The sign that will indicate that what is remaining from the line 
						# is a comment
	exception_sign='\\' # '\#' '\|' will not considered a special sign in the file
	entry_separator_sign=':' # a constant in the file shall have the form of
								# " constant_key : constant_value "
	separator_sign='|' #the calues chall be separated by this sign
	def __init__(self,pathway,constants):
		"""
		- pathway : the path to the "config.txt" file
		- constants : the WWConstants instance that will be overright
		"""
		
		self.pathway=pathway
		self.result_dictionary={}
		
		# We read the config.txt file
		self.fid=codecs.open(self.pathway,'rb', "utf-8")
		try :
			self.file=self.fid.readlines()
		finally :
			self.fid.close()

		# We get rid of the comments and empty lines
		self.clean_file()
		
		# We fill the self.result_dictionary with the values contained into the file
		for i,ligne in enumerate(self.file):
			try :
				# We call the method interpret_ligne to seperate the key from the values
				e,v=self.interpret_ligne(ligne)
				self.result_dictionary[e]=v
			except WWConfigFileError , e:
				e_other = WWConfigFileError(e.raison,
							line=self.equivalent_line[i],
							file=self.pathway)
				
				raise	e_other
				
		# We try to overight the file (some conversion error might occur if the config 
		# file was not correct:
		try :
			constants.overright(**self.result_dictionary)
		except WWError , e:
			raise WWConfigFileError (e.raison,file=self.pathway)
		
				
	def clean_file(self):
		"""
		This function will get rid of the empty line and the comments in self.file.
		"""
		new_file=[]
		self.equivalent_line=[]
		
		i=0
		
		for indice, ligne in enumerate(self.file):
			ligne=string.strip(ligne) #we remove the spaces at the begining end at the 
																				# end.
			
			if ligne == "":
				pass #if it is empty, we consider nothing
			elif ligne[0]==self.comment_sign:
					pass #if it all the line is a commment, we consider nothing
			else:
				for i in range(1,len(ligne)):
					# if we encouter the comment_sign, we get rid of the end of the line
					if ligne[i]==self.comment_sign and ligne[i-1]!=self.exception_sign:
						new_file.append(ligne[:i])
						break
				else:
					new_file.append(ligne)
				
				self.equivalent_line.append(i)
			i+=1
		self.file=new_file
	
	def interpret_ligne(self,ligne):
		"""
		Will interpret the line : it will seperate the entry from the value (separeted by self.entry_separator_sign and the values from each others by  self.separator_sign.
		It will return :
		- (entry,value) : if there is only one value
		- (entry,[value1,value2,...]) : if there is more that one value
		"""
		dp_pos=ligne.find(self.entry_separator_sign) #the position of the separator
		if dp_pos<0:
			raise WWConfigFileError( " This line has no entry-value separator. " )
		if dp_pos==len(ligne)-1:
			raise WWConfigFileError( " This entry has no value " )
		
		# We find the entry
		entry 	 = ligne[:dp_pos]
		entry	 = entry.strip() # get rid of the spaces from each part
		
		# We find the values
		line_tmp = ligne[dp_pos+1:]
		line_tmp = line_tmp.split(self.separator_sign)
		line_tmp = [value.strip() for value in line_tmp]
		
		# We return the result depending on the number of values
		if len(line_tmp)==1:
			return entry, line_tmp[0]
		else:
			return entry, line_tmp
		
		

		

if __name__ == "__main__":
	from WolfWriterConstants import *
	path = "C:\\Users\\Renaud\\Documents\\Programmation\\Python\\WolfWriter\\config\\config.txt"
	CONSTANTS = WWConstants()
	print CONSTANTS
	WWReadConfigFile(path,CONSTANTS)
	print CONSTANTS.__str__(True)
				
					