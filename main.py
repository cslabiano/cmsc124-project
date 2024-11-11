from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog
from PyQt5 import uic
import sys

class UI(QMainWindow):
  def __init__(self):
    super(UI, self).__init__()

    # load the ui file
    uic.loadUi("gui.ui", self)

    # define widgets
    self.button = self.findChild(QPushButton, "open_file_button")
    self.label = self.findChild(QTextEdit, "print_file_name")

    # call widget functions
    self.button.clicked.connect(self.clicker)

    # shows the app
    self.show()
  
  def clicker(self):
    # self.label.setText("You clicked the button!")
    fname = QFileDialog.getOpenFileName(self, "Select File", "", "LOLCode Files (*.lol)")
    path = fname[0]

    with open(path, "r") as f:
      content = f.read()  # Read the entire file content
      self.label.setText(content)  # Display the content in the label

       

# initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()