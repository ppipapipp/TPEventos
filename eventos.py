from datetime import datetime
import random

#A HACER: FACTURACION: MAXIMO DE ENTRADAS POR PERSONA Y NUMERO RANDOM DE FACTURA
#HACER DISTINTOS SECTORES: CAMPO, PLATEA, ETC
#TRY-EXCEPT, ARCHIVO EXTERNO PARA GUARDAR DATOS

eventos = [
    ["Taylor", "Estadio Nacional", "2025-09-15", "20:00", 50000, {"total":1000, "disponibles":1000}],
    ["Coldplay", "Estadio Nacional", "2023-11-01", "21:00", 60000, {"total":1500, "disponibles":1500}],
    ["Bad bunny", "Estadio Nacional", "2023-12-01", "22:00", 70000, {"total":2000, "disponibles":2000}],
    ["Taylor the Creator", "Estadio Nacional", "2023-12-01", "22:00", 70000, {"total":2000, "disponibles":2000}]
]


#FUNCIONES

def validar_no_es_vacio(cadena):
    """Valida que la cadena ingresada no esté vacía"""

    while not cadena.isalnum(): 
        try:
            cadena = input("El valor no puede estar vacío. Ingrese nuevamente: ")
        except ValueError:
            print("Error, valor inválido.")
    return cadena

def validar_indice(indice):
    """Valida que el índice ingresado sea válido"""

    indice = validar_no_es_vacio(indice)
    while not indice.isdigit() or int(indice) <= 0 or int(indice) > len(eventos):
        try:
            indice = input("Ingrese un índice válido: ")
        except ValueError:
            print("Error, valor inválido.")
    return int(indice) -1


def validar_fecha(fecha):
    """Valida que la fecha ingresada esté en el formato YYYY-MM-DD y no sea una fecha pasada"""

    fecha = validar_no_es_vacio(fecha)
    valido = False

    hoy = datetime.now()
    hoy_anio = int(str(hoy)[:4])
    hoy_mes = int(str(hoy)[5:7])
    hoy_dia = int(str(hoy)[8:10])

    while not valido:

        if len(fecha) == 10 and fecha[4] == '-' and fecha[7] == '-' and fecha[:4].isdigit() and fecha[5:7].isdigit() and fecha[8:].isdigit():

            anio = int(fecha[:4])
            mes = int(fecha[5:7])
            dia = int(fecha[8:])

            if mes < 1 or mes > 12:
                print("El mes ingresado no es válido.")

            elif mes in [1, 3, 5, 7, 8, 10, 12] and (dia < 1 or dia > 31):
                print("El día no es válido para ese mes.")

            elif mes in [4, 6, 9, 11] and (dia < 1 or dia > 30):
                print("El día no es válido para ese mes.")

            elif mes == 2:
                if (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0):
                    if dia < 1 or dia > 29:
                        print("El día no es válido para febrero en año bisiesto.")
                    else:
                        valido = True
                else:
                    if dia < 1 or dia > 28:
                        print("El día no es válido para febrero.")
                    else:
                        valido = True
            else:
                valido = True

            if valido:
                if (anio < hoy_anio) or (anio == hoy_anio and mes < hoy_mes) or (anio == hoy_anio and mes == hoy_mes and dia < hoy_dia):
                    print("La fecha ingresada ya pasó.")
                    valido = False
                else:
                    return fecha

        else:
            print("El formato no es válido.")

        fecha = input("Ingrese nuevamente (YYYY-MM-DD): ")

    return fecha



def validar_numero(valor):
    """Valida que el valor ingresado sea un número positivo"""

    valor = validar_no_es_vacio(valor)
    while not valor.isdigit() or int(valor) <= 0:
        valor = input("El valor debe ser un número positivo. Ingrese nuevamente: ")
    return int(valor)

