"""
Part of the WolfWriter project. Written by Renaud Dessalles.
Contains a re-implementation of the WWRuleAbstract. Each of these class codes for a 
typography rule in a given language. They are used in the WWLanguge classses in order to make
corections.
Every rule should reimplement the following attributes.
- title : the title will be display in the status bar of the main Windows, it should be a line
	long description of the rule.
- decription : it is a more complete descritpion of the rule stating precicesly what the rule 
	is doing, with exemples
- correct : this method will make the correction. It has in entry the left and right character,
	and check if they are correct. It corrects the possible errors. It should return True if
	there has been an correction of False otherwise.
	
Note: it is possible in the "correct" reimplementation to have access to more distant 
	charaters via self.language.lastChar and self.language.nextChar.
"""


class WWRuleAbstract:
	title="None"
	description="None"
	in_languges=[]
	def __init__(self,language):
		self.language=language
		pass
	
	def __str__(self):
		return title+'\n'+description
	
	def correct(self,last_char,next_char,cursor):
		raise NotImplementedError
		return False


class WWRuleEnglish0001 (WWRuleAbstract):
	title="No space before a space or a break of line"
	description=	\
		"It deletes the space before another space of a break of line\n \n\
		example :	'A  thing' -> 'A thing' \n\
					'end of block. \\n' -> 'end of block.\\n'"
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char==u' ' and next_char in [u' ',u'\n']:
			cursor.deletePreviousChar()
			return True
		return False
		
class WWRuleEnglish0002 (WWRuleAbstract):
	title="No space or unbreakable space after an unbreakable space"
	description=	\
		"It delete the space or an unbreakable space (\\US) after an unbreakable space. \n\
		example :	'year[US] 2001' -> 'year[US]2001' \n\
					'year[US][US]2001' -> 'year[US]2001'"
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\u00A0' and next_char in [u'\u00A0',' ']:
			cursor.deleteChar()
		return False	
		
class WWRuleEnglish0003 (WWRuleAbstract):
	title="No space or break of line after a break of line. "
		
	description=	\
		"It deletes the space or break of line after a break of line\n\
		example :	'end of block.\\n ' -> 'end of block.\\n'\n\
						'end of block.\\n\\n' -> 'end of block.\\n'"
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\n' and next_char in [u' ',u'\n']:
			cursor.deleteChar()
			return True
		return False		
		
class WWRuleEnglish0004 (WWRuleAbstract):
	title="No space or unbreakable space before ',', ';', ':', '!', '?'"
	description=	\
		"Delete a space or an unbreakable space (US) before some ponctuation : ';', ':', '!', '?' or a closing guillemet (CG).\n\
		example :	'Hello !' 		-> 'Hello!'\n\
					'Hello[US]!'	-> 'Hello!'\n\
					'Hello ;'	 	-> 'Hello;'\n\
					'Hello[US];' 	-> 'Hello;'\n\
					'Hello :'		-> 'Hello:'\n\
					'Hello ?'		-> 'Hello?'\n\
					'Hello. [CG]'	-> 'Hello.[CG]'"
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if next_char in [u',',u';',u':',u'!',u'?',u'\201d']:
			if last_char==' ' or last_char==u'\u00A0': 
				cursor.deletePreviousChar()
				return True
		return False	
		
		
class WWRuleEnglish0005 (WWRuleAbstract):
	title="Replace the char [\"] by a opening or closing guillemet"
	description=	\
		"When pressing the char [\"], it replace by : an opening guillemet (OG) if it is preceded by a space, an unbreakable space (US) or a newline ; a closing guillemet (CG) otherwise. It also insert an unbreakable space after the opening guillemet and before the closing guillemet.\n\
		example :	'\"Hello' -> '[OG]Hello'\n\
					'Bye.\"' -> 'Bye.[CG]'"
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if next_char==u'"':
			if last_char in [u' ',u'\n',u'\u00A0']:
				cursor.deleteChar()
				cursor.insertText(u'\u201c')
			else :
				cursor.deleteChar()
				cursor.insertText(u'\u201d')
			return True
	
		return False		

