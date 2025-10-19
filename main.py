from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import user_router, training_studio_router, training_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sports Center API",
    description="API za upravljanje sportskim centrima, treninzima i rezervacijama",
    version="1.0.0"
)

origins = ["*"]  
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(training_studio_router.router)
app.include_router(training_router.router)

#app.include_router(sports_center.router, prefix="/sports_centers", tags=["Sports Centers"])
#app.include_router(trainings.router, prefix="/trainings", tags=["Trainings"])
#app.include_router(training_studios.router, prefix="/training_studios", tags=["Training Studios"])
#app.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
#app.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])
#app.include_router(attendances.router, prefix="/attendances", tags=["Attendances"])

@app.get("/")
def root():
    return {"message": "Sports Center API is running 🚀"}

