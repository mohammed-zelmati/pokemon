import json
import random
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P

# Liste des 18 types de Pokémon
POKEMON_TYPES = [
    "normal", "fire", "water", "electric", "grass", "ice",
    "fighting", "poison", "ground", "flying", "psychic",
    "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"
]

class Pokemon:
    def __init__(self, name, types, hp, attack, defense, level=5, evolution=None):
        self.name = name
        self.types = types
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.evolution = evolution  # Nom du Pokémon évolué

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_fainted(self):
        return self.hp <= 0

    def evolve(self):
        if self.evolution:
            print(f"{self.name} évolue en {self.evolution}!")
            self.name = self.evolution
            self.hp += 20
            self.attack += 10
            self.defense += 10
            self.level += 1
            self.evolution = None  # Empêche une double évolution
        else:
            print(f"{self.name} ne peut pas évoluer davantage.")

    def __str__(self):
        return f"{self.name} (Niv. {self.level}) - PV: {self.hp}, ATK: {self.attack}, DEF: {self.defense}, Types: {', '.join(self.types)}"

    @staticmethod
    def from_json(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return [Pokemon(**pokemon) for pokemon in data]

    @staticmethod
    def random_pokemon(file_path):
        pokemon_list = Pokemon.from_json(file_path)
        return random.choice(pokemon_list)
    
    @classmethod
    def load_pokemon_from_ods(cls, file_path):
        # Charge les Pokémon depuis un fichier ODS et renvoie une liste d'objets Pokemon.
        try:
            # Charger le fichier ODS
            doc = load(file_path)

            # Récupérer la première table du fichier ODS
            table = doc.getElementsByType(Table)[0]
            
            pokemon_list = []

            for row in table.getElementsByType(TableRow):
                # Récupérer les cellules de la ligne
                cells = row.getElementsByType(TableCell)
                
                # Assumer que les données sont dans cet ordre : Nom, Type, HP, Attaque, Défense
                if len(cells) >= 5:
                    name = cells[0].firstChild.data.strip()
                    types = cells[1].firstChild.data.strip().split(', ')  # Par exemple "Feu, Vol"
                    hp = int(cells[2].firstChild.data.strip())
                    attack = int(cells[3].firstChild.data.strip())
                    defense = int(cells[4].firstChild.data.strip())
                    
                    # Créer une instance de Pokemon et l'ajouter à la liste
                    pokemon = cls(name, types, hp, attack, defense)
                    pokemon_list.append(pokemon)
            
            return pokemon_list
        
        except Exception as e:
            print(f"Erreur lors du chargement du fichier ODS: {e}")
            return []

