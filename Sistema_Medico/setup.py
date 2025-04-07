from setuptools import setup, find_packages

setup(
    name="medhub",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "alembic",
        "python-multipart",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "jinja2",
        "aiofiles",
        "psycopg2-binary"
    ],
) 