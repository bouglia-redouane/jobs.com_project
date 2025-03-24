from pydantic import BaseModel
from typing import List

# Définir les modèles de données pour le formData
class Diplome(BaseModel):
    etablissement: str
    annee: str
    diplome: str

class FormData(BaseModel):
    nom: str
    prenom: str
    motDePass: str
    mail: str
    telephone: str
    description: str
    domaineExpertise: str
    localisation: str
    diplomes: List[Diplome]
    competences: List[str]
    photo: str