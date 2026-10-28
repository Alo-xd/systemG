from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime

class UserProfile(Base):
    """
    Tabla para los datos extendidos del usuario.
    NOTA: Las contraseñas y correos principales los manejará Keycloak.
    Aquí solo guardamos datos operativos de la institución.
    """
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    keycloak_id = Column(String, unique=True, index=True)
    employee_id = Column(String, unique=True, index=True) 
    name = Column(String)
    section = Column(String) 
    role = Column(String, default="user") 
    phrase = Column(String, default="")
    profile_pic = Column(String, nullable=True)

    events_organized = relationship("Event", back_populates="organizer")

class Event(Base):
    """
    Tabla central de GestiBuap: Registro de eventos y solicitudes de espacio.
    """
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    folio = Column(String, unique=True, index=True, nullable=True) 
    
    name = Column(String, index=True)
    event_type = Column(String) 
    objective = Column(String)
    scope = Column(String)
    description = Column(Text)
    
    
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String)
    
 
    attendee_count = Column(Integer, default=0)
    fee = Column(String, default="Gratuito")
    contact_phone = Column(String)
    contact_email = Column(String)
    
    background = Column(Text, nullable=True)
    media = Column(Text, nullable=True)
    requires_internet = Column(Boolean, default=False)
    has_guests = Column(Boolean, default=False)
    guest_details = Column(Text, nullable=True) 
    requires_equipment = Column(Boolean, default=False)
    equipment_image = Column(String, nullable=True)
    
    status = Column(String, default="PENDING")
    resolution_conditions = Column(Text, nullable=True)
    authorized_by = Column(String, nullable=True)
    
    organizer_id = Column(Integer, ForeignKey("user_profiles.id"))
    organizer = relationship("UserProfile", back_populates="events_organized")
