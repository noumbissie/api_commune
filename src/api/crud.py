import requests,csv

from sqlalchemy.orm import Session

from fastapi import HTTPException

from models import Commune

from schemas import CommuneCreate, CommuneBase

from schemas import Commune as CommuneSchemas

from sqlalchemy import update, delete

import folium

#Cette fonction permet de rajouter les données dans la base de données
def create_commune(db:Session, commune:CommuneCreate):

    db_commune =Commune(**commune.dict())

    db.add(db_commune)

    db.commit()

    db.refresh(db_commune)

    return db_commune



# Cette fonction retrourne un liste de commune allant du skip à limit 
def get_list_communes(db:Session, skip: int, limit:int= 100):
    
    if db.query(Commune).offset(skip).limit(limit).all():
        
        return db.query(Commune).offset(skip).limit(limit).all()
 
    else:
        
        raise HTTPException(status_code=500, detail="taille trop grande ! ")



#Retourner l'information d'une commune à partir de son nom
def get_commune_by_name(db: Session, nom_commune : str):
    
    if db.query(Commune).filter(Commune.nom_commune == nom_commune).first():
        
        return db.query(Commune).filter(Commune.nom_commune == nom_commune).first()
 
    else:
        
        raise HTTPException(status_code=500, detail="Cette commmune n'existe pas dans la bas de données! ")
    


#Retourne la liste des communes appartenant à un département
def get_listCommune_by_dept(db: Session, departement : str):
    
    if db.query(Commune).filter(Commune.departement == departement).all():
        
        return db.query(Commune).filter(Commune.departement == departement).all()
    
    else:
        
        raise HTTPException(status_code=500, detail="Ce departement n'existe pas ! ")



#Permet de mettre à jour une commune dans la base , on en profite pour passer les valeurs de la longitude et de la latitude 
def update_commune(db: Session, commune : CommuneCreate ):
    
    updated_commune = db.query(Commune).filter(Commune.nom_commune == commune.nom_commune)
    
    if updated_commune.first():
        
        updated_commune.update(commune.dict(), synchronize_session = False)
        
        db.commit()
        
        return updated_commune.first()
    
    else :
        raise HTTPException(status_code=500, detail="Impossible de mettre a jour cette commune ")
    



#Permet de supprimer une commune de la base de donnée 

def delete_commune(nom_commune :str, db:Session):
    
    commune = db.query(Commune).filter(Commune.nom_commune == nom_commune)
    
    if commune :
        
        commune.delete(synchronize_session = False)
        
        db.commit()
        db.refresh()
        
        return{"message": "la commune  {commune.nom_commune}  a été supprimée"}
    
    else :
        raise HTTPException(status_code=500, detail="Impossible de supprimer cette commune ")
    


# cette permet de charger recuperer les données a partir d'une url 
def data_commune(url_file):
    
    resp = requests.get(url_file)
    
    resp.raise_for_status()
    
    resp.encoding='utf8'
    
    extracted_data = []
    
    f = resp.text.splitlines()
    
    reader = csv.DictReader(f)

    for row in reader : 
        
        code_postal = row.get('code_postal')
        
        nom_commune= (row.get('nom_commune_complet')).upper()
        
        departement = code_postal[:2]
        
        extracted_data.append({'code_postal': code_postal,'nom_commune': nom_commune, 'departement': departement})
    
    return extracted_data




def get_gps(commune : str):
    
    params = {
        "q": commune,
        "format": "json",
        "limit": 1
    }
    url_map = "https://nominatim.openstreetmap.org"
    
    response = requests.get(url_map, params=params)
    
    if response.status_code == 200:
        
        data = response.json()
        
        if data:
            
            latitude = (data[0]["lat"])
            
            longitude = (data[0]["lon"])
             
            # nom_commune  = folium.Map(location = [latitude, longitude], zoom_start = 12)
            
            #marqueur = folium.Marker([latitude, longitude], popup = commune.upper()).add_to(nom_commune)
            

            
            return {"latitude:" :latitude, "longitude:":  longitude}
        
        else:
            raise HTTPException(status_code=404, detail="Commune introuvable ! ")
    else:
        raise HTTPException(status_code=500, detail="Erreur de recherche sur le site de Nominatim")
    
