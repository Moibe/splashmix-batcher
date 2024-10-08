import pandas as pd

# Leer el archivo Excel
df = pd.read_excel('trimmable.xlsx')

# Eliminar las columnas
columnas_a_eliminar = ['Source Path', 'Name', 'File', 'File Path', 'style', 'subject', 'Shot']
df.drop(columnas_a_eliminar, axis=1, inplace=True)

# Guardar el DataFrame en un nuevo archivo Excel
df.to_excel('trimado.xlsx', index=False)