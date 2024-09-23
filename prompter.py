from objetosCreacion import Hotgirl, Superhero
import time

def obten(dataframe, indice, atributo):

    #print(f"Para calcular usaré el índice: {indice}, y el atributo {atributo}...")
        
    valor = dataframe.loc[indice[0], atributo]
    #print("Y éste es el valor que obtuve: ", valor)
    

    return valor

def obtenAtributosObjeto(sample_objeto): 

    atributos = []

    for nombre_atributo in dir(sample_objeto):
        if not nombre_atributo.startswith("__"):
            atributos.append(nombre_atributo)

    #print("Lista de atributos:", atributos)
    return atributos


def creaContenedorTemplate(dataframe, indice, objeto):
    #PROMPT para CHICA
    #Prompt es la frase que ordena a los atributos que ya tenemos.

    if objeto == "Superhero":
        sample_objeto = Superhero()
    else:
        sample_objeto = Hotgirl()
    

    atributos = obtenAtributosObjeto(sample_objeto)

    contenedor = {}

    for atributo in atributos:
        
        contenedor[atributo] = obten(dataframe, indice, atributo) if isinstance(obten(dataframe, indice, atributo), str) else ""
        # print("Lo recién impreso es: ", contenedor[atributo])
        # print("Y el tipo de lo recién impreso es: ", type(contenedor[atributo]))
                
        
    #Al final agrega el shot porque siempre lo traerá.
    contenedor['shot'] = obten(dataframe, indice, 'Shot')
    
    #print("Y esto es el contendio de contenedor: ", contenedor)    
    
    return contenedor

def creaPrompt(contenedor, creacion):

    print("Entré a crearPrompt....")    

    #FUTURE: Detectar atributos dinámicamente.

    if creacion == "Superhero":
        print("Si entré a Superhero...")
        

        style = contenedor['style'] #if isinstance(contenedor.get('style'), str) else ""
        subject = contenedor['subject'] #if isinstance(contenedor.get('style'), str) else ""  
    
    
        #PROMPT PARA HEROE
        prompt = f"A {style} of a superhero like {subject} " #agregar otros atributos random aquí posteriormente.
   
    
    else:
    
        sample_objeto = Hotgirl()
        
        #Importante El if instance es porque si viene como float nan, lo cambio a texto que sea vacío.
        #Porque si no me parece que deja la palabra nan o lo manifiesta como float, tendríamos que probar.

        style = contenedor['style'] #if isinstance(contenedor.get('style'), str) else ""
        adjective = contenedor['adjective'] #if isinstance(contenedor.get('adjective'), str) else ""
        boobs = contenedor['boobs'] #if isinstance(contenedor.get('style'), str) else ""
        complemento = contenedor['complemento'] #if isinstance(contenedor.get('style'), str) else ""
        hair_style = contenedor['hair_style'] #if isinstance(contenedor.get('style'), str) else ""
        place = contenedor['place'] #if isinstance(contenedor.get('place'), str) else ""
        situacion = contenedor['situacion'] #if isinstance(contenedor.get('style'), str) else ""
        subject = contenedor['subject'] #if isinstance(contenedor.get('style'), str) else ""
        type_girl = contenedor['type_girl'] #if isinstance(contenedor.get('style'), str) else ""
        wardrobe_top = contenedor['wardrobe_top'] #if isinstance(contenedor.get('style'), str) else ""
        wardrobe_accesories = contenedor['wardrobe_accesories'] #if isinstance(contenedor.get('style'), str) else ""
        wardrobe_bottom = contenedor['wardrobe_bottom'] #if isinstance(contenedor.get('style'), str) else ""
        wardrobe_shoes = contenedor['wardrobe_shoes'] #if isinstance(contenedor.get('style'), str) else ""
        
        prompt = f"""A {style} of a {adjective} {type_girl} {subject} with {boobs} and {hair_style} wearing {wardrobe_top}, 
                {wardrobe_accesories}, {wardrobe_bottom}, {wardrobe_shoes}, {situacion} at {place} {complemento}"""   

    return prompt