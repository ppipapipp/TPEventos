from datetime import datetime




#COSAS QUE FALTAN
#FECHA ARREGLADA, QUEDA VER SI SE PUEDE CAMBIAR EL WHILE TRUE :) 
#VER SI PODEMOS AGREGAR BUSCAR EVENTO POR NOMBRE DE ARTISTA

#DECLARACIÓN DE VARIABLES

eventos = [
    ["Taylor", "Estadio Nacional", "2025-09-15", "20:00", 50000, 1000, 1000],
    ["Coldplay", "Estadio Nacional", "2023-11-01", "21:00", 60000, 1500, 1500],
    ["Bad_bunny", "Estadio Nacional", "2023-12-01", "22:00", 70000, 2000, 2000]
]

#FUNCIONES

def mostrar_eventos():
    print("\n📋   LISTA DE EVENTOS  ━━━━━━━━━━━━━━━━")
    for i, evento in enumerate(eventos): #SEPARA LA LISTA EN INDICES Y SUS VALORES, OSEA QUE ES UNA TUPLA
        print("%2d. " % (i+1) \
            + "Artista: %-15s " % evento[0] \
            + "Estadio: %-20s " % evento[1] \
            + "Fecha: %-12s " % evento[2] \
            + "Hora: %-5s " % evento[3] \
            + "Precio: $%-8d " % evento[4] \
            + "Entradas disponibles: %-5d" % evento[6])
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

def validar_fecha(): 
    fecha=(input("Ingrese la fecha del evento (YYYY-MM-DD): "))
    while True: 
        if len(fecha) != 10 or fecha[4] != '-' or fecha[7] != '-': #si fecha ej 2006-10-20 la posicion del guion es 4 y 7, y el largo sera 10 
            fecha = input("Error, formato de fecha inválido. Ingrese la fecha en formato YYYY-MM-DD: ") 
            continue 
        anio_str = fecha[:4]
        mes_str = fecha[5:7]
        dia_str = fecha[8:] #slice para tener cada parte de la fecha, en strings 
        if not (anio_str.isdigit() and mes_str.isdigit() and dia_str.isdigit()): 
            fecha = input("Error, formato de fecha inválido. Ingrese la fecha en formato YYYY-MM-DD: ") 
            continue
        anio = int(anio_str) #los pasamos a enteros para poder calcular las fechas
        mes = int(mes_str)
        dia = int(dia_str)
        if mes < 1 or mes > 12: 
            fecha = input("Error, formato de fecha inválido. Ingrese la fecha en formato YYYY-MM-DD: ") 
            continue
        if dia < 1 or dia > 31:
            fecha = input("Error, formato de fecha inválido. Ingrese la fecha en formato YYYY-MM-DD: ") 
            continue

        hoy=datetime.now()
        hoy_str = str(hoy)
        hoy_anio = int(hoy_str[:4]) #volvemos a separar para poder comparar con la fecha de hoy y ya lo pasamos a enteros para hacerlos 
        hoy_mes = int(hoy_str[5:7])
        hoy_dia = int(hoy_str[8:10])

        if anio < hoy_anio or (anio == hoy_anio and mes < hoy_mes) or (anio == hoy_anio and mes == hoy_mes and dia < hoy_dia): 
            fecha = input("Error, esta fecha ya ha pasado. Ingrese una fecha mayor a hoy (YYYY-MM-DD): ") 
            continue
        break 
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
    print("\n🎟️   MENÚ PRINCIPAL  ━━━━━━━━━━━━━━━━━━━")
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
print("━━   SISTEMA DE GESTIÓN DE EVENTOS   ━━")
mostrar_menu()
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
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