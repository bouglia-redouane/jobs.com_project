from pydantic import BaseModel
from typing import List

# Définir les modèles de données pour le formData
class Diplome(BaseModel):
    etablissement: str
    annee: str
    specialite: str
    intitule: str
    niveau:str

class FormData(BaseModel):
    nom: str
    prenom: str
    motDePass: str
    mail: str
    telephone: str
    description: str
    domaineExpertise: str
    localisation: str
    photo: str
    diplomes: List[Diplome]
    competences: List[str]
