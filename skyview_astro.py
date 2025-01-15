from astropy.io import fits
from astroquery.skyview import SkyView
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import os

print(SkyView.list_surveys())

target_name = 'M42'
obs_collection = ['2MASS-H', 'SwiftXRTInt', 'DSS']
radius = '0.5 deg'

# examples target : NGC 2024 M42 Andromeda Galaxy Betelgeuse Eta Carinae

def telecharger_fit(target_name, obs_collection):
    paths = SkyView.get_images(position=target_name, survey=obs_collection)
    for path in paths:
        print(' new file:', path)
    for i, img in enumerate(paths):
        filename = os.path.join('./images', f"image_{obs_collection[i]}.fits")
        img.writeto(filename, overwrite=True)
        print(f"Image sauvegardée : {filename}")
    SkyView.clear_cache()


telecharger_fit(target_name, obs_collection)
# DSS-M82


# data = fits.getdata(paths[0])

# # Afficher l’image
# plt.imshow(data, norm=LogNorm(), origin='lower', cmap='viridis')
# plt.colorbar()
# plt.show()


SkyView.clear_cache()