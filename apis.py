from fastapi import FastAPI, Query
import json
from utils import FormData
from DB import DBClass  # Import the DBClass
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

app = FastAPI()

# Configuration CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize DBClass once to avoid reconnecting for every request
db = DBClass()

@app.get("/")
def search_jobs(
    key_word: str = Query(..., description="Keyword for job title"),
    location: str = Query(..., description="Location for the job search")
):
    """
    API endpoint to search jobs based on a keyword and location.
    """
    result = db.execute_query(key_word, location)
    if result:
        return json.loads(result)  # Return JSON response
    return {"error": "No data found or database connection issue"}


@app.post("/sign_up")
async def sign_up(form_data: FormData):
    # Check if the user already exists
    if db.user_exists(form_data.mail):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Attempt to add the user to the database
    success = db.add_user(
        nom=form_data.nom,
        prenom=form_data.prenom,
        motDePass=form_data.motDePass,
        mail=form_data.mail,
        telephone=form_data.telephone,
        description=form_data.description,
        domaineExpertise=form_data.domaineExpertise,
        localisation=form_data.localisation,
        diplomes=form_data.diplomes,
        competences=form_data.competences,
        photo=form_data.photo
    )

    if not success:
        raise HTTPException(status_code=500, detail="Failed to register user")

    return {"message": "User registered successfully", "data": form_data.dict()}