"""
Part of the WolfWriter project. Written by Renaud Dessalles
This file decribe the creation of the widget of the Char table
"""



from PyQt4 import QtGui, QtCore

class WWCharWidgetTable(QtGui.QWidget):
	list_char_fields=[	"Basic Latin","Latin-1 Supplement","Latin Extended-A","Latin Extended-B",\
						"IPA Extensions","Spacing Modifier Letters","Greek","Cyrillic","Latin Extended Additional",\
						"Greek Extended","General Punctuation","Superscripts and Subscripts","Currency Symbols",\
						"Letterlike Symbols","Number Forms","Arrows","Mathematical Operators","Miscellaneous Technical",\
						"Box Drawing","Block Elements","Geometric Shapes","Miscellaneous Symbols","Private Use Area",\
						"Alphabetic Presentation Forms"]

	
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
		# source : https://en.wikipedia.org/wiki/Unicode
	
	def __init__(self,linked_text_widget=None,nb_columns=16,*args,**kargs):
		QtGui.QWidget.__init__(self,*args,**kargs)
		self.linked_text_widget=linked_text_widget
		self.comboBox = QtGui.QComboBox()
		self.charTable=WWCharTable(nb_columns=nb_columns)
		for k in self.list_char_fields:
			self.comboBox.addItem(k)
		
		self.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.SLOT_changeTable)
		self.connect(self.charTable, QtCore.SIGNAL("itemActivated(QTableWidgetItem *)"), self.SLOT_itemActivated)
		layout=QtGui.QVBoxLayout()
		layout.addWidget( self.comboBox )
		layout.addWidget( self.charTable )
		self.setLayout ( layout )
	
	def SLOT_changeTable(self):
		field=unicode(self.comboBox.itemText(self.comboBox.currentIndex()))
		self.charTable.changeRange(self.dico_char_ranges[field])

	def SLOT_itemActivated(self,item):
		if self.linked_text_widget!=None:
			self.linked_text_widget.insertPlainText(item.text())
			
		
class WWCharTable (QtGui.QTableWidget):

	def __init__(self,nb_columns=16,range_char=(int('0020',16),int('024F',16))):
		self.nb_columns=nb_columns
		QtGui.QTableWidget.__init__(self)
		self.setColumnCount(self.nb_columns)
		self.changeRange(range_char)
		
	def changeRange(self,range_char):
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