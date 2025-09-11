from datetime import datetime




#COSAS QUE FALTAN
#Podriamos agregar que el modificar evento se un while para que pueda modificar varios campos sin tener que volver al menu principal y agregar un 7 para salir
#DECLARACIÓN DE VARIABLES
#Verificar que no halla dos conciertos en el mismo dia en el mismo estadio

eventos = [
    ["Taylor", "Estadio Nacional", "2025-09-15", "20:00", 50000, 1000, 1000],
    ["Coldplay", "Estadio Nacional", "2023-11-01", "21:00", 60000, 1500, 1500],
    ["Bad bunny", "Estadio Nacional", "2023-12-01", "22:00", 70000, 2000, 2000]
]

#FUNCIONES

def mostrar_eventos():
    """Muestra los eventos que se encuentran disponible, si no hay eventos muestra un mensaje"""
    titulo = "\n📋   LISTA DE EVENTOS "
    print(titulo.ljust(40, "━"))
 
    print(f"{'N°':<3} {'Artista':<15} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas':<9}")
    for i, evento in enumerate(eventos): #SEPARA LA LISTA EN INDICES Y SUS VALORES, OSEA QUE ES UNA TUPLA
        print(f"{i+1:<3} {evento[0]:<15} {evento[1]:<20} {evento[2]:<12} {evento[3]:<7} ${evento[4]:<7} {evento[6]:<9}")
    
    if not eventos:
        print("No hay eventos registrados.")

def verificacionindice(indice):
    """Chequea que el índice ingresado sea válido"""
    if 0 <= indice < len(eventos):
        return True
    else:
        print("Índice inválido.")
        return False


def crear_evento(artista, estadio, fecha, hora, precio, cantidad):
    """Crea un nuevo evento si no existe otro con el mismo artista en la misma fecha y lo agrega a la lista de eventos"""
    for evento in eventos:
        if evento[0] == artista and evento[2] == fecha:
            print("Error, ya existe un evento con ese artista en esa fecha.")
            return

    nuevo_evento = [artista, estadio, fecha, hora, precio, cantidad, cantidad]
    eventos.append(nuevo_evento)
    print("Evento creado con éxito.")


def modificar_evento(indice, opcion, nuevo_valor):
    """Modifica un evento existente en la lista de eventos"""
    no_es_vacio(nuevo_valor)
    verificacionindice(indice)
    if opcion == 5: #SI LA OPCION ES 5, OSEA QUE QUIERE MODIFICAR LA CANTIDAD DE ENTRADAS
        while not str(nuevo_valor).isdigit() or int(nuevo_valor) < 0 or int(nuevo_valor) < (eventos[indice][5] - eventos[indice][6]):
            """VALIDO QUE SEA UN NUMERO, QUE NO SEA NEGATIVO Y QUE NO SEA MENOR A LAS ENTRADAS YA VENDIDAS"""
            nuevo_valor = input("Error, la cantidad de entradas no puede ser menor a las ya vendidas. Ingrese nuevamente: ")
        nuevo_valor=int(nuevo_valor)
        diferencia = nuevo_valor - eventos[indice][opcion] #CALCULO LA DIFERENCIA ENTRE LA CANT ANTERIORY ACTUAL DE ENTRADAS
        eventos[indice][opcion] = nuevo_valor #estoy reemplazando el TOTAL DE ENTRADAS
        eventos[indice][opcion+1] += diferencia
    else:
        eventos[indice][opcion] = nuevo_valor


def eliminar_evento(indice):
    """Elimina un evento existente en la lista de eventos"""
    verificacionindice(indice)
    eliminado = eventos.pop(indice)
    print("Evento eliminado: ", eliminado[0])



def vender_entrada(indice, cantidad):
    """Vende una cantidad de entradas para un evento específico si hay suficientes entradas disponibles, 
    en caso de acabarse se notifica que el evento está agotado"""
    verificacionindice(indice)
    if eventos[indice][6] >= cantidad:
        eventos[indice][6] -= cantidad

        print("Vendidas ", cantidad, " entradas para " , eventos[indice][0])
    else:
        print("No hay suficientes entradas disponibles.")

    if eventos[indice][6] == 0:
        print("El evento de ", eventos[indice][0], " está agotado.")


def cancelar_entrada(indice, cantidad):
    """Cancela una cantidad de entradas vendidas para un evento específico si no se excede la cantidad total de entradas vendidas"""
    verificacionindice(indice)
    if eventos[indice][6] + cantidad <= eventos[indice][5]:
        eventos[indice][6] += cantidad
        print("Canceladas ", cantidad, " entradas para ", eventos[indice][0])
    else:
        print("No se puede cancelar más entradas de las que existen.")


def ver_entradas_vendidas():
    """Muestra la cantidad de entradas vendidas y disponibles para cada evento"""
    print("\nEntradas vendidas por evento:")
    for evento in eventos:
        vendidas = evento[5] - evento[6]
        print(evento[0], " -> ", vendidas, " vendidas ", evento[6], "disponibles")


def analisis_datos():
    """Realiza un análisis de los datos de los eventos, mostrando el total recaudado, total de entradas vendidas, promedio de entradas vendidas por evento y el evento más vendido"""
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

def validar_fecha(fecha):
    """Valida que la fecha ingresada esté en el formato YYYY-MM-DD y no sea una fecha pasada"""
    no_es_vacio(fecha)
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
                    return fecha
        fecha = input("Error, formato de fecha inválido o ya pasó. Ingrese nuevamente (YYYY-MM-DD): ")


def no_es_vacio(cadena):
    """Valida que la cadena ingresada no esté vacía"""
    while cadena == "": 
        cadena = input("El valor no puede estar vacío. Ingrese nuevamente: ")
    return str(cadena)


