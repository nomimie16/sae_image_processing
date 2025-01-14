from astropy.io import fits
# from astroquery.skyview import SkyView
from astroquery.skyview import SkyView
from matplotlib.colors import LogNorm

# SkyView.list_surveys()  

paths = SkyView.get_images(position='Eta Carinae', survey=['Fermi 5', 'HRI', 'DSS'])
print(paths)

import matplotlib.pyplot as plt

# Charger le fichier FITS
data = fits.getdata ('Tarantula_Nebula-sii.fit' )

# Afficher l’image
plt.imshow (data, norm=LogNorm() , origin='lower' ,cmap='viridis')
plt.colorbar()
plt.show()
