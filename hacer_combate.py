import numpy as np
import pandas as pd
import random
from tqdm import tqdm
from fun_crear_pokemon import lista_pokemones, pokediccionario, df_to_dictionary
from fun_principal import crear_primera_gen, contrincantes_ronda
from utils.team import Team
from utils.pokemon import Pokemon
from utils.combat import __fight__, get_winner

pokemon_df = pd.read_csv('data/pokemons.csv')
moves_df = pd.read_csv('data/moves.csv')
effectivenes_df = pd.read_csv('data/effectiveness_chart.csv')

dicc_de_pokemones = pokediccionario(pokemon_df, moves_df)

lista_de_pokemones = lista_pokemones(dicc_de_pokemones)

dicc_effectiveness = df_to_dictionary(effectivenes_df)

def aptitud_del_equipo(equipo_actual: object, lista_contrincantes: list, dicc_effectiveness: dict)->float:
    '''
    Simula la batalla entre el pokemon que se le da y todos los equipos en lista_contrincantes
    El resultado es el promedio de batallas ganadas que tuvo el equipo en cuestion.
    Argumentos:
        equipo_actual: el equipo del cual se calcula la aptitud como objeto Team
        lista_contrincantes: la lista con los contrincantes como objetos Team
        dicc_effectiveness: diccionario con la efectividad que tiene cada ataque con cada tipo.
    Devuelve:
        float con el promedio de batallas ganadas que tiene el equipo, lo que representa su aptitud
    '''
    victorias = 0
    for i in lista_contrincantes:
        ganador = get_winner(equipo_actual, i, dicc_effectiveness)
        if ganador == equipo_actual:
            victorias += 1
    aptitud = victorias / 400
    return aptitud

def dicc_apt(lista_de_equipos: list, lista_contrincantes: list, dicc_effectiveness: dict) -> dict:
    '''
    Crea un diccionario de aptitudes a partir la funcion "aptitud_del_equipo"
    Argumentos:
        lista_de_equipos: lista a recorrer para llenar el diccionario con aptitudes de cada equipo
        lista_contrincantes: parametro usado por aptitud_del_equipo
        dicc_effectiveness: parametro usado por aptitud_del_equipo
    Devuelve:
        diccionario con los nombres de los equipos como clave, y la aptitud y el objeto equipo como valor 
    '''
    dic={}
    for equipo in tqdm(range(len(lista_de_equipos)), desc='Calculating', unit=' iteration', colour='Yellow'):
        dic[lista_de_equipos[equipo].name]={'aptitud':aptitud_del_equipo(lista_de_equipos[equipo], lista_contrincantes, dicc_effectiveness), 'eq_obj': lista_de_equipos[equipo]}
    return dic


def add_probabilidad(dic_poke_y_apt: dict):
    '''
    Toma el diccionario con los nombres de los equipos y les agrega una probabilidad de ser elegidos como padres.
    Argumentos:
        dic_poke_y_apt: diccionario con los nombres de los equipos como clave y valor diccionario {'aptitud':float, 'obj':objeto del equipo}
    Devuelve:
        El diccionario que se le paso como argumento con la clave de probability agregada para cada equipo.
    '''
    #Para hacer la probabilidad, normalizo las aptitudes para que entre todas sumen 1 (100%)
    #La probabilidad que tengan depende de su aptitud, porque se calcula como aptitud / suma total de aptitudes
    apt_total = 0
    for equipo in dic_poke_y_apt:
        apt_total += dic_poke_y_apt[equipo]['aptitud']
    for equipo in dic_poke_y_apt:
        dic_poke_y_apt[equipo]['probability'] = dic_poke_y_apt[equipo]['aptitud'] / apt_total
    return dic_poke_y_apt

def select_equipos_padres(lista_de_equipos, lista_de_probabilidades)-> list:
    '''
    Elije dos padres (distintos) segun sus probabilidades asignadas.
    Argumentos:
        lista_de_equipos : lista con los nombres de todos los equipos
        lista_de_probabilidades : lista con las probabilidades que tiene cada equipo de ser elegido como padre.
                                IMPORTANTE las listas estan en el orden que corresponden, el primer valor de probabilidades es el 
                                correspondiente al primer equipo y asi sucesivamente
    Devuelve:
        lista con los nombres de los equipos seleccionados como padres
    '''
    #choices toma: una lista de la que selecciona  el resultado, una lista con los weights (probabilidades) que le corresponden 
    #a cada elemento de la primera y la cantidad de selecciones que debe hacer (k)
    padres_elegidos = random.choices(lista_de_equipos, lista_de_probabilidades, k=2)
    #si estan repetidos vuelve a elegir
    while padres_elegidos[0] == padres_elegidos[1]:
        padres_elegidos = random.choices(lista_de_equipos, lista_de_probabilidades, k=2)
    return padres_elegidos

def get_total_stats(pokemon)->int: 
    """
    Suma todas las estadisticas que queremos del pokemon
    Devuelve:
    int: Suma de estadisticas.
    """
    return pokemon.max_hp + pokemon.attack + pokemon.defense + pokemon.sp_attack + pokemon.sp_defense + pokemon.speed

def cruces(equipo_1, equipo_2, lista_pokemones, pokedex) -> tuple[list, int]:
    '''
    Esta funcion agarra dos equipos y los cruza, pokemon por pokemon y el que tiene mas estadisticas en total
    se agrega a un nuevo equipo formado por pokemones mas fuertes, asi con todos
    Argumentos:
        equipo_1, equipo_2: dos equipos que se cruzan y una lista_pokemones
    Devuelve: 
        lista_hijos: Una lista con objetos pokemon
    '''
    lista_hijos=[]
    print('')
    print('Cruces:')
    for i in range(len(equipo_1.pokemons)):
        mute=random.random()

        print(f"cruce {i+1} - mute: {'si' if mute<0.03 else 'no'}")

        if mute>0.03:
            stats1 = get_total_stats(equipo_1.pokemons[i])
            stats2 = get_total_stats(equipo_2.pokemons[i])
            if stats1 > stats2:
                if equipo_1.pokemons[i].name not in lista_hijos:
                    lista_hijos.append(equipo_1.pokemons[i].name)
                else:
                    lista_hijos.append(equipo_2.pokemons[i].name)
            else: 
                if equipo_2.pokemons[i].name not in lista_hijos:
                    lista_hijos.append(equipo_2.pokemons[i].name)
                else:
                    lista_hijos.append(equipo_1.pokemons[i].name)
        else:
            while True:
                hijo = random.choice(lista_pokemones)
                if hijo not in lista_hijos and hijo.is_legendary==False:
                    lista_hijos.append(hijo.name)
                    break   
    
    for i in range(len(lista_hijos)):
        '''reemplaza el nombre en la lista_hijos por el objeto del pokemon que le corresponde
        Para hacerlo toma (del diccionario con pokemones y su data) el pokedex number del pokemon
        y reemplaza con el objeto en el indice de la lista de pokemones como objeto. 
        '''
        lista_hijos[i]=lista_de_pokemones[pokedex[lista_hijos[i]]['data']['pokedex_number']-1]
    
    print('')
    print('hijo:')
    for j in lista_hijos:
        print(j.name)

    starter_1 = equipo_1.current_pokemon_index
    starter_2 = equipo_2.current_pokemon_index
    if equipo_1.pokemons[starter_1] == lista_hijos[starter_1]:
        starter_nuevo=starter_1
    else:
        starter_nuevo=starter_2
    return lista_hijos, starter_nuevo
