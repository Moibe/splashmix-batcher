import postools, configuracion, time
import pandas as pd



filename = configuracion.filename

dataframe = pd.read_excel('results_excel/' + 'firstBatch.xlsx')

print("Tamaño del dataframe: ", len(dataframe))
time.sleep(5)

# Filter rows where 'Download Status' is 'Success' and 'Diffusion Status' is empty
df_images_ok = dataframe[dataframe['Download Status'] == 'Success'] 
#df_images_ok = dataframe[dataframe['Download Status'] == 'Success']

# Print the filtered DataFrame
print(df_images_ok)
print(len(df_images_ok))


# Filter rows where 'Diffusion Status' is NaN and print them
nan_df = df_images_ok[df_images_ok['Diffusion Status'].isna()]
print(nan_df)
print(len(nan_df))

columna_imagenes = nan_df['File'].to_list()

# Print the columna_imagenes list
print(columna_imagenes)
print(len(columna_imagenes))
