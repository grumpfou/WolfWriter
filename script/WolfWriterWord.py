import string
"""
Part of the WolfWriter project. Written by Renaud Dessalles
Contains classes relative to Words, the reason I need theses classes is that I needed to
deal with the capital letters.
"""

# This static class allows to detect the format of a word and to change it:
class WWWordTools:
	IND_LOWER=1
	IND_FIRST_CAP=2
	IND_ALL_CAP=4
	
	@staticmethod
	def whatID(word):
		# return 1 ( IND_LOWER ) if the first letter is not a capital
		# return 2 ( IND_FIRST_CAP ) if the first letter is a capital (and not the rest)
		# return 4 ( IND_ALL_CAP ) if the all the letters are capitals
		# if the word is single cpaital then it return IND_FIRST_CAP
		
		if len(word)==0:
			return False
		elif word.isupper():
			if len(word)==1:
				return WWWordTools.IND_FIRST_CAP
			else:
				return WWWordTools.IND_ALL_CAP
		elif word[0].isupper():
			return WWWordTools.IND_FIRST_CAP
		else:
			return WWWordTools.IND_LOWER

	@staticmethod
	def toID(word,id):
		# return a correspondant version of the word the corresponding ID
		# Deals with composed word, for instance:
		# WWWordTools.toID("jean-louis",WWWordTools.IND_FIRST_CAP) gives "Jean-Louis"
		word=unicode(word)
		if id==WWWordTools.IND_FIRST_CAP:
			word=string.capwords(word,sep=u'-')

				
		elif id==WWWordTools.IND_ALL_CAP:
			word=word.upper()
		return word
	
    # whatID = staticmethod(whatID)
    # toID = staticmethod(toID)

class WWWordSet:
	# This class is mainly a dictionary that deals with capitalization
	# every word is goes with an id that stipulate the different version of capitilization
	# possible for the word.
	# the main attribute : WWWordSet.dico has as key the word in the lower version and the
	# value is the corresponding IDs. For instance
	# WWWordSet.addWord("apple",WWWordTools.IND_LOWER|WWWordTools.IND_FIRST_CAP) will
	# add the word "apple" which can be written with a first letter as a capital or not, but 
	# not with all letters as capitals.
	def __init__(self,data_list=None):
		self.dico={}
		if data_list!=None:
			self.input_from_list(data_list)
	
	def addWord(self,word_entry,id=None): # if id is None, all the version will be possible
		word_entry=unicode(word_entry).lower()
		if id==None:
			id=WWWordTools.IND_LOWER|WWWordTools.IND_FIRST_CAP|WWWordTools.IND_ALL_CAP
		
		self.dico[word_entry]=id
	
	def removeWord(self,word): # remove the word (whatever it version)
		word=unicode(word).lower()
		if self.dico.has_key(word):
			self.dico.remove(word)
			return True
		else:
			return False
	
	def yieldSet(self):
		list_id=[WWWordTools.IND_LOWER,WWWordTools.IND_FIRST_CAP,WWWordTools.IND_ALL_CAP]
		for word,id in self.dico.items():
			for id_tmp in list_id:
				if id_tmp&id>0:
					yield WWWordTools.toID(word,id_tmp)

		
	
	def isIn(self,word): # tell if the word is in the strucure with the same capitilization.
		word=unicode(word)
		word_tmp=unicode(word).lower()
		coresp=self.dico.get(word_tmp,False)
		if not coresp: return False
		id=WWWordTools.whatID(word)
		if (id&coresp)>0:
			return True
			
	def input_from_list(self,data_list): # add the words contained in the list their own capitalization
		for data in data_list:
			id=WWWordTools.whatID(data)
			self.addWord(data,id)
	
	# def get(self,word):
		# word=unicode(word)
		# word_tmp=unicode(word).lower()
		# coresp=self.dico.get(word_tmp,False)
		# if not coresp: return False
		# id=WWWordTools.whatID(word)
		# if id|coresp[1]>0:
			
			# return WWWordTools.toID(coresp[0],id)
		# else: return False
	
		
	
	
class WWWordDico:
	def __init__(self,data_list=None):
		self.dico={}
		if data_list!=None:
			
			self.input_from_CONSTANTS(data_list)
	
	def addWord(self,word_entry,word_out,id=None):
		word_entry=unicode(word_entry)
		word_out=unicode(word_out)
		if id==None:
			id=WWWordTools.IND_LOWER|WWWordTools.IND_FIRST_CAP|WWWordTools.IND_ALL_CAP
		
		self.dico[word_entry]=(word_out,id)
	
	def get(self,word):
		word=unicode(word)
		word_tmp=unicode(word).lower()
		coresp=self.dico.get(word_tmp,False)
		if not coresp: return False
		id=WWWordTools.whatID(word)
		if id|coresp[1]>0:
			
			return WWWordTools.toID(coresp[0],id)
		else: return False
	
	def input_from_CONSTANTS(self,data_list):
		for data in data_list:
			# print "data : ",data.encode('ascii','replace')
			data_tmp=data.strip()
			i=data_tmp.find(' ')
			if i!= -1:
				k=data_tmp[:i]
				v=data_tmp[i:].strip()
				self.addWord(k,v)
	
	def output_for_CONSTANTS(self):
		data_list=[]
		for k in self.dico.keys():
			data_list.append(k+' '+self.dico[k])

		return data_list
		