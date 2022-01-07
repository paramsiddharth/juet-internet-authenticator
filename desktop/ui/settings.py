from PySide2.QtCore import Qt
from PySide2.QtGui import QMovie
from PySide2.QtWidgets \
	import QLabel, QLineEdit, QMainWindow, \
	QMessageBox, QPushButton, QVBoxLayout, QWidget
from data import app_name
from helpers import resolve_icon
from auth import get_username, get_password, set_credentials

class Settings(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setWindowFlag(Qt.Tool, True)
		# self.setWindowFlag(Qt.CustomizeWindowHint, True)
		# self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

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

		save_button = QPushButton('Save changes')
		save_button.setDisabled(True)
		layout.addWidget(save_button)
		self.save_button = save_button
		save_button.clicked.connect(self.save_settings)

		username.textEdited.connect(lambda: save_button.setDisabled(False))
		password.textEdited.connect(lambda: save_button.setDisabled(False))

		self.setWindowTitle('Settings - ' + app_name)
	
	def load_settings(self):
		u, p = get_username(), get_password()
		if u is not None:
			self.username.setText(u)
		if p is not None:
			self.password.setText(p)
		self.loading_icon.stop()
		self.loading.setVisible(False)
		self.username.setVisible(True)
		self.password.setVisible(True)
	
	def save_settings(self):
		u, p = self.username.text(), self.password.text()
		if len(u) < 1:
			error = QMessageBox()
			error.setWindowTitle('Error')
			error.setIcon(QMessageBox.Warning)
			error.setText('Enter a username.')
			error.exec_()
			return
		if len(p) < 1:
			error = QMessageBox()
			error.setWindowTitle('Error')
			error.setIcon(QMessageBox.Warning)
			error.setText('Enter a password.')
			error.exec_()
			return
		if set_credentials(u, p):
			done = QMessageBox()
			done.setWindowTitle('Success')
			done.setIcon(QMessageBox.Information)
			done.setText('Changes saved.')
			done.exec_()
		else:
			error = QMessageBox()
			error.setWindowTitle('Error')
			error.setIcon(QMessageBox.Critical)
			error.setText('Failed to save changes.')
			error.exec_()
	
	def show(self):
		self.load_settings()
		super().show()

	def closeEvent(self, event):
		# Just for the sake of it (yes)...
		self.username.setText('')
		self.password.setText('')
		return super().closeEvent(event)