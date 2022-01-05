import asyncio
from threading import Thread
import requests as req
from PySide2.QtWidgets \
	import QMainWindow, QVBoxLayout, QPushButton, QWidget

from data import app_name, test_url

# class Main(QMainWindow):
class Main(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		main_widget = QWidget()
		self.setCentralWidget(main_widget)

		layout = QVBoxLayout()
		main_widget.setLayout(layout)

		connect_button = QPushButton('Checking for connection...')
		connect_button.setDisabled(True)
		connect_button.clicked.connect(self.click_connect)
		layout.addWidget(connect_button)
		self.connect_button = connect_button

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
		except:
			self.connected = False
			self.connect_button.setText('Connect')
		else:
			self.connected = True
			self.connect_button.setText('Disconnect')
		self.connect_button.setDisabled(False)