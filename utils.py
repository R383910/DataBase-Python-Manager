import os
# Fonction pour nettoyer la console
def nettoyer_console():
    """
    Nettoie la console.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# Fonction pour obtenir la liste des tables dans la base de données
def obtenir_tables(conn):
    """
    Obtient la liste des tables dans la base de données.
    """
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in cursor.fetchall()]