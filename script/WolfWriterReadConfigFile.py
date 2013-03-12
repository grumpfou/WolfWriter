from WolfWriterError import WWError
import string
import codecs

class WWConfigFileError (Exception):
	def __init__(self,raison,line=False,file=False):
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
	comment_sign='#'
	exception_sign='\\'
	entry_separator_sign=':'
	separator_sign='|'
	def __init__(self,pathway,constants):
		
		self.pathway=pathway
		self.result_dictionary={}
		
		self.fid=codecs.open(self.pathway,'rb', "utf-8")
		try :
			self.file=self.fid.readlines()
		
		finally :
			self.fid.close()

		self.clean_file()
		for i,ligne in enumerate(self.file):
			try :
				e,v=self.interpret_ligne(ligne)
				self.result_dictionary[e]=v
			except WWConfigFileError , e:
				e_other = WWConfigFileError(e.raison,
							line=self.equivalent_line[i],
							file=self.pathway)
				
				raise	e_other
		try :
			constants.overright(**self.result_dictionary)
		except WWError , e:
			raise WWConfigFileError (e.raison,file=self.pathway)
		
				
	def clean_file(self):
		new_file=[]
		self.equivalent_line=[]
		
		i=0
		
		for indice, ligne in enumerate(self.file):
			ligne=string.strip(ligne)
			
			if ligne == "":
				pass
			elif ligne[0]==self.comment_sign:
					pass
			else:
				for i in range(1,len(ligne)):
					if ligne[i]==self.comment_sign and ligne[i-1]!=self.exception_sign:
						new_file.append(ligne[:i])
						break
				else:
					new_file.append(ligne)
				
				self.equivalent_line.append(i)
			i+=1
		self.file=new_file
	
	def interpret_ligne(self,ligne):
		# ligne.decode('utf-8')
		dp_pos=ligne.find(self.entry_separator_sign)
		if dp_pos<0:
			raise WWConfigFileError( " This line has no entry-value separator. " )
		if dp_pos==len(ligne)-1:
			raise WWConfigFileError( " This entry has no value " )
		
		
		entry 	 = ligne[:dp_pos]
		entry	 = entry.strip()
		
		line_tmp = ligne[dp_pos+1:]
		line_tmp = line_tmp.split(self.separator_sign)
		line_tmp = [value.strip() for value in line_tmp]
		
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
				
					