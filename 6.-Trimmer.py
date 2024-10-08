import time
import tools
import pandas as pd
import configuracion.globales as globales
import configuracion.configuracion as configuracion 

excel = globales.excel_results_path + configuracion.sesion + '.xlsx'
#Primero extraemos el dataframe:
dataframe = pd.read_excel(excel)  

# Eliminar las columnas estáticas.
columnas_a_eliminar = ['Source Path', 'Name', 'File', 'File Path']
dataframe.drop(columnas_a_eliminar, axis=1, inplace=True)


#Eliminar las colúmnas dinámicas (las relacionadas al objeto creación).
columna_limite = 'URL'
# Obtener el índice de la columna límite
indice_limite = dataframe.columns.get_loc(columna_limite)

# Crear una lista con los índices de las columnas a eliminar
columnas_a_eliminarv2 = list(range(indice_limite + 1, len(dataframe.columns)))

# Eliminar las columnas
dataframe.drop(dataframe.columns[columnas_a_eliminarv2], axis=1, inplace=True)

# Guardar el DataFrame en un nuevo archivo Excel
tools.df2Excel(dataframe, configuracion.sesion + ' - deliver.xlsx')