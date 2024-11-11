from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog
from PyQt5 import uic
import sys

class UI(QMainWindow):
  def __init__(self):
    super(UI, self).__init__()

    # load the ui file
    uic.loadUi("gui.ui", self)

    # define widgets
    self.open_button = self.findChild(QPushButton, "open_file_button")
    self.text_editor = self.findChild(QTextEdit, "print_file")
    self.execute_button = self.findChild(QPushButton, "execute_button")

    # call widget functions
    self.open_button.clicked.connect(self.open_file)
    self.execute_button.clicked.connect(self.save_file)

    # initialize the file path
    self.file_path = None

    # shows the app
    self.show()
  
  def open_file(self):
    # self.label.setText("You clicked the button!")
    fname = QFileDialog.getOpenFileName(self, "Select File", "", "LOLCode Files (*.lol)")
    self.file_path = fname[0]

    with open(self.file_path, "r") as f:
      content = f.read()  # read the entire file content
      self.text_editor.setText(content)  # display the content in the label

  def save_file(self):
    # check if there's a file opened
    if self.file_path:
      with open(self.file_path, "w") as f:
        content = self.text_editor.toPlainText()  # get content from QTextEdit
        f.write(content)  # write content back to the file
    else:
      print("No file opened to save.")
       

# initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()