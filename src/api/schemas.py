
# ce fichier les schémas des données entrantes et sortantes pour les endpoints de notre de API
from typing import Union

from pydantic import BaseModel


#la classe de base contient les informations capitales
class CommuneBase(BaseModel):

    code_postal: Union[str, None] = None

    nom_commune: Union[str, None] = None

    departement: Union[str, None] = None


#cette classe permet de rajouter les coordonées gps de la commune
class CommuneCreate(CommuneBase):

    longitude : Union[str, None] = None

    latitude : Union[str, None] = None


#cette classe permet de pouvoir recuperer nos données dans la base de donnée
class Commune(CommuneCreate):

    id_commune : int

    class Config:

        orm_mode = True