class WWRuleEnglish0006 (WWRuleAbstract):
	title="No space or unbreakable space after an opening guillemet."
	description=	\
		"It deletes any space or unbreakable space (US) after an opening gullemet (OG).\n\
		example :	'[OG] Hello' 	-> '[OG]Hello'\n\
					'[OG][US]Hello' -> '[OG]Hello'"
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\u201c':
			if next_char==' ' or next_char==u'\u00AB': 
				cursor.deleteChar()
				return True
		return False
		
class WWRuleEnglish0007 (WWRuleAbstract):
	title="No space or unbreakable space before an closing guillemet."
	description=	\
		"It deletes any space or unbreakable space (US) before an closing gullemet (CG).\n\
		example :	'Hello [CG]' 	-> 'Hello[CG]'\n\
					'Hello[US][CG]' -> 'Hello[CG]'"
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if next_char==u'\u201d':
			if last_char==' ' or last_char==u'\u00AB': 
				cursor.deletePreviousChar()
				return True
		return False
		
				
		
class WWRuleEnglish0008 (WWRuleAbstract):
	title="A space or a newline after ';', ':', '!' or '?' except if it a closing guillemet (CG) or '!', '?'"
	description=	\
		"Check if there is a newline or a space after ';', ':', '!' or '? and if it is not the case, it inserts one (replacing the unbreakable space is necessary).\n\
		example :	'I agree;and you' -> 'I agree; and you'\n\
					'I agree:it is coherent' -> 'I agree: it is coherent'\n\
					'I agree!It is coherent' -> 'I agree! It is coherent'\n\
					'Do you agree?It is coherent' -> 'Do you agree? It is coherent'\n\
					'I agree![CG]' -> same\n\
					'I agree!!' -> same\n\
					'I agree?!' -> same\n\
					'I said to him:\n' -> same"
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char in [u';',u':',u'!',u'?'] and (next_char not in [u'\n',u' ']):
			if next_char== u'\u201d' or next_char== u'?' or next_char== u'!':
				return False
			if next_char== u'\u00A0':
				cursor.deleteChar()
			cursor.insertText(u' ')
			return True	
				
		return False
		
class WWRuleEnglish0009 (WWRuleAbstract):
	title="A space or a newline after '.' or ',' except if it is a figure or a closing guillemet (CG)."
	description=	\
		"Check if there is a newline or a space after '.' or ',' and if it is not the case, it inserts one (replacing the unbreakable space is necessary. This rule does not apply if the next character is a figure.\n\
		example :	'I agree.And you' -> 'I agree. And you'\n\
					'I agree,it is coherent' -> 'I agree, it is coherent'\n\
					'I agree.[CG]' -> same\n\
					'The speed was 33.7 mph' -> same"
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char in [u'.',u','] and \
				(next_char not in [u'\n',u' ',u'\u201d']+[unicode(i) for i in range(10)]):
			if next_char== u'\u00A0':
				cursor.deleteChar()
			cursor.insertText(u' ')
			return True	
				
		return False

class WWRuleEnglish0010 (WWRuleAbstract):
	title="Replace the typewriter apostrophe by a curved apostrophe."
	description=	\
		"Replace a the char ['] by a curved apostrophe (CA).\n\
		example :	'It's me' -> 'It[CA]s me'"
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char==u"'":
			cursor.deletePreviousChar()
			cursor.insertText(u'\u2019')
		return False	
		
class WWRuleEnglish0011 (WWRuleAbstract):
	title="Replace 3 consecutive points by an ellipsis."
	description=	\
		"Replace 3 consecutive points into an ellipsis (E):\n\
		example :	'\"So...' -> 'So[E]'"
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'.' and next_char==u'.':
			
			if self.language.lastChar(cursor,n=2)==u'.':
				cursor.deleteChar()
				cursor.deletePreviousChar()
				cursor.deletePreviousChar()
				cursor.insertText(u'\u2026')
				return True
		return False		
		
		
