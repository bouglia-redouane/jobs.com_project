import uvicorn
from fastapi import FastAPI, Query
from apis import app  # Importing the FastAPI app from your API file

# Main entry point to run the FastAPI app
if __name__ == "__main__":
    uvicorn.run("apis:app", host="0.0.0.0", port=8000, reload=True)
