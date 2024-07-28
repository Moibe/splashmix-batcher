import postools, configuracion, time
import pandas as pd

filename = configuracion.filename

dataframe = pd.read_excel('results_excel/' + filename)

print(dataframe)