import asyncio
from threading import Thread
from PySide2.QtWidgets \
	import QMainWindow, QVBoxLayout, QPushButton, QWidget, \
	QStatusBar, QLabel
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt, Signal

from data import app_name
from network import is_connected, disconnect, connect

class Main(QMainWindow):
	set_status = Signal(str, str)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		main_widget = QWidget()
		self.setCentralWidget(main_widget)

		layout = QVBoxLayout()
		main_widget.setLayout(layout)

		title = QLabel('JUET Internet Authenticator')
		title.setFont(QFont(QFont.defaultFamily(QFont()), 17))
		title.setAlignment(Qt.AlignCenter)
		layout.addWidget(title)

		connect_button = QPushButton('Checking for connection...')
		connect_button.setDisabled(True)
		connect_button.clicked.connect(self.click_connect)
		layout.addWidget(connect_button)
		self.connect_button = connect_button

		status_bar = QStatusBar()
		status = QLabel()
		self.status = status
		status_bar.addPermanentWidget(status)
		layout.addWidget(status_bar)

		# self.set_status.connect(self.on_set_status)
		self.set_status('Loading...', 'grey')

		thread = Thread(target=asyncio.run, args=(self.check_status(),))
		thread.start()

		# A reminder for future me to not use the below technique because the
		# resulting UI isn't very good. Rather, use an extra QWidget as the central
		# for the QMainWindow.
		# self.setLayout(layout) # So this won't work for some unknown reason
		# self.layout().addChildLayout(layout)

		self.setWindowTitle(app_name)

	def click_connect(self):
		self.connect_button.setDisabled(True)
		def click_action():
			if self.connected:
				self.set_status('Disconnecting...', 'blue')
				self.connect_button.setText('Disconnecting...')
				if disconnect():
					self.connected = False
					self.connect_button.setText('Connect')
					self.connect_button.setDisabled(False)
					self.set_status('DISCONNECTED', 'grey')
				else:
					self.connect_button.setText('Disconnect')
					self.connect_button.setDisabled(False)
					self.set_status('ERROR', 'red')
			else:
				self.set_status('Connecting...', 'blue')
				self.connect_button.setText('Connecting...')
				if connect():
					self.connected = True
					self.connect_button.setText('Disconnect')
					self.connect_button.setDisabled(False)
					self.set_status('CONNECTED', 'green')
				else:
					self.connect_button.setText('Connect')
					self.connect_button.setDisabled(False)
					self.set_status('ERROR', 'red')
		thread = Thread(target=click_action)
		thread.start()

	async def check_status(self):
		self.connected = is_connected()
		if self.connected:
			self.connect_button.setText('Disconnect')
			self.set_status('CONNECTED', 'green')
		else:
			self.connect_button.setText('Connect')
			self.set_status('DISCONNECTED', 'grey')
		self.connect_button.setDisabled(False)
	
	def set_status(self, msg='READY', color='green'):
		self.status.setText(msg)
		self.status.setStyleSheet(f'color: {color};')

