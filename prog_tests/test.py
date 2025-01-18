from astroquery.mast import Observations

def telechargement(objet: str):
    from astroquery.mast import Observations
    import numpy as np
    
    from astroquery.mast import Observations

 
    jwst_observations = Observations.query_criteria(obs_collection="JWST", target_name="M82")
    print(jwst_observations)


    data_products = Observations.get_product_list(jwst_observations)
    print(f"Produits associés disponibles : {len(data_products)}")

    if len(data_products) > 0:
        print(data_products['productFilename', 'productType', 'description'][0:10])

    
    # Filtrage pour les fichiers FITS de type SCIENCE
    science_products = data_products[
        (data_products['productType'] == 'SCIENCE') & 
        (np.char.endswith(data_products['productFilename'].astype(str), '.fits'))
    ]
    print(f"Produits scientifiques FITS trouvés : {len(science_products)}")
    if len(science_products) == 0:
        print("Aucun produit scientifique avec extension FITS trouvé.")
        return None
    
    # Téléchargement des produits
    manifest = Observations.download_products(science_products)
    print("Téléchargement terminé.")
    return manifest

# Testez avec une cible
telechargement("M82B")



