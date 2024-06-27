import pandas as pd
from fun_crear_pokemon import pokediccionario, lista_pokemones, df_to_dictionary
from fun_principal import crear_primera_gen, contrincantes_ronda, simular_generacion
from fun_cruces import mejor_equipo
from CSVs import epochsCSV, best_teamsCSV
from utils.team import Team
from utils.pokemon import Pokemon
from fun_peleafinal import jugar_jueguito
from graficos import diversidad_x_epoca, aptitud_x_epoca, pokemones_ultima_epoca, estadisticas_mejor_equipo

def main():
    print(f'\n ########## SIMULADOR GENETICO POKEMON ##########\n')
    print("Si desea visualizar los graficos debe simular al menos 15 generaciones")
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
    if numero_generaciones > 14:
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

        #Se le ofrece al usuario jugar nuevamente
        repetir = input('Desea jugar de nuevo? (Si/No)\n')
        if repetir == 'No' or repetir == 'no':
            break
        for pokemon in users_team.pokemons:
            pokemon.current_hp = pokemon.max_hp
        for pokemon in AI_team.pokemons:
            pokemon.current_hp = pokemon.max_hp

if __name__ == '__main__':
    main()