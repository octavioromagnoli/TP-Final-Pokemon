import numpy as np
import pandas as pd
import random
from fun_crear_pokemon import lista_pokemones, pokediccionario, df_to_dictionary
from fun_principal import crear_primera_gen, contrincantes_ronda
from utils.team import Team
from utils.combat import __fight__, get_winner

pokemon_df = pd.read_csv('data/pokemons.csv')
moves_df = pd.read_csv('data/moves.csv')
effectivenes_df = pd.read_csv('data/effectiveness_chart.csv')

dicc_de_pokemones = pokediccionario(pokemon_df, moves_df)

lista_de_pokemones = lista_pokemones(dicc_de_pokemones)

dicc_effectiveness = df_to_dictionary(effectivenes_df)


equipos_prueba = []
for i in range(2):
    equipo=[]
    while len(equipo)<6:
        pokemon = random.choice(lista_de_pokemones)
        if pokemon not in equipo:
            equipo.append(pokemon) 
    starter = random.randint(0,5)
    equipos_prueba.append(Team("Team " + str(i + 1), equipo, starter))

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
    for equipo in lista_de_equipos:
        dic[equipo.name]={'aptitud':aptitud_del_equipo(equipo, lista_contrincantes, dicc_effectiveness), 'eq_obj': equipo}
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
        apt_total += equipo['aptitud']
    for equipo in dic_poke_y_apt:
        equipo['probability'] = equipo['aptitud'] / apt_total
    return dic_poke_y_apt
    
#lista_de_equipos = dic_con_prob.keys()
#lista_de_probabilidades = []

personas = ['Octa', 'Luca', 'Mati']
probs = [0.6, 0.3, 0.1]

def select_equipos_padres(lista_de_equipos, lista_de_probabilidades)-> list:
    '''
    '''
    padres_elegidos = random.choices(lista_de_equipos, lista_de_probabilidades, k=2)
    return padres_elegidos
'''
padres = (select_equipos_padres(personas, probs))
print(padres)





def cruce_5050(t1,t2)
    ch=
'''


