import random
import tools
import configuracion.globales as globales
import data.data as data, data.data_girls as data_girls, data.data_heroes as data_heroes


class Prompt:
    #Future, que el databank se defina arriba para todos.
    def __init__(self, style=None):
        databank = data_heroes
        self.style = style or random.choice(databank.lista_estilos)
        print("El estilo fué: ", self.style)       

#Aplica la función randomNull para aquellos valores de una lista en donde deseas que también exista la posibilidad...
#...de que no regrese nada.

class Superhero(Prompt):
    def __init__(self,
                 subject=None, 
                 ):
        super().__init__()  # Call the parent class constructor
        #Se especifica cuál es su databank:
        #IMPORTANTE: Databank son las variables que rellenan los atributos de cada objeto, al gusto de un cliente en específico.
        #Por ejemplo, el objeto es heroes, pero el cliente en particular es RevGenLabs, que tiene su propio databank ...
        #...crafted a su gusto.
        databank = globales.databank_heroes
        #Random null es una función que regresa al sujeto pero también puede no regresar nada, añadir q probabilidades...
        #de que eso suceda se desean.
        self.subject = subject or tools.randomNull(0.2, databank.lista_subjects)
        print("El heroe fué: ", self.subject)
                
class Hotgirl(Prompt):
    def __init__(self,
                 style=None,
                 subject=None,
                 adjective=None,
                 type_girl=None,
                 hair_style=None,
                 boobs=None,
                 wardrobe_top=None,
                 wardrobe_accesories=None,
                 wardrobe_bottom=None,
                 wardrobe_shoes=None,
                 situacion=None,
                 place=None,
                 complemento=None,
                 ):
        super().__init__(style)  # Call the parent class constructor

        #Se especifica cuál es su databank:
        databank = globales.databank_girls
        
        self.subject = subject or random.choice(databank.lista_subjects)
        self.adjective = adjective or random.choice(databank.lista_adjective)
        self.type_girl = type_girl or random.choice(databank.lista_type_girl)
        self.hair_style = hair_style or random.choice(databank.lista_hair_style)
        self.boobs = boobs or random.choice(databank.lista_boobs)
        self.wardrobe_top = wardrobe_top or random.choice(data_girls.lista_wardrobe_top)
        self.wardrobe_accesories = wardrobe_accesories or random.choice(databank.lista_wardrobe_accesories)
        self.wardrobe_bottom = wardrobe_bottom or random.choice(databank.lista_wardrobe_bottom)
        self.wardrobe_shoes = wardrobe_shoes or random.choice(databank.lista_wardrobe_shoes)
        self.situacion = situacion or random.choice(databank.lista_situacion)
        self.place = place or random.choice(databank.lista_place)
        self.complemento = complemento or random.choice(databank.lista_complemento)