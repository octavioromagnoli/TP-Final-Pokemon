from tqdm import tqdm

def epochsCSV(quants: list):
    with open('epochs.csv', 'w') as epochs:
        for generacion in tqdm(range(len(quants)), desc='Creando epochs.csv', unit=' iteration', colour='Green'):
            
            #Pasamos el diccionario a lista para ordenarlos de manera descendiente
            lista=[]
            for pokenombre in quants[generacion]:
                lista.append((quants[generacion][pokenombre],pokenombre))
            lista.sort()
            lista.reverse()

            #Se escribe una linea
            epochs.writelines(f'{generacion},{len(lista)}') #numero de generacion , variedad de pokemones
            epochs.writelines(f',{lista[k][1]},{lista[k][0]}' for k in range(len(lista))) #nombre , cant para cada pokemon
            epochs.write('\n')

def best_teamsCSV(apts: list):
    """
    Crea un archivo CSV con los mejores equipos de cada generacion.

    Parametros:
    apts (list): Lista de diccionarios que contiene las aptitudes y detalles de los equipos por cada generacion.

    El archivo CSV generado tendra el siguiente formato:
    epoch,aptitude,team_name,starter,pokemon_1,pokemon_2,pokemon_3,pokemon_4,pokemon_5,pokemon_6
    """
    with open('best_teams.csv', 'w') as best:
        best.write('epoch,aptitude,team_name,starter,pokemon_1,pokemon_2,pokemon_3,pokemon_4,pokemon_5,pokemon_6\n')
        for generacion in tqdm(range(len(apts)), desc='Creando best_teams.csv', unit=' iteration', colour='Green'):

            #Pasamos el diccionario a lista para ordenarlos de manera descendiente
            lista=[]
            for equipo in apts[generacion]:
                lista.append((apts[generacion][equipo]['aptitud'],equipo))
            lista.sort()
            lista.reverse()
            
            #Se escriben las tres lineas de cada gen
            for top in range(3):
                best.writelines(f'{generacion},{lista[top][0]},{lista[top][1]}') #numero de generacion , aptitud , nombre
                best.writelines(f',{apts[generacion][lista[top][1]]["eq_obj"].current_pokemon_index}') #starter
                best.writelines(f',{apts[generacion][lista[top][1]]["eq_obj"].pokemons[k].name}' for k in range(6)) #pokemones del equipo
                best.write('\n')