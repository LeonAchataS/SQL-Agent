from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import get_settings
from app.services import db as db_service

# Attempt to import the agent router if the package is present. This file
# remains runnable even if the skeleton packages are not yet populated.
try:
    from app.api.v1 import agent_router  # type: ignore
except Exception:
    agent_router = None

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await db_service.init_db_pool()
    except Exception:
        # If DB not configured, skip initialization (tests/dev)
        pass
    
    yield
    
    # Shutdown
    try:
        await db_service.close_db_pool()
    except Exception:
        pass


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "app_name": settings.app_name, "version": "1.0.0"}


# Mount the agent router if available. The router will be created under
# `app/api/v1/agent_router.py` as part of the skeleton.
if agent_router is not None and hasattr(agent_router, "router"):
    app.include_router(agent_router.router, prefix="/api/v1/agent")


if __name__ == "__main__":
    import uvicorn
    # Use settings host/port
    uvicorn.run("app.main:app", host=settings.api_host, port=settings.api_port, reload=settings.api_reload)


