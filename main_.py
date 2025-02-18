import pygame
import sys
import json
import requests
from pokemon import Pokemon
from battle import Battle
from evolution import Evolution

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokémon Game")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Police de texte
font = pygame.font.Font(None, 28)

# Définir les rectangles pour les boutons
start_button = pygame.Rect(500, 200, 200, 50)
add_pokemon_button = pygame.Rect(500, 300, 200, 50)
pokedex_button = pygame.Rect(500, 400, 200, 50)
exit_button = pygame.Rect(500, 500, 200, 50)

 # Constantes
POKEMON_PER_PAGE = 5
current_page = 0  # Page courante

def draw_text(text, x, y, color=BLACK):
    """Affiche du texte à l'écran."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_menu():
    """Dessine le menu avec les boutons."""
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, start_button)
    pygame.draw.rect(screen, GREEN, add_pokemon_button)
    pygame.draw.rect(screen, GREEN, pokedex_button)
    pygame.draw.rect(screen, RED, exit_button)

    # Ajouter du texte sur les boutons
    draw_text("Start Game", start_button.x + 20, start_button.y + 10)
    draw_text("Add Pokémon", add_pokemon_button.x + 20, add_pokemon_button.y + 10)
    draw_text("View Pokédex", pokedex_button.x + 20, pokedex_button.y + 10)
    draw_text("Exit", exit_button.x + 70, exit_button.y + 10)

    pygame.display.flip()

def load_image(path):
    """Charge une image depuis un fichier."""
    try:
        return pygame.image.load(path).convert_alpha()
    except FileNotFoundError:
        print(f"Image manquante : {path}. Utilisation d'une image par défaut.")
        return pygame.image.load("assets/images/dracaufeu.png").convert_alpha()

def draw_hp_bar(pokemon, x, y):
    """Dessine une barre de vie pour un Pokémon."""
    bar_width = 200
    bar_height = 20
    fill = (pokemon.hp / 100) * bar_width
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(screen, RED, outline_rect)
    pygame.draw.rect(screen, GREEN, fill_rect)

def combat_screen(player_pokemon, opponent_pokemon, draw_menu):
    """Affiche l'écran de combat."""
    player_image = load_image(f"assets/images/{player_pokemon.name.lower()}.png")
    opponent_image = load_image(f"assets/images/{opponent_pokemon.name.lower()}.png")
    player_image = pygame.transform.scale(player_image, (150, 150))
    opponent_image = pygame.transform.scale(opponent_image, (150, 150))

    battle = Battle(player_pokemon, opponent_pokemon)
    messages = []
    winner_message = ""
    running = True

    def draw_pokemon_info(pokemon, x, y):
        draw_text(f"{pokemon.name}", x, y)
        draw_text(f"PtVie: {pokemon.hp}", x, y + 20)
        draw_text(f"ATTACK: {pokemon.attack}", x, y + 40)
        draw_text(f"DEFENSE: {pokemon.defense}", x, y + 60)
        draw_text(f"LEVEL: {pokemon.level}", x, y + 80)

    while running:
        screen.fill(WHITE)
        background1 = pygame.image.load('assets/images/forest.png')
        screen.blit(background1, (0, 0))

        y_offset = 50
        for message in messages[-5:]:
            draw_text(message, 50, y_offset)
            y_offset += 40

        if winner_message:
            draw_text(winner_message, 750, 400, WHITE)

        button_rect = pygame.Rect(510, 500, 210, 50)
        pygame.draw.rect(screen, (0, 128, 0), button_rect)
        draw_text("Retour au menu", button_rect.x + 50, button_rect.y + 10, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    draw_menu()
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not player_pokemon.is_fainted() and not opponent_pokemon.is_fainted():
                        if battle.attack_success():
                            damage = battle.calculate_damage(player_pokemon, opponent_pokemon)
                            opponent_pokemon.take_damage(damage)
                            messages.append(f"{player_pokemon.name} attaque {opponent_pokemon.name} pour {damage} dégâts!")
                        else:
                            messages.append(f"{player_pokemon.name} a raté son attaque!")

                        if opponent_pokemon.is_fainted():
                            winner_message = f"{player_pokemon.name} a gagné!"
                            Evolution.check_evolution(player_pokemon)
                            break

                        if battle.attack_success():
                            damage = battle.calculate_damage(opponent_pokemon, player_pokemon)
                            player_pokemon.take_damage(damage)
                            messages.append(f"{opponent_pokemon.name} attaque {player_pokemon.name} pour {damage} dégâts!")
                        else:
                            messages.append(f"{opponent_pokemon.name} a raté son attaque!")

                        if player_pokemon.is_fainted():
                            winner_message = f"{opponent_pokemon.name} a gagné!"
                            Evolution.check_evolution(opponent_pokemon)
                            break

        screen.blit(player_image, (200, 350))
        screen.blit(opponent_image, (700, 150))
        draw_hp_bar(player_pokemon, 200, 320)
        draw_hp_bar(opponent_pokemon, 700, 120)
        draw_pokemon_info(player_pokemon, 410, 320)
        draw_pokemon_info(opponent_pokemon, 910, 70)
        draw_text("Appuyez sur ESPACE pour attaquer", 10, SCREEN_HEIGHT - 50)
        pygame.display.update()
        pygame.time.Clock().tick(30)

def draw_pokedex(pokemon_list, current_page):
    """Affiche le Pokédex avec tous les Pokémon enregistrés."""
    screen.fill(WHITE)
    draw_text("Pokédex", SCREEN_WIDTH // 2 - 60, 50, BLACK)

    # Vérification de la pagination
    start_idx = current_page * POKEMON_PER_PAGE
    end_idx = start_idx + POKEMON_PER_PAGE
    paginated_pokemon = pokemon_list[start_idx:end_idx]

    if not paginated_pokemon:
        draw_text("Aucun Pokémon à afficher pour cette page", 50, 100, BLACK)
        pygame.display.flip()
        return

    # Afficher les Pokémon dans une liste
    y_offset = 100
    for i, pokemon in enumerate(paginated_pokemon):
        draw_text(f"{start_idx + i + 1}. {pokemon['name']}", 50, y_offset)
        draw_text(f"  Type: {pokemon['types']} | HP: {pokemon['hp']} | ATTACK: {pokemon['attack']} | DEFENSE: {pokemon['defense']}", 200, y_offset)
        y_offset += 40

    # Afficher les boutons de navigation (Précédent / Suivant)
    if current_page > 0:
        prev_button = pygame.Rect(50, SCREEN_HEIGHT - 70, 120, 40)
        pygame.draw.rect(screen, GREEN, prev_button)
        draw_text("Précédent", prev_button.x + 15, prev_button.y + 10)

    if end_idx < len(pokemon_list):
        next_button = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 70, 120, 40)
        pygame.draw.rect(screen, GREEN, next_button)
        draw_text("Suivant", next_button.x + 15, next_button.y + 10)

    # Ajouter une option pour quitter le Pokédex
    draw_text("Appuyez sur ESC pour revenir au menu", 250, SCREEN_HEIGHT - 50)

    pygame.display.flip()  # Mettre à jour l'affichage

def show_pokemon_details(pokemon):
    """Affiche les détails d'un Pokémon sélectionné."""
    screen.fill(WHITE)
    
    # Titre
    draw_text(f"Détails de {pokemon['name']}", SCREEN_WIDTH // 2 - 100, 50, BLACK)

    # Afficher l'image du Pokémon
    image_path = f"assets/images/{pokemon['name'].lower()}.png"
    pokemon_image = load_image(image_path)
    if pokemon_image:
        pokemon_image = pygame.transform.scale(pokemon_image, (200, 200))
        screen.blit(pokemon_image, (SCREEN_WIDTH // 2 - 100, 100))

    # Afficher les détails du Pokémon
    draw_text(f"Nom: {pokemon['name']}", 50, 350)
    draw_text(f"Type: {pokemon['types']}", 50, 400)
    draw_text(f"HP: {pokemon['hp']}", 50, 450)
    draw_text(f"Attaque: {pokemon['attack']}", 50, 500)
    draw_text(f"Défense: {pokemon['defense']}", 50, 550)

    # Bouton pour revenir au Pokédex
    draw_text("Appuyez sur ESC pour revenir au Pokédex", 50, SCREEN_HEIGHT - 50)

    pygame.display.flip()

def pokedex_loop(pokemon_list):
    """Boucle principale pour la navigation dans le Pokédex."""
    global current_page
    pokedex_running = True
    details_mode = False  # Mode détail (True = afficher les détails, False = afficher le Pokédex)
    selected_pokemon = None  # Pokémon sélectionné pour afficher les détails

    while pokedex_running:
        if not details_mode:
            # Afficher le Pokédex
            draw_pokedex(pokemon_list, current_page)
        else:
            # Afficher les détails du Pokémon sélectionné
            show_pokemon_details(selected_pokemon)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not details_mode:
                # Gérer la navigation dans le Pokédex
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Si l'utilisateur clique sur "Précédent"
                    if current_page > 0 and pygame.Rect(50, SCREEN_HEIGHT - 70, 100, 40).collidepoint(mouse_pos):
                        current_page -= 1

                    # Si l'utilisateur clique sur "Suivant"
                    if len(pokemon_list) > (current_page + 1) * POKEMON_PER_PAGE and pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 70, 100, 40).collidepoint(mouse_pos):
                        current_page += 1

                    # Vérifier si l'utilisateur a cliqué sur un Pokémon
                    start_idx = current_page * POKEMON_PER_PAGE
                    end_idx = start_idx + POKEMON_PER_PAGE
                    paginated_pokemon = pokemon_list[start_idx:end_idx]

                    for i, pokemon in enumerate(paginated_pokemon):
                        if 50 <= mouse_pos[0] <= 500 and 100 + i * 40 <= mouse_pos[1] <= 140 + i * 40:
                            selected_pokemon = pokemon  # Sélectionner le Pokémon
                            details_mode = True  # Passer en mode détail

                # Gérer la touche ESC pour revenir au menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pokedex_running = False  # Retourner au menu principal

            else:
                # Gérer les événements en mode détail
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        details_mode = False  # Revenir au Pokédex

        pygame.display.flip()  # Mettre à jour l'affichage

def main():
    running = True
    pokemon_list = []
    active_input = False
    input_text = ""

    # Charger les Pokémon existants
    try:
        with open("pokemon.json", "r") as file:
            pokemon_list = json.load(file)
    except FileNotFoundError:
        pokemon_list = []

    current_page = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if start_button.collidepoint(mouse_pos):
                    player_pokemon = Pokemon.random_pokemon('pokemon.json')
                    max_attempts = 10
                    attempts = 0
                    while attempts < max_attempts:
                        opponent_pokemon = Pokemon.random_pokemon('pokemon.json')
                        if opponent_pokemon.name != player_pokemon.name:
                            break
                        attempts += 1
                    else:
                        print("Impossible de trouver un Pokémon adverse différent.")
                        continue
                    combat_screen(player_pokemon, opponent_pokemon, draw_menu)

                elif add_pokemon_button.collidepoint(mouse_pos):
                    active_input = True

                elif pokedex_button.collidepoint(mouse_pos):
                    pokedex_loop(pokemon_list)  # Appeler la boucle de navigation du Pokédex

                elif exit_button.collidepoint(mouse_pos):
                    running = False

            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_RETURN:
                    # Ajouter un Pokémon (non implémenté ici)
                    active_input = False
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(WHITE)
        draw_menu()

        if active_input:
            draw_text("Entrez le nom du Pokémon:", 10, SCREEN_HEIGHT - 50)
            draw_text(input_text, 10, SCREEN_HEIGHT - 100)

        pygame.display.flip()

if __name__ == "__main__":
    main()