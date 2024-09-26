import json
import os

LOGS_DIR = 'logs'
CONFIG_FILE = os.path.join(LOGS_DIR, 'config.json')
LANG_FILE = os.path.join(LOGS_DIR, 'lang.json')

def lire_config():
    """
    Lit la configuration depuis un fichier JSON.
    Si le fichier n'existe pas, retourne un dictionnaire vide.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def lire_lang(lang):
    """
    Lit les chaînes de caractères localisées depuis un fichier JSON.
    """
    with open(LANG_FILE, 'r') as f:
        return json.load(f).get(lang, {})
    