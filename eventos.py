from datetime import datetime




#COSAS QUE FALTAN
#FECHA ARREGLADA, QUEDA VER SI SE PUEDE CAMBIAR EL WHILE TRUE :) 
#VER SI PODEMOS AGREGAR BUSCAR EVENTO POR NOMBRE DE ARTISTA
#NO VALIDAMOS LA HORA
#FALTA DOCUMENTACION

#DECLARACIÓN DE VARIABLES

eventos = [
    ["Taylor", "Estadio Nacional", "2025-09-15", "20:00", 50000, 1000, 1000],
    ["Coldplay", "Estadio Nacional", "2023-11-01", "21:00", 60000, 1500, 1500],
    ["Bad bunny", "Estadio Nacional", "2023-12-01", "22:00", 70000, 2000, 2000]
]

#FUNCIONES

def mostrar_eventos():
    titulo = "\n📋   LISTA DE EVENTOS "
    print(titulo.ljust(40, "━"))
 
    print(f"{'N°':<3} {'Artista':<15} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas':<9}")
    for i, evento in enumerate(eventos): #SEPARA LA LISTA EN INDICES Y SUS VALORES, OSEA QUE ES UNA TUPLA
        print(f"{i+1:<3} {evento[0]:<15} {evento[1]:<20} {evento[2]:<12} {evento[3]:<7} ${evento[4]:<7} {evento[6]:<9}")
    
    if not eventos:
        print("No hay eventos registrados.")

def verificacionindice(indice):
    if 0 <= indice < len(eventos):
        return True
    else:
        print("Índice inválido.")
        return False


def crear_evento(artista, estadio, fecha, hora, precio, cantidad):

    for evento in eventos:
        if evento[0] == artista and evento[2] == fecha:
            print("Error, ya existe un evento con ese artista en esa fecha.")
            return

    nuevo_evento = [artista, estadio, fecha, hora, precio, cantidad, cantidad]
    eventos.append(nuevo_evento)
    print("Evento creado con éxito.")


def modificar_evento(indice, opcion, nuevo_valor):
    if opcion == 5:
        nuevo_valor=int(nuevo_valor)
        diferencia = nuevo_valor - eventos[indice][opcion] #CALCULO LA DIFERENCIA ENTRE LA CANT ANTERIORY ACTUAL DE ENTRADAS
        eventos[indice][opcion] = nuevo_valor #estoy reemplazando el TOTAL DE ENTRADAS
        eventos[indice][opcion+1] += diferencia
    else:
        eventos[indice][opcion] = nuevo_valor


def eliminar_evento(indice):
    verificacionindice(indice)
    eliminado = eventos.pop(indice)
    print("Evento eliminado: ", eliminado[0])



def vender_entrada(indice, cantidad):
    verificacionindice(indice)
    if eventos[indice][6] >= cantidad:
        eventos[indice][6] -= cantidad

        print("Vendidas ", cantidad, " entradas para " , eventos[indice][0])
    else:
        print("No hay suficientes entradas disponibles.")


def cancelar_entrada(indice, cantidad):
    verificacionindice(indice)
    if eventos[indice][6] + cantidad <= eventos[indice][5]:
        eventos[indice][6] += cantidad
        print("Canceladas ", cantidad, " entradas para ", eventos[indice][0])
    else:
        print("No se puede cancelar más entradas de las que existen.")


def ver_entradas_vendidas():
    print("\nEntradas vendidas por evento:")
    for evento in eventos:
        vendidas = evento[5] - evento[6]
        print(evento[0], " -> ", vendidas, " vendidas ", evento[6], "disponibles")


def analisis_datos():
    if not eventos:
        print("No hay eventos registrados.")
        return

    total_vendidas = sum(e[5] - e[6] for e in eventos)
    total_recaudado = sum((e[5] - e[6]) * e[4] for e in eventos)
    promedio = total_vendidas / len(eventos)
    mas_vendido = max(eventos, key=lambda x: x[5] - x[6])

    if total_vendidas == 0:
        print("No se han vendido entradas aún.")
    else:
        print("\nAnálisis de datos:")
        print("Total recaudado: $",total_recaudado, sep="")
        print("Total entradas vendidas:",total_vendidas)
        print(f"Promedio de entradas vendidas por evento: {promedio:.2f}")
        print("Evento más vendido:", mas_vendido[0] ,"(",(mas_vendido[5] - mas_vendido[6]), "entradas vendidas",")")

from datetime import datetime

