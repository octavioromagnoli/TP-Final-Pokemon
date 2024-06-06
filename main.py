import numpy as np
import pandas as pd
import random
from funciones import is_legendary

pks = pd.read_csv('data/pokemons.csv')




#144 es pokemon legendario
print(is_legendary(pks, 144))
