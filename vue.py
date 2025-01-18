#vue.py

import os
import sys
from astroquery.skyview import SkyView
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal, Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QListWidget, QLineEdit, QToolBar, QCompleter
from modele import Modele
from astropy.io import fits
import NouveauxFits



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
        self.labelObject = QLabel("Choisir une Object :")
        listObject = ['NGC 2024','M42', 'M82','M12','M31','M104', 'Andromeda Galaxy', 'Betelgeuse', 'Eta Carinae']
        listObject.sort()
        
        resultObject = QCompleter(listObject, self)
        resultObject.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        resultObject.setMaxVisibleItems(10)
        resultObject.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        
        self.researchObject = QLineEdit()
        self.researchObject.setPlaceholderText('Rechercher un objet ici')
        self.researchObject.setCompleter(resultObject)
        
        
        # choix du filtre
        self.labelFilter = QLabel("Choisir un filtre :")
        listFilter = ['Bleu', 'InfraRouge', 'Rouge']
        listFilter.sort()
        
        resultFilter = QCompleter(listFilter, self)
        resultFilter.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        resultFilter.setMaxVisibleItems(10)
        resultFilter.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        
        
        self.researchFilter = QLineEdit()
        self.researchFilter.setPlaceholderText('Rechercher une Object ici')
        self.researchFilter.setCompleter(resultFilter)

        #ajout dans le layout puis la fenetre
        self.selection.addWidget(self.labelObject)
        self.selection.addWidget(self.researchObject)
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
        self.btnValidate.clicked.connect(self.nouveaux_fits)
                
        # self.display_image(self.nouveaux_fits())
        
        
    # SLOT vers extérieur ------------------------------------------------
    closeBtnClicked = pyqtSignal()
    loadBtnClicked = pyqtSignal(str)



    # FONCTIONS ------------------------------------------------
    #Appel la fermeture de la fenêtre
    def closeWindow(self) -> None:
        self.closeBtnClicked.emit()
    
    def nouveaux_fits(self):
        
        object_searched = self.researchObject.text()
        filter_searched = self.researchFilter.text()
        match filter_searched:
            case "InfraRouge" | "infrarouge" | 'Infrarouge':
                filter_searched = "DSS2 IR"
            case "Rouge" | "rouge" :
                filter_searched = "DSS2 Red"
            case "Bleu" | "bleu" :
                filter_searched = "DSS2 Blue"
                
        print(object_searched)
        print(filter_searched)
        
        mFits : NouveauxFits = NouveauxFits.NouveauxFits(object_searched)                    
        paths : list = SkyView.get_images(position=mFits.object, survey=mFits.surveys, pixels=900)
        
        if paths == None:
            print("erreur : objet non trouvé")
        
        if mFits.fits_existe(paths):
            mFits.supprimer_fits()
        else:
            data = mFits.telecharger_fits(paths)
            chemin = mFits.chemin_fits(paths, filter_searched)            
            mFits.supprimer_fits(paths)
        
        mFits.supprimer_cache()
        self.loadBtnClicked.emit(chemin)
        
        return chemin
    
    #Affiche l'image de base
    def display_default_image(self):
        img_default = self.modele.load_image_default()
        if img_default is not None:
            self.ax.clear()
            self.ax.imshow(img_default)
            self.ax.set_title('Image par défaut')
            self.ax.axis('off')
            self.canvas.draw()
            
    #Centre la fenêtre
    def center_window(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)