import sys
from PySide2.QtWidgets import QApplication

from ui import Main

def main():
	global app
	app = QApplication(sys.argv)
	window = Main()
	window.show()
	app.exec_()

if __name__ == '__main__':
	main()