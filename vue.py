#vue.py

import os
import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QListWidget, QLineEdit, QToolBar, QCompleter
from modele import Modele



class VueAstroPy(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.modele = Modele()
        
        # BARRE DE TITRE -----------------------------------------------------
        self.setWindowTitle('ASTRO')
        icon_path = os.path.join(sys.path[0], './img/logo.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Icon non trouvé à : {icon_path}")

        # CREATION DES LAYOUTS ----------------------------------------------------------
        self.central_widget = QWidget()
        self.central_layout = QHBoxLayout(self.central_widget)
        
        # LAYOUT IMAGE --------------------------------------------------------

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        #supprime les options non souhaitées de la tool-bar
        for action in self.toolbar.actions():
            if action.text() in ['Subplots', 'Home']:
                self.toolbar.removeAction(action)
            elif action.isSeparator() or not action.text():
                self.toolbar.removeAction(action)

        self.ax = self.figure.add_subplot(111)
        self.central_layout.addWidget(self.toolbar)
        self.central_layout.addWidget(self.canvas)
        
        self.display_default_image()
        
        
        # RECHERCHE DE L'UTILISATEUR --------------------------------------------------------
        self.selection = QVBoxLayout()       

        # choix de l'objet
        self.labelMission = QLabel("Choisir une mission :")
        listMission = ['ngc2024','m42', 'andromeda', 'galaxie', 'betelgeuse', 'etacarinae']
        listMission.sort()
        
        resultMission = QCompleter(listMission, self)
        resultMission.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        resultMission.setMaxVisibleItems(10)
        
        self.researchMission = QLineEdit()
        self.researchMission.setPlaceholderText('Rechercher une mission ici')
        self.researchMission.setCompleter(resultMission)
        
        
        # choix du filtre
        self.labelFilter = QLabel("Choisir un filtre :")
        listFilter = ['visible', 'rayon X', 'infrarouge', 'ultraviolet']
        listFilter.sort()
        
        resultFilter = QCompleter(listFilter, self)
        resultFilter.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        resultFilter.setMaxVisibleItems(10)
        
        self.researchFilter = QLineEdit()
        self.researchFilter.setPlaceholderText('Rechercher une mission ici')
        self.researchFilter.setCompleter(resultFilter)

        #ajout dans le layout puis la fenetre
        self.selection.addWidget(self.labelMission)
        self.selection.addWidget(self.researchMission)
        self.selection.addWidget(self.labelFilter)
        self.selection.addWidget(self.researchFilter)
        
        # bouton valider
        self.btnValidate = QPushButton("GO ! 🚀")
        self.selection.addWidget(self.btnValidate)
        
        # FERMETURE DE LA FENÊTRE --------------------------------------------
        self.btnClose = QPushButton("Fermer ❌")
        self.selection.addWidget(self.btnClose)
               
        
        # AFFICHAGE DE LA FENÊTRE --------------------------------------------
        self.central_layout.addLayout(self.selection)
        self.setCentralWidget(self.central_widget)
        self.center_window()
        self.show()
        
        # SLOT vers intérieur --------------------------------------------
        self.btnClose.clicked.connect(self.closeWindow)
        self.btnValidate.clicked.connect(self.loadFits)
        

    # SLOT vers extérieur ------------------------------------------------
    closeBtnClicked = pyqtSignal()
    loadBtnClicked = pyqtSignal(str)


    # FONCTIONS ------------------------------------------------
    def closeWindow(self) -> None:
        self.closeBtnClicked.emit()

    def loadFits(self):
        img_path = "C:/Users/lIcha/Documents/but/2_SAE/SAE_ASTRO_PHOTO/Tarantula_Nebula-halpha.fit"
        self.loadBtnClicked.emit(img_path)
    
    def display_default_image(self):
        img_default = self.modele.load_image_default()
        if img_default is not None:
            self.ax.clear()
            self.ax.imshow(img_default)
            self.ax.set_title('Image par défaut')
            self.ax.axis('off')
            self.canvas.draw()

    def center_window(self):
        #Centre la fenêtre
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)