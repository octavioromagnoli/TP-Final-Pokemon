import pandas as pd 
import numpy as np
from utils.pokemon import Pokemon

def create_pokemon_data(pokemon_df, nombre_pokemon: str) -> dict:
    '''
    Crea una diccionario con las caracteristicas de cada Pokemon.
    IMPORTANTE: si un pokemon no tiene un dato rellena con un 0, 
    los pokemones de un solo tipo van a tener type2 = ''
    los pokemones sin moves tienen una lista vacia en esa posicion
    Argumentos:
        pokemon_df: Dataframe de pandas
            Dataframe con toda la data de los pokemons.
        nombre_pokemon: str
            Nombre del pokemon del que se quiere crear el diccionario de data
    Devuelve: 
        diccionario con 
        key (nombre del Pokemon) 
        value (diccionario con la data y sin el nombre)
            Ese diccionario tiene los tipos de dato como key y el valor correspondiente a ese tipo de dato
    '''
    #Agarra la fila del dataframe que tiene el nombre especificado
    data_poke = pokemon_df.loc[pokemon_df['name'] == nombre_pokemon]
    data_poke.pop('name')
    pokemon_dicc = data_poke.to_dict('records')[0]
    
    #Chequeo que si hay algun valor vacio y si lo hay reemplazo por 0
    for atribute, value in pokemon_dicc.items():
        #isinstance chequea que sea un float, el valor nan que da numpy es de tipo float
        #si el isinstance no esta, np.isnan trata de leer valores de tipo no float y da error
        if isinstance(value, float) and np.isnan(value): 
            pokemon_dicc[atribute] = 0

    if pokemon_dicc['moves'] != 0:
        pokemon_dicc['moves'] = pokemon_dicc["moves"].split(';')
    else:
        pokemon_dicc['moves'] = []

    if pokemon_dicc['type2'] == 0:
        pokemon_dicc['type2'] = ''

    pokemon_dicc['is_legendary']=bool(pokemon_dicc['is_legendary'])

    return pokemon_dicc

def lista_de_nombres(pokemon_df) -> list:
    """
    Toma el dataframe de pokemons y devuelve una lista con todos
    los nombres.
    Argumentos:
        pokemon_df : Dataframe de pandas con los pokemones y su data
    Devuelve:
        Lista con los nombres
    """
    nombre_columna = 'name'
    lista_nombres = pokemon_df[nombre_columna].tolist()
    return lista_nombres

def df_to_dictionary(file) -> dict:
    """
    Crea diccionarios a partir de un DataFrame.
    Nos sirve para los diccionarios de movimientos y efectividad.
    Esta funcion toma un DataFrame y crea un diccionario donde 
    cada clave es el valor de la primera columna del DataFrame
    cada valor es un diccionario que contiene las demas columnas y sus correspondientes valores para esa fila.

    Argumentos:
        file (pd.DataFrame): Un DataFrame que contiene los datos de los que se 
            crearan los diccionarios. La primera columna se 
            utiliza como clave en el diccionario resultante y 
            las demas columnas como valores.

    Devuelve:
        dict: Un diccionario donde cada clave es un valor de la primera columna 
              del DataFrame y cada valor es un diccionario que contiene las 
              demas columnas y sus correspondientes valores para esa fila.
    """
    dic={}
    for i,j in zip(file[file.columns[0]],range(len(file))): #i -> cada elemento de la primer columna, j -> de 0 a len
        #key: nombre, value: agarra la fila j+1 y todas las columnas excepto name y lo hace una lista con un diccionario
        dic[i]=file.iloc[j:j+1,1:].to_dict('records')[0] #el cero agarra el unico elemnto de la lista
    return dic

def pokediccionario(pokemon_df, moves_df) -> dict:
    """
    Crea un diccionario con datos y movimientos de Pokemones.

    Esta funcion genera un diccionario donde cada clave es el nombre de un 
    Pokemon y su valor es otro diccionario con dos claves: 'data' y 'moves'. 
    La clave 'data' contiene informacion especifica del Pokemon obtenida del 
    DataFrame `pokemon_df` y la clave 'moves' contiene un diccionario de los 
    movimientos del Pokemon obtenidos del DataFrame `moves_df`.

    Argumentos:
        pokemon_df (pd.DataFrame): Un DataFrame que contiene datos de los 
                Pokemones. Se espera que tenga una columna 
                'name' con los nombres de los Pokemones.
        moves_df (pd.DataFrame): Un DataFrame que contiene datos de los 
                movimientos de los Pokemones.

    Devuelve:
        dict: Un diccionario donde cada clave es el nombre de un Pokemon y su 
              valor es otro diccionario con dos claves: 'data' y 'moves'. 'data' 
              contiene los datos del Pokemon y 'moves' contiene un diccionario 
              de los movimientos del Pokemon.
    """
    lista_nombres=lista_de_nombres(pokemon_df)
    poke_diccionario = {}
    poke_moves = df_to_dictionary(moves_df)#Esta funcion todavia no esta
    for poke_nombre in lista_nombres:
        poke_data = create_pokemon_data(pokemon_df, poke_nombre)
        poke_diccionario[poke_nombre] = {'data': poke_data, 'moves': {i:poke_moves[i] for i in poke_data['moves']}} #en  moves va la funcion que falta
    return poke_diccionario

def lista_pokemones(dicc_de_pokemones: dict) -> list[Pokemon]:
    '''
    Crea una lista con todos los pokemones como objetos.
    Esta funcion toma un diccionario que contiene informacion sobre diferentes pokemones y
    crea una lista de objetos de la clase `Pokemon` a partir de dicha informacion. Cada entrada
    en el diccionario representa un pokemon con sus datos y movimientos correspondientes.
    Argumentos:
        dicc_de_pokemones (dict): Un diccionario donde las claves son los nombres de los pokemones y
                                  los valores son otros diccionarios con dos claves:
                                  - 'data': Informacion del pokemon (p.ej. estadisticas, tipo).
                                  - 'moves': Lista de movimientos que el pokemon puede aprender.
    Devuelve:
        list[Pokemon]: Una lista de objetos `Pokemon` creados a partir de la informacion del diccionario.
    '''
    lista_de_pokemones = []
    for nombre in dicc_de_pokemones:
        #Crea un pokemon y lo mete en la lista de pokemones
        poke=Pokemon.from_dict(nombre, dicc_de_pokemones[nombre]['data'], dicc_de_pokemones[nombre]['moves'])
        lista_de_pokemones.append(poke)
    return lista_de_pokemones
