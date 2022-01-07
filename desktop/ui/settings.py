from threading import Thread
import asyncio
from PySide2.QtGui import QMovie
from PySide2.QtWidgets import QLabel, QLineEdit, QMainWindow, QVBoxLayout, QWidget

from data import app_name
from helpers import resolve_icon
from auth import get_username, get_password

class Settings(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		main_widget = QWidget()
		self.setCentralWidget(main_widget)

		layout = QVBoxLayout()
		main_widget.setLayout(layout)

		loading = QLabel()
		loading_icon = QMovie(resolve_icon('loader.gif'))
		loading.setMovie(loading_icon)
		layout.addWidget(loading)
		loading_icon.start()
		self.loading = loading
		self.loading_icon = loading_icon

		layout.addWidget(QLabel('Username:'))
		username = QLineEdit(self)
		username.setVisible(False)
		username.setPlaceholderText('Username')
		layout.addWidget(username)
		self.username = username

		layout.addWidget(QLabel('Password:'))
		password = QLineEdit(self)
		password.setEchoMode(QLineEdit.Password)
		password.setVisible(False)
		password.setPlaceholderText('Password')
		layout.addWidget(password)
		self.password = password

		self.setWindowTitle('Settings - ' + app_name)
	
	def load_settings(self):
		u, p = get_username(), get_password()
		# print(u, p)
		if u is not None:
			self.username.setText(u)
		if p is not None:
			self.password.setText(p)
		self.loading_icon.stop()
		self.loading.setVisible(False)
		self.username.setVisible(True)
		self.password.setVisible(True)
	
	def show(self):
		self.load_settings()
		super().show()