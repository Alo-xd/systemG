from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# Crea las tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="GestiBuap API")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

import crud
from fastapi import HTTPException
from pydantic import BaseModel
import datetime

class EventCreateSchema(BaseModel):
    name: str
    event_type: str
    objective: str
    scope: str
    description: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    location: str
    attendee_count: int
    fee: str
    contact_phone: str
    contact_email: str
    
    background: str | None = None
    media: str | None = None
    requires_internet: bool = False
    has_guests: bool = False
    guest_details: str | None = None
    requires_equipment: bool = False

@app.post("/events/")
def create_event(event: EventCreateSchema, db: Session = Depends(get_db)):
   
    organizer_id = 1 

    new_event = crud.create_event(db=db, event_data=event.dict(), organizer_id=organizer_id)
    

    if new_event is None:
        raise HTTPException(status_code=400, detail="Conflicto detectado: Ya existe un evento aprobado en ese horario y ubicación.")
    
    return {"status": "Evento registrado exitosamente en estado PENDING", "event_id": new_event.id}

@app.get("/api/calendar")
def obtener_eventos_calendario():
    return [
        {"id": "001", "title": "Taller de Ingeniería", "start": "2026-10-26T10:00:00", "end": "2026-10-26T12:00:00", "extendedProps": {"location": "Auditorio Principal"}},
    ]

@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse(url="/login")

# 2. LOGIN
@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"error": None, "success": None})

@app.post("/login")
def login_post():
    return RedirectResponse(url="/dashboard", status_code=303)

# 3. REGISTRO
@app.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={"error": None})

@app.post("/register")
def register_post():
    return RedirectResponse(url="/activate", status_code=303)

# 4. ACTIVACIÓN
@app.get("/activate", response_class=HTMLResponse)
def activate_get(request: Request):
    return templates.TemplateResponse(request=request, name="activate.html", context={"email": "nuevo_usuario@valhala.com", "error": None})

@app.post("/activate")
def activate_post():
    return RedirectResponse(url="/login", status_code=303)

# 5. DASHBOARD Y PANTALLAS INTERNAS
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    mock_user = {"name": "Coordinador Demo", "role": "admin"}
    return templates.TemplateResponse(request=request, name="dashboard.html", context={"user": mock_user})

@app.get("/my_events", response_class=HTMLResponse)
def mis_registros(request: Request):
    mock_user = {"name": "Coordinador Demo", "role": "admin"}
    return templates.TemplateResponse(request=request, name="my_events.html", context={"user": mock_user, "organized_events": [], "attended_events": []})

@app.get("/profile", response_class=HTMLResponse)
def perfil(request: Request):
    mock_user = {"name": "Coordinador Demo", "role": "admin", "employee_id": "EMP-001"}
    return templates.TemplateResponse(request=request, name="profile.html", context={"user": mock_user})

# 6. SOLICITUD DE ESPACIO
@app.get("/request_space", response_class=HTMLResponse)
def request_space_get(request: Request):
    mock_user = {"name": "Coordinador Demo", "role": "admin", "employee_id": "EMP-001", "email": "coord@valhala.com"}
    return templates.TemplateResponse(request=request, name="request_space.html", context={"user": mock_user})

@app.post("/request_space")
def request_space_post():
    return RedirectResponse(url="/dashboard", status_code=303)

# 7. EL INDEX CON MAPA DE LEAFLET
@app.get("/mapa", response_class=HTMLResponse)
def mapa(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# 8. LOGOUT
@app.get("/logout")
def logout():
    return RedirectResponse(url="/login")
