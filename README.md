# Documentation EcoTrack

## Choix des données

Pour choisir mes jeux de données, j'ai utilisé les sites recommandés dans l'énoncé. Le premier provient de **data.gouv** et concerne la collecte des déchets selon les régions. J'ai préféré travailler au niveau des départements afin de disposer d'un plus grand volume de données pour réaliser les différents tests.

Le deuxième jeu de données provient de l’**ADEME** et porte sur les flux de CO₂ par commune. Comme nous disposions également du numéro de département, j'ai pu combiner les deux jeux de données en un seul.

Il a été difficile de trouver un jeu de données couvrant l’ensemble des communes ou de récupérer toutes les coordonnées pour effectuer des appels à une API afin d’obtenir des données climatiques. C’est pourquoi j’ai choisi de rester au niveau départemental, ce qui permet également de travailler avec un volume de données suffisant pour l’analyse.

## Lancer l'API

pour lancer l'APi vous devez être dans le dossier **app** de l'application et lancer la commande :

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 5000
```

La base de données se créera à ce moment-là avec l'injection des données de chaque dataset. Mais également la création d'un utilisateur admin.

Vous pourrez voir la liste des différentes routes à cette url:

```
http://127.0.0.1:5000/docs#/
```
