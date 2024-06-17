import matplotlib.pyplot as plt
import pandas as pd
""""
def diversidad_x_epoca():
    with open('epochs_prueba.csv', 'r') as file:
        epochs = file.readlines()

    epocas = []
    diversidad = []
    i = 1
    for linea in epochs:
        elementos = [elem.strip() for elem in linea.split(',')]
        print(elementos)
        epocas.append(int(elementos[0])) 
        diversidad.append(sum(1 for elem in elementos[1:] if not elem.replace('.', '', 1).isdigit()))
        Así deberia ser si no se mostrará la diversidad de cada pokemon en el archivo, 
        lo cual si tiene que devolever solo que no se especifica en el tp.
        
        diversidad.append(int(elementos[1]))
        i += 1

    print(epocas)
    print(diversidad)
    plt.plot(epocas, diversidad, color='m')
    plt.xlabel('Epocas')
    plt.ylabel('Diversidad')
    plt.title('Diversidad por epoca')
    plt.show()

diversidad_x_epoca()
"""
def aptitud_x_epoca():
    with open('best_teams.csv', 'r') as file:
        best_teams = file.readlines()
    epocas = []
    aptitud = []
    i = 1
    for linea in best_teams:
        elementos = [elem.strip() for elem in linea.split(',')]
        print(elementos)
        epocas.append(int(elementos[0])) 
        aptitud.append(float(elementos[1]))
        i += 1

    print(epocas)
    print(aptitud)
    plt.plot(epocas, aptitud, color='m')
    plt.xlabel('Epocas')
    plt.ylabel('Aptitud')
    plt.title('Aptitud por epoca')
    plt.show()

aptitud_x_epoca()