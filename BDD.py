import sqlite3

# Établir une connexion à la base de données
bdd = sqlite3.connect('C:/Users/Gabriel/DataGripProjects/test/materiel_informatique.sqlite')

# Créer un curseur
cursor = bdd.cursor()

def GetInfo():
    table = input("Dans quelle table voulez vous executé la commande ? ")
    commande = input("récupéré des information (get) , supprimer des information (delete), ajouter des information (add) ?")

    return table, commande

def CommandeToExecute():
    table, commande = GetInfo()
    if commande.upper() == "GET":
        commande = "SELECT * FROM " + table
    elif commande.upper() == "DELETE":
        # Add your DELETE command here
        pass
    elif commande.upper() == "ADD":
        # Add your ADD command here
        pass
    else:
        print("Commande non reconnue")
        return None

    print(commande)
    return commande

def Execute(cursor):
    commande = CommandeToExecute()
    if commande is not None:
        cursor.execute(commande)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    cursor.close()

Execute(cursor)
