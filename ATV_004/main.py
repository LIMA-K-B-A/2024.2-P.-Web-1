from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json

app = FastAPI()

# Função para carregar os dados do JSON
def load_countries():
    with open("countries.json", "r") as file:
        return json.load(file)

# Função para salvar os dados no JSON
def save_countries(countries):
    with open("countries.json", "w") as file:
        json.dump(countries, file, indent=4)


# Modelo para adicionar novos países
class Country(BaseModel):
    capital: str
    population: int
    continent: str


# 1. Endpoint: Consultar informações de um país
@app.get("/country/{country_name}")
def get_country(country_name: str):
    countries = load_countries()
    for country in countries:
        if country["country_name"].lower() == country_name.lower():
            return country
    raise HTTPException(status_code=404, detail="País não encontrado")


# 2. Endpoint: Filtrar países por continente
@app.get("/countries/")
def get_countries(continent: Optional[str] = None):
    countries = load_countries()
    if continent:
        filtered_countries = [
            country for country in countries
            if country["continent"].lower() == continent.lower()
        ]
        return filtered_countries
    return countries


# 3. Endpoint: Adicionar um novo país
@app.post("/country/{country_name}")
def add_country(country_name: str, country: Country):
    countries = load_countries()
    for existing_country in countries:
        if existing_country["country_name"].lower() == country_name.lower():
            raise HTTPException(
                status_code=400, detail="País já existe"
            )
    # Criar o novo país
    new_country = {
        "country_name": country_name,
        "capital": country.capital,
        "population": country.population,
        "continent": country.continent,
    }
    countries.append(new_country)
    save_countries(countries)
    return {"message": "País adicionado com sucesso!", "country_name": country_name}
