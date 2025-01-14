from astropy.io import fits
from astroquery.mast import Observations
from matplotlib.colors import LogNorm



import matplotlib.pyplot as plt
import csv

def recherche_csv(fichier_csv, chaine_recherchee):
    with open(fichier_csv, mode='r', newline='', encoding='utf-8') as csvfile:
        lecteur_csv = csv.reader(csvfile)
        for ligne in lecteur_csv:
            if chaine_recherchee in ','.join(ligne):
                print(f"Chaîne trouvée dans la ligne: {ligne[3]}")
                break
    return ligne[3]
                

                
def telechargement(objet: str):
    """ Fonction qui recupère les données d'une observation JWST et les télécharge. """
    
    obs = Observations.query_criteria(obs_collection='JWST', instrument_name='NIRCAM/IMAGE', proposal_id=['1783'],  dataRights="public",)
    
    # obs = Observations.query_criteria(obs_collection="JWST", dataRights="public", obs_id="jw01522-o002_t001_miri_f1800w-brightsky")
    # obs = Observations.query_criteria(obs_collection="JWST", dataRights="public", obs_id=recherche_csv('mast.csv', 'A611'))
    print(f"Observations trouvées: {obs}")

    if len(obs) == 0:
        raise ValueError("Aucune observation trouvée pour les critères spécifiés.")

    data_products = Observations.get_product_list(obs)
    print(f"Data obtenues: {data_products}")

    dowload_fits = Observations.download_products(data_products, productType="SCIENCE", extension="fits")
    print(f"dowload_fits de téléchargement: {dowload_fits}")

    if dowload_fits is None or len(dowload_fits) == 0:
        raise ValueError("Aucun produit téléchargé.")

    # Récupérer le chemin local du premier fichier téléchargé
    path = dowload_fits['Local Path'][0]
    print(f"Chemin local du fichier téléchargé: {path}")

    return path


# Charger le fichier FITS
obs_dowload = fits.getdata(telechargement('objet_choisi'))

# Afficher l’image
plt.imshow (obs_dowload, norm=LogNorm() , origin='lower', cmap='viridis')
plt.title('JWST')
plt.colorbar()
plt.show()
