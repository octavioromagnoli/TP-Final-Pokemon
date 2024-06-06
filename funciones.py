import numpy as np
import pandas as pd
import random


def is_legendary(pks: pd.DataFrame, pokedex_num:int)->bool:
    '''
    La función recibe un pokemon y chequea que sea legendario.
    Si no lo es devuelve false.
    Argumentos:
        pks : pd.DataFrame
            base de datos con los pokemons.
        pokedex_num : int
            numero de pokedex del pokemon que se quiere chequear si
            es o no legendario.
    Devuelve:
        True si es legendario. False si no es legendario.
    '''
    pokemon = pks[pks['pokedex_number'] == pokedex_num]

    if pokemon['is_legendary'].iloc[0] == 1:
        return True
    return False
