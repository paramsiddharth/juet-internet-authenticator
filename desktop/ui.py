import asyncio
from threading import Thread
import requests as req
from PySide2.QtWidgets \
	import QMainWindow, QVBoxLayout, QPushButton, QWidget, \
	QStatusBar, QLabel
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt

from data import app_name, test_url

class Main(QMainWindow):
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
		self.set_status('Loading...', color='grey')
		status_bar.addPermanentWidget(status)
		layout.addWidget(status_bar)

		# A reminder for future me to not use the below technique because the
		# resulting UI isn't very good. Rather, use an extra QWidget as the central
		# for the QMainWindow.
		# self.setLayout(layout) # So this won't work for some unknown reason
		# self.layout().addChildLayout(layout)

		self.setWindowTitle(app_name)

		thread = Thread(target=asyncio.run, args=(self.check_status(),))
		thread.start()

	def click_connect(self):
		if self.connected:
			self.connected = False
			self.connect_button.setText('Connect')
		else:
			self.connected = True
			self.connect_button.setText('Disconnect')
	
	async def check_status(self):
		try:
			req.get(test_url)
		except Exception as e:
			print(e.args)
			self.connected = False
			self.connect_button.setText('Connect')
		else:
			self.connected = True
			self.connect_button.setText('Disconnect')
		self.connect_button.setDisabled(False)
		self.set_status()
	
	def set_status(self, msg='READY', color='green'):
		self.status.setText(msg)
		self.status.setStyleSheet(f'color: {color};')