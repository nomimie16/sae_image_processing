from astropy.io import fits
from astroquery.mast import Observations
from matplotlib.colors import LogNorm



import matplotlib.pyplot as plt


# results = Observations.query_criteria(
#     obs_collection="JWST",            # Rechercher uniquement les observations de JWST
#     dataproduct_type="image",         # Type de produit (image)
#     instrument_name=["NIRCam", "MIRI"],  # Instruments (exemple : NIRCam, MIRI)
#     calib_level=3                     # Niveau de calibration (3 = données prêtes pour la science)
# )

# # Afficher quelques informations sur les observations
# print(results[:10]) 
# obs_ids = results['obs_id']
# print("IDDDDDD :", obs_ids[:1])    
             
def telechargement(objet: str):
    """ Fonction qui recupère les données d'une observation JWST et les télécharge. """
    
    jwst_observations = Observations.query_criteria( obs_collection="JWST", target_name=objet, dataRights="public")
    if len(jwst_observations) == 0:
        print(f"Aucune observation JWST trouvée pour l'objet {objet}.")
    #jwst_observations = Observations.query_object(objet,radius=".02 deg")
    # print(f"Observations trouvées: {jwst_observations}")
        
        
    data_products_by_obs = Observations.get_product_list(jwst_observations[0:2])
    # print(data_products_by_obs) 
    
    # obs = Observations.query_criteria(obs_collection="JWST", dataRights = "public",obs_id = 'jw01522-o002_t001_miri_f1800w-brightsky')
    

    # if len(obs) == 0:
    #     raise ValueError("Aucune observation trouvée pour les critères spécifiés.")

    # data_products = Observations.get_product_list(obs)
    # print(f"Data obtenues: {data_products}")
    
 
    manifest = Observations.download_products(data_products_by_obs, productType="SCIENCE",extension="fits")
    # print(manifest)
    
    local_path = manifest['Local Path'][0]
    # print(f"Chemin local du fichier téléchargé: {local_path}")

    return local_path

telechargement("NGC 1433")

# Charger le fichier FITS
# data = fits.getdata(telechargement('galaxie'))

# # Afficher l’image
# plt.imshow (data, norm=LogNorm() , origin='lower', cmap='viridis')
# plt.title('JWST')
# plt.colorbar()
# plt.show()
