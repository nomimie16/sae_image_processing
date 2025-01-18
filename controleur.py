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
        try:
            received_data = json.loads(data_json)  # Décoder le JSON
            img_data = np.array(received_data)
            # img_data = img_path
            print("IMMMMMGGG_______PATHHHHHH",received_data)
            #affichage des données
            self.vue.ax.clear()
            self.vue.ax.imshow(img_data, origin='lower')
            self.vue.ax.set_title("Astroquery")
            self.vue.ax.axis('on')
            self.vue.canvas.draw()
        except FileNotFoundError as e:
            print("ftgvrhbndnjd,s",e)