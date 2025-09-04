from datetime import datetime

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
        print(f"{i+1:>3}. "
      f"Artista: {evento[0]:<15} "
      f"Estadio: {evento[1]:<20} "
      f"Fecha: {evento[2]:<12} "
      f"Hora: {evento[3]:<5} "
      f"Precio: ${evento[4]:<8} "
      f"Entradas disponibles: {evento[6]:<5}")
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

def crear_un_evento():
    
    artista = no_es_vacio(input("Ingrese el nombre del artista: "))
    estadio = no_es_vacio(input("Ingrese el nombre del estadio: "))
    fecha = validar_fecha()
    hora = no_es_vacio(input("Ingrese la hora del evento (HH:MM): "))
    precio = validar_numero(input("Ingrese el precio de la entrada: "))
    cantidad = validar_numero(input("Ingrese la cantidad de entradas disponibles: "))

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
    if 0 <= indice < len(eventos):
        eliminado = eventos.pop(indice)
        print(f"Evento eliminado: {eliminado[0]}")
    else:
        print("Índice de evento inválido.")


def vender_entrada(indice, cantidad):
    if 0 <= indice < len(eventos):
        if eventos[indice][6] >= cantidad:
            eventos[indice][6] -= cantidad

            print("Vendidas ", cantidad, " entradas para " , eventos[indice][0])
        else:
            print("No hay suficientes entradas disponibles.")
    else:
        print("Índice de evento inválido.")


def cancelar_entrada(indice, cantidad):
    if 0 <= indice < len(eventos):
        if eventos[indice][6] + cantidad <= eventos[indice][5]:
            eventos[indice][6] += cantidad
            print("Canceladas ", cantidad, " entradas para ", eventos[indice][0])
        else:
            print("No se puede cancelar más entradas de las que existen.")
    else:
        print("Índice de evento inválido.")


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
    today = datetime.today().date()
    fecha = input("Ingrese la fecha del evento (YYYY-MM-DD): ")
    
    while len(fecha)<10 or len(fecha)>10:
            fecha = input("Error, formato de fecha inválido. Ingrese la fecha en formato YYYY-MM-DD: ")
    input_date = datetime.strptime(fecha, "%Y-%m-%d").date()
    while input_date < today:
            fecha = input("Error, esta fecha ya a pasado. Ingrese una fecha mayor a hoy (YYYY-MM-DD): ")
            input_date = datetime.strptime(fecha, "%Y-%m-%d").date() 
            while len(fecha)<10 or len(fecha)>10:
                fecha = input("Error, formato de fecha inválido. Ingrese la fecha en formato YYYY-MM-DD: ")
    return fecha



def no_es_vacio(cadena):
    while True:
        if cadena != "":
            return str(cadena)
        else:
            cadena = input("El valor no puede estar vacío. Ingrese nuevamente: ")

def validar_numero(valor):
    if valor.isnumeric():
        valor = int(valor)
        while valor <= 0: 
            valor = input("El valor debe ser un número positivo. Ingrese nuevamente: ")
            return validar_numero(valor)
        valor = int(valor)
        return valor
    else:
        valor = input("El valor debe ser un número positivo. Ingrese nuevamente: ")
        return validar_numero(valor)


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
        """crear_un_evento()"""
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