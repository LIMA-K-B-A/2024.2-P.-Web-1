# crud.py
from sqlalchemy.orm import Session
from app import models, schemas

# MÉDICO
def get_medicos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Medico).offset(skip).limit(limit).all()

def get_medico(db: Session, medico_id: int):
    return db.query(models.Medico).filter(models.Medico.id == medico_id).first()

def create_medico(db: Session, medico: schemas.MedicoCreate):
    db_medico = models.Medico(**medico.dict())
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico

def update_medico(db: Session, medico_id: int, medico: schemas.MedicoUpdate):
    db_medico = db.query(models.Medico).filter(models.Medico.id == medico_id).first()
    if db_medico:
        for key, value in medico.dict(exclude_unset=True).items():
            setattr(db_medico, key, value)
        db.commit()
        db.refresh(db_medico)
        return db_medico
    return None

def delete_medico(db: Session, medico_id: int):
    db_medico = db.query(models.Medico).filter(models.Medico.id == medico_id).first()
    if db_medico:
        db.delete(db_medico)
        db.commit()
        return True
    return False

# PACIENTE
def get_pacientes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Paciente).offset(skip).limit(limit).all()

def get_paciente(db: Session, paciente_id: int):
    return db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()

def create_paciente(db: Session, paciente: schemas.PacienteCreate):
    db_paciente = models.Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def update_paciente(db: Session, paciente_id: int, paciente: schemas.PacienteUpdate):
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if db_paciente:
        for key, value in paciente.dict(exclude_unset=True).items():
            setattr(db_paciente, key, value)
        db.commit()
        db.refresh(db_paciente)
        return db_paciente
    return None

def delete_paciente(db: Session, paciente_id: int):
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if db_paciente:
        db.delete(db_paciente)
        db.commit()
        return True
    return False

# CONSULTA
def get_consultas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Consulta).offset(skip).limit(limit).all()

def get_consulta(db: Session, consulta_id: int):
    return db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()

def create_consulta(db: Session, consulta: schemas.ConsultaCreate):
    db_consulta = models.Consulta(**consulta.dict())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

def update_consulta(db: Session, consulta_id: int, consulta: schemas.ConsultaUpdate):
    db_consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if db_consulta:
        for key, value in consulta.dict(exclude_unset=True).items():
            setattr(db_consulta, key, value)
        db.commit()
        db.refresh(db_consulta)
        return db_consulta
    return None

def delete_consulta(db: Session, consulta_id: int):
    db_consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if db_consulta:
        db.delete(db_consulta)
        db.commit()
        return True
    return False