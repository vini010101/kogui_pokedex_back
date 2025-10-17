import requests

BASE_URL = "https://pokeapi.co/api/v2/"

def get_pokemon(identifier):
    """Retorna dados de um Pokémon da PokeAPI por ID ou nome"""
    response = requests.get(f"{BASE_URL}pokemon/{identifier}/")
    if response.status_code == 200:
        return response.json()
    return None
