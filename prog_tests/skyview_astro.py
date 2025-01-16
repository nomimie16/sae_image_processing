from astropy.io import fits
from astroquery.skyview import SkyView
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import os

print(SkyView.list_surveys())

objet = 'M82'
obs_collection = ['DSS2 Red', 'DSS2 Blue', 'DSS2 IR']
radius = '0.5 deg'

# examples target : NGC 2024 M42 Andromeda Galaxy Betelgeuse Eta Carinae

def telecharger_fit(objet, obs_collection):
    paths = SkyView.get_images(position=objet, survey=obs_collection)

    for i, img in enumerate(paths):
        filename = os.path.join('./images', f"{objet}_{obs_collection[i]}.fit")
        img.writeto(filename, overwrite=True)
        print(f"Image sauvegardée : {filename}")
        
    data = fits.getdata(filename)
    
    return data



# DSS-M82




# Afficher l’image
plt.imshow(telecharger_fit(objet, obs_collection), norm=LogNorm(), origin='lower', cmap='viridis')
plt.colorbar()
plt.show()


SkyView.clear_cache()