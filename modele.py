#modele.py

import os
from astropy.io import fits
import matplotlib.pyplot as plt


class Modele:
        
    #récupère les image fits
    def load_fits_data(self, img_path):
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image file not found at {img_path}")
        return fits.getdata(img_path)
    
    #récupère l'image par défaut
    def load_image_default(self):
        img_path = "./img/logo.png"
        if os.path.exists(img_path):
            return plt.imread(img_path)
        else:
            print(f"Image non trouvée à : {img_path}")
            return None