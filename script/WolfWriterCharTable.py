"""
Part of the WolfWriter project. Written by Renaud Dessalles
This file decribe the creation of the widget of the Char table
"""

from PyQt4 import QtGui, QtCore

class WWCharWidgetTable(QtGui.QWidget):
	# the list of the fields (to have them in a given order)
	list_char_fields=[	"Basic Latin","Latin-1 Supplement","Latin Extended-A","Latin Extended-B",\
						"IPA Extensions","Spacing Modifier Letters","Greek","Cyrillic","Latin Extended Additional",\
						"Greek Extended","General Punctuation","Superscripts and Subscripts","Currency Symbols",\
						"Letterlike Symbols","Number Forms","Arrows","Mathematical Operators","Miscellaneous Technical",\
						"Box Drawing","Block Elements","Geometric Shapes","Miscellaneous Symbols","Private Use Area",\
						"Alphabetic Presentation Forms"]

	# the diconary of the fields : to every field it gives the range of the of the chars adress to consider.
	# (source : https://en.wikipedia.org/wiki/Unicode)
	dico_char_ranges=\
		{"Basic Latin"					:(int('0020',16), int('007F',16)),\
		"Latin-1 Supplement"			:(int('0080',16), int('00FF',16)),\
		"Latin Extended-A"				:(int('0100',16), int('017F',16)),\
		"Latin Extended-B"				:(int('0180',16), int('024F',16)),\
		"IPA Extensions"				:(int('0250',16), int('02AF',16)),\
		"Spacing Modifier Letters"		:(int('02B0',16), int('02FF',16)),\
		"Greek"							:(int('0370',16), int('03FF',16)),\
		"Cyrillic"						:(int('0400',16), int('04FF',16)),\
		"Latin Extended Additional"		:(int('1E00',16), int('1EFF',16)),\
		"Greek Extended"				:(int('1F00',16), int('1FFF',16)),\
		"General Punctuation"			:(int('2000',16), int('206F',16)),\
		"Superscripts and Subscripts"	:(int('2070',16), int('209F',16)),\
		"Currency Symbols"				:(int('20A0',16), int('20CF',16)),\
		"Letterlike Symbols"			:(int('2100',16), int('214F',16)),\
		"Number Forms"					:(int('2150',16), int('218F',16)),\
		"Arrows"						:(int('2190',16), int('21FF',16)),\
		"Mathematical Operators"		:(int('2200',16), int('22FF',16)),\
		"Miscellaneous Technical"		:(int('2300',16), int('23FF',16)),\
		"Box Drawing"					:(int('2500',16), int('257F',16)),\
		"Block Elements"				:(int('2580',16), int('259F',16)),\
		"Geometric Shapes"				:(int('25A0',16), int('25FF',16)),\
		"Miscellaneous Symbols"			:(int('2600',16), int('26FF',16)),\
		"Private Use Area"				:(int('F000',16), int('F0FF',16)),\
		"Alphabetic Presentation Forms"	:(int('FB00',16), int('FB4F',16))}
		
	
	def __init__(self,linked_text_widget=None,nb_columns=16,*args,**kargs):
		"""
		The Wiget that will will contain the WWCharTable. It allows to choose the file.
		TODO : a direct code access of the char.
		- linked_text_widget : A WWTextEdit or WWLineEdit instance where to add the 
				chosen chars
		- nb_columns : the number of columns to display in the WWCharTable
		"""
		QtGui.QWidget.__init__(self,*args,**kargs)
		self.linked_text_widget=linked_text_widget
		self.comboBox = QtGui.QComboBox() # will contain the field list
		self.charTable=WWCharTable(nb_columns=nb_columns)
		for k in self.list_char_fields: # We add the field name to the comboBox
			self.comboBox.addItem(k)
		
		self.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.SLOT_changeTable)
		self.connect(self.charTable, QtCore.SIGNAL("itemActivated(QTableWidgetItem *)"), self.SLOT_itemActivated)
		layout=QtGui.QVBoxLayout()
		layout.addWidget( self.comboBox )
		layout.addWidget( self.charTable )
		self.setLayout ( layout )
	
	def SLOT_changeTable(self):
		"""
		Slot called when changing the field in the comboBox to apply it in the  	
		WWCharTable.
		"""
		field=unicode(self.comboBox.itemText(self.comboBox.currentIndex()))
		self.charTable.changeRange(self.dico_char_ranges[field])

	def SLOT_itemActivated(self,item):
		"""Slot called when a char of the table is activated. It insert the selected 
		char in the corresponding linked_text_widget """
		if self.linked_text_widget!=None:
			if isinstance(self.linked_text_widget,QtGui.QTextEdit):
				self.linked_text_widget.insertPlainText(item.text())
			if isinstance(self.linked_text_widget,QtGui.QLineEdit):
				self.linked_text_widget.insert(item.text())
			
		
class WWCharTable (QtGui.QTableWidget):
	
	def __init__(self,nb_columns=16,range_char=(int('0020',16),int('024F',16))):
		"""
		A re-implementation of QTableWidget. It will display all the chars contained 
		in the given range.
		- nb_columns : number of columns to display
		- range_char : a tuple that contains the borns of the field range to display.
		Note : range_char=(0,10) includes 10.
		"""
		self.nb_columns=nb_columns
		QtGui.QTableWidget.__init__(self)
		self.setColumnCount(self.nb_columns)
		self.changeRange(range_char)
		
	def changeRange(self,range_char):
		"""Method that is called when changing the range of the chars"""
		size=(range_char[1]+1)-range_char[0]
		self.setRowCount((size/self.nb_columns)+1)
		for i,char_nb in enumerate(range(range_char[0],range_char[1]+1)):
			
			item = QtGui.QTableWidgetItem (unichr(char_nb))
			item.setTextAlignment (QtCore.Qt.AlignCenter)
			item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
			self.setItem(i/self.nb_columns,i%self.nb_columns,item)
		self.resizeRowsToContents()
		self.resizeColumnsToContents()
	

		
if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	
	widTable = WWCharWidgetTable()	
	
	main_window=QtGui.QMainWindow()
	main_window.setCentralWidget(widTable)

	main_window.show()
	sys.exit(app.exec_())
	# sys.exit(textedit.exec_())