def validar_fecha():
    fecha = input("Ingrese la fecha del evento (YYYY-MM-DD): ")

    valido = False
    while not valido:
        if len(fecha) == 10 and fecha[4] == '-' and fecha[7] == '-' and fecha[:4].isdigit() and fecha[5:7].isdigit() and fecha[8:].isdigit():

            anio = int(fecha[:4])
            mes = int(fecha[5:7])
            dia = int(fecha[8:])

            if 1 <= mes <= 12 and 1 <= dia <= 31:
                hoy = datetime.now()
                hoy_anio = int(str(hoy)[:4])
                hoy_mes = int(str(hoy)[5:7])
                hoy_dia = int(str(hoy)[8:10])

                if (anio > hoy_anio) or (anio == hoy_anio and mes > hoy_mes) or (anio == hoy_anio and mes == hoy_mes and dia >= hoy_dia):
                    valido = True
                    continue
        fecha = input("Error, formato de fecha inválido o ya pasó. Ingrese nuevamente (YYYY-MM-DD): ")

    return fecha


def no_es_vacio(cadena):
    while cadena == "": 
        cadena = input("El valor no puede estar vacío. Ingrese nuevamente: ")
    return str(cadena)


def validar_numero(valor):
    while not valor.isdigit() or int(valor) <= 0:
        valor = input("El valor debe ser un número positivo. Ingrese nuevamente: ")
    return int(valor)


def mostrar_menu():
    titulo = "\n 🎟️   MENÚ PRINCIPAL  "
    print(titulo.ljust(40, "━"))
    print("1. Mostrar eventos")
    print("2. Crear un evento")
    print("3. Modificar un evento")
    print("4. Eliminar un evento")
    print("5. Vender entrada")
    print("6. Cancelar entrada")
    print("7. Ver entradas vendidas")
    print("8. Análisis de datos")
    print("9. Salir")
    

#PROGRAMA PRINCIPAL

print("\n")

titulo = "  SISTEMA DE GESTIÓN DE EVENTOS  "
print(titulo.center(100, "━"))
mostrar_menu()
print("".ljust(40, "━"))
opcion = validar_numero(input("Elija una opción: "))-1

while opcion != 8:
    
    if opcion == 0:
        mostrar_eventos()

    elif opcion == 1:
        artista = no_es_vacio(input("Ingrese el nombre del artista: "))
        estadio = no_es_vacio(input("Ingrese el nombre del estadio: "))
        fecha = validar_fecha()
        hora = no_es_vacio(input("Ingrese la hora del evento (HH:MM): "))
        precio = validar_numero(input("Ingrese el precio de la entrada: "))
        cantidad = validar_numero(input("Ingrese la cantidad de entradas disponibles: "))
        crear_evento(artista, estadio, fecha, hora, precio, cantidad)

    elif opcion == 2:
        for i, artista in enumerate(eventos):
            print(i+1,". ", artista[0], sep="")
        indice = int(input("Seleccione el evento a modificar: "))-1
        while not verificacionindice(indice):
            indice = int(input("Ingrese un índice válido: "))-1
        print("1. Artista\n2. Estadio\n3. Fecha\n4. Hora\n5. Precio\n6. Cantidad de entradas")
        opcion_mod = int(input("¿Qué desea modificar?: "))-1
        while opcion_mod < 0 or opcion_mod > 5:
            opcion_mod = int(input("Opción inválida. Ingrese una opción válida: "))-1
        if opcion_mod == 2:
            nuevo_valor = validar_fecha()
        else:
            nuevo_valor = no_es_vacio(input("Ingrese el nuevo valor: "))
        modificar_evento(indice, opcion_mod, nuevo_valor)
 

    elif opcion == 3:
        mostrar_eventos()
        indice = int(input("Ingrese el índice del evento a eliminar: "))-1
        while not verificacionindice(indice):
            indice = int(input("Ingrese un índice válido: "))-1
        eliminar_evento(indice)

    elif opcion == 4:
        mostrar_eventos()
        indice = int(input("Ingrese el índice del evento: "))-1
        while not verificacionindice(indice):
            indice = int(input("Ingrese un índice válido: "))-1
        cantidad = int(input("Cantidad de entradas a vender: "))
        vender_entrada(indice, cantidad)

    elif opcion == 5:
        mostrar_eventos()
        indice = int(input("Ingrese el índice del evento: "))-1
        while not verificacionindice(indice):
            indice = int(input("Ingrese un índice válido: "))-1
        cantidad = int(input("Cantidad de entradas a cancelar: "))
        cancelar_entrada(indice, cantidad)

    elif opcion == 6:
        ver_entradas_vendidas()

    elif opcion == 7:
        analisis_datos()

    else:
        print("Opción inválida. Intente nuevamente.")
    
    mostrar_menu()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    opcion = int(input("Elija una opción: "))-1

print("¡Chau!")