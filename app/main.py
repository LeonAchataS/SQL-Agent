from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
# from app.graph.workflow import 
# from app.models.state import GraphState
# from app.models.schemas import 
# from app.utils.helpers import 

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok",
            "app_name": settings.app_name,
            "version": "1.0.0",
            }