class WWRuleFrench0001 (WWRuleAbstract):
	title="No space before a space or a break of line"
	description=	\
		"It deletes the space before another space of a break of line\n \n\
		example :	'A  thing' -> 'A thing' \n\
					'end of block. \\n' -> 'end of block.\\n'"
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u' ' and next_char in [u' ',u'\n']:
			cursor.deletePreviousChar()
			return True
		return False

class WWRuleFrench0002 (WWRuleAbstract):
	title="No space or unbreakable space after an unbreakable space"
	description=	\
		"It delete the space or an unbreakable space (\\US) after an unbreakable space. \n\
		example :	'year[US] 2001' -> 'year[US]2001' \n\
					'year[US][US]2001' -> 'year[US]2001'"
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\u00A0' and next_char in [u'\u00A0',' ']:
			cursor.deleteChar()
		return False

class WWRuleFrench0003 (WWRuleAbstract):
	title="No space or break of line after a break of line. "
		
	description=	\
		"It deletes the space or break of line after a break of line\n\
		example :	'end of block.\\n ' -> 'end of block.\\n'\n\
						'end of block.\\n\\n' -> 'end of block.\\n'"
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\n' and next_char in [u' ',u'\n']:
			cursor.deleteChar()
			return True
		return False

class WWRuleFrench0004 (WWRuleAbstract):
	title="An unbreakable space before ';', ':', '!', '?', and closing guillemets."
	description=	\
		"Put an unbreakable space (US) before some ponctuation : ';', ':', '!', '?' and the french closing guillemets.\n\
		example :	'Bonjour! ' -> 'Bonjour[US]!'\n\
					'Bonjour; ' -> 'Bonjour[US];'\n\
					'Bonjour: ' -> 'Bonjour[US]:'\n\
					'Bonjour? ' -> 'Bonjour[US]?'\n\
					'Bonjour ! ' -> 'Bonjour[US]!'\n\
					'Bonjour ? ' -> 'Bonjour[US]?'"				
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if next_char in [u';',u':',u'!',u'?',u'\u00BB']:
			if last_char==' ': 
				cursor.deletePreviousChar()
				cursor.insertText(u'\u00A0')
				return True
			if last_char!=u'\u00A0': 
				cursor.insertText(u'\u00A0')
				return True
		return False

class WWRuleFrench0005 (WWRuleAbstract):
	title="An unbreakable space after an opening guillemet"
	description=	\
		"It puts an unbreakable space (US) after an opening gullemet (OG) (or replace the simple space that was there).\n\
		example :	'[OG] Bonjour' -> '[OG][US]Bonjour'\n\
					'[OG]Bonjour' -> '[OG][US]Bonjour'"
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\u00AB':
			if next_char==' ': 
				cursor.deleteChar()
				cursor.insertText(u'\u00A0')
				return True
			if next_char!=u'\u00A0':
				cursor.insertText(u'\u00A0')
				return True
		return False

class WWRuleFrench0006 (WWRuleAbstract):
	title="No unbreakable space if it is not before a ponctuation or after an oppening guillemet"
	description=	\
		"Usually we prevent using an unbreakable space (US) if it is not before a ponctuation like ';', ':', '!', '?', or a closing guillemet. It can also be used after an opening guillemet. It replaces the unbreakable space by a simple space.\n\
		example :	'Je[US]suis' -> 'Je suis'\n\
					'[OG][US]\\Bonjour' -> same\n\
					'Bonjour[US]!' -> same"
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\u00A0' and (next_char not in [u';',u':',u'!',u'?',u'\u00BB']): 
			last_last_char=self.language.lastChar(cursor,n=2)
			if last_last_char!=u'\u00AB': # we cheak it caused by an oppening "guillemet"
				cursor.deletePreviousChar()
				cursor.insertText(u' ')
				return True
		return False

