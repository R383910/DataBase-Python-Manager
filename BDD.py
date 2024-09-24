import sqlite3
import json
import os
from datetime import datetime

# Fichiers de configuration et de log
LOGS_DIR = 'logs'
CONFIG_FILE = os.path.join(LOGS_DIR, 'config.json')
COMMAND_LOG_FILE = os.path.join(LOGS_DIR, 'command_log.txt')
DEFAULT_LOG_FILE = os.path.join(LOGS_DIR, 'log.txt')

# Créer le sous-dossier 'logs' s'il n'existe pas
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Fonction pour lire la configuration depuis un fichier JSON
def lire_config():
    """
    Lit la configuration depuis un fichier JSON.
    Si le fichier n'existe pas, retourne un dictionnaire vide.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

# Fonction pour écrire la configuration dans un fichier JSON
def ecrire_config(config):
    """
    Écrit la configuration dans un fichier JSON avec une mise en forme pour une meilleure lisibilité.
    """
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# Fonction pour obtenir la liste des tables dans la base de données
def obtenir_tables(conn):
    """
    Obtient la liste des tables dans la base de données.
    """
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in cursor.fetchall()]

# Fonction pour obtenir les colonnes d'une table spécifique
def obtenir_colonnes(conn, table):
    """
    Obtient les colonnes d'une table spécifique.
    """
    with conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table})")
        return [col[1] for col in cursor.fetchall()]

# Fonction pour afficher le menu principal
def afficher_menu():
    """
    Affiche le menu principal de l'application.
    """
    nettoyer_console()
    print("1. Gérer les informations")
    print("2. Gérer les tables")
    print("3. Gérer les bases de données")
    print("4. Configurer les paramètres")
    print("5. Quitter")

# Fonction pour afficher le sous-menu de gestion des informations
def afficher_sous_menu_gestion():
    """
    Affiche le sous-menu de gestion des informations.
    """
    nettoyer_console()
    print("1. Récupérer des informations")
    print("2. Ajouter des informations")
    print("3. Supprimer des informations")
    print("4. Retour")

# Fonction pour afficher le sous-menu de gestion des tables
def afficher_sous_menu_tables():
    """
    Affiche le sous-menu de gestion des tables.
    """
    nettoyer_console()
    print("1. Créer une nouvelle table")
    print("2. Supprimer une table")
    print("3. Récupérer toute la table")
    print("4. Retour")

# Fonction pour afficher le sous-menu de gestion des bases de données
def afficher_sous_menu_bases():
    """
    Affiche le sous-menu de gestion des bases de données.
    """
    nettoyer_console()
    print("1. Créer une nouvelle base de données")
    print("2. Supprimer une base de données")
    print("3. Retour")

# Fonction pour afficher le menu des tables disponibles
def afficher_menu_tables(conn):
    """
    Affiche le menu des tables disponibles dans la base de données.
    """
    tables = obtenir_tables(conn)
    for i, table in enumerate(tables, start=1):
        print(f"{i}. {table}")

# Fonction pour obtenir le nom de la table choisie par l'utilisateur
def obtenir_table(conn):
    """
    Permet à l'utilisateur de choisir une table parmi celles disponibles dans la base de données.
    """
    afficher_menu_tables(conn)
    choix_table = input("Choisissez le numéro de la table: ")

    tables = obtenir_tables(conn)
    if choix_table.isdigit() and 1 <= int(choix_table) <= len(tables):
        return tables[int(choix_table) - 1]
    else:
        print("Table non reconnue.")
        return None

# Fonction pour obtenir et afficher les informations d'une table spécifique
def obtenir_informations(conn, table, choix, enregistrer=False):
    """
    Récupère et affiche les informations d'une table spécifique en fonction de l'ID ou du nom fourni par l'utilisateur.
    """
    with conn:
        cursor = conn.cursor()
        if choix.isdigit():
            cursor.execute(f"SELECT * FROM {table} WHERE Id = ?", (choix,))
        else:
            cursor.execute(f"SELECT * FROM {table} WHERE Nom = ?", (choix,))

        result = cursor.fetchone()
        if result:
            columns = obtenir_colonnes(conn, table)
            print("\nInformations récupérées :")
            for col, val in zip(columns, result):
                print(f"{col}: {val}")
            print()

            if enregistrer:
                config = lire_config()
                log_file = config.get('log_file', DEFAULT_LOG_FILE)
                with open(log_file, 'a') as f:
                    f.write(f"Table: {table}\n")
                    for col, val in zip(columns, result):
                        f.write(f"{col}: {val}\n")
                    f.write("============================================\n")
        else:
            print("Aucune information trouvée.")

# Fonction pour obtenir et afficher toutes les informations d'une table spécifique
def obtenir_toute_table(conn, table, enregistrer=False):
    """
    Récupère et affiche toutes les informations d'une table spécifique.
    """
    with conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        results = cursor.fetchall()

        if results:
            columns = obtenir_colonnes(conn, table)
            print("\nInformations récupérées :")
            for result in results:
                for col, val in zip(columns, result):
                    print(f"{col}: {val}")
                print()

            if enregistrer:
                config = lire_config()
                log_file = config.get('log_file', DEFAULT_LOG_FILE)
                with open(log_file, 'a') as f:
                    f.write(f"Table: {table}\n")
                    for result in results:
                        for col, val in zip(columns, result):
                            f.write(f"{col}: {val}\n")
                        f.write("============================================\n")
        else:
            print("Aucune information trouvée.")

# Fonction pour enregistrer les commandes exécutées dans un fichier de log
def log_command(action, command, success):
    """
    Enregistre les commandes exécutées dans un fichier de log avec la date et l'heure, l'action, la commande et le résultat (réussite ou erreur).
    """
    config = lire_config()
    log_file = config.get('command_log_file', COMMAND_LOG_FILE)
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{action}\n")
        f.write(f"{command}\n")
        f.write(f"{'réussite' if success else 'erreur'}\n")
        f.write("============================================\n")

# Fonction pour récupérer des informations d'une table spécifique
def recuperer_informations(conn):
    """
    Permet à l'utilisateur de récupérer des informations d'une table spécifique.
    """
    table = obtenir_table(conn)
    if table:
        choix = input("Entrez l'ID ou le Nom pour récupérer les informations: ")
        config = lire_config()
        enregistrer = config.get('enregistrer_recuperation', False)
        if choix.isdigit():
            command = f"SELECT * FROM {table} WHERE Id = {choix}"
        else:
            command = f"SELECT * FROM {table} WHERE Nom = '{choix}'"
        log_command("get", command, True)
        obtenir_informations(conn, table, choix, enregistrer)
        input("Appuyez sur Entrée pour continuer...")  # Ajouter une pause ici
        nettoyer_console()

# Fonction pour ajouter des informations dans une table spécifique
def ajouter_informations(conn):
    """
    Permet à l'utilisateur d'ajouter des informations dans une table spécifique.
    """
    table = obtenir_table(conn)
    if table:
        columns = obtenir_colonnes(conn, table)
        values = []
        for col in columns:
            val = input(f"{col}: ")
            values.append(val)

        placeholders = ", ".join(["?"] * len(columns))
        command = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor = conn.cursor()

        try:
            cursor.execute(command, values)
            log_command("add", command, True)
            conn.commit()
            print("Information ajoutée avec succès.")
        except sqlite3.Error as e:
            log_command("add", command, False)
            print(f"Erreur lors de l'ajout des informations : {e}")
        nettoyer_console()

# Fonction pour supprimer des informations d'une table spécifique
def supprimer_informations(conn):
    """
    Permet à l'utilisateur de supprimer des informations d'une table spécifique.
    """
    table = obtenir_table(conn)
    if table:
        choix = input("Entrez l'ID ou le Nom pour supprimer les informations: ")
        cursor = conn.cursor()
        if choix.isdigit():
            command = f"DELETE FROM {table} WHERE Id = {choix}"
        else:
            command = f"DELETE FROM {table} WHERE Nom = '{choix}'"

        try:
            cursor.execute(command)
            if cursor.rowcount > 0:
                log_command("delete", command, True)
                conn.commit()
                print("Information supprimée avec succès.")
            else:
                log_command("delete", command, False)
                print("Aucune information trouvée.")
        except sqlite3.Error as e:
            log_command("delete", command, False)
            print(f"Erreur lors de la suppression des informations : {e}")
        nettoyer_console()

# Fonction pour créer une nouvelle table
def creer_table(conn):
    """
    Permet à l'utilisateur de créer une nouvelle table.
    """
    nom_table = input("Entrez le nom de la nouvelle table: ")
    if not nom_table.isidentifier():
        print("Le nom de la table doit être un identifiant valide.")
        return

    nb_colonnes = int(input("Entrez le nombre de colonnes: "))
    colonnes = []
    for i in range(nb_colonnes):
        nom_colonne = input(f"Entrez le nom de la colonne {i+1}: ")
        type_colonne = input(f"Entrez le type de la colonne {i+1}: ")
        colonnes.append(f"{nom_colonne} {type_colonne}")

    command = f"CREATE TABLE {nom_table} ({', '.join(colonnes)})"
    cursor = conn.cursor()

    try:
        cursor.execute(command)
        log_command("create", command, True)
        conn.commit()
        print("Table créée avec succès.")
    except sqlite3.Error as e:
        log_command("create", command, False)
        print(f"Erreur lors de la création de la table : {e}")
    nettoyer_console()

# Fonction pour supprimer une table
def supprimer_table(conn):
    """
    Permet à l'utilisateur de supprimer une table existante.
    """
    table = obtenir_table(conn)
    if table:
        command = f"DROP TABLE {table}"
        cursor = conn.cursor()

        try:
            cursor.execute(command)
            log_command("drop", command, True)
            conn.commit()
            print("Table supprimée avec succès.")
        except sqlite3.Error as e:
            log_command("drop", command, False)
            print(f"Erreur lors de la suppression de la table : {e}")
        nettoyer_console()

# Fonction pour récupérer toutes les informations d'une table spécifique
def recuperer_toute_table(conn):
    """
    Permet à l'utilisateur de récupérer toutes les informations d'une table spécifique.
    """
    table = obtenir_table(conn)
    if table:
        config = lire_config()
        enregistrer = config.get('enregistrer_recuperation', False)
        command = f"SELECT * FROM {table}"
        log_command("get_all", command, True)
        obtenir_toute_table(conn, table, enregistrer)
        input("Appuyez sur Entrée pour continuer...")  # Ajouter une pause ici
        nettoyer_console()

# Fonction pour créer une nouvelle base de données
def creer_base_de_donnees():
    """
    Permet à l'utilisateur de créer une nouvelle base de données.
    """
    db_path = input("Entrez le chemin de la nouvelle base de données: ")
    config = lire_config()
    config['db_path'] = db_path
    ecrire_config(config)
    print("Base de données créée avec succès.")
    nettoyer_console()

# Fonction pour supprimer une base de données
def supprimer_base_de_donnees():
    """
    Permet à l'utilisateur de supprimer une base de données existante.
    """
    db_path = input("Entrez le chemin de la base de données à supprimer: ")
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Base de données supprimée avec succès.")
    else:
        print("La base de données n'existe pas.")
    nettoyer_console()

# Fonction pour ouvrir le dossier des logs
def ouvrir_logs():
    """
    Ouvre le dossier des logs dans l'explorateur de fichiers.
    """
    if os.name == 'nt':  # Pour Windows
        os.startfile(LOGS_DIR)
    else:
        print("Système d'exploitation non pris en charge.")
    nettoyer_console()

# Fonction pour afficher le menu des paramètres
def afficher_menu_parametres():
    """
    Affiche le menu des paramètres disponibles.
    """
    nettoyer_console()
    print("1. Enregistrer les résultats des commandes de récupération")
    print("2. Chemin du fichier de journalisation")
    print("3. Chemin du fichier de journalisation des commandes")
    print("4. Chemin de la base de données")
    print("5. Ouvrir le dossier des logs")
    print("6. Retour")

# Fonction pour configurer les paramètres de l'application
def configurer_parametres(conn):
    """
    Permet à l'utilisateur de configurer les paramètres de l'application, tels que l'enregistrement des résultats des commandes de récupération et les fichiers de log.
    """
    config = lire_config()

    while True:
        afficher_menu_parametres()
        choix = input("Choisissez le paramètre à modifier: ")
        match choix:
            case '1':
                enregistrer = input("Voulez-vous enregistrer les résultats des commandes de récupération ? (oui/non): ").lower() == 'oui'
                config['enregistrer_recuperation'] = enregistrer
                if enregistrer:
                    log_file = input(f"Entrez le chemin du fichier de journalisation (par défaut '{DEFAULT_LOG_FILE}'): ") or DEFAULT_LOG_FILE
                    config['log_file'] = log_file
            case '2':
                log_file = input(f"Entrez le chemin du fichier de journalisation (par défaut '{DEFAULT_LOG_FILE}'): ") or DEFAULT_LOG_FILE
                config['log_file'] = log_file
            case '3':
                command_log_file = input(f"Entrez le chemin du fichier de journalisation des commandes (par défaut '{COMMAND_LOG_FILE}'): ") or COMMAND_LOG_FILE
                config['command_log_file'] = command_log_file
            case '4':
                db_path = demander_chemin_db()
                config['db_path'] = db_path
            case '5':
                ouvrir_logs()
            case '6':
                break
            case _:
                print("Option invalide.")

    ecrire_config(config)
    print("Paramètres configurés avec succès.")
    nettoyer_console()

# Fonction pour demander le chemin de la base de données lors du premier lancement
def demander_chemin_db():
    """
    Demande le chemin de la base de données lors du premier lancement du script.
    """
    config = lire_config()
    anciens_chemins = config.get('anciens_chemins', [])
    chemins_valides = [chemin for chemin in anciens_chemins if os.path.exists(chemin)]

    if chemins_valides:
        print("Anciens chemins de bases de données disponibles:")
        for i, chemin in enumerate(chemins_valides, start=1):
            print(f"{i}. {chemin}")
        print(f"{len(chemins_valides) + 1}. Nouveau chemin")

        choix = input("Choisissez un chemin ou entrez un nouveau chemin: ")
        if choix.isdigit() and 1 <= int(choix) <= len(chemins_valides):
            db_path = chemins_valides[int(choix) - 1]
        else:
            db_path = input("Entrez le nouveau chemin de la base de données: ")
    else:
        db_path = input("Entrez le chemin de la base de données: ")

    # Vérifier si le chemin est déjà enregistré
    if db_path not in chemins_valides:
        config['anciens_chemins'] = chemins_valides + [db_path]

    config['db_path'] = db_path
    ecrire_config(config)
    return db_path

# Fonction pour détecter automatiquement les bases de données dans le même dossier ou sous-dossier du script
def detecter_bases_de_donnees():
    """
    Détecte automatiquement les bases de données dans le même dossier ou sous-dossier du script.
    """
    bases_de_donnees = []
    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith('.db'):
                bases_de_donnees.append(os.path.join(root, file))
    return bases_de_donnees

# Fonction pour nettoyer la console
def nettoyer_console():
    """
    Nettoie la console.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# Fonction principale pour exécuter le menu de l'application
