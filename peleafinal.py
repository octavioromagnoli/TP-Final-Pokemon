import pygame
import pandas as pd
from utils.team import Team
from fun_crear_pokemon import pokediccionario, lista_pokemones, df_to_dictionary
from utils.combat import __faint_change__, desmayados

effectivenes_df = pd.read_csv('data/effectiveness_chart.csv')
dicc_effectiveness = df_to_dictionary(effectivenes_df)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("MusicaBatalla.mp3")


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Batalla Pokemon")

bgimage = pygame.image.load("FondoPelea.png")

font = pygame.font.Font(None, 36)

inicial_font = pygame.font.Font(None, 60)




white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
name_color = (1, 5, 48)



def draw_pokemon(pokemon, x, y):
    name_text = font.render(pokemon.name, True, name_color)
    #imprimo el nombre en posicion x y
    screen.blit(name_text, (x, y))

    
    hp_text = font.render(f"HP: {pokemon.current_hp:.0f}/{pokemon.max_hp:.0f}", True, black)
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

def draw_battle(team1, team2, log, muertos1, muertos2):
    #screen.fill((17,65,64))
    screen.blit(bgimage, (0, 0))
    #dibujo ambos pokemones en pantalla
    draw_pokemon(team1.get_current_pokemon(), 50, 50)
    draw_pokemon(team2.get_current_pokemon(), 450, 50)

    log_font = pygame.font.Font(None, 36)
    muertos_font = pygame.font.Font(None, 20)
    log_text = log_font.render(log, True, black)
    muertos1_text = muertos_font.render(f'Derrotados: {str(muertos1)}', True, black)
    muertos2_text = muertos_font.render(f'Derrotados: {str(muertos2)}', True, black)
    screen.blit(log_text, (60, 480))
    screen.blit(muertos1_text, (149, 559))
    screen.blit(muertos2_text, (542, 559))

    pygame.display.flip()

def draw_winner(winner):
    screen.fill((17,65,64))   
    #screen.blit(bgimage, (0, 0))
    winner_font = pygame.font.Font(None, 50) 
    winner_text = winner_font.render(f'Ganador: ¡{winner.name}!', True, white)
    screen.blit(winner_text, (200, 300))
    pygame.display.flip()
    
def batalla_jueguito(team1, team2, effectiveness):
    #clock = pygame.time.Clock()
    running = True
    log_temporal = "Press Enter to Start the Battle!"
    battle_started = False
    advance_turn = False  # Flag to wait for Enter press before each turn
    
    vuelta = 0
    muertos1 = 0
    muertos2 = 0

    inicial_texto = inicial_font.render(f'Presiona Enter para avanzar', True, white)
    screen.blit(inicial_texto, (110, 270))
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not battle_started:
                    battle_started = True
                    screen.fill(black)
                    inicial_texto = inicial_font.render(f'Empieza la batalla!', True, white)
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)  
                    screen.blit(inicial_texto, (110, 270))
                    pygame.display.flip()
                    
                elif event.key == pygame.K_RETURN and battle_started and not advance_turn:
                    advance_turn = True

        
        if battle_started:
            
            
            if advance_turn:
                
                log_temporal = ""
                if vuelta == 0:
                    accion_1, objetivo_1 = team1.get_next_action(team2, effectiveness)
                    accion_2, objetivo_2 = team2.get_next_action(team1, effectiveness)
                    if accion_1 == 'switch':
                        first = team1
                        second = team2
                    elif accion_2 == 'switch':
                        first = team2
                        second = team1
                        accion_1, objetivo_1, accion_2, objetivo_2 = accion_2, objetivo_2, accion_1, objetivo_1
                        # If nobody is switching, the fastest pokemon goes firsts
                    elif team1.get_current_pokemon().speed > team2.get_current_pokemon().speed:
                        first = team1
                        second = team2
                    else:
                        first = team2
                        second = team1
                        accion_1, objetivo_1, accion_2, objetivo_2 = accion_2, objetivo_2, accion_1, objetivo_1
                    draw_battle(team1, team2, log_temporal, muertos1, muertos2)
                    pygame.display.flip()
                    vuelta = 1
                    advance_turn = False
                
                elif vuelta == 1:
                    ataco = 'a'
                    log_temporal = first.accionar_casero(accion_1, objetivo_1, second, effectiveness)
                    if team1.get_current_pokemon().current_hp == 0:
                        vuelta = 2
                        muertos1 += 1
                    elif team2.get_current_pokemon().current_hp == 0:
                        vuelta = 2
                        muertos2 += 1
                    else:
                        vuelta = 3
                    draw_battle(team1, team2, log_temporal, muertos1, muertos2)
                    pygame.display.flip()
                    advance_turn = False
                
                elif vuelta == 2:
                    cambio1, cambio2 = desmayados(team1, team2, effectiveness)
                    log_temporal = cambio1 + cambio2
                    if ataco == 'a':
                        vuelta = 3
                    else:
                        vuelta = 1
                    if not any(pokemon.esta_vivo() for pokemon in team1.pokemons):
                        log_temporal = "Terminó la pelea, Ganó el equipo 2."
                        winner=team2
                        running = False
                
                    if not any(pokemon.esta_vivo() for pokemon in team2.pokemons):
                        log_temporal = "Terminó la pelea, Ganó el equipo 1."
                        winner=team1
                        running = False
                        

                    draw_battle(team1, team2, log_temporal, muertos1, muertos2)
                    pygame.display.flip()
                    advance_turn = False
                
                elif vuelta == 3:
                    ataco = 'b'
                    #Si murio el objetivo cambia de accion
                    if accion_2 == 'attack' and objetivo_2 is None:
                        accion_2, objetivo_2 = second.get_next_action(first, effectiveness)

                    log_temporal = second.accionar_casero(accion_2, objetivo_2, first, effectiveness)

                    if team1.get_current_pokemon().current_hp == 0:
                        muertos1 += 1
                        vuelta = 2
                    elif  team2.get_current_pokemon().current_hp == 0:
                        muertos2 += 1
                        vuelta = 2
                    else: 
                        vuelta = 1
                    draw_battle(team1, team2, log_temporal, muertos1, muertos2)
                    pygame.display.flip()
                    advance_turn = False
    wait=True
    while wait:
        draw_winner(winner)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    wait=False
    
        

pokemon_df = pd.read_csv('data/pokemons.csv')
moves_df = pd.read_csv('data/moves.csv')
pokedex=pokediccionario(pokemon_df, moves_df)
pokemones=lista_pokemones(pokedex)

poks1=['Blaziken','Gastrodon','Gengar','Mightyena','Minior','Tauros']
for i in range(len(poks1)):
    poks1[i]=pokemones[pokedex[poks1[i]]['data']['pokedex_number']-1]
team1=Team('Equipo 1',poks1,0)

poks2=['Skuntank', 'Toxicroak', 'Swalot', 'Venomoth', 'Muk', 'Crobat']
for i in range(len(poks2)):
    poks2[i]=pokemones[pokedex[poks2[i]]['data']['pokedex_number']-1]
team2=Team('Equipo 2',poks2,0)

effectivenes_df = pd.read_csv('data/effectiveness_chart.csv')
dicc_effectiveness = df_to_dictionary(effectivenes_df)

batalla_jueguito(team1, team2, dicc_effectiveness)