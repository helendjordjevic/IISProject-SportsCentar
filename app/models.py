from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Date, TIMESTAMP, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# ENUMS
class UserTypeEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    INSTRUCTOR = "INSTRUCTOR"
    CLIENT = "CLIENT"

class ReservationStatusEnum(str, enum.Enum):
    RESERVED = "RESERVED"
    CANCELLED = "CANCELLED"

class AttendanceStatusEnum(str, enum.Enum):
    ATTENDED = "ATTENDED"
    NOT_ATTENDED = "NOT_ATTENDED"

# MODELS
class SportsCenter(Base):
    __tablename__ = "sports_centers"

    sports_center_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    # Veze
    users = relationship("User", back_populates="sports_center")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    user_type = Column(Enum(UserTypeEnum), nullable=False)
    sports_center_id = Column(Integer, ForeignKey("sports_centers.sports_center_id", ondelete="SET NULL"))

    sports_center = relationship("SportsCenter", back_populates="users")
    trainings = relationship("Training", back_populates="instructor", cascade="all, delete")
    reservations = relationship("Reservation", back_populates="client", cascade="all, delete")
    attendances = relationship("Attendance", back_populates="client", cascade="all, delete")


class TrainingStudio(Base):
    __tablename__ = "training_studios"
    __table_args__ = (
        CheckConstraint('capacity > 0', name='chk_capacity_positive'),
    )

    training_studio_id = Column(Integer, primary_key=True, index=True)
    training_studio_number = Column(String(20), nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)

    sessions = relationship("Session", back_populates="training_studio", cascade="all, delete")


class Training(Base):
    __tablename__ = "trainings"

    training_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    training_type = Column(String(50))
    instructor_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))

    instructor = relationship("User", back_populates="trainings")
    sessions = relationship("Session", back_populates="training", cascade="all, delete")


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    training_id = Column(Integer, ForeignKey("trainings.training_id", ondelete="CASCADE"))
    training_studio_id = Column(Integer, ForeignKey("training_studios.training_studio_id", ondelete="SET NULL"))

    training = relationship("Training", back_populates="sessions")
    training_studio = relationship("TrainingStudio", back_populates="sessions")
    reservations = relationship("Reservation", back_populates="session", cascade="all, delete")
    attendances = relationship("Attendance", back_populates="session", cascade="all, delete")


class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = (UniqueConstraint("client_id", "session_id", name="uq_client_session"),)

    reservation_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    session_id = Column(Integer, ForeignKey("sessions.session_id", ondelete="CASCADE"))
    reservation_date = Column(Date, nullable=False)
    status = Column(Enum(ReservationStatusEnum), nullable=False)

    client = relationship("User", back_populates="reservations")
    session = relationship("Session", back_populates="reservations")


class Attendance(Base):
    __tablename__ = "attendances"
    __table_args__ = (UniqueConstraint("client_id", "session_id", name="uq_client_session_attendance"),)

    attendance_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    session_id = Column(Integer, ForeignKey("sessions.session_id", ondelete="CASCADE"))
    attendance_date = Column(Date)
    training_rating = Column(Integer)
    attendance_status = Column(Enum(AttendanceStatusEnum), nullable=False)

    client = relationship("User", back_populates="attendances")
    session = relationship("Session", back_populates="attendances")

    __table_args__ = (
        UniqueConstraint("client_id", "session_id", name="uq_client_session_attendance"),
        CheckConstraint("training_rating BETWEEN 1 AND 10", name="chk_training_rating"),
    )
