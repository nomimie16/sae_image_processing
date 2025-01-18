from astropy.io import fits
from astroquery.skyview import SkyView
from matplotlib.colors import LogNorm
import matplotlib.C as plt
import os
import random


class NouveauxFits:
    
    def __init__(self, object=None):
        # filtres
        self.surveys = ['DSS2 Red', 'DSS2 Blue', 'DSS2 IR']
        # self.surveys = ['2MASS-J', '2MASS-H', '2MASS-K']
        # self.surveys = ['SwiftXRTCnt', 'SwiftXRTExp', 'SwiftXRTInt']
        # self.surveys = ['RASS Background 1', 'RASS Background 2', 'RASS Background 3']
    # Exemples de relevés à utiliser
        # self.surveys = ['2MASS-J', 'GALEX Near UV', 'DSS2 Red']

        
        
        
        # si on a un parametre on l'utilise pour choisir l'objet
        if object:
            self.object = object           
        #sinon on choisit un objet au hasard   
        else:
            liste_fits=['NGC 2024', 'NGC 2237', 'M82','M45','M42','M31','M104', 'M87', 'Andromeda Galaxy', 'Betelgeuse', 'Eta Carinae']
            num = random.randint(0, len(liste_fits)-1)
            self.object = liste_fits[num]
        
        self.destination_dir = './images'
    
    def getSurveys(self):
        return self.surveys
    
    def getObject(self):
        return self.object
    
    def setObject(self, object):
        self.object = object
        
    import os

    def chemin_fits(self, paths, survey):
        if paths:
            # Vérification de l'existence du répertoire de destination
            if not os.path.exists(self.destination_dir):
                try:
                    os.makedirs(self.destination_dir)  # Crée le répertoire si nécessaire
                except Exception as e:
                    print(f"Erreur lors de la création du répertoire : {e}")
                    return None
            
            # Recherche d'un fichier qui contient à la fois self.object et le survey dans son nom
            found_file = None
            for filename in os.listdir(self.destination_dir):
                if self.object in filename and survey in filename:  # Le fichier doit contenir self.object et survey
                    found_file = filename
                    break  # Quitter dès qu'on trouve un fichier correspondant

            if found_file:
                # Si un fichier correspondant a été trouvé
                file_path = os.path.join(self.destination_dir, found_file)
                print(f"Fichier trouvé : {file_path}")
                return file_path
            else:
                print(f"Erreur : aucun fichier trouvé avec '{self.object}' et '{survey}' dans {self.destination_dir}")
                return None
        else:
            print("Erreur : objet non trouvé ou relevé non disponible")
            return None


            
    def telecharger_fits(self, paths): 
        # fonction qui télécharge les fits grace à une liste récupérée par le programme sur Skyview
        # paths = SkyView.get_images(position=self.object, surveys=self.surveyss)

        for i, img in enumerate(paths):
            filename = os.path.join('./images', f"{self.object}_{self.surveys[i]}.fit")
            img.writeto(filename, overwrite=True)
            print(f"Image sauvegardée : {filename}")
        data = fits.getdata(filename)
        
        return data
    
    def fits_existe(self, paths):
        # fonction qui vérifie si les fits existent
        existe :bool =False
        for i, img in enumerate(paths):
            filename = os.path.join('./images', f"{self.object}_{self.surveys[i]}.fit")
            if os.path.exists(filename):
                existe=True
            else:
                existe=False
    
    def supprimer_fits(self, paths):
        #fonction qui supprime les fichiers fits
        for i, img in enumerate(paths):
            try:
                filename = os.path.join('./images', f"{self.object}_{self.surveys[i]}.fit")
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"Image supprimée : {filename}")
                else:
                    print(f"Erreur : fichier non trouvé : {filename}")      
            except Exception as e:
                print(f"Erreur lors de la suppression de {filename} : {e}")
            
    def supprimer_cache(self):
        SkyView.clear_cache()

    
            
    def afficher_fits(self,data):
        # fonction qui affiche les fits à l'aide de matplotlib
        plt.imshow(data, norm=LogNorm(), origin='lower', cmap='magma')
        plt.colorbar()
        plt.show()
        
    
    def supprimer_cache(self):
        SkyView.clear_cache()
        
if __name__ == '__main__':
    
    mFits : NouveauxFits = NouveauxFits('M104')
    # mFits = NouveauxFits()
    
    paths : list = SkyView.get_images(position=mFits.object, survey=mFits.surveys, pixels=100)
    
    if paths == None:
        print("erreur : objet non trouvé")
    
    if mFits.fits_existe(paths):
        mFits.supprimer_fits()
    else:
        data = mFits.telecharger_fits(paths)
        mFits.afficher_fits(data)
        mFits.chemin_fits(paths,'DSS2 IR')
        mFits.supprimer_fits(paths)
        
   
    mFits.supprimer_cache()
    