from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main_crew import run_resume_screening_crew
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestQuestion(BaseModel):
    description: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the API server!"}

@app.post("/response")
def get_response(description: RequestQuestion):
    try:
        result = run_resume_screening_crew(job_description=description.description)

        if result:   
            return {"response": result}
        else:
            raise HTTPException(status_code=500, detail="Invalid response format from CrewAI")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred during prediction: {str(e)}")