def validar_numero(valor):
    """Valida que el valor ingresado sea un número positivo"""
    no_es_vacio(valor)
    while not valor.isdigit() or int(valor) <= 0:
        valor = input("El valor debe ser un número positivo. Ingrese nuevamente: ")
    return int(valor)

def validar_hora(hora):
    """Valida que la hora ingresada esté en el formato HH:MM y sea una hora válida"""
    no_es_vacio(hora)
    valido = False
    while not valido:
        if len(hora) == 5 and hora[2] == ':' and hora[:2].isdigit() and hora[3:].isdigit():
            horas = int(hora[:2])
            minutos = int(hora[3:])
            if 0 <= horas < 24 and 0 <= minutos < 60:
                valido = True
                return hora
        hora = input("Error, formato de hora inválido. Ingrese nuevamente (HH:MM): ")

def busqueda_artista(artista):
    """Busca eventos por el nombre del artista y muestra los resultados"""
    no_es_vacio(artista)
    artista_encontrado = [evento for evento in eventos if evento[0].lower() == artista.lower()]
    if artista_encontrado:
        print("Eventos encontrados para", artista, ":")
        print(f"{'N°':<3} {'Artista':<15} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas':<9}")
        for evento in artista_encontrado:
            print(f"{evento[0]:<15} {evento[1]:<20} {evento[2]:<12} {evento[3]:<7} ${evento[4]:<7} {evento[6]:<9}")
    else:
        print("No se encontraron eventos para", artista)

def mostrar_menu():
    """Muestra el menú principal con las opciones disponibles"""
    titulo = "\n 🎟️   MENÚ PRINCIPAL  "
    print(titulo.ljust(40, "━"))
    print("1. Mostrar eventos")
    print("2. Crear un evento")
    print("3. Buscar evento por artista")
    print("4. Modificar un evento")
    print("5. Eliminar un evento")
    print("6. Vender entrada")
    print("7. Cancelar entrada")
    print("8. Ver entradas vendidas")
    print("9. Análisis de datos")
    print("10. Salir")
    

#PROGRAMA PRINCIPAL

print("\n")

titulo = "  SISTEMA DE GESTIÓN DE EVENTOS  "
print(titulo.center(100, "━"))
mostrar_menu()
print("".ljust(40, "━"))
opcion = validar_numero(input("Elija una opción: "))-1

while opcion != 9:
    
    if opcion == 0:
        mostrar_eventos()

    elif opcion == 1:
        artista = no_es_vacio(input("Ingrese el nombre del artista: "))
        estadio = no_es_vacio(input("Ingrese el nombre del estadio: "))
        fecha = validar_fecha(input("Ingrese la fecha del evento (YYYY-MM-DD): "))
        hora = validar_hora(input("Ingrese la hora del evento (HH:MM): "))
        precio = validar_numero(input("Ingrese el precio de la entrada: "))
        cantidad = validar_numero(input("Ingrese la cantidad de entradas disponibles: "))
        crear_evento(artista, estadio, fecha, hora, precio, cantidad)

    elif opcion == 2:
        artista = no_es_vacio(input("Ingrese el nombre del artista a buscar: "))
        busqueda_artista(artista)

    elif opcion == 3:
        for i, artista in enumerate(eventos):
            print(i+1,". ", artista[0], sep="")
        indice = validar_numero(input("Seleccione el evento a modificar: "))-1
        while not verificacionindice(indice):
            indice = validar_numero(input("Ingrese un índice válido: "))-1
        print("1. Artista\n2. Estadio\n3. Fecha\n4. Hora\n5. Precio\n6. Cantidad de entradas")
        opcion_mod = int(input("¿Qué desea modificar?: "))-1
        while opcion_mod < 0 or opcion_mod > 5:
            opcion_mod = int(input("Opción inválida. Ingrese una opción válida: "))-1
        if opcion_mod == 2:
            nuevo_valor = validar_fecha(input("Ingrese la nueva fecha (YYYY-MM-DD): "))
        elif opcion_mod == 3:
            nuevo_valor = validar_hora(input("Ingrese la nueva hora (HH:MM): "))
        elif opcion_mod == 4 or opcion_mod == 5:
            nuevo_valor = validar_numero(input("Ingrese el nuevo valor: "))
        else:
            nuevo_valor = no_es_vacio(input("Ingrese el nuevo valor: "))
        modificar_evento(indice, opcion_mod, nuevo_valor)
 

    elif opcion == 4:
        mostrar_eventos()
        indice = int(input("Ingrese el índice del evento a eliminar: "))-1
        while not verificacionindice(indice):
            indice = int(input("Ingrese un índice válido: "))-1
        eliminar_evento(indice)

    elif opcion == 5:
        mostrar_eventos()
        indice = int(input("Ingrese el índice del evento: "))-1
        while not verificacionindice(indice):
            indice = int(input("Ingrese un índice válido: "))-1
        cantidad = int(input("Cantidad de entradas a vender: "))
        vender_entrada(indice, cantidad)

    elif opcion == 6:
        mostrar_eventos()
        indice = int(input("Ingrese el índice del evento: "))-1
        while not verificacionindice(indice):
            indice = int(input("Ingrese un índice válido: "))-1
        cantidad = int(input("Cantidad de entradas a cancelar: "))
        cancelar_entrada(indice, cantidad)

    elif opcion == 7:
        ver_entradas_vendidas()

    elif opcion == 8:
        analisis_datos()

    else:
        print("Opción inválida. Intente nuevamente.")
    
    mostrar_menu()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    opcion = int(input("Elija una opción: "))-1

print("¡Chau!")