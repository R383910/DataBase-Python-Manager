import sqlite3
import json
import os
from datetime import datetime
from frontend import obtenir_table, afficher_menu_parametres
from utils import nettoyer_console

# Fichiers de configuration et de log
LOGS_DIR = 'logs'
CONFIG_FILE = os.path.join(LOGS_DIR, 'config.json')
COMMAND_LOG_FILE = os.path.join(LOGS_DIR, 'command_log.txt')
DEFAULT_LOG_FILE = os.path.join(LOGS_DIR, 'log.txt')

# Créer le sous-dossier 'logs' s'il n'existe pas
os.makedirs(LOGS_DIR, exist_ok=True)

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

# Fonction pour lire les chaînes de caractères localisées
def lire_lang(lang):
    lang_file = os.path.join(LOGS_DIR, f'{lang}.json')
    if os.path.exists(lang_file):
        with open(lang_file, 'r') as f:
            lang_dict = json.load(f)
            lang_dict['lang'] = lang  # Définir la clé lang
            return lang_dict
    return {}

# Fonction pour recharger la langue
def recharger_langue():
    """
    Recharge la langue actuelle depuis le fichier de configuration.
    """
    config = lire_config()
    lang_code = config.get('lang', 'fr')  # Langue par défaut : français
    return lire_lang(lang_code)

# Fonction pour obtenir les colonnes d'une table spécifique
def obtenir_colonnes(conn, table):
    """
    Obtient les colonnes d'une table spécifique.
    """
    with conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table})")
        return [col[1] for col in cursor.fetchall()]

# Fonction pour obtenir et afficher les informations d'une table spécifique
def obtenir_informations(conn, table, choix, enregistrer=False, lang=None):
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
            print(lang["aucune_information"])

# Fonction pour obtenir et afficher toutes les informations d'une table spécifique
def obtenir_toute_table(conn, table, enregistrer=False, lang=None):
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
            print(lang["aucune_information"])

# Fonction pour enregistrer les commandes exécutées dans un fichier de log
def log_command(action, command, success, lang=None):
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
def recuperer_informations(conn, lang):
    """
    Permet à l'utilisateur de récupérer des informations d'une table spécifique.
    """
    table = obtenir_table(conn, lang)
    if table:
        choix = input(lang["entrer_id_nom"])
        config = lire_config()
        enregistrer = config.get('enregistrer_recuperation', False)
        if choix.isdigit():
            command = f"SELECT * FROM {table} WHERE Id = {choix}"
        else:
            command = f"SELECT * FROM {table} WHERE Nom = '{choix}'"
        log_command("get", command, True, lang)
        obtenir_informations(conn, table, choix, enregistrer, lang)
        input(lang["appuyer_entree"])  # Ajouter une pause ici
        nettoyer_console()

# Fonction pour ajouter des informations dans une table spécifique
def ajouter_informations(conn, lang):
    """
    Permet à l'utilisateur d'ajouter des informations dans une table spécifique.
    """
    table = obtenir_table(conn, lang)
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
            log_command("add", command, True, lang)
            conn.commit()
            print(lang["information_ajoutee"])
        except sqlite3.Error as e:
            log_command("add", command, False, lang)
            print(lang["erreur_ajout"] + str(e))
        nettoyer_console()

# Fonction pour supprimer des informations d'une table spécifique
def supprimer_informations(conn, lang):
    """
    Permet à l'utilisateur de supprimer des informations d'une table spécifique.
    """
    table = obtenir_table(conn, lang)
    if table:
        choix = input(lang["entrer_id_nom_supprimer"])
        cursor = conn.cursor()
        if choix.isdigit():
            command = f"DELETE FROM {table} WHERE Id = {choix}"
        else:
            command = f"DELETE FROM {table} WHERE Nom = '{choix}'"

        try:
            cursor.execute(command)
            if cursor.rowcount > 0:
                log_command("delete", command, True, lang)
                conn.commit()
                print(lang["information_supprimee"])
            else:
                log_command("delete", command, False, lang)
                print(lang["aucune_information_supprimee"])
        except sqlite3.Error as e:
            log_command("delete", command, False, lang)
            print(lang["erreur_suppression"] + str(e))
        nettoyer_console()

# Fonction pour créer une nouvelle table
def creer_table(conn, lang):
    """
    Permet à l'utilisateur de créer une nouvelle table.
    """
    nom_table = input(lang["entrer_nom_table"])
    if not nom_table.isidentifier():
        print(lang["nom_table_invalide"])
        return

    nb_colonnes = int(input(lang["entrer_nb_colonnes"]))
    colonnes = []
    for i in range(nb_colonnes):
        nom_colonne = input(lang["entrer_nom_colonne"] + f" {i+1}: ")
        type_colonne = input(lang["entrer_type_colonne"] + f" {i+1}: ")
        colonnes.append(f"{nom_colonne} {type_colonne}")

    command = f"CREATE TABLE {nom_table} ({', '.join(colonnes)})"
    cursor = conn.cursor()

    try:
        cursor.execute(command)
        log_command("create", command, True, lang)
        conn.commit()
        print(lang["table_creee"])
    except sqlite3.Error as e:
        log_command("create", command, False, lang)
        print(lang["erreur_creation_table"] + str(e))
    nettoyer_console()

