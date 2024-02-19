# Gestion des données des communes

L'idée du projet est de charger les données des communes dans une base de donné et de les interoger à travers fastapi, tout en tenant compte des contraintes imposées.
 

## Docker / Docker-compose:

· Nous avons un container avec fastapi ici api-web.

```bash
    api-web:
        build: 
        context: ../../src
        image: api_commune:latest
        ports:
        - "8085:80"
        depends_on:
        - db
```

· Un container avec un gestionnaire de BDD au choix, ici postgresql.

```bash
    db:
        image: postgres
        restart: always
        shm_size: 128mb
        ports:
        - 5433:5432
        environment:
        - POSTGRES_PASSWORD=postgres
        - POSTGRES_USER=postgres
        - POSTGRES_DB=commune
        volumes:
        - ./data:/var/lib/postgresql/data

```

Importation et gestion des données :

· Envoyer des données dans la base à partir d'une url, ici nous avons cette url  [données des communes](https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25).


![Importer les données](./Images/enregistrementbd.png "Description de la capture d'écran 1")


## Méthodes du FastAPI 

· Mettre à jour une commune, son code postal et son département dans la BDD.
![Importer les données](./Images/update_commune.png "Description de la capture d'écran 1")


· Récupérer les informations d'une commune sur la base de son nom.

![Importer les données](./Images/commune_nom.png "Description de la capture d'écran 1")


· Récupérer la liste de toutes les communes d'un département.

![Importer les données](./Images/liste_commune_dept.png "Description de la capture d'écran 1")



· calculer les coordonnées GPS d'une commune. 


![Importer les données](./Images/gps_coord.png " le calcul des coordonnés gps se fait avec le nom de la commune ainsi que le lien vers le mappers dockerisé")

. mapper open-source dockerisé 

le mapper "nominatim" est un exemple de mapper dockerisé (il permet de retourner les coordonnées gps d'une commune ).

```bash
    nominatim:
        container_name: nominatim
        image: mediagis/nominatim:4.3
        ports:
            - "8086:8080"
        environment:
            # see https://github.com/mediagis/nominatim-docker/tree/master/4.3#configuration for more options
            PBF_URL: https://download.geofabrik.de/europe/france-latest.osm.pbf
            #https://download.geofabrik.de/europe/monaco-latest.osm.pbf
            EPLICATION_URL: https://download.geofabrik.de/europe/france-updates/
            #https://download.geofabrik.de/europe/monaco-updates/
            NOMINATIM_PASSWORD: very_secure_password
        volumes:
        - nominatim-data:/var/lib/postgresql/14/main
        shm_size: 1gb
```


· Utilisation du git !

## Installation

1. Cloner le dépôt :

```bash
    git clone https://github.com/noumbissie/api_commune.git
```

2. Installer les dépendances :

```bash
    pip install -r requirements.txt
```



## Utilisation

1. Lancer l'application dockerisée :

```bash
    docker compose build
    docker compose up

```
Vous devrez normalement avoir cette image d'acceuil !
![Importer les données](./Images/capture_acceuil.png " le calcul des coordonnés gps se fait avec le nom de la commune ainsi que le lien vers le mappers dockerisé")

Vous aurez egalement cette image dans la partie documentation de l'api

![Importer les données](./Images/page_doc.png " le calcul des coordonnés gps se fait avec le nom de la commune ainsi que le lien vers le mappers dockerisé")

## Licence

Ce projet est sous licence [Apache](http://www.apache.org/licenses/).
