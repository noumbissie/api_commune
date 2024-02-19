from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import csv, requests
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
version = 0.1


#url_file ="https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25"

app = FastAPI()




def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 



@app.post(f"/api/v{version}/commune/enregistrement_fichier_BDD", response_model=schemas.Commune)
async def create_commune(url: str, db: Session = Depends(get_db)):

    resp = requests.get(url=url)
    
    resp.encoding="utf-8"
    
    f = resp.text.splitlines()
    
    reader = csv.DictReader(f)

    rows = []

    for row in reader:

        commune = schemas.CommuneCreate(code_postal=row.get("code_postal"), nom_commune=row.get('nom_commune_complet').upper(), departement = row.get("code_postal")[:2])

        rows.append(crud.create_commune(db, commune = commune))
    
    return{"message":"Les données ont été enregistrées avec succès!"}




@app.get(f"/api/v{version}/commune/liste_des_communes/", response_model=list[schemas.Commune])
async def read_list_communes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

   return crud.get_list_communes(db, skip=skip, limit=limit)
   





@app.get(f"/api/v{version}/commune/liste_commune_par_departement", response_model=list[schemas.Commune])
async def read_commune_dept(department: str, db: Session = Depends(get_db)):

    return crud.get_listCommune_by_dept(db, department)




@app.get(f"/api/v{version}/commune", response_model=schemas.Commune)

async def read_commune_name(nom_commune: str, db: Session = Depends(get_db)):

    return crud.get_commune_by_name(db, nom_commune)




@app.put(f"/api/v{version}/commune/update_commune/")  

async def update_commune_( commune : schemas.CommuneCreate, db: Session = Depends(get_db)):
  
   if crud.update_commune(db, commune ):
       
       return {"message": f"la commune de {commune.nom_commune} a été mise à jour !"}
        






@app.delete(f"/api/v{version}/commune/delete_commune/")

async def delete_commune_(nom_commune :str, db: Session = Depends(get_db)):
    
    if crud.delete_commune(nom_commune , db):
        
        return {"message": "la commune {nom_commune} a été supprimée"}




@app.get("/")
async def welcome():
    
    return{"message": "Gestion des données de commune, Bienvenue"}


@app.get("/gps_commune/")
async def get_gps_parameters(commune :str):
    
    return crud.get_gps(commune)
    
