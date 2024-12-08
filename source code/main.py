from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QLabel, QTableWidget, QTableWidgetItem, QPlainTextEdit
from PyQt5 import uic
from PyQt5.QtCore import QEventLoop, QTimer
import sys
import analyzers.lexical_analyzer as lexical_analyzer
from analyzers.syntax_analyzer import Syntax_Analyzer
from analyzers.semantic_analyzer import Semantic_Analyzer

class UI(QMainWindow):
  def __init__(self):
    super(UI, self).__init__()

    # load the ui file
    uic.loadUi("gui.ui", self)

    # buttons
    self.open_button = self.findChild(QPushButton, "open_file_button")
    self.execute_button = self.findChild(QPushButton, "execute_button")

    # label
    self.label_filename = self.findChild(QLabel, "label_filename")
    self.label_console = self.findChild(QPlainTextEdit, "console")
    self.label_console.setReadOnly(True)

    # tables
    self.lexeme_table = self.findChild(QTableWidget, "lexeme_table")
    self.symbol_table = self.findChild(QTableWidget, "symbol_table")

    # text editor and input
    self.text_editor = self.findChild(QTextEdit, "print_file")

    # call widget functions
    self.open_button.clicked.connect(self.open_file)
    self.execute_button.clicked.connect(self.execute)

    # initializations
    self.file_path = None
    self.analyzer = None

    # shows the app
    self.show()
  
  # --------------------------------------------------------------------------------------------------
  # function for opening file, ensuring that only file with .lol are opened
  # --------------------------------------------------------------------------------------------------
  def open_file(self):
    fname = QFileDialog.getOpenFileName(self, "Select File", "", "LOLCode Files (*.lol)")
    if not fname[0]:  # check if a file was selected
        return
    self.file_path = fname[0]

    self.label_filename.setText(self.file_path)

    with open(self.file_path, "r") as f:
      content = f.read()  # read the entire file content
      self.text_editor.setText(content)  # display the content in the label

    # clear contents when execute is pressed
    self.clear_contents()

  # --------------------------------------------------------------------------------------------------
  # function that calls the lexical, syntactical, and semantical analyzers
  # --------------------------------------------------------------------------------------------------
  def execute(self):
    # clear contents in gui at every execute
    self.clear_contents()

    # get the current content of the text editor after clicking the execute button
    content = self.text_editor.toPlainText()

    lexemes_copy = []

    # if file is not empty, perform lexeme analysis
    if content:
      # lexical analysis
      lexemes, error_msg = lexical_analyzer.analyze_lexemes(content)
      print(lexemes)
      if error_msg:
        self.label_console.setPlainText(error_msg)
      else:
        try:
          lexemes_copy = lexemes.copy()
          # syntactical analysis
          parser = Syntax_Analyzer(lexemes)
          parse_tree = parser.analyze()
          if isinstance(parse_tree, str):
            self.label_console.setPlainText(parse_tree)
        except SyntaxError as e:
          self.label_console.setPlainText(str(e))
      self.populate_lexeme_table(lexemes_copy)

      # if parse tree is not empty 
      if parse_tree:
        # semantical analysis
        try:
          self.analyzer = Semantic_Analyzer(parse_tree, self)
          symbols = self.analyzer.analyze()
          self.populate_symbol_table(symbols)
        except Exception as e:
          self.label_console.setPlainText(f"Error during semantic analysis: {str(e)}")

      # changes made in the text editor will be saved in the original file
      if self.file_path:
        with open(self.file_path, "w") as f:
          f.write(content)

  # --------------------------------------------------------------------------------------------------
  # function to print in the console when VISIBLE is implemented
  # --------------------------------------------------------------------------------------------------
  def print_in_console(self, message):
    current_text = self.label_console.toPlainText()  # get the current text
    if message == "None":
      message = "NOOB"
    elif message == "True":
      message = "WIN"
    elif message == "False":
      message = "FAIL"
    else: 
      if ":)" in message: 
        message = message.replace(":)", '\n')
      if ":>" in message: 
        message = message.replace(":>", '\t')
      # if ":o" in message: 
      #   message = message.replace(":o", '\g')
      if "::" in message:
        message = message.replace("::", ":")
      # if ':"' in message:
      #   message = message.replace(':"', '\"')

    new_text = current_text + "\n" + message if current_text else message  # append the new message
    self.label_console.setPlainText(new_text)  # update the console

  # --------------------------------------------------------------------------------------------------
  # function for populating the lexeme table, clearing the previous contents
  # --------------------------------------------------------------------------------------------------
  def populate_lexeme_table(self, lexemes):
    self.lexeme_table.setRowCount(len(lexemes))   # get the length of the lexemes and set it as the number of rows of the table widget
      
    # populate the table
    for row, (lexeme, classification) in enumerate(lexemes):
      self.lexeme_table.setItem(row, 0, QTableWidgetItem(lexeme))
      self.lexeme_table.setItem(row, 1, QTableWidgetItem(classification))

  # --------------------------------------------------------------------------------------------------
  # function for populating the symbol table, clearing the previous contents
  # --------------------------------------------------------------------------------------------------
  def populate_symbol_table(self, symbols):
    self.symbol_table.setRowCount(len(symbols))

    # populate the table
    for row, (symbol, value) in enumerate(symbols.items()):
      self.symbol_table.setItem(row, 0, QTableWidgetItem(symbol))
      if isinstance(value, str):
        str_value = "\"" + str(value) + "\""
        self.symbol_table.setItem(row, 1, QTableWidgetItem(str_value))
      elif value == None:
        self.symbol_table.setItem(row, 1, QTableWidgetItem("NOOB"))
      elif value == True:
        self.symbol_table.setItem(row, 1, QTableWidgetItem("WIN"))
      elif value == False:
        self.symbol_table.setItem(row, 1, QTableWidgetItem("FAIL"))
      else:
        self.symbol_table.setItem(row, 1, QTableWidgetItem(str(value)))

  # --------------------------------------------------------------------------------------------------
  # function for clearing the contents in the lexeme table, symbol table, and console
  # --------------------------------------------------------------------------------------------------
  def clear_contents(self):
    # clear tables and console when a new file is opened
    self.lexeme_table.clearContents()
    self.symbol_table.clearContents()
    self.label_console.clear()
        

# initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()