#la foto del pokemon que esta en batalla de cada equipo

#movimiento que se hace: ataque/cambio de pokemon
#si es un ataque cual hace y cuanto daño hace


#vida restante de los pokemon que estan peleando

#cuantos pokemon de cada equipo han sido derrotados

#El equipo ganador

import pygame
import pandas as pd
from utils.team import Team
from fun_crear_pokemon import pokediccionario, lista_pokemones, df_to_dictionary
from fun_principal import crear_primera_gen
from utils.combat import __faint_change__, desmayados


'''# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Batalla Pokémon")

# Crear una fuente
font = pygame.font.SysFont(None, 30)

# Crear un mensaje de texto
move = font.render("Pikachu se comio un palito!", True, (0, 0, 0))
dano = font.render("Hizo 37 de daño!", True, (0, 0, 0))


# Obtener el rectángulo del texto
move_rect = move.get_rect(center=(400, 50))
dano_rect = dano.get_rect(center=(400, 100))

#cargar las fotos
fotoA = pygame.image.load("imgs/023.png")
fotoB = pygame.image.load("imgs/132.png")




# Bucle principal del juego
running = True
while running:
    #Cierra la ventana cuando tocas la x
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.ENTER:
            pygame.quit()

    # Lógica de la batalla y actualización de la pantalla
    screen.fill((255, 255, 255))  # Fondo blanco

    screen.blit(move, move_rect)
    screen.blit(dano, dano_rect)
    screen.blit(fotoA, (50, 300))
    screen.blit(fotoB, (600, 300))
    # Aquí iría el código para mostrar los Pokémon, vida, ataques, etc.

    pygame.display.flip()

pygame.quit()
'''


###

'''class Pokemon:
    def __init__(self, name, hp, attack, defense, speed, moves):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.moves = moves
        

    def is_alive(self):
        return self.current_hp > 0'''

'''class Team:
    def __init__(self, pokemons):
        self.pokemons = pokemons
        self.current_pokemon_index = 0

    def get_current_pokemon(self):
        return self.pokemons[self.current_pokemon_index]

    def get_next_action(self, opponent_team, effectiveness):
        # Placeholder logic for getting the next action
        current_pokemon = self.get_current_pokemon()
        return 'attack', current_pokemon.moves[0]'''

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Batalla Pokemon")

# Fonts
font = pygame.font.Font(None, 36)
log_font = pygame.font.Font(None, 18)
# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)


