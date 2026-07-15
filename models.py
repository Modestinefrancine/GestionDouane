# models.py

class DossierDouane:
    def __init__(self, id_dossier, client, type_marchandise, statut, valeur_declaration):
        self.id_dossier = id_dossier
        self.client = client
        self.type_marchandise = type_marchandise
        self.statut = statut  # Ex: "En cours", "Dédouané"
        self.valeur_declaration = valeur_declaration