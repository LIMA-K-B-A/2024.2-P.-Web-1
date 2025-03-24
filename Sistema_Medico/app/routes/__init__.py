from .register import router as register_router
from .auth import router as auth_router
from .consulta import router as consulta_router
from .medico import router as medico_router
from .paciente import router as paciente_router

__all__ = [
    'register_router',
    'auth_router',
    'consulta_router',
    'medico_router',
    'paciente_router'
] 