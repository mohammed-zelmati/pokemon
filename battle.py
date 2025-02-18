import random

class Battle:
    TYPE_EFFECTIVENESS = {
        # Exemple d'efficacité des types (à compléter pour les 18 types)
        "fire": {"water": 0.5, "grass": 2, "normal": 1},
        "water": {"fire": 2, "grass": 0.5, "normal": 1},
        "grass": {"fire": 0.5, "water": 2, "normal": 1},
        "normal": {"fire": 1, "water": 1, "grass": 1}
    }

    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2

    def calculate_damage(self, attacker, defender):
        effectiveness = 1
        for attack_type in attacker.types:
            for defense_type in defender.types:
                effectiveness *= self.TYPE_EFFECTIVENESS.get(attack_type, {}).get(defense_type, 1)
        damage = (attacker.attack * effectiveness) - defender.defense
        return max(1, int(damage))  # Au moins 1 point de dégât

    def attack_success(self):
        # 60% de chance de réussir une attaque
        return random.random() < 0.6

    def fight(self):
        while not self.pokemon1.is_fainted() and not self.pokemon2.is_fainted():
            # Pokémon 1 attaque
            if self.attack_success():
                damage = self.calculate_damage(self.pokemon1, self.pokemon2)
                self.pokemon2.take_damage(damage)
                print(f"{self.pokemon1.name} attaque {self.pokemon2.name} pour {damage} dégâts!")
            else:
                print(f"{self.pokemon1.name} a raté son attaque!")

            if self.pokemon2.is_fainted():
                break

            # Pokémon 2 attaque
            if self.attack_success():
                damage = self.calculate_damage(self.pokemon2, self.pokemon1)
                self.pokemon1.take_damage(damage)
                print(f"{self.pokemon2.name} attaque {self.pokemon1.name} pour {damage} dégâts!")
            else:
                print(f"{self.pokemon2.name} a raté son attaque!")

        # Déterminer le gagnant
        winner = self.pokemon1 if self.pokemon2.is_fainted() else self.pokemon2
        print(f"{winner.name} a gagné le combat!")
        return winner