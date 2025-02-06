from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import Base, engine
from .routers import auth, dashboard, doctors, patients, appointments
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(appointments.router)

@app.get("/")
async def root():
    return RedirectResponse(url="/register")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)