import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('materiel_informatique.sqlite')
cursor = conn.cursor()

def afficher_menu():
    print("1. Récupérer des informations")
    print("2. Ajouter des informations")
    print("3. Supprimer des informations")
    print("4. Quitter")

def afficher_menu_tables():
    print("1. GPUs")
    print("2. CPUs")
    print("3. NPUs")
    print("4. AutresComposants")
    print("5. Fabricants")
    print("6. TypesMemoire")
    print("7. Interfaces")
    print("8. TypesComposants")

def obtenir_table():
    afficher_menu_tables()
    choix_table = input("Choisissez le numéro de la table: ")

    tables = {
        '1': 'GPUs',
        '2': 'CPUs',
        '3': 'NPUs',
        '4': 'AutresComposants',
        '5': 'Fabricants',
        '6': 'TypesMemoire',
        '7': 'Interfaces',
        '8': 'TypesComposants'
    }

    if choix_table not in tables:
        print("Table non reconnue.")
        return None

    return tables[choix_table]

def obtenir_informations(table, choix):
    if choix.isdigit():
        cursor.execute(f"SELECT * FROM {table} WHERE Id = ?", (choix,))
    else:
        cursor.execute(f"SELECT * FROM {table} WHERE Nom = ?", (choix,))

    result = cursor.fetchone()
    if result:
        # Récupérer les noms des colonnes
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]

        # Afficher les informations avec une mise en forme améliorée
        print("\nInformations récupérées :")
        for col, val in zip(columns, result):
            print(f"{col}: {val}")
        print()
    else:
        print("Aucune information trouvée.")

def recuperer_informations():
    table = obtenir_table()
    if table:
        choix = input("Entrez l'ID ou le Nom pour récupérer les informations: ")
        obtenir_informations(table, choix)

def ajouter_informations():
    table = obtenir_table()
    if table:
        match table:
            case "GPUs":
                nom = input("Nom: ")
                marque = input("Marque: ")
                modele = input("Modèle: ")
                frequence = int(input("Fréquence (en MHz): "))
                vram = int(input("VRAM (en Go): "))
                type_de_memoire = input("Type de mémoire: ")
                consommation = int(input("Consommation (en watts): "))
                date_de_sortie = input("Date de sortie (YYYY-MM-DD): ")
                prix = float(input("Prix (en €): "))
                cursor.execute("INSERT INTO GPUs (Nom, Marque, Modele, Frequence, VRAM, TypeDeMemoire, Consommation, DateDeSortie, Prix) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (nom, marque, modele, frequence, vram, type_de_memoire, consommation, date_de_sortie, prix))
            case "CPUs":
                nom = input("Nom: ")
                marque = input("Marque: ")
                modele = input("Modèle: ")
                frequence = int(input("Fréquence (en MHz): "))
                nb_coeur = int(input("Nombre de cœurs: "))
                nb_threads = int(input("Nombre de threads: "))
                date_de_sortie = input("Date de sortie (YYYY-MM-DD): ")
                prix = float(input("Prix (en €): "))
                cursor.execute("INSERT INTO CPUs (Nom, Marque, Modele, Frequence, NbCoeur, NbThreads, DateDeSortie, Prix) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               (nom, marque, modele, frequence, nb_coeur, nb_threads, date_de_sortie, prix))
            case "NPUs":
                nom = input("Nom: ")
                marque = input("Marque: ")
                modele = input("Modèle: ")
                frequence = int(input("Fréquence (en MHz): "))
                nb_coeur = int(input("Nombre de cœurs: "))
                memoire = int(input("Mémoire (en Go): "))
                type_memoire = input("Type de mémoire: ")
                date_de_sortie = input("Date de sortie (YYYY-MM-DD): ")
                prix = float(input("Prix (en €): "))
                cursor.execute("INSERT INTO NPUs (Nom, Marque, Modele, Frequence, NbCoeur, Memoire, TypeMemoire, DateDeSortie, Prix) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (nom, marque, modele, frequence, nb_coeur, memoire, type_memoire, date_de_sortie, prix))
            case "AutresComposants":
                nom = input("Nom: ")
                marque = input("Marque: ")
                modele = input("Modèle: ")
                type_composant = input("Type de composant: ")
                frequence_vitesse = int(input("Fréquence/Vitesse (en MHz/Mo/s): "))
                interface = input("Interface: ")
                date_de_sortie = input("Date de sortie (YYYY-MM-DD): ")
                prix = float(input("Prix (en €): "))
                cursor.execute("INSERT INTO AutresComposants (Nom, Marque, Modele, Type, FrequenceVitesse, Interface, DateDeSortie, Prix) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               (nom, marque, modele, type_composant, frequence_vitesse, interface, date_de_sortie, prix))
            case "Fabricants":
                nom = input("Nom: ")
                site_web = input("Site web: ")
                cursor.execute("INSERT INTO Fabricants (Nom, SiteWeb) VALUES (?, ?)", (nom, site_web))
            case "TypesMemoire":
                nom = input("Nom: ")
                description = input("Description: ")
                cursor.execute("INSERT INTO TypesMemoire (Nom, Description) VALUES (?, ?)", (nom, description))
            case "Interfaces":
                nom = input("Nom: ")
                description = input("Description: ")
                cursor.execute("INSERT INTO Interfaces (Nom, Description) VALUES (?, ?)", (nom, description))
            case "TypesComposants":
                nom = input("Nom: ")
                description = input("Description: ")
                cursor.execute("INSERT INTO TypesComposants (Nom, Description) VALUES (?, ?)", (nom, description))
            case _:
                print("Table non reconnue.")
                return

        conn.commit()
        print("Information ajoutée avec succès.")

def supprimer_informations():
    table = obtenir_table()
    if table:
        choix = input("Entrez l'ID ou le Nom pour supprimer les informations: ")

        if choix.isdigit():
            cursor.execute(f"DELETE FROM {table} WHERE Id = ?", (choix,))
        else:
            cursor.execute(f"DELETE FROM {table} WHERE Nom = ?", (choix,))

        if cursor.rowcount > 0:
            conn.commit()
            print("Information supprimée avec succès.")
        else:
            print("Aucune information trouvée.")

def main():
    while True:
        afficher_menu()
        choix = input("Choisissez une option: ")
        match choix:
            case '1':
                recuperer_informations()
            case '2':
                ajouter_informations()
            case '3':
                supprimer_informations()
            case '4':
                break
            case _:
                print("Option invalide.")

if __name__ == "__main__":
    main()
    conn.close()
