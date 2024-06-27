import pandas as pd
from fun_crear_pokemon import pokediccionario, lista_pokemones, df_to_dictionary
from fun_principal import crear_primera_gen, contrincantes_ronda, equipo_post_cruza
from fun_cruces import dicc_apt, add_probabilidad, select_equipos_padres, cruces, mejor_equipo
from CSVs import epochsCSV, best_teamsCSV
from utils.team import Team
from utils.pokemon import Pokemon
from peleafinal import jugar_jueguito
from graficos import diversidad_x_epoca, aptitud_x_epoca, pokemones_ultima_epoca, estadisticas_mejor_equipo

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

def main():
    print(f'\n ########## SIMULADOR GENETICO POKEMON ##########\n')

    #Se leen las bases de datos como pandas Dataframes
    pokemon_df = pd.read_csv('data/pokemons.csv')
    moves_df = pd.read_csv('data/moves.csv')
    effectivenes_df = pd.read_csv('data/effectiveness_chart.csv')
    
    dicc_effectiveness = df_to_dictionary(effectivenes_df)

    numero_generaciones = int(input('Numero de generaciones a simular: '))

    dicc_de_pokemones = pokediccionario(pokemon_df, moves_df)
    lista_de_pokemones = lista_pokemones(dicc_de_pokemones)

    #Se crea la generacion base de equipos
    primera_gen = crear_primera_gen(lista_de_pokemones)
    gen_actual = primera_gen

    #Estas dos "listas de estadisticas" son para llevar la cuenta de
    gen_quants = [primera_gen[1]]   #diversidad
    all_apts = []                   #aptitudes

    for epoca in range(numero_generaciones-1): #Inicia la simulacion de todas las generaciones
        #Se crea una lista con 400 equipos aleatorios, se actualiza con cada paso de generacion
        conts=contrincantes_ronda(lista_de_pokemones)

        #Se lleva a cabo la simulacion
        gen_actual=simular_generacion(gen_actual[0], conts, dicc_effectiveness, epoca, lista_de_pokemones, all_apts)

        #Se actualizan las "listas de estadisticas" 
        gen_quants.append(gen_actual[1]) #la cantidad de cada pokemon
        all_apts = gen_actual[2] #las aptitudes de los 50 equipos de cada generacion

    #Se generan los 400 equipos contrincantes de la ulitma generacion 
    cont_prueba_final = contrincantes_ronda(lista_de_pokemones)

    #Se testea la ulitma gen y guardamos al equipo con mejor aptitud de toda la generacion
    equipo_definitivo = mejor_equipo(gen_actual[0], cont_prueba_final, dicc_effectiveness, all_apts, numero_generaciones)
    users_team = equipo_definitivo[0]

    #Se añaden las ultimas aptitudes a la "lista de estadisticas"
    all_apts = equipo_definitivo[1]

    print('Equipo del usuario:')
    for i in users_team.pokemons:
        print(f'{i.name}')
    print()
    print(f'Starter: {equipo_definitivo[0].current_pokemon_index}')
    
    #Archivos CSV
    epochsCSV(gen_quants)
    best_teamsCSV(all_apts)

    #Graficos
    deseo_graficos = input("¿Desea ver los graficos para visualizar los resultados? (Si/No) \n")
    if deseo_graficos == 'Si' or deseo_graficos == 'si':
        diversidad_x_epoca()
        aptitud_x_epoca()
        pokemones_ultima_epoca()
        estadisticas_mejor_equipo()

    print(f'\n ########## PELEA FINAL ##########\n')
    
    dicc_campeones = {'Will': ["Bronzong", "Jynx", "Grumpig", "Slowbro", "Gardevoir", "Xatu"],
                    'Koga': ['Skuntank', 'Toxicroak', 'Swalot', 'Venomoth', 'Muk', 'Crobat'],
                    'Bruno': ['Hitmontop', 'Hitmonlee', 'Hariyama', 'Machamp', 'Lucario', 'Hitmonchan'],
                    'Karen': ['Weavile', 'Spiritomb', 'Honchkrow', 'Umbreon', 'Houndoom', 'Absol'],
                    'Lance': ['Salamence', 'Garchomp', 'Dragonite', 'Charizard', 'Altaria', 'Gyarados']}

    #Se elige el campeon que se quiere enfrentar
    while True:
        while True:
            equipo_seleccionado = input("Seleccione el equipo contra el que quiere pelear (Will, Koga, Bruno, Karen o Lance): ")
            if equipo_seleccionado in dicc_campeones.keys():
                break
            else:
                print("Nombre incorrecto, ingrese de nuevo")
        
        #Se define el equipo del campeon seleccionado
        AI_team = Team(equipo_seleccionado, [Pokemon.from_dict(nombre, dicc_de_pokemones[nombre]['data'], dicc_de_pokemones[nombre]['moves']) for nombre in dicc_campeones[equipo_seleccionado]], 0)
        
        #Simulacion de la batalla
        jugar_jueguito(users_team, AI_team, dicc_effectiveness)

        #Se le pregunta al usuario si desea jugar contra otro equipo
        repetir = input('Desea jugar de nuevo? (Si/No)\n')
        if repetir == 'No' or repetir == 'no':
            break
        for pokemon in users_team.pokemons:
            pokemon.current_hp = pokemon.max_hp
        for pokemon in AI_team.pokemons:
            pokemon.current_hp = pokemon.max_hp

if __name__ == '__main__':
    main()