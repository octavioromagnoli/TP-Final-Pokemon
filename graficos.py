import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def diversidad_x_epoca():
    with open('epochs_prueba.csv', 'r') as file:
        epochs = file.readlines()
    epocas = []
    diversidad = []
    for linea in epochs:
        elementos = [elem.strip() for elem in linea.split(',')]
        print(elementos)
        epocas.append(int(elementos[0])) 
        diversidad.append(int(elementos[1]))

    print(epocas)
    print(diversidad)
    plt.plot(epocas, diversidad, color='m')
    plt.xlabel('Epocas')
    plt.ylabel('Diversidad')
    plt.title('Diversidad por epoca')
    plt.show()

diversidad_x_epoca()

def aptitud_x_epoca():
    with open('best_teams.csv', 'r') as file:
        best_teams = file.readlines()
    epocas = []
    aptitud = []
    
    for linea in best_teams[1:]:
        elementos = [elem.strip() for elem in linea.split(',')]
        print(elementos)
        epocas.append(int(elementos[0])) 
        aptitud.append(float(elementos[1]))

    print(epocas)
    print(aptitud)
    plt.plot(epocas, aptitud, color='m')
    plt.xlabel('Epocas')
    plt.ylabel('Aptitud')
    plt.title('Aptitud por epoca')
    plt.show()

aptitud_x_epoca()

def pokemones_ultima_epoca():
    with open('epochs_prueba.csv', 'r') as file:
        epochs = file.readlines()
        ultima_epoca = epochs[-1].strip().split(',')
        cantidad_cada_pokemon = []
        pokemones = []
        for i in range(2, len(ultima_epoca), 2):
            cantidad_cada_pokemon.append(int(ultima_epoca[i+1]))
            pokemones.append(ultima_epoca[i])
        
    print(pokemones)
    print(cantidad_cada_pokemon)
    plt.figure(figsize=(10, 6))  # Tamaño de la figura
    plt.bar(pokemones, cantidad_cada_pokemon, color='m')
    plt.xlabel('Pokemones')
    plt.ylabel('Cantidad')
    plt.title('Distribucion de pokemones en los equipos, en la Última Época')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

pokemones_ultima_epoca()

def estadisticas_mejor_equipo():
    with open('best_teams.csv', 'r') as file:
        best_teams = file.readlines()
        ultima_epoca = best_teams[-1].strip().split(',')[0]
        i = 0
        while best_teams[i].strip().split(',')[0] != ultima_epoca:
            i += 1
        
        equipo = best_teams[i].strip().split(',')[4:10]  
        pokemones = equipo
            
        print("Pokémon del mejor equipo:")
        print(pokemones)
    estadisticas_pokemones = []
    pokemon_df = pd.read_csv('pokemons.csv')
    stats_columns = pokemon_df[['name', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']]
    for pokemon_name in pokemones:
        pokemon_stats = stats_columns[stats_columns['name'] == pokemon_name].values.tolist()
        estadisticas_pokemones.append(pokemon_stats[0][1:])
    print(estadisticas_pokemones)
    
    # Radar chart

    angles = np.linspace(0, 2*np.pi, 6, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    for i, (pokemon_name, stats) in enumerate(zip(pokemones, estadisticas_pokemones)):
        stats += stats[:1]
        ax.plot(angles, stats, label=pokemon_name)
        ax.fill(angles, stats, alpha=0.25)
  
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'])

    plt.title('Radar Chart de Estadísticas de Pokémon')
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.show()
    
estadisticas_mejor_equipo()
