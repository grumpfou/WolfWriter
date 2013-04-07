from WolfWriterMainWindow import *
from WolfWriterBook import *
import sys





#
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	
	
	pp="C:\\Users\\Renaud\\Documents\\Programmation\\Python\\WolfWriter_Test\\TestPerso\\testa.zip"
	
	
	bk=WWBook(zippath=pp)
	
	# try :
		# print "DJJJJLJDKJDLKJLKD0"
	mainWindow = WWMainWindow(bk)
	mainWindow.show()
	# except Exception,e:
		# print "DJJJJLJDKJDLKJLKD"
		# msgBox=QtGui.QMessageBox.critical(mainWindow, e.__class__.__name__, str(e))
		# msgBox.show()
	sys.exit(app.exec_())