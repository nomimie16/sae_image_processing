# SAE - Traitement d'images Astrophoto
## LIGNIEZ Noémie - CHATELAIN Lilou
✎ Algorithme du 18 janvier 


⚠ L'affichage entre chaque objet dépend du nombre de pixel et peut durer parfois plusieurs secondes jusqu'à quelques minutes.
⚠ Soyez patient lorsque vous lancez une recherche.
⚠ SI l'objet choisit est inconnu il afffiche un objet au hasard


## Pour le lancement de l'application astrophoto :

- Executez le programme ```main.py``` via un terminal ou directement depuis VisualStudioCode grace à l'icone d'execution en forme de flêche (situé en haut à gauche)

##### Une fois l'application lancée,

1. Chosssisez votre objet celeste dans la barre de recherche (si vous n'avez pas d'idée tapez une lettre, des noms apparaîtrons)

⚠ Si aucun objet n'est choisi alors l'application choisira un objet pour vous, ne vous inquiètez pas ;)

2. Choissisez le nombre de pixels voulus (+ de pixel = meilleure résolution mais + de temps d'attente).

3. Appuyez sur le boton de lancement "Go 🚀" et attendez.

🚀 Et voilà , après quelques secondes vous devriez arriver dans l'espace et observer votre objet celeste sous forme d'image fit traitée selon 3 spectre , Rouge Bleu Et infrarouge. 🚀

### Contenu des fichiers sources :

```NouveauxFits.py ```

    - Classe qui permet de créer (télécharger) des fichiers fit(s) dans un dossier image.

    Contructeur : 
        -> Prends en parametre un objet et utilise une liste de trois collection d'images capturées en différentes longueurs d'onde
        -> si pas de parametres : objet choisit au hasard dans une liste donnée

    Methodes :
        -> gettter (objet, surveys)
        -> setter (objet)
        -> telecharger_fits() : fonction qui télécharge les fits grace a une liste récupérée par le programme sur Skyview
        -> fits_existe() : fonction qui vérifie si les fits existent
        -> supprimer_fits() : fonction qui supprime les fits
        -> afficher_fits() : fonction qui affiche les fits à l'aide de matplotlib


```Traitement.py``` :

    - Classe qui s'occupe du traitement des images FIts

    - Constructeur 
        ->  Prends en parametre un groupe de 3 fit et un telechargement d'images
        -> self.red_file : chemin du fichier fit rouge
        -> self.blue_file : chemin du fichier fit bleu
        -> self.ir_file : chemin du fihier fits infrarouge
        -> self.colors : couleurs des 3 images rassemblées

    Methodes :
        -> load_fits_data() : fonction qui recuprere les data des 3 fichiers fits rassemblés
        -> normalize_data(self) : fonction qui utilise une matrice afin du superposer les data de chaque images dans les couleurs
        -> get Colors() : renvoit les couleurs pour afficher l'image traitée

```MVC``` (modele, vue , controleur):

    - Interface qui contient l'affichage de boutons, images(matplolib), barre de recherche pour l'utilisateur
    - Utlise la classe NouveauxFits et la classe Traitement
    - La vue envoie les donnée de l'image traitée dans un json qui est ensuite remit sous forme de données(data) pour ouvrir l'image dans le controleur avec matplolib. C'est cette éxecution qui ralentit l'affichage mais c'est la seule solutions qui nous avons trouvé.



/
/

## RECHERCHE MAST :

mast_astro.py : Fichier pour telecharger des donnees des telescopes spatiaux à l’aide de la bibliotheque Mast 

Contenu : 

    - fonction telechargement() : fonction de téléchargement qui prends en paramètre un objet que l'utilisateur choisira via l'interface afin de choisir un obs_id qui concerne ce type de mission

    // 
    - fonction recherche_csv() : fonction qui lit un fichier csv ( recuperé sur MAST ) rempli d'id pour les observations du télescope Webb. La fonction parcours le csv afin de recuperer les id qui concernent uniquement l'objet que l'utilisateur a choisi comme objet 

    // Nous sommes actuellement en train de rechercher une autre façon pour permettre le téléchargement directement depuis le lancement de l'application sans passer par un fichier csv

    - affichage du l'image FITS via matplolib



LIGNIEZ Noémie - CHATELAIN Lilou



