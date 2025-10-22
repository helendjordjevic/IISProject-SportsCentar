from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.recommendation_service import MLRecommender
from app import models
from app.schemas import RecommendationOut


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommender System"]
)

@router.get("/{client_id}", response_model=list[RecommendationOut])
def get_recommendations(client_id: int, top_n: int = 5, db: Session = Depends(get_db)):
    recommender = MLRecommender(db)

    client = db.query(models.User).filter(
        models.User.user_id == client_id,
        models.User.user_type == "CLIENT"
    ).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    recommended_ids = recommender.recommend_for_user(client_id, top_n)
    trainings = db.query(models.Training).filter(models.Training.training_id.in_(recommended_ids)).all()

    result = []
    for tid in recommended_ids:
        t = next((tr for tr in trainings if tr.training_id == tid), None)
        if t:
            result.append({
                "training_id": t.training_id,
                "training_name": t.name,
                "training_type": t.training_type,
                "difficulty_level": t.difficulty_level,
                "instructor_name": f"{t.instructor.first_name} {t.instructor.last_name}"
            })

    return result