def validar_hora(hora):
    """Valida que la hora ingresada esté en el formato HH:MM y sea una hora válida"""

    hora = validar_no_es_vacio(hora)
    valido = False
    while not valido:
        if len(hora) == 5 and hora[2] == ':' and hora[:2].isdigit() and hora[3:].isdigit():
            horas = int(hora[:2])
            minutos = int(hora[3:])
            if 0 <= horas < 24 and 0 <= minutos < 60:
                valido = True
                return hora
        hora = input("Error, formato de hora inválido. Ingrese nuevamente (HH:MM): ")

def mostrar_eventos():
    """Muestra los eventos que se encuentran disponible, si no hay eventos muestra un mensaje"""

    try:
        hay_eventos = eventos[0]
        titulo = "\n📋   LISTA DE EVENTOS "
        print(titulo.ljust(40, "━"))

        print(f"{'N°':<3} {'Artista':<20} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas disponibles':<9}")
        for i, evento in enumerate(eventos): 
            print(f"{i+1:<3} {evento[0]:<20} {evento[1]:<20} {evento[2]:<12} {evento[3]:<7} ${evento[4]:<7} {evento[5]['disponibles']:<9}")
    
    except IndexError:
        print("No hay eventos registrados.")
        #PODRIAMOS HACER QUE PREGUNTE SI QUEREMOS AGREGAR UN EVENTO? SI/NO
        #PERO ESO REQUERIRIA TENER QUE CREAR LA FUNCION PARA PEDIR LOS DATOS DEL EVENTO APARTE
        
    
def crear_evento(artista, estadio, fecha, hora, precio, cantidad):
    """Crea un nuevo evento si no existe otro con el mismo artista en la misma fecha y lo agrega a la lista de eventos"""

    for evento in eventos:
        if evento[0] == artista and evento[2] == fecha:
            print("Error, ya existe un evento con ese artista en esa fecha.")


    nuevo_evento = [artista, estadio, fecha, hora, precio, {"total": cantidad, "disponibles": cantidad}]
    eventos.append(nuevo_evento)
    print("Evento creado con éxito.")


def modificar_evento(indice, opcion, nuevo_valor):
    """Modifica un evento existente en la lista de eventos"""

    if opcion == 0:   # Artista
        eventos[indice][opcion] = validar_no_es_vacio(nuevo_valor)
    elif opcion == 1:   # Estadio
        eventos[indice][opcion] = validar_no_es_vacio(nuevo_valor)
    elif opcion == 2:   # Fecha
        eventos[indice][opcion] = validar_fecha(nuevo_valor)
    elif opcion == 3:   # Hora
        eventos[indice][opcion] = validar_hora(nuevo_valor)
    elif opcion == 4:   # Precio
        eventos[indice][opcion] = validar_numero(nuevo_valor)
    elif opcion == 5:   # Cantidad de entradas
        nuevo_valor = validar_numero(nuevo_valor)
        vendidas = eventos[indice][5]["total"] - eventos[indice][5]["disponibles"]
        while nuevo_valor < vendidas:
            nuevo_valor = validar_numero(input("La nueva cantidad no puede ser menor a las entradas ya vendidas. Ingrese nuevamente: "))
        diferencia = nuevo_valor - eventos[indice][5]["total"]
        eventos[indice][5]["total"] = nuevo_valor
        eventos[indice][5]["disponibles"] += diferencia
    
    print("Evento modificado con éxito.")


def eliminar_evento(indice):
    """Elimina un evento existente en la lista de eventos"""
    eliminado = eventos.pop(indice)
    print("Evento eliminado: ", eliminado[0])


def vender_entrada(indice, cantidad):
    """Vende entradas de un evento, si hay suficientes disponibles, 
    en caso de acabarse se notifica que el evento está agotado"""

    if eventos[indice][5]["disponibles"] >= cantidad:
        eventos[indice][5]["disponibles"] -= cantidad
        print("Vendidas ", cantidad, " entradas para " , eventos[indice][0])
    else:
        print("No hay suficientes entradas disponibles.")
    
    if eventos[indice][5]["disponibles"] == 0:
        print("El evento de ", eventos[indice][0], " está agotado.")


