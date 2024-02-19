#ce fichier est utilisé pour définir la structure des tables de la base de données 
#et gérer les opérations de base de données à l'aide de SQLAlchemy

from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base

Base  = declarative_base()

class Commune(Base):
    __tablename__ = 'communes'
    
    id_commune  = Column(Integer, primary_key=True, index=True)

    code_postal = Column(String)
    
    nom_commune = Column(String)
    
    departement = Column(String)
    
    longitude = Column(String)
    
    latitude = Column(String)

    

