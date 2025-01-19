#vue.py

import os
import sys
from astroquery.skyview import SkyView
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import pyqtSignal, Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QListWidget, QLineEdit, QToolBar, QCompleter
from modele import Modele
from astropy.io import fits
import json
import NouveauxFits, Traitement



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
        self.total_layout = QHBoxLayout(self.central_widget)
        
        # POLICE D'ECRITURE ----------------------------------------------------------
        fontBig = QFont()
        fontBig.setPointSize(12)
        
        # LAYOUT IMAGE --------------------------------------------------------
        self.central_layout = QVBoxLayout()
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
        self.selection.addSpacing(50)

        # choix de l'objet
        self.labelObject = QLabel("Choisir un objet :")
        self.labelObject.setFont(fontBig)
        listObject = ['Vega', 'Meissa', 'Alnilam', 'Deneb','NGC 7635','NGC 2024', 'IC 5070', 'IC 435', 'NGC 2237', 'Alnitak', 'NGC 4631', 'M82','M45','M42','M31','M104', 'M87', 'IC 434', 'IC 5070', 'Rigel', 'Barnard 33', 'SH 2-308', 'Andromeda Galaxy', 'Betelgeuse', 'Roslund 4','Barnard’s Loop']
        listObject.sort()
        
        resultObject = QCompleter(listObject, self)
        resultObject.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        resultObject.setMaxVisibleItems(10)
        resultObject.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        
        self.researchObject = QLineEdit()
        self.researchObject.setFont(fontBig)
        self.researchObject.setFixedSize(210,40)
        self.researchObject.setPlaceholderText('Rechercher un objet ici')
        self.researchObject.setCompleter(resultObject)

        
        # choix du nb pixel
        self.labelPixel = QLabel("Choisir un nombre de pixel :")
        self.labelPixel.setFont(fontBig)
        self.listPixel = QComboBox()
        self.listPixel.setFixedSize(210,40)
        self.listPixel.setFont(fontBig)
        self.listPixel.addItems(['500', '1000','1300','1800'])
        

        #ajout dans le layout puis la fenetre
        self.selection.addWidget(self.labelObject)
        self.selection.addSpacing(-80)
        self.selection.addWidget(self.researchObject)
        self.selection.addWidget(self.labelPixel)
        self.selection.addSpacing(-80)
        self.selection.addWidget(self.listPixel) 
        self.selection.addSpacing(100)
        
        # bouton valider
        self.btnValidate = QPushButton("GO ! 🚀")
        self.btnValidate.setObjectName("bothButton")
        self.btnValidate.setFixedSize(210,40)
        self.btnValidate.setFont(fontBig)
        self.selection.addWidget(self.btnValidate)
        
        
        # FERMETURE DE LA FENÊTRE --------------------------------------------
        self.btnClose = QPushButton("Fermer ❌")
        self.btnClose.setObjectName("bothButton")
        self.btnClose.setFixedSize(210,40)
        self.btnClose.setFont(fontBig)
        self.selection.addWidget(self.btnClose)

        
        # AFFICHAGE DE LA FENÊTRE --------------------------------------------
        self.total_layout.addLayout(self.central_layout)
        self.total_layout.addSpacing(10)
        self.total_layout.addLayout(self.selection)
        self.total_layout.addSpacing(10)
        self.setCentralWidget(self.central_widget)
        self.setFixedSize(800,600)
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
        pixel_searched = self.listPixel.currentText()
                
        print(object_searched)
        print(pixel_searched)
        
        mFits : NouveauxFits = NouveauxFits.NouveauxFits(object_searched)    
        paths : list = SkyView.get_images(position=mFits.object, survey=mFits.surveys, pixels = pixel_searched)
        
        if paths == None:
            print("erreur : objet non trouvé")
        
        if mFits.fits_existe(paths):
            mFits.supprimer_fits()
        else:
            data = mFits.telecharger_fits(paths)


        # print("FILTRRRRRE",filter_searched)
        traitement = Traitement.Traitement(mFits,paths)
        traitement.load_fits_data()
        traitement.normalize_data()
        data_img = traitement.getColors()
        data_str = json.dumps(data_img.tolist())
        
        # print(data_img)
        self.loadBtnClicked.emit(data_str)
        mFits.supprimer_cache()
        
        return data_img
    
    #Affiche l'image de base
    def display_default_image(self):
        img_default = self.modele.load_image_default()
        if img_default is not None:
            self.ax.clear()
            self.ax.imshow(img_default)

            self.ax.axis('off')
            self.canvas.draw()
            
    #Centre la fenêtre
    def center_window(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)