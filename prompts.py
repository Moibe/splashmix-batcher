import data.data as data, data.data_girls as data_girls, data.data_heroes as data_heroes
import time
import random

class Prompt:
    def __init__(self, style=None):

        self.style = style or random.choice(data.lista_estilos)
        
        

class Superhero(Prompt):
    def __init__(self,
                 subject=None, 
                 ):
        super().__init__()  # Call the parent class constructor
        #Se especifica cuál es su databank:
        databank = data_heroes
        self.subject = subject or random.choice(databank.lista_subjects)
        print("El heroe será: ", self.subject)
                
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
        databank = data_girls
        
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

        print(f"**Character Description:**")
        print(f"- Style: {self.style}")
        print(f"- Adjective: {self.adjective}")
        print(f"- Type of girl: {self.type_girl}")
        print(f"- Hair style: {self.hair_style}")
        print(f"- Boobs: {self.boobs}")
        print(f"- Wardrobe top: {self.wardrobe_top}")
        print(f"- Wardrobe accessories: {self.wardrobe_accesories}")
        print(f"- Wardrobe bottom: {self.wardrobe_bottom}")
        print(f"- Wardrobe shoes: {self.wardrobe_shoes}")
        print(f"- Situation: {self.situacion}")
        print(f"- Place: {self.place}")
        print(f"- Complemento: {self.complemento}")

       