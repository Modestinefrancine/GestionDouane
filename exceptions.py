# exceptions.py

class AgenceDouaneException(Exception):
    """Exception de base pour le système."""
    pass

class ConfigurationBaseDonneesError(AgenceDouaneException):
    """Erreur liée à la base de données."""
    pass

class GenerationRapportError(AgenceDouaneException):
    """Erreur liée à la génération du PDF."""
    pass