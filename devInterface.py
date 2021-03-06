from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from rules import Rules
from statement import Statement
from workmemory import WorkMemory
from cnfStatement import CNFStatement

class DeveloperInterface(QWidget):
    """Graphic interface of the project (developer edition)"""
    #
    #   memRules: Ruleset to be saved to file. This is not for propagation
    #   variables: The work memory. It stores the values of the different 
    #       variables that had a value assigned to them.
    #   ruleHeap: Full copy of memRules in order to be used for propagation
    #   
    def __init__(self, parent=None):
        super(DeveloperInterface, self).__init__(parent)

        self.memRules = Rules("rulelist.json")
        self.variables = WorkMemory()

        self.inst_lbl = QLabel("Escribe una sentencia antecedente->consecuente")
        self.id_lbl = QLabel("Id:")
        self.val_lbl = QLabel("Value:")
        self.solv_lbl = QLabel("No se ha llegado a una solucion")

        self.st_edit = QLineEdit()
        self.var_edit = QLineEdit()

        self.values = QComboBox()
        self.values.addItem("T")
        self.values.addItem("F")

        self.refresh_button = QPushButton("Evaluate!")
        self.propagate_button = QPushButton("Propagate!")

        self.statements = QPlainTextEdit()
        self.rules = QPlainTextEdit()
        self.solutions = QPlainTextEdit()

        self.statements.setReadOnly(True)
        self.rules.setReadOnly(True)
        self.solutions = QPlainTextEdit()

        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.st_edit)
        self.hlayout.addWidget(self.refresh_button)

        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.id_lbl)
        self.hlayout2.addWidget(self.var_edit)
        self.hlayout2.addWidget(self.val_lbl)
        self.hlayout2.addWidget(self.values)
        self.hlayout2.addWidget(self.propagate_button)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.inst_lbl, 0, 0)
        self.main_layout.addLayout(self.hlayout, 1, 0)
        self.main_layout.addWidget(self.statements, 2, 0)
        self.main_layout.addLayout(self.hlayout2, 3, 0)
        self.main_layout.addWidget(self.rules, 4, 0)
        self.main_layout.addWidget(self.solv_lbl, 5, 0)
        self.main_layout.addWidget(self.solutions, 6, 0)

        self.refresh_button.clicked.connect(self.Evaluate)
        self.propagate_button.clicked.connect(self.Propagation)

        self.st_edit.setText("((a ^ b) ^ c) -> d")

        self.setLayout(self.main_layout)
        self.setWindowTitle("My first expert system")
        self.UpdateCache()
        self.PrintWorkMemory()

    def Evaluate(self):
        """Evaluates the statement and adds it to the rules"""
        statement = self.st_edit.text().strip()

        if(statement == ""):
            return

        new_cnf = CNFStatement(statement)
        cnf_list = new_cnf.Branch()

        for cnf in cnf_list:
            print("New Statement:", cnf)
            self.memRules.CreateRule(cnf)

        self.memRules.Save()
        self.UpdateCache()
        self.PrintWorkMemory()

    def UpdateCache(self):
        """Updates the rule buffer. Also displays all rules found until now"""
        self.ruleHeap = self.memRules.copy()
        self.rules.setPlainText( str(self.ruleHeap) )

    def PrintWorkMemory(self):
        self.statements.setPlainText( str(self.memRules) )

    def Propagation(self):
        var = self.var_edit.text().strip()
        value = self.values.currentText().strip()
        self.ruleHeap.Propagate(var, value)
        self.rules.setPlainText( str(self.ruleHeap) )