# Fonction pour supprimer une table
def supprimer_table(conn, lang):
    """
    Permet à l'utilisateur de supprimer une table existante.
    """
    table = obtenir_table(conn, lang)
    if table:
        command = f"DROP TABLE {table}"
        cursor = conn.cursor()

        try:
            cursor.execute(command)
            log_command("drop", command, True, lang)
            conn.commit()
            print(lang["table_supprimee"])
        except sqlite3.Error as e:
            log_command("drop", command, False, lang)
            print(lang["erreur_suppression_table"] + str(e))
        nettoyer_console()

# Fonction pour récupérer toutes les informations d'une table spécifique
def recuperer_toute_table(conn, lang):
    """
    Permet à l'utilisateur de récupérer toutes les informations d'une table spécifique.
    """
    table = obtenir_table(conn, lang)
    if table:
        config = lire_config()
        enregistrer = config.get('enregistrer_recuperation', False)
        command = f"SELECT * FROM {table}"
        log_command("get_all", command, True, lang)
        obtenir_toute_table(conn, table, enregistrer, lang)
        input(lang["appuyer_entree"])  # Ajouter une pause ici
        nettoyer_console()

# Fonction pour créer une nouvelle base de données
def creer_base_de_donnees(lang):
    """
    Permet à l'utilisateur de créer une nouvelle base de données.
    """
    db_path = input(lang["entrer_chemin_db"])
    config = lire_config()
    config['db_path'] = db_path
    ecrire_config(config)
    print(lang["base_creee"])
    nettoyer_console()

# Fonction pour supprimer une base de données
def supprimer_base_de_donnees(lang):
    """
    Permet à l'utilisateur de supprimer une base de données existante.
    """
    db_path = input(lang["entrer_chemin_db_supprimer"])
    if os.path.exists(db_path):
        os.remove(db_path)
        print(lang["base_supprimee"])
    else:
        print(lang["base_non_existe"])
    nettoyer_console()

# Fonction pour ouvrir le dossier des logs
def ouvrir_logs(lang):
    """
    Ouvre le dossier des logs dans l'explorateur de fichiers.
    """
    if os.name == 'nt':  # Pour Windows
        os.startfile(LOGS_DIR)
    elif os.name == 'posix':  # Pour Linux et macOS
        if os.uname().sysname == 'Darwin':  # macOS
            os.system(f'open {LOGS_DIR}')
        else:  # Linux
            os.system(f'xdg-open {LOGS_DIR}')
    else:
        print(lang["systeme_non_supporte"])
    nettoyer_console()

# Fonction pour configurer les paramètres de l'application
def configurer_parametres(conn, lang):
    """
    Permet à l'utilisateur de configurer les paramètres de l'application, tels que l'enregistrement des résultats des commandes de récupération et les fichiers de log.
    """
    config = lire_config()
    while True:
        afficher_menu_parametres(lang)
        choix = input(lang["choisir_option"])
        match choix:
            case '1':
                enregistrer = input(lang["enregistrer_recuperation"] + " ? (oui/non): ").lower() == 'oui'
                config['enregistrer_recuperation'] = enregistrer
                if enregistrer:
                    log_file = input(lang["entrer_chemin_log"].format(DEFAULT_LOG_FILE)) or DEFAULT_LOG_FILE
                    config['log_file'] = log_file
            case '2':
                log_file = input(lang["entrer_chemin_log"].format(DEFAULT_LOG_FILE)) or DEFAULT_LOG_FILE
                config['log_file'] = log_file
            case '3':
                command_log_file = input(lang["entrer_chemin_log_commandes"].format(COMMAND_LOG_FILE)) or COMMAND_LOG_FILE
                config['command_log_file'] = command_log_file
            case '4':
                db_path = demander_chemin_db(lang)
                config['db_path'] = db_path
            case '5':
                lang = changer_langue(lang)  # Mettre à jour la langue
            case '6':
                ouvrir_logs(lang)
            case '7':
                break
            case _:
                print(lang["option_invalide"])

    ecrire_config(config)
    config = lire_config()
    print(lang["parametres_configures"])
    nettoyer_console()
    return lang  # Retourner la langue mise à jour

# Fonction pour changer la langue
def changer_langue(lang):
    config = lire_config()
    nouvelle_langue = input("Choisissez la langue (fr/en): ").lower()
    if nouvelle_langue in ["fr", "en"]:
        config["lang"] = nouvelle_langue  # Mettre à jour la valeur de la langue dans le fichier config.json
        ecrire_config(config)  # Enregistrer la configuration
        print(f"Langue changée en {nouvelle_langue}.")
        return lire_lang(nouvelle_langue)  # Retourner la nouvelle langue
    else:
        print("Langue non reconnue.")
        return lang  # Retourner la langue actuelle si la nouvelle langue n'est pas valide

# Fonction pour demander le chemin de la base de données lors du premier lancement
def demander_chemin_db(lang):
    """
    Demande le chemin de la base de données lors du premier lancement du script.
    """
    config = lire_config()
    anciens_chemins = config.get('anciens_chemins', [])
    chemins_valides = [chemin for chemin in anciens_chemins if os.path.exists(chemin)]

    if chemins_valides:
        print(lang["anciens_chemins_db"])
        for i, chemin in enumerate(chemins_valides, start=1):
            print(f"{i}. {chemin}")
        print(f"{len(chemins_valides) + 1}. " + lang["nouveau_chemin"])

        choix = input(lang["choisir_chemin_ou_nouveau"])
        if choix.isdigit() and 1 <= int(choix) <= len(chemins_valides):
            db_path = chemins_valides[int(choix) - 1]
        else:
            db_path = input(lang["entrer_nouveau_chemin_db"])
    else:
        db_path = input(lang["entrer_chemin_db"])

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
