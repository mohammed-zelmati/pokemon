
import json
import os

class Pokedex:
    def __init__(self, file_path='pokedex.json'):
        self.file_path = file_path
        self.pokemon_data = self.load_pokedex()

    def load_pokedex(self):
        if not os.path.exists(self.file_path):
            # Crée un fichier vide avec un objet JSON vide
            with open(self.file_path, 'w') as file:
                json.dump({}, file)
            return {}
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            # Si le fichier est corrompu, retourne un dictionnaire vide
            return {}

    def save_pokedex(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.pokemon_data, file, indent=4)

    def add_pokemon(self, pokemon):
        if pokemon.name not in self.pokemon_data:
            self.pokemon_data[pokemon.name] = {
                'types': pokemon.types,
                'health': pokemon.health,
                'attack': pokemon.attack,
                'defense': pokemon.defense,
                'level': pokemon.level
            }
            self.save_pokedex()

    def display_pokedex(self):
        return self.pokemon_data
