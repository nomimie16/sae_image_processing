from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os
import NouveauxFits
from astroquery.skyview import SkyView


class Traitement:
    
    def __init__(self,fit, paths):
        self.red_file = fit.chemin_fits(paths, 'DSS2 Red')            
        self.blue_file = fit.chemin_fits(paths, 'DSS2 Blue')   
        self.ir_file = fit.chemin_fits(paths, 'DSS2 IR')  
        self.colors = None
        
    def load_fits_data(self):
        self.image_list = [
            fits.getdata(self.red_file),
            fits.getdata(self.blue_file),
            fits.getdata(self.ir_file)
        ]

    def normalize_data(self):
        color = []
        for img in self.image_list:
            vmin, vmax = np.percentile(img, [1, 99])
            normalized = np.clip((img - vmin) / (vmax - vmin), 0, 1)
            color.append(normalized)
        self.colors = np.dstack([color[0],color[1],color[2]])
        

    
    def getColors(self):
        return self.colors
        
        
        
if __name__ == '__main__':
    mFits : NouveauxFits = NouveauxFits.NouveauxFits('M104')    
    paths : list = SkyView.get_images(position=mFits.object, survey=mFits.surveys, pixels = 500)
    
    traitement = Traitement(mFits,paths)
    traitement.load_fits_data()
    traitement.normalize_data()
    traitement.getColors()
    plt.imshow(traitement.colors, origin='lower')
    plt.colorbar()
    plt.show()
    