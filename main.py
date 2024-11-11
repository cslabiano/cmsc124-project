from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QLabel, QTableWidget, QTableWidgetItem
from PyQt5 import uic
import sys
import lexical_analyzer

class UI(QMainWindow):
  def __init__(self):
    super(UI, self).__init__()

    # load the ui file
    uic.loadUi("gui.ui", self)

    # define widgets
    self.open_button = self.findChild(QPushButton, "open_file_button")
    self.text_editor = self.findChild(QTextEdit, "print_file")
    self.execute_button = self.findChild(QPushButton, "execute_button")
    self.lexeme_table = self.findChild(QTableWidget, "lexeme_table")

    # call widget functions
    self.open_button.clicked.connect(self.open_file)
    self.execute_button.clicked.connect(self.execute)

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

  def execute(self):
    # get the current content of the text editor after clicking the execute button
    content = self.text_editor.toPlainText()

    # if file is not empty, perform lexeme analysis
    if content:
      lexemes = lexical_analyzer.analyze_lexemes(content)
      self.lexeme_table.clearContents()   # clear previous contents of the table

      self.lexeme_table.setRowCount(len(lexemes))   # get the length of the lexemes and set it as the number of rows of the table widget

      # populate the table
      for row, (lexeme, classification) in enumerate(lexemes):
        self.lexeme_table.setItem(row, 0, QTableWidgetItem(lexeme))
        self.lexeme_table.setItem(row, 1, QTableWidgetItem(classification))

      # changes made in the text editor will be saved in the original file
      if self.file_path:
        with open(self.file_path, "w") as f:
          f.write(content)

# initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()