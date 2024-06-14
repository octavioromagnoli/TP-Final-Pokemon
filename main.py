import numpy as np
import pandas as pd
import random
from fun_crear_pokemon import pokediccionario, lista_pokemones, df_to_dictionary
from fun_principal import crear_primera_gen, contrincantes_ronda, equipo_post_cruza
from hacer_combate import dicc_apt, add_probabilidad, select_equipos_padres, cruces

print('ejecutando')

#Se leen las bases de datos como pandas Dataframes
pokemon_df = pd.read_csv('data/pokemons.csv')
moves_df = pd.read_csv('data/moves.csv')
effectivenes_df = pd.read_csv('data/effectiveness_chart.csv')


dicc_de_pokemones = pokediccionario(pokemon_df, moves_df)
lista_de_pokemones = lista_pokemones(dicc_de_pokemones)
print('hecha lista de pokemones')

#Se crea la generacion base de equipos
primera_gen = crear_primera_gen(lista_de_pokemones)
print('primera gen')
print(primera_gen)
gen_actual = primera_gen

dicc_effectiveness = df_to_dictionary(effectivenes_df)
#print('dic effectiveness')

''' 

def simular_generacion(gen_actual:list, contrincantes_gen:list, dicc_effectiveness: dict, epoca:int) -> list:
    dicc_de_apt=dicc_apt(gen_actual, contrincantes_gen, dicc_effectiveness)
    #print(' dic apt hecho ')
    #print(dicc_de_apt)
    dicc_con_prob = add_probabilidad(dicc_de_apt)
    #print(dicc_con_prob)

    #Se guarda la lista con los nombres de los equipos y la lista con las probabilidades en el mismo orden correspondiente
    #Cada equipo queda alineado con su probabilidad en index
    nombres_de_equipos = list(dicc_con_prob.keys())
    lista_de_probabilidades = []
    for equipo in dicc_con_prob.values():
        lista_de_probabilidades.append(equipo['probability'])

    #Se crea una nueva generacion de 50 pokemons 
    #nueva_generacion es una lista[(lista de pokemones, starter)]
    nueva_generacion = []
    for i in range(50):
        padres = select_equipos_padres(nombres_de_equipos, lista_de_probabilidades)

        papa = dicc_con_prob[padres[0]]['eq_obj']
        mama = dicc_con_prob[padres[1]]['eq_obj']

        hijo = cruces(papa, mama, lista_de_pokemones)
        nueva_generacion.append(hijo)

    #Se formaliza la generacion creando los objetos de cada equipo
    generacion_terminada = []
    for contador, tupla in enumerate(nueva_generacion):

        objeto_equipo = equipo_post_cruza(tupla[0], tupla[1], contador + 1, epoca)
        generacion_terminada.append(objeto_equipo)

    return generacion_terminada


for epoca_actual in range(4):
    #comienza la epoca 0 hasta la 50
    contrincantes_gen = contrincantes_ronda(lista_de_pokemones)
    #print('contrincantes')
    gen_nueva = simular_generacion(gen_actual, contrincantes_gen, dicc_effectiveness, epoca_actual)
    gen_actual = gen_nueva



for i in gen_actual:
    print(f'{i.name}\n {[p for p in i.pokemons]} \n--------------------------\n')'''

contrincantes_gen = contrincantes_ronda(lista_de_pokemones)
dicc_de_apt=dicc_apt(gen_actual, contrincantes_gen, dicc_effectiveness)
#print(' dic apt hecho ')
#print(dicc_de_apt)
dicc_con_prob = add_probabilidad(dicc_de_apt)
#print(dicc_con_prob)

#Se guarda la lista con los nombres de los equipos y la lista con las probabilidades en el mismo orden correspondiente
#Cada equipo queda alineado con su probabilidad en index
nombres_de_equipos = list(dicc_con_prob.keys())
lista_de_probabilidades = []
for equipo in dicc_con_prob.values():
    lista_de_probabilidades.append(equipo['probability'])

#Se crea una nueva generacion de 50 pokemons 
#nueva_generacion es una lista[(lista de pokemones, starter)]
nueva_generacion = []
for i in range(50):
    padres = select_equipos_padres(nombres_de_equipos, lista_de_probabilidades)

    papa = dicc_con_prob[padres[0]]['eq_obj']
    mama = dicc_con_prob[padres[1]]['eq_obj']

    hijo = cruces(papa, mama, lista_de_pokemones)
    nueva_generacion.append(hijo)

#Se formaliza la generacion creando los objetos de cada equipo
generacion_terminada = []
print(f' \n primer equipo de la nueva generacion{nueva_generacion[0][0][0]} \n')
for contador, tupla in enumerate(nueva_generacion):

    objeto_equipo = equipo_post_cruza(tupla[0], tupla[1], contador + 1, 0)
    generacion_terminada.append(objeto_equipo)

for i in generacion_terminada:
    print(f'{i.name}\n')
    lista_print = [p for p in i.pokemons]
    for a, j in enumerate(lista_print):
        print(f'{a+1}. {j.name}')
    print('---------------------------------------')