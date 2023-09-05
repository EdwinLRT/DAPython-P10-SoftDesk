# SoftDesk

![Texte alternatif de l'image](https://user.oc-static.com/upload/2023/06/28/16879473703315_P10-02.png)

#### Projet 10 du parcours Développeur d'Applications Python d'OpenClassrooms : API-SoftDesk

API-SoftDesk est une API RESTful conçue pour gérer le suivi et la résolution de problèmes techniques traités de la société SoftDesk via ces différentes plateformes d'assistance. 

Grâce à cette application, les utilisateurs peuvent créer différents projets, ajouter des contributeurs à des projets spécifiques, soumettre des problèmes (issues) au sein des projets et leur attribuer des libellés en fonction de leur priorité, de leurs balises, etc.

Le projet a été testé avec succès sous OsX 10.15.7 avec Python 3.11, Django 4.2.3 et DjangoRestFramework 3.14.


# Installation

### Windows :

Dans votre terminal, naviguer vers le dossier souhaité.

###### • Récupération du projet

```
git clone https://github.com/EdwinLRT/P10-SoftDesk

```

###### • Activer l'environnement virtuel

```
cd OC_SOFTDESK
python -m venv env 
env\Scripts\activate

```

###### • Installer les paquets requis

```
pip install -r requirements.txt

```

### MacOS et Linux :

Dans le terminal, naviguer vers le dossier souhaité.

###### • Récupération du projet

```
git clone https://github.com/EdwinLRT/P10-SoftDesk

```

###### • Activer l'environnement virtuel

```
cd OC_SOFTDESK
python3 -m venv env 
source env/bin/activate

```

###### • Installer les paquets requis

```
pip install -r requirements.txt
```

## Utilisation de l'API

#### Faire les migrations :

```
python manage.py migrate

```

#### Lancer le serveur Django :

```
python manage.py runserver

```

Il est possible de naviguer dans l'API avec différents outils :

-   la plateforme  [Postman](https://www.postman.com/)  ;
-   l'outil de commandes  [cURL](https://curl.se/)  ;
-   l'interface intégrée Django REST framework à l'adresse  [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  (adresse par défaut, retrouvez les end-points ci-dessous).

# Documentation & Endpoints

Afin de faciliter l'accès à l'API et la mise à jour des différents éléments de la documentation le choix a été fait d'utiliser la librairie drf-yasg Swagger accessible via ce lien une fois l'API lancée.  http://127.0.0.1:8000/swagger/

Vous pouvez retrouver une capture d'écran de l'état des endpoints au 05/09/2023 ci-dessous.   



## Informations complémentaires 

Utilisateurs : 

Liste des endpoints : 

Divers : 
