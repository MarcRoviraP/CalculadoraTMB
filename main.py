from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
        
rutaBase = os.path.dirname(__file__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Valors default
        self.pes = 0
        self.altura = 0
        self.edat = 0
        self.sexe = "H"
        self.tmb = ""
        
        # Configuració de la finestra principal
        self.setWindowTitle("Calculadora de TMB")
        
        self.setFixedSize(300, 400)

        # Gestió del menú
        menu = self.menuBar()
        fitxer = menu.addMenu("Fitxer")
        
        tancaAction = QAction(QIcon(f"{rutaBase}/img/close.png"), "Tanca", self)
        resetAction = QAction(QIcon(f"{rutaBase}/img/reset.png"), "Restableix", self)
        tanca = fitxer.addAction(tancaAction)
        reset = fitxer.addAction(resetAction)
        
        tancaAction.triggered.connect(self.close)
        resetAction.triggered.connect(self.reset)
        
        toolbar = QToolBar("Toolbar reset")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(16, 16))
        toolbar.addAction(resetAction)
        self.addToolBar(toolbar)
        
        # Tabs
        
        tabs = QTabWidget()
        tabs.setMovable(False)
        tabs.setTabPosition(QTabWidget.North)
        
        tabs.addTab(self.calculs(), "Càlculs")
        tabs.addTab(self.informacio(), "Informació")
        
        
        statusBar = QStatusBar()
        self.tips = QLabel("Passa el ratolí per sobre del botó")
        self.tips.setObjectName("tips")
        statusBar.addWidget(self.tips)
        self.setStatusBar(statusBar)
        self.setCentralWidget(tabs)
    def reset(self):

        self.pesSpin.setValue(int(self.pes))
        self.alturaSpin.setValue(int(self.altura))
        self.edatSpin.setValue(int(self.edat))
        self.radioH.setChecked(True)
        self.resultat.setText("")
        
    
    def calculs(self) -> QWidget:
        grid = QGridLayout()

        # Etiquetas y widgets de la primera columna
        lblGenere = QLabel("Gènere:")
        grid.addWidget(lblGenere, 0, 0)

        lblPes = QLabel("Pes:")
        grid.addWidget(lblPes, 0, 1)

        # Selección de género
        radioGroup = QVBoxLayout()
        self.radioH = QRadioButton("Home")
        self.radioH.setChecked(True)
        self.radioD = QRadioButton("Dona")
        radioGroup.addWidget(self.radioH)
        radioGroup.addWidget(self.radioD)

        grid.addLayout(radioGroup, 1, 0)

        # SpinBox para peso
        self.pesSpin = QSpinBox()
        self.pesSpin.setRange(0, 300)
        self.pesSpin.setValue(int(self.pes))
        self.pesSpin.setSuffix(" kg")
        grid.addWidget(self.pesSpin, 1, 1)

        # Etiquetas y widgets de la segunda fila
        lblEdat = QLabel("Edat:")
        grid.addWidget(lblEdat, 2, 0)

        lblAltura = QLabel("Alçada:")
        grid.addWidget(lblAltura, 2, 1)

        # SpinBox para edad
        self.edatSpin = QSpinBox()
        self.edatSpin.setRange(0, 150)
        self.edatSpin.setValue(int(self.edat))
        self.edatSpin.setSuffix(" anys")
        grid.addWidget(self.edatSpin, 3, 0)

        # SpinBox para altura
        self.alturaSpin = QSpinBox()
        self.alturaSpin.setRange(0, 250)
        self.alturaSpin.setValue(int(self.altura))
        self.alturaSpin.setSuffix(" cm")
        grid.addWidget(self.alturaSpin, 3, 1)

        

        hLayout = QHBoxLayout()
        # Botón Calcular y Resultado
        self.btnCalcular = QPushButton("Calcular")
        self.btnCalcular.clicked.connect(self.calcular)
        
        hLayout.addWidget(self.btnCalcular)

        self.resultat = QLineEdit("")
        self.resultat.setReadOnly(True)
        self.resultat.setAlignment(Qt.AlignCenter) 
        hLayout.addWidget(self.resultat)
        
        grid.addLayout(hLayout, 4, 0, 1, 2)

        # Igualar el ancho de las columnas
        grid.setColumnStretch(0, 1)  # Primera columna
        grid.setColumnStretch(1, 1)  # Segunda columna

        widget = QWidget()
        widget.setLayout(grid)
        
        # Instalar el filtro de eventos
        self.btnCalcular.installEventFilter(self)
        self.pesSpin.installEventFilter(self)
        self.alturaSpin.installEventFilter(self)
        self.edatSpin.installEventFilter(self)
        self.radioH.installEventFilter(self)
        self.radioD.installEventFilter(self)
        
        return widget
    
    def informacio(self) -> QWidget:
        rutaDocument = rutaBase + "/txt/text_info.txt"
        
        document = open(rutaDocument, "r")
        lineas = document.readlines()
        document.close()
        
        masInfo = QLabel(lineas[0])
        mainInfo = QLabel(lineas[1])
        mainInfo.setWordWrap(True)
        mainInfo.setObjectName("mainInfo")
        
        mainInfo.setAlignment(Qt.AlignJustify)

        formules = QLabel(f"{lineas[2]}\n{lineas[3]}")
        formules.setWordWrap(True)
        formules.setObjectName("formules")
        
        layout = QVBoxLayout()
        layout.addWidget(mainInfo)
        layout.addWidget(formules)
        
        self.btnMasInfo = QPushButton("+Info")
        self.btnMasInfo.setObjectName("btnMasInfo")
        
        self.btnMasInfo.clicked.connect(lambda: QMessageBox.information(self, "Informacio Adicional", masInfo.text()))
        layout.addWidget(self.btnMasInfo)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        
        
        self.btnMasInfo.installEventFilter(self)
        return widget

    
    
    def eventFilter(self, source, event):
        
        tip = ""
        
        if event.type() == QEvent.Enter:
            if source == self.btnCalcular:
                tip = "Fes clic per a calcular"
            elif source == self.pesSpin:
                tip = "Introdueix el teu pes en kg"
            elif source == self.alturaSpin:
                tip = "Introdueix la teua altura en cm"
            elif source == self.edatSpin:
                tip = "Introdueix la teua edat en anys"
            elif source == self.radioH:
                tip = "Selecciona el teu gènere (Home)"
            elif source == self.radioD:
                tip = "Selecciona el teu gènere (Dona)"
            elif source == self.btnMasInfo:
                tip = "Clica per a més informació"
            
            self.tips.setText(tip)
        if event.type() == QEvent.Leave:
            self.tips.setText("") 
        return super().eventFilter(source, event)
    
    def calcular(self):
        pes = self.pesSpin.value()
        altura = self.alturaSpin.value()
        edat = self.edatSpin.value()
        
        if self.radioH.isChecked():
            sexe = "H"
        else:
            sexe = "D"
        
        if sexe == "H":
            self.tmb = 10 * pes + 6.25 * altura - 5 * edat + 5
        else:
            self.tmb = 10 * pes + 6.25 * altura - 5 * edat - 161
        self.resultat.setText(str(self.tmb))
        
    
        
app = QApplication([])
app.setStyleSheet(open(f"{rutaBase}/styles/style.qss").read())
window = MainWindow()
window.show()
app.exec_()

