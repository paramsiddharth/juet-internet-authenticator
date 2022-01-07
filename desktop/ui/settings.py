from PySide2.QtCore import Qt
from PySide2.QtGui import QMovie
from PySide2.QtWidgets \
	import QLabel, QLineEdit, QMainWindow, \
	QMessageBox, QPushButton, QVBoxLayout, QWidget
from data import app_name
from helpers import resolve_icon
from auth import flush_credentials, get_username, get_password, set_credentials

class Settings(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setWindowFlag(Qt.Tool, True)

		main_widget = QWidget()
		self.setCentralWidget(main_widget)

		layout = QVBoxLayout()
		main_widget.setLayout(layout)

		flush_button = QPushButton('Flush credentials')
		flush_button.setDisabled(True)
		layout.addWidget(flush_button)
		self.flush_button = flush_button
		flush_button.clicked.connect(self.flush)

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
		if u is not None or p is not None:
			self.flush_button.setDisabled(False)
		self.loading_icon.stop()
		self.loading.setVisible(False)
		self.username.setVisible(True)
		self.password.setVisible(True)
		self.removeFocus()
	
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
			self.flush_button.setDisabled(False)
			self.save_button.setDisabled(True)
			done = QMessageBox()
			done.setWindowTitle('Success')
			done.setIcon(QMessageBox.Information)
			done.setText('Changes saved.')
			done.exec_()
			self.removeFocus()
		else:
			error = QMessageBox()
			error.setWindowTitle('Error')
			error.setIcon(QMessageBox.Critical)
			error.setText('Failed to save changes.')
			error.exec_()

	def flush(self):
		confirm = QMessageBox()
		confirm.setWindowTitle('Confirmation')
		confirm.setText('This will delete your credentials stored on this system. Are you sure you wish to continue?\nPress OK to proceed.')
		confirm.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		confirm.setIcon(QMessageBox.Question)
		if confirm.exec_() == QMessageBox.Ok:
			if flush_credentials():
				self.username.setText('')
				self.password.setText('')
				self.flush_button.setDisabled(True)
				self.save_button.setDisabled(False)
				done = QMessageBox()
				done.setWindowTitle('Success')
				done.setIcon(QMessageBox.Information)
				done.setText('Credentials flushed.')
				done.exec_()
				self.removeFocus()
			else:
				error = QMessageBox()
				error.setWindowTitle('Error')
				error.setIcon(QMessageBox.Critical)
				error.setText('Failed to flush credentials.')
				error.exec_()
	
	def removeFocus(self):
		focus_widget = self.focusWidget()
		if focus_widget is not None:
			focus_widget.clearFocus()

	def show(self):
		self.load_settings()
		super().show()

	def closeEvent(self, event):
		# Just for the sake of it (yes)...
		self.username.setText('')
		self.password.setText('')
		return super().closeEvent(event)