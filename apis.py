from fastapi import FastAPI, Query
import json
from utils import FormData
from DB import DBClass  # Import the DBClass
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from datetime import timedelta
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
    if db.user_exists(form_data.mail):
        raise HTTPException(status_code=400, detail="Email already registered")
    response = db.sing_up(form_data)
    if not response:
        raise HTTPException(status_code=500, detail="Failed to register user")
    print(response)
    return {"message": "User registered successfully", "data": form_data.dict()}

@app.post("/login")
async def login(email: str, password: str):
    """
    API endpoint to authenticate a user and generate a token.
    """
    if not db.user_exists(email):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify the password
    if not db.verify_password(email, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = db.generate_token()
    if not token:
        raise HTTPException(status_code=500, detail="Failed to generate token")

    return {
        "message": "Login successful",
        "token": token,
        "expires_in": int(timedelta(hours=1).total_seconds())  # Token expires in 1 hour
    }


@app.get("/validate-token")
async def validate_token(token: str):
    """
    API endpoint to validate a token.
    """
    is_valid = db.validate_token(token)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return is_valid

