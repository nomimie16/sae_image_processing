from astroquery.mast import Mast
from astroquery.mast import Observations
from astropy.io import fits


obs_collection = 'JWST'
target_name = 'M82'
instrument_name = 'NIRCAM/IMAGE'
proposal_id = ['1783']
obs_id = 'jw01522-o002_t001_miri_f1800w-brightsky'

obs = Observations.query_criteria(obs_collection=obs_collection, target_name=target_name)

print(f"Nombre d'observations trouvées: {obs}")

# telechargement

files = Observations.get_product_list(obs)
print(files)
Observations.download_products(files, productType="SCIENCE", extension="fits")
print("Téléchargement terminé.")


# obs_dowload = fits.getdata(telechargement('objet_choisi'))