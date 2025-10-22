import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import func
from app import models

class MLRecommender:
    def __init__(self, db):
        self.db = db

    def build_training_matrix(self):
        trainings = self.db.query(models.Training).all()
        data = []

        for t in trainings:
            avg_rating = (
                self.db.query(func.avg(models.Attendance.training_rating))
                .join(models.Session)
                .filter(models.Session.training_id == t.training_id)
                .scalar()
            ) or 0

            # uzimamo sve sesije treninga da pokupimo weekday i period
            sessions = self.db.query(models.Session).filter(models.Session.training_id == t.training_id).all()
            weekdays = list({s.weekday or "UNKNOWN" for s in sessions}) or ["UNKNOWN"]
            periods = list({s.day_period or "UNKNOWN" for s in sessions}) or ["UNKNOWN"]

            data.append({
                "training_id": t.training_id,
                "training_type": t.training_type or "UNKNOWN",
                "instructor_id": str(t.instructor_id),
                "difficulty_level": t.difficulty_level or "UNKNOWN",
                "avg_rating": float(avg_rating),
                "weekdays": ",".join(weekdays),
                "periods": ",".join(periods)
            })

        df = pd.DataFrame(data)

        # One-hot enkodovanje svih kategorija osim avg_rating
        categorical_cols = ["training_type", "instructor_id", "difficulty_level", "weekdays", "periods"]
        encoder = OneHotEncoder(sparse_output=False)
        encoded = encoder.fit_transform(df[categorical_cols])
        feature_df = pd.DataFrame(encoded, index=df.index)

        full_df = pd.concat([df[["training_id", "avg_rating"]], feature_df], axis=1)
        full_df["avg_rating"] = full_df["avg_rating"].astype(float)
        return full_df.set_index("training_id")

    def recommend_for_user(self, client_id: int, top_n: int = 5):
        training_matrix = self.build_training_matrix()

        attended = (
            self.db.query(models.Attendance)
            .join(models.Session)
            .filter(models.Attendance.client_id == client_id)
            .filter(models.Attendance.training_rating.isnot(None))
            .all()
        )
        attended_ids = [a.session.training_id for a in attended if a.session.training_id in training_matrix.index]

        if not attended_ids:
            # Ako korisnik nije pohađao nijedan trening
            return list(training_matrix.nlargest(top_n, "avg_rating").index)

        # Korisnikov profil = prosek svih treninga koje je pohađao
        user_profile = training_matrix.loc[attended_ids].mean().values.reshape(1, -1)
        similarities = cosine_similarity(user_profile, training_matrix)[0]

        sim_scores = pd.Series(similarities, index=training_matrix.index)
        recommendations = sim_scores.drop(attended_ids, errors="ignore").nlargest(top_n)

        return list(recommendations.index)
