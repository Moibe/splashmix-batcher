from prompts import Hotgirl
import time

def obten(dataframe, indice, atributo):

    print("Entre a obten a secas, que es de donde sacamos del excel...")
    print(f"Para calcular usaré el índice: {indice}, y el atributo {atributo}...")
        
    valor = dataframe.loc[indice[0], atributo]
    print("Y éste es el valor que obtuve: ", valor)
    

    return valor

def obtenAtributosObjeto(sample_objeto): 

    atributos = []

    for nombre_atributo in dir(sample_objeto):
        if not nombre_atributo.startswith("__"):
            atributos.append(nombre_atributo)

    print("Lista de atributos:", atributos)

    return atributos


def creaPrompt(dataframe, indice):
    #PROMPT para CHICA
    #Prompt es la frase que ordena a los atributos que ya tenemos.

    sample_objeto = Hotgirl()

    atributos = obtenAtributosObjeto(sample_objeto)

    contenedor = {}

    for atributo in atributos:
        print("Entramos al for de atributos...")
        contenedor[atributo] = obten(dataframe, indice, atributo)
        print("Lo recién impreso es: ", contenedor[atributo])
        
    #Al final agrega el shot porque siempre lo traerá.
    contenedor['shot'] = obten(dataframe, indice, 'Shot')

    print("Terminó el for de atributos...")
    time.sleep(3)
    print("Y esto es el contendio de contenedor: ", contenedor)
    time.sleep(5)
    
    return contenedor

if __name__ == "__main__":
    creaPrompt()

   

    # prompt = f"A {} 
    #         of a {creacion.adjective} 
    #         {creacion.type_girl} 
    #         {creacion.subject} with 
    #         {creacion.boobs} and 
    #         {creacion.hair_style} 
    #         wearing 
    #         {creacion.wardrobe_top}, 
    #         {creacion.wardrobe_accesories}, 
    #         {creacion.wardrobe_bottom}, 
    #         {creacion.wardrobe_shoes}, 
    #         {creacion.situacion} 
    #         at {creacion.place} 
    #         {creacion.complemento}"           





    #PROMPT PARA HEROE
    # prompt = f"A {creacion.style} of a superhero like {creacion.subject} " #agregar otros atributos random aquí posteriormente.
