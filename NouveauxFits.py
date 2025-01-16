from astropy.io import fits
from astroquery.skyview import SkyView
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import os
import random


class NouveauxFits:
    
    def __init__(self, object):
        # filtres
        self.surveys = ['DSS2 Red', 'DSS2 Blue', 'DSS2 IR']
        
        # si on a un parametre on l'utilise pour choisir l'objet
        if object:
            self.object = object
            
        #sinon on choisit un objet au hasard   
        else:
            liste_fits=['M82','M12','M42','M31','M104', 'Andromeda Galaxy', 'Betelgeuse', 'Eta Carinae']
            num = random.randint(0, len(liste_fits)-1)
            self.object = liste_fits[num]
    
    def getSurveys(self):
        return self.surveys
    
    def getObject(self):
        return self.object
    
    def setObject(self, object):
        self.object = object
            
    def telecharger_fits(self, paths): 
        # paths = SkyView.get_images(position=self.object, surveys=self.surveyss)

        for i, img in enumerate(paths):
            filename = os.path.join('./images', f"{self.object}_{self.surveys[i]}.fit")
            img.writeto(filename, overwrite=True)
            print(f"Image sauvegardée : {filename}")
        data = fits.getdata(filename)
        
        return data
    
    def fits_existe(self, paths):
        existe :bool =False
        for i, img in enumerate(paths):
            filename = os.path.join('./images', f"{self.object}_{self.surveys[i]}.fit")
            if os.path.exists(filename):
                existe=True
            else:
                existe=False
    
    def supprimer_fits(self, paths):
        for i, img in enumerate(paths):
            filename = os.path.join('./images', f"{self.object}_{self.surveys[i]}.fit")
            print(f"Image supprimée : {filename}")
            os.remove(filename)
            print(f"Image supprimée : {filename}")
            
            
    def afficher_fits(self,data):
        plt.imshow(data, norm=LogNorm(), origin='lower', cmap='viridis')
        plt.colorbar()
        plt.show()
    
    def supprimer_cache(self):
        SkyView.clear_cache()
        
if __name__ == '__main__':
    
    mFits : NouveauxFits = NouveauxFits('M82')
    # mFits = NouveauxFits()
    
    paths : list = SkyView.get_images(position=mFits.object, survey=mFits.surveys)
    
    if mFits.fits_existe(paths):
        mFits.supprimer_fits()
    else:
        data = mFits.telecharger_fits(paths)
        mFits.afficher_fits(data)
        mFits.supprimer_fits(paths)
        
   
    mFits.supprimer_cache()
    