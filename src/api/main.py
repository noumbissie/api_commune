from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import csv, requests
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.responses import FileResponse

models.Base.metadata.create_all(bind=engine)
version = 0.1

url = "http://nominatim:8086"

#url_file ="https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25"

app = FastAPI()




def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


@app.get("/")
async def welcome():
    
    return FileResponse("welcome.html")



@app.post(f"/api/v{version}/commune/enregistrement_fichier_BDD", response_model=schemas.Commune)
async def create_commune(url: str, db: Session = Depends(get_db)):

    resp = requests.get(url=url)
    
    resp.encoding="utf-8"
    
    f = resp.text.splitlines()
    
    reader = csv.DictReader(f)

    rows = []

    for row in reader:
        
        coord_gps = crud.get_gps(commune=row.get('nom_commune_complet'),url_map=url)

        commune = schemas.CommuneCreate(code_postal=row.get("code_postal"), nom_commune=row.get('nom_commune_complet').upper(), departement = row.get("code_postal")[:2],longitude=coord_gps['longitude'],latitude=coord_gps['latitude'])

        rows.append(crud.create_commune(db, commune = commune))
    
    return{"message":"Les données ont été enregistrées avec succès!"}




@app.get(f"/api/v{version}/commune/liste_des_communes", response_model=list[schemas.Commune])
async def read_list_communes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

   return crud.get_list_communes(db, skip=skip, limit=limit)
   





@app.get(f"/api/v{version}/commune/liste_commune_par_departement", response_model=list[schemas.Commune])
async def read_commune_dept(department: str, db: Session = Depends(get_db)):

    return crud.get_listCommune_by_dept(db, department)




@app.get(f"/api/v{version}/commune/recherche_par_nom", response_model=schemas.Commune)

async def read_commune_name(nom_commune: str, db: Session = Depends(get_db)):

    return crud.get_commune_by_name(db, nom_commune)




@app.put(f"/api/v{version}/commune/update")  

async def update_commune_( commune : schemas.CommuneBase, db: Session = Depends(get_db)):
  
    commune.nom_commune = commune.nom_commune.upper()
  
    if crud.update_commune(db, commune ):
       
       return {"message": f"la commune de {commune.nom_commune} a été mise à jour !"}
   
    return {"message": f"la commune de {commune.nom_commune} n'a pas été mise à jour !"}
       



@app.delete(f"/api/v{version}/commune/delete")

async def delete_commune_(nom_commune :str, db: Session = Depends(get_db)):
    
    if crud.delete_commune(nom_commune , db):
        
        return {"message": "la commune {nom_commune} a été supprimée"}





@app.get(f"/api/v{version}/commune/coordonéees_gps")
async def get_gps_parameters(nom_commune :str, url_map = "https://nominatim.openstreetmap.org"):
    
    return crud.get_gps(nom_commune, url_map)
    
