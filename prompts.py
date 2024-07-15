import random
import data

class Prompt:
    def __init__(self, style=None, subject=None):
        
        self.style = random.choice(data.lista_estilos)
        self.subject = random.choice(data.lista_subjects)
        self.message = f"A {self.style} of a superhero like {self.subject} "

        print("Style: ", self.style)
        print("Subject: ", self.subject)
        print("Message: ", self.message)

class Superhero(Prompt):
    def __init__(self, logo, affiliation):
        super().__init__()  # Call the parent class constructor
        self.logo = logo
        self.affiliation = affiliation

        print("Logo: ", self.logo)
        print("Affiliation: ", self.affiliation)

class Hotgirl(Prompt):
    def __init__(self, logo=None, affiliation=None):
        super().__init__()  # Call the parent class constructor
        self.logo = logo
        self.affiliation = affiliation
        self.adjective = random.choice(data.lista_estilos)
        self.type_girl = random.choice(data.lista_type_girl)
        self.hair_style = random.choice(data.lista_hair_style)
        self.boobs = random.choice(data.lista_boobs)
        self.wardrobe_top = random.choice(data.lista_wardrobe_top)
        self.wardrobe_accesories = random.choice(data.lista_wardrobe_accesories)
        self.wardrobe_bottom = random.choice(data.lista_wardrobe_bottom)
        self.wardrobe_shoes = random.choice(data.lista_wardrobe_shoes)
        self.situacion = random.choice(data.lista_situacion)
        self.place = random.choice(data.lista_place)
        self.complemento = random.choice(data.lista_complemento)

        print(f"**Character Description:**")
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

       