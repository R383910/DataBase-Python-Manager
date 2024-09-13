# Base de Données de Matériel Informatique

Cette base de données est conçue pour stocker des informations sur divers composants informatiques tels que les GPU, CPU, NPU, et autres composants comme la RAM et les SSD.

## Tables

### GPUs

| Colonne          | Type       | Description                           |
|------------------|------------|---------------------------------------|
| Id               | INTEGER    | Clé primaire                         |
| Nom              | TEXT       | Nom du GPU                            |
| Marque           | TEXT       | Marque du GPU                         |
| Modele           | TEXT       | Modèle du GPU                         |
| Frequence        | INTEGER    | Fréquence de base (en MHz)            |
| VRAM             | INTEGER    | Mémoire vidéo (en Go)                |
| TypeDeMemoire    | TEXT       | Type de mémoire (GDDR6, HBM2, etc.)  |
| Consommation     | INTEGER    | Consommation électrique (en watts)   |
| DateDeSortie     | DATE       | Date de sortie                        |
| Prix             | REAL       | Prix (en €)                           |

### CPUs

| Colonne          | Type       | Description                           |
|------------------|------------|---------------------------------------|
| Id               | INTEGER    | Clé primaire                         |
| Nom              | TEXT       | Nom du CPU                            |
| Marque           | TEXT       | Marque du CPU                         |
| Modele           | TEXT       | Modèle du CPU                         |
| Frequence        | INTEGER    | Fréquence de base (en MHz)            |
| NbCoeur          | INTEGER    | Nombre de cœurs                       |
| NbThreads        | INTEGER    | Nombre de threads                     |
| DateDeSortie     | DATE       | Date de sortie                        |
| Prix             | REAL       | Prix (en €)                           |

### NPUs

| Colonne          | Type       | Description                           |
|------------------|------------|---------------------------------------|
| Id               | INTEGER    | Clé primaire                         |
| Nom              | TEXT       | Nom du NPU                            |
| Marque           | TEXT       | Marque du NPU                         |
| Modele           | TEXT       | Modèle du NPU                         |
| Frequence        | INTEGER    | Fréquence de base (en MHz)            |
| NbCoeur          | INTEGER    | Nombre de cœurs                       |
| Memoire          | INTEGER    | Mémoire (en Go)                       |
| TypeMemoire      | TEXT       | Type de mémoire                       |
| DateDeSortie     | DATE       | Date de sortie                        |
| Prix             | REAL       | Prix (en €)                           |

### AutresComposants (RAM, SSD, etc.)

| Colonne          | Type       | Description                           |
|------------------|------------|---------------------------------------|
| Id               | INTEGER    | Clé primaire                         |
| Nom              | TEXT       | Nom du composant                      |
| Marque           | TEXT       | Marque du composant                   |
| Modele           | TEXT       | Modèle du composant                   |
| Type             | TEXT       | Type de composant (RAM, SSD, etc.)    |
| FrequenceVitesse | INTEGER    | Fréquence/Vitesse (en MHz/Mo/s)      |
| Interface        | TEXT       | Interface (DDR4, PCIe, etc.)          |
| DateDeSortie     | DATE       | Date de sortie                        |
| Prix             | REAL       | Prix (en €)                           |

### Fabricants

| Colonne          | Type       | Description                           |
|------------------|------------|---------------------------------------|
| Id               | INTEGER    | Clé primaire                         |
| Nom              | TEXT       | Nom du fabricant                      |
| SiteWeb          | TEXT       | Site web du fabricant                 |

### TypesMemoire

| Colonne          | Type       | Description                           |
|------------------|------------|---------------------------------------|
| Id               | INTEGER    | Clé primaire                         |
| Nom              | TEXT       | Nom du type de mémoire               |
| Description      | TEXT       | Description du type de mémoire        |

### Interfaces

| Colonne          | Type       | Description                           |
|------------------|------------|---------------------------------------|
| Id               | INTEGER    | Clé primaire                         |
| Nom              | TEXT       | Nom de l'interface                   |
| Description      | TEXT       | Description de l'interface            |

### TypesComposants

| Colonne          | Type       | Description                           |
|------------------|------------|---------------------------------------|
| Id               | INTEGER    | Clé primaire                         |
| Nom              | TEXT       | Nom du type de composant              |
| Description      | TEXT       | Description du type de composant      |
