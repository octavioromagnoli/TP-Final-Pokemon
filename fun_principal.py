import numpy as np
import pandas as pd
import random
from utils.team import Team
from fun_cruces import dicc_apt, add_probabilidad, select_equipos_padres, cruces

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
    quants={}
    for i in range(50):
        equipo=[]
        while len(equipo)<6:
            pokemon = random.choice(lista_de_pokemones)
            if pokemon not in equipo and pokemon.is_legendary==False:
                equipo.append(pokemon) 

                #Se cuenta la cantidad de veces que aparece cada pokemon
                if pokemon.name in quants:
                    quants[pokemon.name]+=1
                else:
                    quants[pokemon.name]=1
        
        starter = random.randint(0,5)
        equipos_iniciales.append(Team("Team E0 "+ str(i), equipo, starter))
    return equipos_iniciales, quants

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

def equipo_post_cruza(equipo_nuevo: list[object], starter: int, contador:int, contador_gen: int) -> object:
    """
    Crea un objeto de equipo despues de los cruces.

    Parametros:
    equipo_nuevo (list[object]): Lista de objetos Pokemon del equipo.
    starter (int): Starter del equipo.
    contador (int): Numero del equipo.
    contador_gen (int): Numero de generacion.

    Retorna:
    object: Un objeto de tipo Team que representa el nuevo equipo creado.
    """
    equipo_armado = Team("Team E"+str(contador_gen+1)+" "+ str(contador-1), equipo_nuevo, starter)
    return equipo_armado

def simular_generacion(gen_actual:list, contrincantes_gen:list, dicc_effectiveness: dict, epoca:int, lista_de_pokemones:list, all_apts: list) -> tuple[list, dict, list]:
    """
    Esta funcion simula una nueva generacion y cruza los equipos de la misma para crear los que participaran en la proxima.

    Parametros:
    gen_actual (list): Lista de los 50 equipos de la generacion actual.
    contrincantes_gen (list): Lista de los 400 equipos contrincantes de la generacion actual.
    dicc_effectiveness (dict): Diccionario que contiene la efectividad de los ataques entre tipos de pokemones.
    epoca (int): Numero de la epoca actual.
    lista_de_pokemones (list): Lista con todos los pokemones en tipo objeto pokemon.
    all_apts (list): Lista que contiene las estadisticas de aptitud de todas las generaciones anteriores.

    Retorna:
    tuple: Una tupla que contiene:
        - generacion_terminada (list): Lista de los equipos luego de cruzarlos, para la siguiente generacion.
        - this_quants (dict): Diccionario con la cantidad de cada pokemon que aparece en la generacion.
        - all_apts (list): Lista actualizada que contiene las estadisticas de aptitud de todas las generaciones.
    """
    dicc_de_apt=dicc_apt(gen_actual, contrincantes_gen, dicc_effectiveness, epoca+1)

    #Entra la "lista de estadidticas" de las aptitudes a la funcion
    all_apts.append(dicc_de_apt) #se le agregan las aptitudes de los equipos de esta generacion

    dicc_con_prob = add_probabilidad(dicc_de_apt)

    #Se guarda la lista con los nombres de los equipos y la lista con las probabilidades en el mismo orden correspondiente
    #Cada equipo queda alineado con su probabilidad en index
    nombres_de_equipos = list(dicc_con_prob.keys())
    lista_de_probabilidades = []
    for equipo in dicc_con_prob.values():
        lista_de_probabilidades.append(equipo['probability'])

    #Se crea una nueva generacion de 50 pokemons 
    #nueva_generacion es una lista[(lista de pokemones, starter)]
    nueva_generacion = []
    this_quants = {} #Este diccionario se ira llenando con el numero de pokemones que aparecen
    for i in range(50):
        padres = select_equipos_padres(nombres_de_equipos, lista_de_probabilidades)

        papa = dicc_con_prob[padres[0]]['eq_obj']
        mama = dicc_con_prob[padres[1]]['eq_obj']

        hijo = cruces(papa, mama, lista_de_pokemones, this_quants)
        nueva_generacion.append(hijo[0:2])

        #Se actualiza el diccionario con los 6 pokemones que se agregaron en el cruce
        this_quants = hijo[2]

    #Se formaliza la generacion creando los objetos de cada equipo
    generacion_terminada = []
    for contador, tupla in enumerate(nueva_generacion):

        objeto_equipo = equipo_post_cruza(tupla[0], tupla[1], contador + 1, epoca)
        generacion_terminada.append(objeto_equipo)

    return generacion_terminada, this_quants, all_apts