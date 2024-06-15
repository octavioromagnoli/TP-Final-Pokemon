import matplotlib.pyplot as plt
import pandas as pd

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
        i += 1

    print(epocas)
    print(diversidad)
    plt.plot(epocas, diversidad, color='m')
    plt.xlabel('Epocas')
    plt.ylabel('Diversidad')
    plt.title('Diversidad por epoca')
    plt.show()

diversidad_x_epoca()
