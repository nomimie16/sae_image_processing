#controleur.py


from PyQt6.QtWidgets import QMessageBox, QComboBox, QFileDialog
from PyQt6.QtGui import QIcon
from modele import Modele
from vue import VueAstroPy


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

    def load_img(self, img_path):
        try:
            img_data = self.modele.load_fits_data(img_path)
            #affichage des données
            self.vue.ax.clear()
            self.vue.ax.imshow(img_data, cmap='magma', origin='lower')
            self.vue.ax.set_title(img_path)
            self.vue.ax.axis('on')
            self.vue.canvas.draw()
        except FileNotFoundError as e:
            print(e)