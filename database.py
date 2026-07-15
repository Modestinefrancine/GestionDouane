# database.py
import sqlite3
from models import DossierDouane
from exceptions import ConfigurationBaseDonneesError

def connecter_db():
    try:
        return sqlite3.connect("agence.db")
    except sqlite3.Error as e:
        raise ConfigurationBaseDonneesError(f"Erreur de connexion : {e}")

def initialiser_db():
    try:
        conn = connecter_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dossiers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client TEXT NOT NULL,
                marchandise TEXT NOT NULL,
                statut TEXT NOT NULL,
                valeur REAL NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise ConfigurationBaseDonneesError(f"Erreur d'initialisation : {e}")

def inserer_nouveau_dossier(client, marchandise, statut, valeur):
    """Cette fonction manquait ! Elle enregistre les calculs de l'utilisateur."""
    try:
        conn = connecter_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dossiers (client, marchandise, statut, valeur)
            VALUES (?, ?, ?, ?)
        """, (client, marchandise, statut, valeur))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise ConfigurationBaseDonneesError(f"Erreur lors de l'enregistrement du dossier : {e}")

def recuperer_tous_les_dossiers():
    try:
        conn = connecter_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, client, marchandise, statut, valeur FROM dossiers")
        lignes = cursor.fetchall()
        conn.close()
        return [DossierDouane(l[0], l[1], l[2], l[3], l[4]) for l in lignes]
    except sqlite3.Error as e:
        raise ConfigurationBaseDonneesError(f"Erreur de récupération : {e}")