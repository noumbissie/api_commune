
# ce fichier les schémas des données entrantes et sortantes pour les endpoints de notre de API
from typing import Union

from pydantic import BaseModel

class CommuneBase(BaseModel):

    code_postal: Union[str, None] = None

    nom_commune: Union[str, None] = None

    departement: Union[str, None] = None


class CommuneCreate(CommuneBase):

    longitude : Union[str, None] = None

    latitude : Union[str, None] = None


class Commune(CommuneCreate):

    id_commune : int

    class Config:

        orm_mode = True