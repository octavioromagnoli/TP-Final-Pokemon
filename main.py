import numpy as np
import pandas as pd
import random
from fun_crear_pokemon import pokediccionario, lista_pokemones, df_to_dictionary
from fun_principal import crear_primera_gen, contrincantes_ronda
from hacer_combate import dicc_apt


pokemon_df = pd.read_csv('data/pokemons.csv')
moves_df = pd.read_csv('data/moves.csv')
effectivenes_df = pd.read_csv('data/effectiveness_chart.csv')

dicc_de_pokemones = pokediccionario(pokemon_df, moves_df)
lista_de_pokemones = lista_pokemones(dicc_de_pokemones)

primera_gen = crear_primera_gen(lista_de_pokemones)
contrincantes_primera_gen = contrincantes_ronda(lista_de_pokemones)
dicc_effectiveness = df_to_dictionary(effectivenes_df)

dicc_de_apt=dicc_apt(primera_gen, contrincantes_primera_gen, dicc_effectiveness)
print(dicc_de_apt)

for i in range(50):
    print(primera_gen[0].pokemons[0].is_legendary)

