class Persona:
    def __init__(self, nombre, edad,dni):
        self.nombre = nombre
        self.edad = edad 
        self.dni = dni


    
persona1 = Persona("Pedro",25, 12224388)
persona2 = Persona("Juan",30,415986)

print(f"Nombre de persona1: {persona1.nombre}, \nedad:{persona1.edad}, \ndni:{persona1.dni}")
print("\n")
print(f"Nombre de persona2: {persona2.nombre}, \nedad:{persona2.edad}, \ndni:{persona2.dni}")
        