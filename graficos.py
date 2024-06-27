import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def diversidad_x_epoca():
    """
    Lee el archivo que contiene la cantidad de casda pokemon a lo largo 
    de las 50 generaciones y crea un grafico de linea que muestra la diversidad 
    por cada epoca.

    La funcion realiza lo siguiente:
    1. Lee el archivo CSV y extrae las epocas y la diversidad.
    2. Almacena las epocas y la diversidad en listas separadas.
    3. Genera y muestra un grafico de linea con las epocas en el eje x 
       y la diversidad en el eje y.

    No toma parametros ni retorna ningun valor.
    """
    with open('epochs.csv', 'r') as file:
        epochs = file.readlines()
    epocas = []
    diversidad = []
    for linea in epochs:
        elementos = [elem.strip() for elem in linea.split(',')]
        epocas.append(int(elementos[0])) 
        diversidad.append(int(elementos[1]))

    plt.plot(epocas, diversidad, color='m')
    plt.xlabel('Epocas')
    plt.ylabel('Diversidad')
    plt.title('Diversidad por epoca')
    plt.show()

def aptitud_x_epoca():
    """
    Lee el archivo de los mejores equipos y genera un grafico
    de linea que muestra la aptitud del mejor equipo de cada epoca.

    La funcion realiza lo siguiente:
    1. Lee el archivo CSV y extrae las epocas y la aptitud.
    2. Almacena las epocas y la aptitud en listas separadas.
    3. Genera y muestra un grafico de linea con las epocas en el eje x 
       y la aptitud en el eje y.

    No toma parametros ni retorna ningun valor.
    """
    with open('best_teams.csv', 'r') as file:
        best_teams = file.readlines()
    epocas = []
    aptitud = []
    
    for linea in range(1, len(best_teams), 3):
        elementos = [elem.strip() for elem in best_teams[linea].split(',')]
        epocas.append(int(elementos[0])) 
        aptitud.append(float(elementos[1]))

    plt.plot(epocas, aptitud, color='m')
    plt.xlabel('Epocas')
    plt.ylabel('Aptitud')
    plt.title('Aptitud por epoca')
    plt.show()


def pokemones_ultima_epoca():
    """
    Lee el archivo que contiene la cantidad de casda pokemon a lo largo, 
    de las 50 generaciones y genera un grafico de barras que muestra la 
    distribucion de pokemones en los equipos en la ultima epoca.

    La funcion realiza lo siguiente:
    1. Lee el archivo CSV y extrae la ultima linea que contiene los datos de la ultima epoca.
    2. Extrae y almacena los nombres de los pokemones y su cantidad en listas separadas.
    3. Genera y muestra un grafico de barras con los nombres de los pokemones en el eje x 
       y su cantidad en el eje y.

    No toma parametros ni retorna ningun valor.
    """
    with open('epochs.csv', 'r') as file:
        epochs = file.readlines()
        ultima_epoca = epochs[-1].strip().split(',')
        cantidad_cada_pokemon = []
        pokemones = []
        for i in range(2, len(ultima_epoca), 2):
            cantidad_cada_pokemon.append(int(ultima_epoca[i+1]))
            pokemones.append(ultima_epoca[i])

    plt.figure(figsize=(10, 6))  
    plt.bar(pokemones, cantidad_cada_pokemon, color='m')
    plt.xlabel('Pokemones')
    plt.ylabel('Cantidad')
    plt.title('Distribucion de pokemones en los equipos, en la Última Época')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def estadisticas_mejor_equipo():
    """
    Lee los archivos CSV que contienen los mejores equipos de cada generacion
    y las estadisticas de los pokemones, genera un grafico de radar que muestra
    las estadisticas de los pokemones en el mejor equipo de la ultima epoca.

    La funcion realiza lo siguiente:
    1. Lee el archivo CSV de los mejores equipos y extrae el equipo de la ultima epoca.
    2. Lee el archivo CSV de las estadisticas de los pokemones y extrae las estadisticas de los pokemones del mejor equipo.
    3. Genera y muestra un grafico de radar con las estadisticas de los pokemones del mejor equipo.

    No toma parametros ni retorna ningun valor.
    """
    with open('best_teams.csv', 'r') as file:
        best_teams = file.readlines()
        ultima_epoca = best_teams[-1].strip().split(',')[0]
        i = 0
        while best_teams[i].strip().split(',')[0] != ultima_epoca:
            i += 1
        
        equipo = best_teams[i].strip().split(',')[4:10]  
        pokemones = equipo
            
    estadisticas_pokemones = []
    pokemon_df = pd.read_csv('data/pokemons.csv')
    stats_columns = pokemon_df[['name', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']]
    for pokemon_name in pokemones:
        pokemon_stats = stats_columns[stats_columns['name'] == pokemon_name].values.tolist()
        estadisticas_pokemones.append(pokemon_stats[0][1:])

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

if __name__ == "__main__":
    diversidad_x_epoca()
    aptitud_x_epoca()
    pokemones_ultima_epoca()
    estadisticas_mejor_equipo()
