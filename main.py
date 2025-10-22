from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import user_router, training_studio_router, training_router, sports_center_router, session_router, reservation_router, attendance_router, recommendation_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sports Center API",
    description="API za upravljanje sportskim centrima, treninzima i rezervacijama",
    version="1.0.0"
)

origins = ["*"]  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:6001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(training_studio_router.router)
app.include_router(training_router.router)
app.include_router(sports_center_router.router)
app.include_router(session_router.router)
app.include_router(reservation_router.router)
app.include_router(attendance_router.router)
app.include_router(recommendation_router.router) 



@app.get("/")
def root():
    return {"message": "Sports Center API is running 🚀"}

