from PyQt4 import QtGui, QtCore, QtNetwork

from WolfWriterMainWindow 	import *

class WWSingleApplication(QtGui.QApplication):
	def __init__(self, argv, key):
		QtGui.QApplication.__init__(self, argv)
		self._memory = QtCore.QSharedMemory(self)
		self._memory.setKey(key)
		if self._memory.attach():
			self._running = True
		else:
			self._running = False
			if not self._memory.create(1):
				raise RuntimeError(
					self._memory.errorString().toLocal8Bit().data())

	def isRunning(self):
		return self._running

class WWSingleApplicationWithMessaging(WWSingleApplication):
	def __init__(self, argv, key):
		WWSingleApplication.__init__(self, argv, key)
		self._key = key
		self._timeout = 1000
		self._server = QtNetwork.QLocalServer(self)
		if not self.isRunning():
			self._server.newConnection.connect(self.handleMessage)
			self._server.listen(self._key)

	def handleMessage(self):
		socket = self._server.nextPendingConnection()
		if socket.waitForReadyRead(self._timeout):
			self.emit(QtCore.SIGNAL('messageAvailable'),
					  QtCore.QString.fromUtf8(socket.readAll().data()))
			socket.disconnectFromServer()
		else:
			QtCore.qDebug(socket.errorString().toLatin1())

	def sendMessage(self, message):
		if self.isRunning():
			socket = QtNetwork.QLocalSocket(self)
			socket.connectToServer(self._key, QtCore.QIODevice.WriteOnly)
			if not socket.waitForConnected(self._timeout):
				print(socket.errorString().toLocal8Bit().data())
				return False
			socket.write(unicode(message).encode('utf-8'))
			if not socket.waitForBytesWritten(self._timeout):
				print(socket.errorString().toLocal8Bit().data())
				return False
			socket.disconnectFromServer()
			return True
		return False
			
	
		
	

if __name__ == '__main__':
	import sys
	# app = QtGui.QApplication(sys.argv)
	key = 'WolfWriter'
	app = WWSingleApplicationWithMessaging(sys.argv, key)
	mainWindow=None
	def my_excepthook(type, value, tback):
		res=type.__name__+":"+unicode(value)
		
		msgBox=QtGui.QMessageBox.critical(mainWindow, type.__name__, res)
		sys.__excepthook__(type, value, tback) 
	sys.excepthook = my_excepthook
	
	create_new_mainwindow=True
	
	if app.isRunning():
		try:
			if len(sys.argv)>1:
				res=app.sendMessage('open '+' '.join(sys.argv[1:]))
			else:
				res=app.sendMessage('new')
			if res:
				create_new_mainwindow=False
		except:
			pass
	
		
	if create_new_mainwindow :
		if len(sys.argv)>1:
			bk=WWBook(zippath=sys.argv[1])
		else:
			bk=WWBook(zippath=abs_path_new_book)
			bk.zippath=None
		
		
		mainWindow = WWMainWindow(bk)
		app.connect(app, QtCore.SIGNAL('messageAvailable'),mainWindow.read_cmd)
		mainWindow.show()
	sys.exit(app.exec_())
	# read_cmd
# #####################
	# key = 'FOO_BAR'

	# if len(sys.argv) > 1:
		# app = SingleApplicationWithMessaging(sys.argv, key)
		# if app.isRunning():
			# app.sendMessage('app is already running')
			# sys.exit(1)
	# else:
		# app = SingleApplication(sys.argv, key)
		# if app.isRunning():
			# print('app is already running')
			# sys.exit(1)

	# window = Window()
	# app.connect(app, QtCore.SIGNAL('messageAvailable'),
				# window.handleMessage)
	# window.show()

	# sys.exit(app.exec_())
			