def cancelar_entrada(indice, cantidad):
    """Cancela entradas vendidas de un evento, si no se excede la cantidad total de entradas vendidas"""

    if eventos[indice][5]["disponibles"] + cantidad <= eventos[indice][5]["total"]:
        eventos[indice][5]["disponibles"] += cantidad
        print("Canceladas ", cantidad, " entradas para ", eventos[indice][0])
    else:
        print("No hay entradas vendidas para ese evento o la cantidad vendidas es inferior a la que desea cancelar.")


def ver_entradas_vendidas():
    """Muestra la cantidad de entradas vendidas y disponibles para cada evento"""

    print("\nEntradas vendidas por evento:")
    for evento in eventos:
        vendidas = evento[5]["total"] - evento[5]["disponibles"]
        print(evento[0], " -> ", vendidas, " vendidas ", evento[5]["disponibles"], "disponibles")


def analisis_datos():
    """Realiza un análisis de los datos de los eventos, mostrando el total recaudado, total de entradas vendidas, promedio de entradas vendidas por evento y el evento más vendido"""
    if not eventos:
        print("No hay eventos registrados.")
        return

    total_vendidas = sum(e[5]["total"] - e[5]["disponibles"] for e in eventos)
    total_recaudado = sum((e[5]["total"] - e[5]["disponibles"]) * e[4] for e in eventos)
    promedio = total_vendidas / len(eventos)
    max_vendidas = max(map(lambda e: e[5]["total"] - e[5]["disponibles"], eventos))
    mas_vendidos = list(filter(lambda e: (e[5]["total"] - e[5]["disponibles"]) == max_vendidas, eventos))
    if total_vendidas == 0:
        print("No se han vendido entradas aún.")
    else:
        print("\nAnálisis de datos:")
        print("Total recaudado: $",total_recaudado, sep="")
        print("Total entradas vendidas:",total_vendidas)
        print(f"Promedio de entradas vendidas: {promedio:.2f}") 
        if len(mas_vendidos) > 1:
            print(f"Empate entre {len(mas_vendidos)} eventos más vendidos:")
        else:
            print("Evento más vendido:")

        for e in mas_vendidos:
            print(f"- {e[0]} ({max_vendidas} entradas vendidas)")

def busqueda_artista(artista):
    """Busca eventos por el nombre del artista y muestra los resultados"""

    artista_encontrado = [evento for evento in eventos if artista.lower() in evento[0].lower()]
    if artista_encontrado:
        titulo = "\nEventos encontrados: "
        print(titulo.ljust(40, "━"))
        print(f"{'Artista':<20} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas disponibles':<9}")
        for evento in artista_encontrado: 
            print(f"{evento[0]:<20} {evento[1]:<20} {evento[2]:<12} {evento[3]:<7} ${evento[4]:<7} {evento[5]['disponibles']:<9}")
    else:
        print("No se encontraron eventos para", artista)

def mostrar_menu():
    """Muestra el menú principal con las opciones disponibles"""

    titulo = "\n 🎟️   MENÚ PRINCIPAL  "
    print(titulo.ljust(40, "━"))
    print("1. Administración de eventos")
    print("2. Administración de entradas")
    print("3. Salir")

def mostrar_menu():
    """Muestra el menú principal con las opciones disponibles"""

    titulo = "\n 🎟️   MENÚ PRINCIPAL  "
    print(titulo.ljust(40, "━"))
    print("1. Administración de eventos")
    print("2. Administración de entradas")
    print("3. Salir")

