from astropy.io import fits
from astroquery.skyview import SkyView
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import os


class NouveauxFits:
    
    def __init__(self, object):
        self.object = object
        self.surveys = ['DSS2 Red', 'DSS2 Blue', 'DSS2 IR']

        
    def telecharger_fits(self, paths): 
        # paths = SkyView.get_images(position=self.object, surveys=self.surveyss)

        for i, img in enumerate(paths):
            filename = os.path.join('./images', f"{self.object}_{self.surveys[i]}.fit")
            img.writeto(filename, overwrite=True)
            print(f"Image sauvegardée : {filename}")
        data = fits.getdata(filename)
        
        return data
    
    def fits_existe(self, paths):
        existe=False;
        for i, img in enumerate(paths):
            filename = os.path.join('./images', f"{self.object}_{self.surveys[i]}.fit")
            if os.path.exists(filename):
                print(f"Image existe : {filename}")
                existe=True
            else:
                print(f"Image n'existe pas : {filename}")
                existe=False
    
    def supprimer_fits(self, paths):
        for i, img in enumerate(paths):
            filename = os.path.join('./images', f"{self.object}_{self.surveys[i]}.fit")
            os.remove(filename)
            print(f"Image supprimée : {filename}")
            
            
    def afficher_fits(self,data):
        plt.imshow(data, norm=LogNorm(), origin='lower', cmap='viridis')
        plt.colorbar()
        plt.show()
    
    def supprimer_cache(self):
        SkyView.clear_cache()
        
if __name__ == '__main__':
    
    mFits = NouveauxFits('M12')
    
    paths = SkyView.get_images(position=mFits.object, survey=mFits.surveys)
    if mFits.fits_existe(paths):
        mFits.supprimer_fits()
    else:
        data = mFits.telecharger_fits(paths)
        mFits.afficher_fits(data)
        mFits.supprimer_fits(paths)
        
   
    mFits.supprimer_cache()
    