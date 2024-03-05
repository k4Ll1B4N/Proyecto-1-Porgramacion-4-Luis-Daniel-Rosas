from api_link_p4 import * 

departamentos = crear_lista_departamentos() 
                                            

                                          
def consulta_nombre(texto):
    if (texto not in departamentos):
        print("Error, el nombre que busca no se encuentra en la base de datos, asegurese de buscar el nombre sin caracteres especiales y/o tildes.")
        return True
        exit()
    else: 
        return False


def comprobacion_limite(numero):
    if ((numero <= 0) or (numero > 1000)):
        print("Error, el numero de registros que quiere buscar no es valido, asegurese de elegir un numero entre 1 y 1000.")
        return True
        exit()
    else: return False  


def ejecutable():

    print("BIENVENIDO AL PROGRAMA DE CONSULTA DE SUELOS EN COLOMBIA")

    nombre = input("Ingrese el nombre del departamento el cualquiera buscar: ").upper()
    limite = input("Ingrese la cantidad de registros que quiera consultar (Por precaucion, el programa tiene un limite maximo de 1000 registros. Recomendamos buscar una cantidad inferior a la mencionada.): ")
    limite = int(limite)

    if ((consulta_nombre(nombre)== False)and(comprobacion_limite(limite)==False)):
        str(limite)
        api(nombre, limite)



