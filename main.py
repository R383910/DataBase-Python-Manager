from frontend import *
from backend import *


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
                    # Sauvegarder et restaurer la base de données
                    backup_path = input("Entrez le chemin de sauvegarde : ")
                    sauvegarder_base_de_donnees(db_path, backup_path)
                    restore_path = input("Entrez le chemin de restauration : ")
                    restaurer_base_de_donnees(restore_path, db_path)
                case '6':
                    # Exporter et importer des données en JSON
                    table = obtenir_table(conn, lang)
                    if table:
                        export_path = input("Entrez le chemin d'exportation : ")
                        exporter_table_en_json(conn, table, export_path)
                        import_path = input("Entrez le chemin d'importation : ")
                        importer_table_depuis_json(conn, table, import_path)
                case '7':
                    # Recherche avancée
                    table = obtenir_table(conn, lang)
                    if table:
                        criteres = {}
                        while True:
                            col = input("Entrez le nom de la colonne (ou 'fin' pour terminer) : ")
                            if col.lower() == 'fin':
                                break
                            val = input(f"Entrez la valeur pour la colonne {col} : ")
                            criteres[col] = val
                        recherche_avancee(conn, table, criteres)
                case '8':
                    # Gérer les utilisateurs
                    creer_table_utilisateurs(conn)
                    nom = input("Entrez le nom de l'utilisateur : ")
                    mot_de_passe = input("Entrez le mot de passe : ")
                    role = input("Entrez le rôle (admin/utilisateur) : ")
                    ajouter_utilisateur(conn, nom, mot_de_passe, role)
                    nom = input("Entrez le nom de l'utilisateur pour l'authentification : ")
                    mot_de_passe = input("Entrez le mot de passe pour l'authentification : ")
                    user = authentifier_utilisateur(conn, nom, mot_de_passe)
                    if user:
                        print(f"Authentification réussie : {user}")
                    else:
                        print("Authentification échouée.")
                case '9':
                    # Automatisation des tâches
                    interval = int(input("Entrez l'intervalle en secondes : "))
                    tache_planifiee(interval, exemple_tache)
                case '10':
                    config['lang'] = lang['lang']  # Enregistrer la langue choisie dans le fichier de configuration
                    ecrire_config(config)  # Enregistrer la configuration
                    break
                case _:
                    print(lang["option_invalide"])
                    nettoyer_console()

# Point d'entrée du script
if __name__ == "__main__":
    main()
