from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import models
import datetime


def get_event_by_id(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_all_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def get_events_by_organizer(db: Session, organizer_id: int):
    return db.query(models.Event).filter(models.Event.organizer_id == organizer_id).all()

def check_time_conflict(db: Session, location: str, start_time: datetime.datetime, end_time: datetime.datetime):
    """
    Algoritmo central de Prevención de Conflictos.
    Verifica si existe algún evento APROBADO en la misma 'location' 
    cuyos horarios se empalmen con el evento que se intenta crear.
    """
    conflict = db.query(models.Event).filter(
        models.Event.location == location,
        models.Event.status == "APPROVED",
        and_(
            start_time < models.Event.end_time,
            end_time > models.Event.start_time
        )
    ).first()
    
    return conflict is not None

def create_event(db: Session, event_data: dict, organizer_id: int):
    
    if check_time_conflict(db, event_data["location"], event_data["start_time"], event_data["end_time"]):
        return None 


    db_event = models.Event(
        name=event_data["name"],
        event_type=event_data["event_type"],
        objective=event_data["objective"],
        scope=event_data["scope"],
        description=event_data["description"],
        start_time=event_data["start_time"],
        end_time=event_data["end_time"],
        location=event_data["location"],
        attendee_count=event_data.get("attendee_count", 0),
        fee=event_data.get("fee", "Gratuito"),
        contact_phone=event_data["contact_phone"],
        contact_email=event_data["contact_email"],
        background=event_data.get("background", ""),
        media=event_data.get("media", ""),
        requires_internet=event_data.get("requires_internet", False),
        has_guests=event_data.get("has_guests", False),
        guest_details=event_data.get("guest_details", ""),
        requires_equipment=event_data.get("requires_equipment", False),
        organizer_id=organizer_id,
        status="PENDING" 
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_user_profile_by_keycloak_id(db: Session, keycloak_id: str):
    return db.query(models.UserProfile).filter(models.UserProfile.keycloak_id == keycloak_id).first()

def get_user_profile_by_employee_id(db: Session, employee_id: str):
    return db.query(models.UserProfile).filter(models.UserProfile.employee_id == employee_id).first()

def create_user_profile(db: Session, profile_data: dict):
    db_profile = models.UserProfile(**profile_data)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile
