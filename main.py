import sqlite3
from utils import nettoyer_console
from frontend import afficher_menu, afficher_sous_menu_gestion, afficher_sous_menu_tables, afficher_sous_menu_bases
from backend import lire_config, ecrire_config, recharger_langue, demander_chemin_db, recuperer_informations, ajouter_informations, supprimer_informations, creer_table, supprimer_table, recuperer_toute_table, creer_base_de_donnees, supprimer_base_de_donnees, configurer_parametres

# Fonction principale pour exécuter le menu de l'application
def main():
    config = lire_config()
    db_path = config.get('db_path')
    lang = recharger_langue()  # Charger la langue initiale

    # Demander le chemin de la base de données lors du premier lancement
    if not db_path:
        db_path = demander_chemin_db(lang)

    # Connexion à la base de données
    with sqlite3.connect(db_path) as conn:
        while True:
            afficher_menu(lang)
            choix = input(lang["choisir_option"])
            match choix:
                case '1':
                    while True:
                        afficher_sous_menu_gestion(lang)
                        sous_choix = input(lang["choisir_option"])
                        match sous_choix:
                            case '1':
                                recuperer_informations(conn, lang)
                            case '2':
                                ajouter_informations(conn, lang)
                            case '3':
                                supprimer_informations(conn, lang)
                            case '4':
                                break
                            case _:
                                print(lang["option_invalide"])
                                nettoyer_console()
                case '2':
                    while True:
                        afficher_sous_menu_tables(lang)
                        sous_choix = input(lang["choisir_option"])
                        match sous_choix:
                            case '1':
                                creer_table(conn, lang)
                            case '2':
                                supprimer_table(conn, lang)
                            case '3':
                                recuperer_toute_table(conn, lang)
                            case '4':
                                break
                            case _:
                                print(lang["option_invalide"])
                                nettoyer_console()
                case '3':
                    while True:
                        afficher_sous_menu_bases(lang)
                        sous_choix = input(lang["choisir_option"])
                        match sous_choix:
                            case '1':
                                creer_base_de_donnees(lang)
                            case '2':
                                supprimer_base_de_donnees(lang)
                            case '3':
                                break
                            case _:
                                print(lang["option_invalide"])
                                nettoyer_console()
                case '4':
                    lang = configurer_parametres(conn, lang)  # Mettre à jour la langue après la configuration des paramètres
                case '5':
                    config['lang'] = lang['lang']  # Enregistrer la langue choisie dans le fichier de configuration
                    ecrire_config(config)  # Enregistrer la configuration
                    break
                case _:
                    print(lang["option_invalide"])
                    nettoyer_console()

# Point d'entrée du script
if __name__ == "__main__":
    main()