def main():
    """
    Fonction principale qui exécute le menu de l'application et gère les choix de l'utilisateur.
    """
    config = lire_config()
    db_path = config.get('db_path')

    # Demander le chemin de la base de données lors du premier lancement
    if not db_path:
        db_path = demander_chemin_db()

    # Connexion à la base de données
    with sqlite3.connect(db_path) as conn:
        while True:
            afficher_menu()
            choix = input("Choisissez une option: ")
            match choix:
                case '1':
                    while True:
                        afficher_sous_menu_gestion()
                        sous_choix = input("Choisissez une option: ")
                        match sous_choix:
                            case '1':
                                recuperer_informations(conn)
                            case '2':
                                ajouter_informations(conn)
                            case '3':
                                supprimer_informations(conn)
                            case '4':
                                break
                            case _:
                                print("Option invalide.")
                                nettoyer_console()
                case '2':
                    while True:
                        afficher_sous_menu_tables()
                        sous_choix = input("Choisissez une option: ")
                        match sous_choix:
                            case '1':
                                creer_table(conn)
                            case '2':
                                supprimer_table(conn)
                            case '3':
                                recuperer_toute_table(conn)
                            case '4':
                                break
                            case _:
                                print("Option invalide.")
                                nettoyer_console()
                case '3':
                    while True:
                        afficher_sous_menu_bases()
                        sous_choix = input("Choisissez une option: ")
                        match sous_choix:
                            case '1':
                                creer_base_de_donnees()
                            case '2':
                                supprimer_base_de_donnees()
                            case '3':
                                break
                            case _:
                                print("Option invalide.")
                                nettoyer_console()
                case '4':
                    configurer_parametres(conn)
                case '5':
                    break
                case _:
                    print("Option invalide.")
                    nettoyer_console()

# Point d'entrée du script
if __name__ == "__main__":
    main()
