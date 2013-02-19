from WolfWriterMainWindow import *
from WolfWriterBook import *





#
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	
	
	pp="C:\\Users\\Renaud\\Documents\\Programmation\\Python\\WolfWriter_Test\\TestPerso\\testa.zip"
	
	
	bk=WWBook(archivepath=pp)
	mainWindow = WWMainWindow(bk)
	mainWindow.show()

	sys.exit(app.exec_())