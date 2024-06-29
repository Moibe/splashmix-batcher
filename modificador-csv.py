import time
import csv

with open('resultados.csv', 'r+') as csvfile:
    reader = csv.reader(csvfile)
    dato = list(reader)
    print("imprimiendo dato: ", dato)
   
    for row in dato:
        print(row[0])
        if row[0]=='D5603AQHv4C6s_JvlKw':
            print("Encontrado")
            row[0]="Éxito"
        else:
            print("Sigo buscando")

    
    print("Ahora impresión 2da vuelta...")
    time.sleep(1)
    for row in dato: 
        print(row[0])

    for row in dato:
        writer.writerow([cell.strip() for cell in row])

    csvfile.seek(0)
    writer = csv.writer(csvfile)
    writer.writerows(dato)  # Escribir las filas modificadas