def draw_pokemon(pokemon, x, y):
    name_text = font.render(pokemon.name, True, white)
    #imprimo el nombre en posicion x y
    screen.blit(name_text, (x, y))

    
    hp_text = font.render(f"HP: {pokemon.current_hp:.0f}/{pokemon.max_hp:.0f}", True, white)
    #imprimo el hp alineado con el nombre pero 30 pixeles abajo
    screen.blit(hp_text, (x, y + 30))

    #saco el pokedex number con 0s a izquierda
    numero_con_ceros = str(pokemon.pokedex_number).zfill(3)
    locacion_foto = "imgs/"+numero_con_ceros+".png"
    fotoA = pygame.image.load(locacion_foto)

    screen.blit(fotoA, (x + 30, y + 200))
    #armo la barra de vida
    hp_bar_width = 200
    hp_bar_height = 20
    hp_bar_x = x
    hp_bar_y = y + 60
    #escribo en pantalla el rectangulo rojo tapado con el verde
    pygame.draw.rect(screen, red, (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
    #Actualizo el rectangulo verde segun la current hp en relacion al maximo
    current_hp_width = int(hp_bar_width * (pokemon.current_hp / pokemon.max_hp))
    #Escribo en pantalla el rectangulo verde
    pygame.draw.rect(screen, green, (hp_bar_x, hp_bar_y, current_hp_width, hp_bar_height))

def draw_battle(team1, team2, log):
    screen.fill((17,65,64))
    #dibujo ambos pokemones en pantalla
    draw_pokemon(team1.get_current_pokemon(), 50, 50)
    draw_pokemon(team2.get_current_pokemon(), 450, 50)
    
    log_text = log_font.render(log, True, white)
    screen.blit(log_text, (30, 500))

    pygame.display.flip()

def visualize_battle(team1, team2, effectiveness):
    clock = pygame.time.Clock()
    running = True
    log = "Press Enter to Start the Battle!"
    battle_started = False
    advance_turn = False  # Flag to wait for Enter press before each turn

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not battle_started:
                    battle_started = True
                    log = "Empieza la batalla!"
                elif event.key == pygame.K_RETURN and battle_started and not advance_turn:
                    advance_turn = True


        if battle_started:
            if advance_turn:
                team1_action, team1_move = team1.get_next_action(team2, effectiveness)
                team2_action, team2_move = team2.get_next_action(team1, effectiveness)
                
                # Simulate the turn based on speed or switching
                team1, team2, turn_log = __simulate_turn__(team1, team2, team1_action, team1_move, team2_action, team2_move, effectiveness)
                log = turn_log

                if not any(pokemon.esta_vivo() for pokemon in team1.pokemons):
                    
                    log = "Terminó la pelea, Ganó el equipo 2."
                    # Optionally, you can add logic to restart the game here.
                
                if not any(pokemon.esta_vivo() for pokemon in team2.pokemons):
                
                    
                    log = "Terminó la pelea, Ganó el equipo 1."
                    # Optionally, you can add logic to restart the game here.

                advance_turn = False  # Reset advance_turn flag

            draw_battle(team1, team2, log)
            pygame.display.flip()

        else:
            draw_battle(team1, team2, log)
            pygame.display.flip()

        clock.tick(60)

    pygame.quit()

def __simulate_turn__(team1, team2, team1_action, team1_move, team2_action, team2_move, effectiveness):
    turn_log = ""
    
    if team1_action == 'switch':
        first = team1
        second = team2
    elif team2_action == 'switch':
        first = team2
        second = team1
        team1_action, team1_move, team2_action, team2_move = team2_action, team2_move, team1_action, team1_move
    elif team1.get_current_pokemon().speed > team2.get_current_pokemon().speed:
        first = team1
        second = team2
    else:
        first = team2
        second = team1
        team1_action, team1_move, team2_action, team2_move = team2_action, team2_move, team1_action, team1_move

    turn_log += first.accionar_casero(team1_action, team1_move, second, effectiveness) + " "


    if team1.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
        desmayados(team1, team2, effectiveness)

    '''if team1.get_current_pokemon().current_hp == 0:
        if team1.current_pokemon_index<5:
            turn_log += team1.cambia_sig(team1.current_pokemon_index+1) + " "
        else:
            print('hfjsgukhfjvuyeghdws')
    if team2.get_current_pokemon().current_hp == 0:
        if team2.current_pokemon_index<5:
            turn_log += team2.cambia_sig(team2.current_pokemon_index+1) + " "
        else:
            print('hfjsgukhfjvuyeghdws')'''
    if team1.get_current_pokemon().current_hp > 0 and team2.get_current_pokemon().current_hp > 0:
        turn_log += second.accionar_casero(team2_action, team2_move, first, effectiveness)

    return team1, team2, turn_log


# Example usage

pokemon_df = pd.read_csv('data/pokemons.csv')
moves_df = pd.read_csv('data/moves.csv')
pokedex=pokediccionario(pokemon_df, moves_df)
pokemones=lista_pokemones(pokedex)

poks1=['Blaziken','Gastrodon','Gengar','Mightyena','Minior','Tauros']
for i in range(len(poks1)):
    poks1[i]=pokemones[pokedex[poks1[i]]['data']['pokedex_number']-1]
team1=Team('Equipo 1',poks1,0)
for i in team1.pokemons:
    print(i.name)

poks2=['Bronzong', 'Jynx', 'Grumpig', 'Slowbro', 'Gardevoir', 'Xatu']
for i in range(len(poks2)):
    poks2[i]=pokemones[pokedex[poks2[i]]['data']['pokedex_number']-1]
team2=Team('Equipo 2',poks2,0)
for i in team2.pokemons:
    print(i.name)

effectivenes_df = pd.read_csv('data/effectiveness_chart.csv')
dicc_effectiveness = df_to_dictionary(effectivenes_df)

print("\n\n")

#team1.current_pokemon_index=0
#team2.current_pokemon_index=0


visualize_battle(team1, team2, dicc_effectiveness)
