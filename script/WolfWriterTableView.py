import sys 
import operator
from PyQt4 import QtGui, QtCore
from WolfWriterCommon import WWRomanNumber,WWIdentity


class WWDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		
		self.table = WWTableView(parent=self,fct_numeral_vetical_headers=WWIdentity)
		layout = QtGui.QHBoxLayout()
		# layout.addWidget(self.table)
		self.button_test = QtGui.QPushButton(self)
		self.button_test.setObjectName("Test")
		layout.addWidget(self.button_test)
		layout.addWidget(self.table)
		self.setLayout(layout)
		self.resize(300,300)
		
		QtCore.QObject.connect(self.button_test, QtCore.SIGNAL("clicked()"), self.table.slot_insertNewItems)
		
	
class WWTableView(QtGui.QTableView):
	def __init__(self,data=None,parent=None,headers=None,fct_numeral_vetical_headers=None):
		QtGui.QTableView.__init__(self,parent)
		if headers==None:
			headers=["Name","Nb scenes","Word number"]
		
		# self.headers=["Name","Nb scenes","Word number"]
		self.headers=headers
		QtCore.QObject.connect(self,QtCore.SIGNAL("activated ( const QModelIndex & )"),self.slot_activated)
		if data==None:
			data=[['Le debut','72','123546'],['Le milieu','10','123546'],['La fin','1','0']]
		
		self.setModel(WWTableModel(data,self.headers,self,fct_numeral_vetical_headers))
		self.setSelectionBehavior ( QtGui.QAbstractItemView.SelectRows )
		self.setShowGrid(False)

	def slot_activated ( self,index ):
		raise NotYetImplementedError

	def slot_insertNewItems(self,place=-1,number=1):
		data=[["No title","0","0"]]*number
		
		self.model().insertRows(data=data,place=place,number=number)
		
	def slot_removeItems(self):
		li=self.selectedIndexes () 
		A=[i.row() for i in li]
		A=list(set(A))
		A.sort(reverse=True)
		for r in A:
			self.model().removeRow(r)
	
	def keyReleaseEvent (self, event ) :
		if event.key()==QtCore.Qt.Key_Delete:
			self.slot_removeItems()
		else :
			QtGui.QTableView.keyReleaseEvent(self,event)		
	

	
	
"""
class WWTableView (QtGui.QTableView):
	def __init__(self,data=None,parent=None):
		QtGui.QTableView.__init__(self,parent)
		self.headers=["Name","Nb scenes","Word number"]
		QtCore.QObject.connect(self,QtCore.SIGNAL("activated ( const QModelIndex & )"),self.slot_activated)
		if data==None:
			data=[['asfs','bsfs','csfsdf'],['as1s','bs1s','cs1sd1'],['as2s','bs2s','cs2sd2']]
		
		self.setModel(WWTableModel(data,self.headers,self))
		self.setSelectionBehavior ( QtGui.QAbstractItemView.SelectRows )
		self.setShowGrid(False)
		
	def slot_activated ( self,index ):
		print "On ouvrirait la scene "+str(index.row())
	
	def slot_insertNewScene(self):
		self.model().appendRow(["No title","0","0"])
		
	def slot_removeScene(self):
		li=self.selectedIndexes () 
		if len(li)>0:
			i=li[0].row()
			self.model().removeRow(i)
	
	def keyReleaseEvent (self, event ) :
		if event.key()==QtCore.Qt.Key_Delete:
			self.slot_removeScene()
		else :
			QtGui.QTableView.keyReleaseEvent(self,event)
		# selectionModel=QtGui.QItemSelectionModel(self.model())
		
		# self.setSelectionModel(selectionModel)
"""
class WWTableModel(QtCore.QAbstractTableModel):
	def __init__(self,data,headers,parent=None,fct_numeral_vetical_headers=None,*args):
		QtCore.QAbstractTableModel.__init__(self, parent, *args) 
		self.arraydata=data
		self.headers=headers
		if fct_numeral_vetical_headers==None:
			self.fct_numeral_vetical_headers=WWIdentity
		else:
			self.fct_numeral_vetical_headers=fct_numeral_vetical_headers
		
	def rowCount(self, parent): 
		return len(self.arraydata) 
 
	def columnCount(self, parent): 
		return len(self.arraydata[0]) 
 
	def data(self, index, role): 
		if not index.isValid(): 
			return QtCore.QVariant() 
		elif role !=  QtCore.Qt.DisplayRole: 
			return QtCore.QVariant() 
		return QtCore.QVariant(self.arraydata[index.row()][index.column()]) 

	def headerData(self, place, orientation, role):
		if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
			return QtCore.QVariant(self.headers[place])
		if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
			return QtCore.QVariant(self.fct_numeral_vetical_headers(place+1))
		return QtCore.QVariant()
	
	def insertRows (self,data,place=-1,number=1):
		size=self.rowCount(QtCore.QModelIndex())
		if place<0:
			place=size+place+1			
		self.beginInsertRows(QtCore.QModelIndex(),place,place+number-1)
		self.arraydata+=data
		self.endInsertRows()
		
	def removeRow (self, i):
		print "i : ",i
		assert 0<=i<self.rowCount(QtCore.QModelIndex())
		self.beginRemoveRows(QtCore.QModelIndex(),i,i)
		self.arraydata.pop(i)
		self.endRemoveRows()
		
	# def sort(self, Ncol, order):
		# """Sort table by given column number.
		# """
		# self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
		# self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))		
		# if order == QtCore.Qt.DescendingOrder:
			# self.arraydata.reverse()
		# self.emit(QtCore.SIGNAL("layoutChanged()"))	
		

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	dialog = WWDialog()
	sys.exit(dialog.exec_())		