class WWRuleFrench0007 (WWRuleAbstract):
	title="No space before a point or a comma."
	description=	\
		"It deletes a space or an unbreakable space (US) before a comma.\n\
		example :	'I agree .' -> 'I agree.'\n\
					'I agree[US].' -> 'I agree.'\n\
					'Charles , you and me.' -> 'Charles, you and me.'"
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char in [u' ', u'\u00A0'] and next_char in [u'.',u',']:
			cursor.deletePreviousChar()
			return True
		return False

class WWRuleFrench0008 (WWRuleAbstract):
	title="A space or a newline after ';' or ':'."
	description=	\
		"Check if there is a newline or a space after ';' or ':' and if it is not the case, it inserts one (replacing the unbreakable space is necessary.\n\
		example :	'I agree;and you' -> 'I agree; and you'\n\
					'I agree:it is coherent' -> 'I agree: it is coherent'\n\
					'I said to him:\n' -> same"
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char in [u';',u':'] and (next_char not in [u'\n',u' ']):
			if next_char== u'\u00A0':
				cursor.deleteChar()
			cursor.insertText(u' ')
			return True	
				
		return False

class WWRuleFrench0009 (WWRuleAbstract):
	title="Replace the typewriter apostrophe by a curved apostrophe."
	description=	\
		"Replace a the char ['] by a curved apostrophe (CA).\n\
		example :	'It's me' -> 'It[CA]s me'"
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u"'":
			cursor.deletePreviousChar()
			cursor.insertText(u'\u2019')
		return False

class WWRuleFrench0010 (WWRuleAbstract):
	title="Replace the char [\"] by a opening or closing guillemet"
	description=	\
		"When pressing the char [\"], it replace by : an opening guillemet (OG) if it is preceded by a space, an unbreakable space (US) or a newline ; a closing guillemet (CG) otherwise. It also insert an unbreakable space after the opening guillemet and before the closing guillemet.\n\
		example :	'\"Bonjour' -> '[OG][US]Bonjour'\n\
					'Salut.\"' -> 'Salut.[US][CG]'"
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if next_char==u'"':
			if last_char in [u' ',u'\n',u'\u00A0']:
				cursor.deleteChar()
				cursor.insertText(u'\u00AB\u00A0')
			else :
				cursor.deleteChar()
				cursor.insertText(u'\u00A0\u00BB')
			return True
	
		return False

class WWRuleFrench0011 (WWRuleAbstract):
	title="Unkown Rule"
	description=""
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		
		if last_char==u'"':
			if next_char==u' ':
				cursor.deletePreviousChar()
				cursor.insertText(u'\u00A0\u00BB')
			else :
				cursor.deletePreviousChar()
				cursor.insertText(u'\u00AB\u00A0')
			return True	
		return False

class WWRuleFrench0012 (WWRuleAbstract):
	title="Replace 3 consecutive points by an ellipsis."
	description=	\
		"Replace 3 consecutive points into an ellipsis (E):\n\
		example :	'\"So...' -> 'So[E]'"
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'.' and next_char==u'.':
			
			if self.language.lastChar(cursor,n=2)==u'.':
				cursor.deleteChar()
				cursor.deletePreviousChar()
				cursor.deletePreviousChar()
				cursor.insertText(u'\u2026')
				return True
		return False

class WWRuleFrench0013 (WWRuleAbstract):
	title="An unbreakable space before after a diolog dash."
	description=	\
		"It puts an unbreakable space (US) after a diolog dash (DD) (or replace the simple space that was there).\n\
		example :	'[DD] Bonjour' -> '[DD][US]Bonjour'\n\
					'[DD]Bonjour' -> '[DD][US]Bonjour"
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\u2014' and next_char!=u'\u00A0':
			if next_char==' ': 
				cursor.deleteChar()
				cursor.insertText(u'\u00A0')
				return True
			if next_char!=u'\u00A0': 
				cursor.insertText(u'\u00A0')
				return True
		return False
		
		