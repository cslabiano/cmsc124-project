from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QLabel, QTableWidget, QTableWidgetItem
from PyQt5 import uic
import sys
import analyzers.lexical_analyzer as lexical_analyzer
from analyzers.syntax_analyzer import Syntax_Analyzer
from analyzers.semantic_analyzer import Semantic_Analyzer

class UI(QMainWindow):
  def __init__(self):
    super(UI, self).__init__()

    # load the ui file
    uic.loadUi("gui.ui", self)

    #buttons
    self.open_button = self.findChild(QPushButton, "open_file_button")
    self.execute_button = self.findChild(QPushButton, "execute_button")

    # label
    self.label_filename = self.findChild(QLabel, "label_filename")
    self.label_console = self.findChild(QLabel, "console")

    # tables
    self.lexeme_table = self.findChild(QTableWidget, "lexeme_table")
    self.symbol_table = self.findChild(QTableWidget, "symbol_table")

    # text editor
    self.text_editor = self.findChild(QTextEdit, "print_file")

    # call widget functions
    self.open_button.clicked.connect(self.open_file)
    self.execute_button.clicked.connect(self.execute)

    # initialize the file path
    self.file_path = None

    # shows the app
    self.show()
  
  def open_file(self):
    fname = QFileDialog.getOpenFileName(self, "Select File", "", "LOLCode Files (*.lol)")
    if not fname[0]:  # check if a file was selected
        return
    self.file_path = fname[0]

    self.label_filename.setText(self.file_path)

    with open(self.file_path, "r") as f:
      content = f.read()  # read the entire file content
      self.text_editor.setText(content)  # display the content in the label
    
    # clear tables and console when a new file is opened
    self.lexeme_table.clearContents()
    self.symbol_table.clearContents()
    self.label_console.setText("")

  def execute(self):
    # get the current content of the text editor after clicking the execute button
    content = self.text_editor.toPlainText()

    lexemes_copy = []

    # if file is not empty, perform lexeme analysis
    if content:
      # lexical analysis
      lexemes, error_msg = lexical_analyzer.analyze_lexemes(content)
      print(lexemes)
      if error_msg:
        self.label_console.setText(error_msg)
      else:
        try:
          lexemes_copy = lexemes.copy()
          # syntactical analysis
          parser = Syntax_Analyzer(lexemes)
          parse_tree = parser.analyze()
          if isinstance(parse_tree, str):
            self.label_console.setText(parse_tree)
          else:
            self.label_console.setText("Syntax is valid.\n")
        except SyntaxError as e:
          self.label_console.setText(str(e))
      self.populate_lexeme_table(lexemes_copy)

      # if parse tree is not empty 
      if parse_tree:
        # semantical analysis
        analyzer = Semantic_Analyzer(parse_tree)
        symbols = analyzer.analyze()
        self.populate_symbol_table(symbols)

      # changes made in the text editor will be saved in the original file
      if self.file_path:
        with open(self.file_path, "w") as f:
          f.write(content)

  def populate_lexeme_table(self, lexemes):
    self.lexeme_table.clearContents()   # clear previous contents of the table
    self.lexeme_table.setRowCount(len(lexemes))   # get the length of the lexemes and set it as the number of rows of the table widget
      
    # populate the table
    for row, (lexeme, classification) in enumerate(lexemes):
      self.lexeme_table.setItem(row, 0, QTableWidgetItem(lexeme))
      self.lexeme_table.setItem(row, 1, QTableWidgetItem(classification))

  def populate_symbol_table(self, symbols):
    self.symbol_table.clearContents()
    self.symbol_table.setRowCount(len(symbols))

    # populate the table
    for row, (symbol, value) in enumerate(symbols.items()):
      self.symbol_table.setItem(row, 0, QTableWidgetItem(symbol))
      self.symbol_table.setItem(row, 1, QTableWidgetItem(str(value)))

# initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()