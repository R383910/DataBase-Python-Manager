from utils import obtenir_tables
from utils import nettoyer_console

# Fonction pour afficher le menu principal
def afficher_menu(lang):
    """
    Affiche le menu principal de l'application.
    """
    nettoyer_console()
    print(lang["menu_principal"])
    print("1. " + lang["gerer_informations"])
    print("2. " + lang["gerer_tables"])
    print("3. " + lang["gerer_bases"])
    print("4. " + lang["configurer_parametres"])
    print("5. " + lang["sauvegarder_restaurer"])
    print("6. " + lang["exporter_importer"])
    print("7. " + lang["recherche_avancee"])
    print("8. " + lang["gerer_utilisateurs"])
    print("9. " + lang["automatisation_taches"])
    print("10. " + lang["quitter"])

# Fonction pour afficher le sous-menu de gestion des informations
def afficher_sous_menu_gestion(lang):
    """
    Affiche le sous-menu de gestion des informations.
    """
    nettoyer_console()
    print("1. " + lang["recuperer_informations"])
    print("2. " + lang["ajouter_informations"])
    print("3. " + lang["supprimer_informations"])
    print("4. " + lang["retour"])

# Fonction pour afficher le sous-menu de gestion des tables
def afficher_sous_menu_tables(lang):
    """
    Affiche le sous-menu de gestion des tables.
    """
    nettoyer_console()
    print("1. " + lang["creer_table"])
    print("2. " + lang["supprimer_table"])
    print("3. " + lang["recuperer_toute_table"])
    print("4. " + lang["retour"])

# Fonction pour afficher le sous-menu de gestion des bases de données
def afficher_sous_menu_bases(lang):
    """
    Affiche le sous-menu de gestion des bases de données.
    """
    nettoyer_console()
    print("1. " + lang["creer_base"])
    print("2. " + lang["supprimer_base"])
    print("3. " + lang["retour"])

# Fonction pour afficher le menu des tables disponibles
def afficher_menu_tables(conn, lang):
    """
    Affiche le menu des tables disponibles dans la base de données.
    """
    tables = obtenir_tables(conn)
    for i, table in enumerate(tables, start=1):
        print(f"{i}. {table}")

# Fonction pour obtenir le nom de la table choisie par l'utilisateur
def obtenir_table(conn, lang):
    """
    Permet à l'utilisateur de choisir une table parmi celles disponibles dans la base de données.
    """
    afficher_menu_tables(conn, lang)
    choix_table = input(lang["choisir_table"])

    tables = obtenir_tables(conn)
    if choix_table.isdigit() and 1 <= int(choix_table) <= len(tables):
        return tables[int(choix_table) - 1]
    else:
        print(lang["table_non_reconnue"])
        return None

# Fonction pour afficher le menu des paramètres
def afficher_menu_parametres(lang):
    """
    Affiche le menu des paramètres disponibles.
    """
    nettoyer_console()
    print("1. " + lang["enregistrer_recuperation"])
    print("2. " + lang["chemin_log"])
    print("3. " + lang["chemin_log_commandes"])
    print("4. " + lang["chemin_db"])
    print("5. " + lang["changer_langue"])
    print("6. " + lang["ouvrir_logs"])
    print("7. " + lang["retour"])
