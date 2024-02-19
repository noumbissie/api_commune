import requests,csv

from sqlalchemy.orm import Session

from fastapi import HTTPException

from models import Commune

from schemas import CommuneCreate, CommuneBase

from schemas import Commune as CommuneSchemas

from sqlalchemy import update, delete


#Cette fonction permet de rajouter une commune dans la base de données
def create_commune(db:Session, commune:CommuneCreate):

    db_commune =Commune(**commune.dict())

    db.add(db_commune)

    db.commit()

    db.refresh(db_commune)

    return db_commune



# Cette fonction retourne un liste de commune allant du skip à limit 
def get_list_communes(db:Session, skip: int, limit:int= 100):
    
    if db.query(Commune).offset(skip).limit(limit).all():
        
        return db.query(Commune).offset(skip).limit(limit).all()
 
    else:
        
        raise HTTPException(status_code=500, detail="taille trop grande ! ")



#Retourne l'information d'une commune à partir de son nom
def get_commune_by_name(db: Session, nom_commune : str):
    
    db_commune = db.query(Commune).filter(Commune.nom_commune == nom_commune.upper()).first()
    
    if db_commune:
        
        return db_commune
 
    else:
        
        raise HTTPException(status_code=500, detail="Cette commmune n'existe pas dans la bas de données! ")
    


#Retourne la liste des communes appartenant à un département
def get_listCommune_by_dept(db: Session, departement : str):
    
    if db.query(Commune).filter(Commune.departement == departement).all():
        
        return db.query(Commune).filter(Commune.departement == departement).all()
    
    else:
        
        raise HTTPException(status_code=500, detail="Ce departement n'existe pas ! ")



#Permet de mettre à jour une commune dans la base , son code_postal et son departement
def update_commune(db: Session, commune : CommuneBase ):
    
    print(commune)
    updated_commune = db.query(Commune).filter(Commune.nom_commune == commune.nom_commune)
    print(updated_commune.first())
    if updated_commune.first():
        
        updated_commune.update(commune.dict(), synchronize_session = False)
        
        db.commit()
        
        return updated_commune.first()
    
    else :
        raise HTTPException(status_code=500, detail="Impossible de mettre a jour cette commune ")
    



#Permet de supprimer une commune de la base de donnée 

def delete_commune(nom_commune :str, db:Session):
    
    commune = db.query(Commune).filter(Commune.nom_commune == nom_commune.upper())
    
    if commune :
        
        commune.delete(synchronize_session = False)
        
        db.commit()
        
        return{"message":f"la commune  {nom_commune}  a été supprimée"}
    
    else :
        raise HTTPException(status_code=500, detail="Impossible de supprimer cette commune ")
    


# cette fonction permet de charger et recuperer les données à partir d'une url 
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


#cette fonction retourne les coordonées gps d'une commune à travers son nom et le lien vers un mappeur dockerisé

def get_gps(commune : str, url_map = "https://nominatim.openstreetmap.org"):
    
    params = {
        "q": commune,
        "format": "json",
        "limit": 1
    }
     
    response = requests.get(url_map, params=params)
    
    if response.status_code == 200:
        
        data = response.json()
        
        if data:
            
            latitude = (data[0]["lat"])
            
            longitude = (data[0]["lon"])
            
            return {"latitude" :latitude, "longitude":  longitude}
        
        else:
            raise HTTPException(status_code=404, detail="Commune introuvable ! ")
    else:
        raise HTTPException(status_code=500, detail="Erreur de recherche sur le site de Nominatim")
    
