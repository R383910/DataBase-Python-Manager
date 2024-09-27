# Nom du Projet

Ce projet est une application de gestion de bases de données SQLite avec des fonctionnalités de gestion des informations, des tables et des bases de données. Il inclut également des options de configuration et de localisation.

## Table des matières

- [Installation](#installation)
- [Fonctionnalités](#fonctionnalités)
- [Utilisation](#utilisation)
- [Configuration](#configuration)
- [Localisation](#localisation)
- [Licence](#licence)

## Installation

Pour utiliser ce projet, vous devez avoir Python installé sur votre machine. Vous pouvez cloner ce dépôt et exécuter le script principal.

```bash
git clone https://github.com/R383910/DataBase-Python-Manager
cd votre-projet
python main.py
```
# Fonctionnalités

- **Gestion des informations** : Récupérer, ajouter et supprimer des informations dans les tables.
- **Gestion des tables** : Créer, supprimer et récupérer toutes les informations d'une table.
- **Gestion des bases de données** : Créer et supprimer des bases de données.
- **Configuration** : Configurer les paramètres de l'application, tels que l'enregistrement des résultats des commandes de récupération et les fichiers de log.
- **Localisation** : Changer la langue de l'interface utilisateur.

# Utilisation

Le script principal `main.py` affiche un menu interactif permettant de naviguer entre les différentes fonctionnalités de l'application. Voici un aperçu des menus disponibles :

## Menu principal

- Gérer les informations
- Gérer les tables
- Gérer les bases de données
- Configurer les paramètres
- Quitter

## Sous-menu de gestion des informations

- Récupérer des informations
- Ajouter des informations
- Supprimer des informations
- Retour

## Sous-menu de gestion des tables

- Créer une table
- Supprimer une table
- Récupérer toutes les informations d'une table
- Retour

## Sous-menu de gestion des bases de données

- Créer une base de données
- Supprimer une base de données
- Retour

## Configuration

Le fichier de configuration `config.json` est utilisé pour stocker les paramètres de l'application. Vous pouvez modifier ce fichier pour ajuster les paramètres selon vos besoins.

## Localisation

Le projet supporte la localisation en français (fr) et en anglais (en). Vous pouvez changer la langue de l'interface utilisateur via le menu de configuration.

# Licence

Ce projet est sous licence Creative Commons Attribution 4.0 International (CC BY 4.0).

Vous êtes libre de :

- **Partager** — copier et redistribuer le matériel dans n'importe quel format ou support
- **Adapter** — remixer, transformer et créer à partir du matériel pour tout usage, y compris commercial.

Sous les conditions suivantes :

- **Attribution** — Vous devez créditer Gabriel Messaoudi comme suit : "Ce projet utilise DataBase-Python-Manager créé par Gabriel Messaoudi, sous licence CC BY 4.0."

Pour plus d'informations, voir la licence complète à :
[Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)
