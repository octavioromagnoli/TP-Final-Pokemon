import pandas as pd

pokemon_info = pd.read_csv('pokemons.csv')
pokemon_lista = pokemon_info.to_dict('records')
pokemon_dicc = {}
for pokemon in pokemon_lista:
    pokemon_dicc[pokemon['name']] = pokemon

print(pokemon_dicc['Bulbasaur'])

moves_info = pd.read_csv('moves.csv')
moves_lista = moves_info.to_dict('records')
moves_dicc = {}
for moviemiento in moves_lista:
    moves_dicc[moviemiento['name']] = moviemiento

print(moves_dicc['Pound'])

effectivenes_info = pd.read_csv('effectiveness_chart.csv')
effectivenes_lista = effectivenes_info.to_dict('records')
effectivenes_dicc = {}
for atacante in effectivenes_lista:
    effectivenes_dicc[atacante['attacking']] = atacante

print(effectivenes_dicc['water']['ground'])