import pandas as pd
import random
from tqdm import tqdm
from fun_crear_pokemon import lista_pokemones, pokediccionario, df_to_dictionary
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

def dicc_apt(lista_de_equipos: list, lista_contrincantes: list, dicc_effectiveness: dict, epoca: int) -> dict:
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
    for equipo in tqdm(range(len(lista_de_equipos)), desc=f'Simulando generacion {epoca}', unit=' iteration', colour='Yellow'):
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

def select_equipos_padres(lista_de_equipos: list, lista_de_probabilidades: list)-> list:
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

def cruces(equipo_1: Team, equipo_2: Team, lista_pokemones: list[Pokemon], quants: dict) -> tuple[list, int, dict]:
    """
    Realiza el cruce de dos equipos de pokemones para generar una lista con los pokemones resultantes.

    Parametros:
    equipo_1 (Team): Primer equipo de pokemones.
    equipo_2 (Team): Segundo equipo de pokemones.
    lista_pokemones (list[Pokemon]): Lista de todos los pokemones disponibles para posibles mutaciones.
    quants (dict): Diccionario que contiene la cantidad de veces que cada pokemon ha aparecido.

    Retorna:
    tuple: Una tupla que contiene:
        - hijos (list): Lista con los nombres de los pokemones del nuevo equipo.
        - starter_nuevo (int): Starter del equipo resultante.
        - quants (dict): Diccionario actualizado con la cantidad de veces que cada pokemon ha aparecido.
    """
    #Se crean las listas qeu se utilizan para crear a los hijos
    hijos=[] #esta lista sera la que retorne la funcion
    ref_hijos=[] #lista de referencia que se usa para comprobar que no se repitan pokemones

    for i in range(len(equipo_1.pokemons)):
        action=random.random() #Numero aleatorio entre 0 y 1
        
        if action<0.03: #Probabilidad de mutacion: 3%
            while True:
                hijo=random.choice(lista_pokemones) #elige un pokemon al azar y comprueba que no este en la lista  
                if hijo.name not in ref_hijos and hijo.is_legendary==False:    #de referencia y que no sea legendario
                    break
        
        elif action<0.515: #Probabilidad de elegir al pokemon del equipo 1: 48,5%
            hijo=equipo_1.pokemons[i]

            if hijo.name in ref_hijos:      #Si el pokemon del equipo 1 ya esta en la lista
                hijo=equipo_2.pokemons[i]   #cambia el elegido al otro

                if hijo.name in ref_hijos:  #Si se da la muy baja probabilidad de que ambos pokemones ya esten
                    while True:             #se fuerza una mutacion para no repetir
                        hijo=random.choice(lista_pokemones)
                        if hijo.name not in ref_hijos and hijo.is_legendary==False:    
                            break

        else: #Probabilidad de elegir al del equipo 2: 48,5%
            hijo=equipo_2.pokemons[i]

            if hijo.name in ref_hijos:      #Si el pokemon del equipo 2 ya esta en la lista
                hijo=equipo_1.pokemons[i]   #cambia el elegido al otro

                if hijo.name in ref_hijos:  #Si se da la muy baja probabilidad de que ambos pokemones esten
                    while True:             #se fuerza una mutacion para no repetir
                        hijo=random.choice(lista_pokemones)
                        if hijo.name not in ref_hijos and hijo.is_legendary==False:    
                            break

        #Agrega el objeto pokemon a la lista del equipo y su nombre a la lista de referencia
        hijos.append(hijo)
        ref_hijos.append(hijo.name)

        #Se cuenta la cantidad de veces que aparece cada pokemon
        if hijo.name in quants:
            quants[hijo.name]+=1
        else:
            quants[hijo.name]=1

    #elige el starter del nuevo equipo 
    starter_1 = equipo_1.current_pokemon_index
    starter_2 = equipo_2.current_pokemon_index
    if equipo_1.pokemons[starter_1] == hijos[starter_1]:
        starter_nuevo=starter_1
    else:
        starter_nuevo=starter_2
    return hijos, starter_nuevo, quants

def mejor_equipo(lista_equipos, contrincantes, dicc_effectiveness, all_apts, max_epoch):
    '''
    La funcion devuelve el mejor equipo como objeto y actualiza la lista de todas las aptitudes.
    Argumentos:
        lista_equipos: lista con los equipos como objeto Team.
        contrincantes: la lista con los contrincantes como objetos Team.
        dicc_effectiveness: diccionario con la efectividad que tiene cada ataque con cada tipo.
        all_apts: lista con diccionarios que indican la aptitud de cada equipo.
        max_epoch: Numero de epocas que se simularon.
    '''
    diccionario_con_aptitudes = dicc_apt(lista_equipos, contrincantes, dicc_effectiveness, max_epoch)
    all_apts.append(diccionario_con_aptitudes)
    actual = 0
    ganador = ''
    for nombre_equipo in diccionario_con_aptitudes:
        if diccionario_con_aptitudes[nombre_equipo]['aptitud'] > actual:
            ganador = diccionario_con_aptitudes[nombre_equipo]['eq_obj']
    return ganador, all_apts
