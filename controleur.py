#controleur.py


from PyQt6.QtWidgets import QMessageBox, QComboBox, QFileDialog
from PyQt6.QtGui import QIcon
from modele import Modele
from vue import VueAstroPy
import json
import numpy as np


class Controleur():
    
    # constructeur
    def __init__(self) -> None: 
        
        self.modele = Modele()
        self.vue = VueAstroPy()
        
        # signaux venant de la vue ---> redirigés vers slots du controleur
        self.vue.closeBtnClicked.connect(self.closeW)
        self.vue.loadBtnClicked.connect(self.load_img)
        
        
    def closeW(self):
        self.vue.close()

    def load_img(self, data_json):
        titre = self.vue.researchObject.text()
        try:
            received_data = json.loads(data_json)  # Décoder le JSON
            img_data = np.array(received_data)
            #affichage des données
            self.vue.ax.clear()
            self.vue.ax.imshow(img_data, origin='lower')
            self.vue.ax.set_title(titre)
            self.vue.ax.axis('on')
            self.vue.canvas.draw()
        except FileNotFoundError as e:
            print(" ⚠ Pas de fichier fits à afficher",e)