import asyncio
from threading import Thread
from os import path, getcwd
from PySide2.QtWidgets \
	import QMainWindow, QVBoxLayout, QPushButton, QWidget, \
	QStatusBar, QLabel, QHBoxLayout
from PySide2.QtGui import QFont, QIcon
from PySide2.QtCore import Qt, Signal

from data import app_name
from network import is_connected, disconnect, connect, is_juet_network
from .settings import Settings

class Main(QMainWindow):
	set_status = Signal(str, str)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.settings = Settings(parent=self)

		main_widget = QWidget()
		self.setCentralWidget(main_widget)

		layout = QVBoxLayout()
		main_widget.setLayout(layout)

		buttons = QHBoxLayout()
		buttons.addStretch()
		layout.addLayout(buttons)

		# std_icon = self.style().standardIcon
		# settings_icon = std_icon(QStyle.SP_DialogOpenButton)
		settings_button = QPushButton('')
		settings_button.setIcon(QIcon(path.join(getcwd(), 'icons', 'settings.svg')))
		buttons.addWidget(settings_button)
		settings_button.clicked.connect(self.settings.show)

		title = QLabel('JUET Internet Authenticator')
		title.setStyleSheet('padding-top: 10px; padding-bottom: 15px; font-weight: bold;')
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
					print(end='\a')
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
					print(end='\a')
		thread = Thread(target=click_action)
		thread.start()

	async def check_status(self):
		if not is_juet_network():
			self.connect_button.setDisabled(True)
			self.connect_button.setText('Unavailable')
			self.set_status('Not on JUET LAN', 'grey')
			return
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