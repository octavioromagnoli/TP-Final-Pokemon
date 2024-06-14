import numpy as np
import pandas as pd
import random
from utils.team import Team

def crear_primera_gen(lista_de_pokemones: list) -> list:
    '''
    Crea una lista con los equipos de pokemones de la primera generacion.
    Esta funcion toma una lista de objetos `Pokemon` y genera 50 equipos iniciales, cada uno con 6 pokemones.
    Los equipos se crean de manera aleatoria y no tienen pokemones repetidos dentro del mismo equipo. 
    Ademas, se selecciona aleatoriamente un pokemon de cada equipo como el inicial.
    Argumentos:
        lista_de_pokemones (list): Una lista de objetos `Pokemon` a partir de la cual se formaran los equipos.
    Devuelve:
        list: Una lista de objetos `Team`, cada uno representando un equipo de pokemones.
    '''
    equipos_iniciales=[]
    for i in range(50):
        equipo=[]
        while len(equipo)<6:
            pokemon = random.choice(lista_de_pokemones)
            if pokemon not in equipo and pokemon.is_legendary==False:
                equipo.append(pokemon) 
        starter = random.randint(0,5)
        equipos_iniciales.append(Team("Team " + str(i+1), equipo, starter))
    return equipos_iniciales

def contrincantes_ronda(lista_de_pokemones: list) -> list:
    '''
    Esta funcion recibe una lista de pokemones, y los va agregando a equipos(sin legendarios, y sin repetir), hasta
    que estos llegan a una cantidad de 6 pokemones. Elige una posicion del 1 al 5 para decidir quien es el starter
    Esto se repite 400 veces y los equipos generados se agregan a una lista --> equipos_contrincantes[]
    Argumentos:
        list: lista_de_pokemones
    Devuelve:
        list: equipos_contrincantes
    '''
    equipos_contrincantes=[]
    for i in range(400):
        equipo=[]
        while len(equipo)<6:
            pokemon = random.choice(lista_de_pokemones)
            if pokemon not in equipo and pokemon.is_legendary==False:
                equipo.append(pokemon) 
        starter = random.randint(0,5)
        equipos_contrincantes.append(Team("Team " + str(i+1), equipo, starter))
    return equipos_contrincantes

def equipo_post_cruza(equipo_nuevo: list[object], starter: int, contador:int, contador_gen: int)->object:
    equipo_armado = Team("Team E"+str(contador_gen)+" "+ str(contador), equipo_nuevo, starter)
    return equipo_armado