def menu_eventos():
    """Muestra el menú secundario con las opciones disponibles"""

    titulo = "\n 🎟️   MENÚ EVENTOS  "
    print(titulo.ljust(40, "━"))
    print("1. Mostrar eventos")
    print("2. Buscar evento por artista")
    print("3. Crear un evento")
    print("4. Modificar un evento")
    print("5. Eliminar un evento")
    print("6. Volver al menú principal")
    print("".ljust(40, "━"))
    opcion_eventos = validar_numero(input("Elija una opción: "))-1
    while opcion_eventos < 0 or opcion_eventos > 5:
        opcion_eventos = validar_numero(input("Opción inválida. Ingrese una opción válida: "))-1

    if opcion_eventos == 0:
        mostrar_eventos()
    elif opcion_eventos == 1:
        artista_buscar = validar_no_es_vacio(input("Ingrese el nombre del artista a buscar: "))
        busqueda_artista(artista_buscar)
    elif opcion_eventos == 2:
        artista = validar_no_es_vacio(input("Ingrese el nombre del artista: "))
        estadio = validar_no_es_vacio(input("Ingrese el nombre del estadio: "))
        fecha = validar_fecha(input("Ingrese la fecha del evento (YYYY-MM-DD): "))
        hora = validar_hora(input("Ingrese la hora del evento (HH:MM): "))
        precio = validar_numero(input("Ingrese el precio de la entrada: "))
        cantidad = validar_numero(input("Ingrese la cantidad de entradas disponibles: "))
        crear_evento(artista, estadio, fecha, hora, precio, cantidad)
    elif opcion_eventos == 3:
        mostrar_eventos()
        indice = validar_indice(input("Seleccione el evento a modificar: "))
        continuar = True
        while continuar:
            print("1. Artista\n2. Estadio\n3. Fecha\n4. Hora\n5. Precio\n6. Cantidad de entradas\n7. Salir")
            opcion_mod = validar_numero(input("¿Qué desea modificar?: ")) - 1
            while opcion_mod < 0 or opcion_mod > 6: 
                opcion_mod = validar_numero(input("Opción inválida. Ingrese una opción válida: ")) - 1
            
            if opcion_mod != 6: 
                nuevo_valor = input("Ingrese el nuevo valor: ")
                modificar_evento(indice, opcion_mod, nuevo_valor)
            else:
                continuar = False

    elif opcion_eventos == 4:
        mostrar_eventos()
        indice = validar_indice(input("Ingrese el índice del evento a eliminar: "))
        eliminar_evento(indice)

    if opcion_eventos != 5:
        menu_eventos()

def menu_entradas():

    print("1. Vender entrada")
    print("2. Cancelar entrada")
    print("3. Ver entradas vendidas")
    print("4. Análisis de datos")
    print("5. Volver al menú principal")
    opcion_entradas = validar_numero(input("Elija una opción: "))-1
    while opcion_entradas < 0 or opcion_entradas > 4:
        opcion_entradas = validar_numero(input("Opción inválida. Ingrese una opción válida: "))-1

    if opcion_entradas == 0:
        mostrar_eventos()
        indice = validar_indice(input("Ingrese el índice del evento: "))
        cantidad = validar_numero(input("Cantidad de entradas a vender: "))
        vender_entrada(indice, cantidad)
    elif opcion_entradas == 1:
        mostrar_eventos()
        indice = validar_indice(input("Ingrese el índice del evento: "))
        cantidad = validar_numero(input("Cantidad de entradas a cancelar: "))
        cancelar_entrada(indice, cantidad)
    elif opcion_entradas == 2:
        ver_entradas_vendidas()
    elif opcion_entradas == 3:
        analisis_datos()
    elif opcion_entradas == 4: #caso base, sale de la recursividad
        print("Volviendo al menú principal")
    
    if opcion_entradas != 4:
        menu_entradas()

print("\n")

titulo = "  SISTEMA DE GESTIÓN DE EVENTOS  "
print(titulo.center(100, "━"))
mostrar_menu()
print("".ljust(40, "━"))
opcion = validar_numero(input("Elija una opción: "))-1


while opcion != 2:
    
    if opcion == 0:
        menu_eventos()

    elif opcion == 1:
        menu_entradas()
    else:
        print("Opción inválida. Intente nuevamente.")
    mostrar_menu()
    print("".ljust(40, "━"))
    opcion = validar_numero(input("Elija una opción: "))-1

print("¡Chau!")