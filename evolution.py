from pokemon import Pokemon

class Evolution:
    """Classe gérant les évolutions des Pokémon."""
    
    @staticmethod
    def check_evolution(pokemon: Pokemon):
        """Vérifie si un Pokémon peut évoluer et l'évolue si possible."""
        if pokemon.evolution:  # Vérifie si l'évolution est possible
            return f"{pokemon.name} peut évoluer !"
            Evolution.evolve(pokemon)  # Appelle la méthode d'évolution
        else:
            return f"{pokemon.name} ne peut pas évoluer pour le moment."
    
    @staticmethod
    def evolve(pokemon: Pokemon):
        """Gère l'évolution du Pokémon."""
        if pokemon.level >= 10:  # Exemple : si le niveau est supérieur ou égal à 16, on peut évoluer
            return f"{pokemon.name} évolue maintenant !"
            # Par exemple : on change son type
            if "PLANTE" in pokemon.types:
                pokemon.types.append("THUNDER")
             
            
            # Ou on modifie d'autres attributs
            pokemon.name = f"Super {pokemon.name}"  # Exemple de changement de nom
            pokemon.level = 5  # Réinitialisation du niveau après évolution
        else:
             return f"{pokemon.name} n'est pas prêt à évoluer."
