from astroquery.mast import Mast
from astroquery.mast import Observations
from astropy.io import fits
import numpy as np



obs_collection = 'JWST'
target_name = 'M-33'
instrument_name = 'NIRCAM/IMAGE'
proposal_id = ['1783']
obs_id = 'jw01522-o002_t001_miri_f1800w-brightsky'

obs = Observations.query_criteria(obs_collection=obs_collection, target_name=target_name)

# print(obs["obs_id", "instrument_name", "target_name", "proposal_id"])
print(obs["obs_id", "dataRights"])

# Telechargement
files = Observations.get_product_list(obs)
print(f"Nombre de fichiers disponibles : {len(files)}")
print("GET PRODUCT LIST ", files[0])
Observations.download_products(files, productType="SCIENCE", extension="fits")
print("Téléchargement terminé.")

def normalize_data(self):
    color = []
    for img in self.image_list:
        vmin, vmax = np.percentile(img, [1, 99])
        normalized = np.clip((img - vmin) / (vmax - vmin), 0, 1)
        color.append(normalized)
    self.colors = np.destack([color[0],color[1],color[2]])
    