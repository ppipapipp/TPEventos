from datetime import datetime

#falta: 
# arreglar un problema con el cancelar entrada
# ver bien lo del try except
# chequear que esté todo bien programado
# ver bien el tema de dejar espacios y que esté todo lindo y bien impreso
# implementar las plateas y eso

# FUNCIONES DE ARCHIVOS Y GUARDADO DE DATOS

def cargar_eventos_desde_archivo():
    """Carga los eventos desde 'eventos.txt'"""

    eventos = []
    try:
        arch = open("eventos.txt", "rt")
        for linea in arch:
            linea = linea.strip()
            if linea:
                partes = linea.split(";")
                if len(partes) == 7:
                    artista, estadio, fecha, hora, precio, total, disponibles = partes
                    eventos.append([artista, estadio, fecha, hora, int(precio), {"total": int(total), "disponibles": int(disponibles)}])
                else:
                    print("Línea inválida: ", linea)
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return eventos


def guardar_eventos_en_archivo(eventos):
    """Guarda los eventos en 'eventos.txt'"""

    try:
        arch = open("eventos.txt", "wt")
        for evento in eventos:
            arch.write(f"{evento[0]};{evento[1]};{evento[2]};{evento[3]};{evento[4]};{evento[5]['total']};{evento[5]['disponibles']}\n")
    except OSError as mensaje:
        print("ERROR al guardar los eventos:", mensaje)
    else:
        print("Evento guardado correctamente.")
    finally:
        try:
            arch.close()
        except NameError:
            pass


def guardar_venta_en_archivo(nombre, apellido, email, numero_de_tramite, cantidad_entradas, factura):
    """Guarda una venta en 'ventas.txt'"""

    try:
        arch = open("ventas.txt", "at")
        arch.write(f"{nombre};{apellido};{email};{numero_de_tramite};{cantidad_entradas};{factura}\n")
    except OSError as mensaje:
        print("ERROR al registrar la venta:", mensaje)
    else:
        print("Venta registrada correctamente.")
    finally:
        try:
            arch.close()
        except NameError:
            pass


def mostrar_ventas_guardadas():
    """Lee y muestra todas las ventas desde 'ventas.txt'"""

    ventas = []
    try:
        arch = open("ventas.txt", "rt")
        print("\n📄 Ventas registradas:")
        vacio = True
        for linea in arch:
            linea = linea.strip()
            if linea:
                vacio = False
                nombre, apellido, email, tramite, cantidad, factura = linea.split(";")
                print(f"- {nombre} {apellido} | {email} | Trámite: {tramite} | Entradas: {cantidad} | Factura: {factura}")
        if vacio:
            print("No hay ventas registradas aún.")
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)
    else:
        print("Lectura finalizada.")
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return ventas


# FUNCIONES DE VALIDACIÓN


def validar_no_es_vacio(cadena):
    """Valida que la cadena no esté vacía"""

    while not cadena.strip(): 
        try:
            cadena = input("El valor no puede estar vacío. Ingrese nuevamente: ").strip()
        except ValueError:
            print("Error, valor inválido.")
    return cadena


def validar_indice(eventos, indice):
    """Valida que el índice ingresado sea válido para la lista de eventos"""

    indice = validar_no_es_vacio(indice)
    while not indice.isdigit() or int(indice) <= 0 or int(indice) > len(eventos):
        try:
            indice = input("Ingrese un índice válido: ")
        except ValueError:
            print("Error, valor inválido.")
    return int(indice) -1


def validar_fecha(fecha):
    """Valida que la fecha ingresada tenga el formato YYYY-MM-DD y no sea una fecha pasada"""

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
            elif mes in [1,3,5,7,8,10,12] and (dia < 1 or dia > 31):
                print("El día no es válido para ese mes.")
            elif mes in [4,6,9,11] and (dia < 1 or dia > 30):
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
                if (anio < hoy_anio) or (anio == hoy_anio and mes < hoy_mes) or (anio == hoy_mes and dia < hoy_dia):
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
    """Valida que la hora ingresada tenga el formato HH:MM"""

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

def validar_numero_tramite(numero_de_tramite):
    """Valida que el número de trámite tenga 11 dígitos"""

    validar_numero(numero_de_tramite)
    while len(str(numero_de_tramite)) != 11:
        numero_de_tramite = validar_numero(input("Número de trámite inválido. Ingrese su número de trámite de 11 dígitos: "))
    return numero_de_tramite


def validar_email(email):
    """Valida que el email ingresado tenga un formato básico válido"""

    validar_no_es_vacio(email)
    while "@" not in email or "." not in email.split("@")[-1]:
        email = input("Email inválido. Ingrese un email válido: ")
    return email


# FUNCIONES PRINCIPALES


def mostrar_eventos(eventos):
    """Muestra la lista de eventos disponibles"""

    try:
        hay_eventos = eventos[0]
        titulo = "\n📋   LISTA DE EVENTOS "
        print(titulo.ljust(40, "━"))
        print(f"{'N°':<3} {'Artista':<20} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas disponibles':<9}")
        for i, evento in enumerate(eventos): 
            print(f"{i+1:<3} {evento[0]:<20} {evento[1]:<20} {evento[2]:<12} {evento[3]:<7} ${evento[4]:<7} {evento[5]['disponibles']:<9}")
    except IndexError:
        print("No hay eventos registrados.")


def crear_evento(eventos, artista, estadio, fecha, hora, precio, cantidad):
    """Crea un nuevo evento si no existe otro con el mismo artista en la misma fecha"""

    for evento in eventos:
        if evento[0] == artista and evento[2] == fecha:
            print("Error, ya existe un evento con ese artista en esa fecha.")
            return
    nuevo_evento = [artista, estadio, fecha, hora, precio, {"total": cantidad, "disponibles": cantidad}]
    eventos.append(nuevo_evento)
    print("Evento creado con éxito.")
    guardar_eventos_en_archivo(eventos)


def modificar_evento(eventos, indice, opcion, nuevo_valor):
    """Modifica un atributo específico de un evento"""

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
    guardar_eventos_en_archivo(eventos)


def eliminar_evento(eventos, indice):
    """Elimina un evento de la lista de eventos"""

    eliminado = eventos.pop(indice)
    print("Evento eliminado: ", eliminado[0])
    guardar_eventos_en_archivo(eventos)


def imprimir_factura(factura, nombre, apellido, email, numero_de_tramite, cantidad_entradas):
    """Imprime la factura de la compra realizada"""

    print("\n"+" FACTURA ".center(40, "━"))
    print("Número de factura: ", factura)
    print("Nombre: ", nombre)
    print("Apellido: ", apellido)
    print("Email: ", email)
    print("Número de trámite: ", numero_de_tramite)
    print("Cantidad de entradas compradas: ", cantidad_entradas)
    print("".ljust(40, "━")+"\n")


def vender_entrada(eventos, indice, nombre, apellido, email, numero_de_tramite, cantidad_entradas):
    """Vende entradas de un evento, si hay suficientes disponibles, 
    en caso de acabarse se notifica que el evento está agotado"""    

    datos_compradores=[]
    while cantidad_entradas > 6:
        print("No se pueden vender más de 6 entradas por persona.")
        cantidad_entradas = validar_numero(input("Ingrese la cantidad de entradas a vender (máximo 6): "))
    if eventos[indice][5]["disponibles"] >= cantidad_entradas:
        eventos[indice][5]["disponibles"] -= cantidad_entradas
        print("Vendidas ", cantidad_entradas, " entradas para " , eventos[indice][0])
        factura = 0
        factura  += 1
        datos_compradores.append({"nombre": nombre, "apellido": apellido, "email": email, "número de trámite": numero_de_tramite, "número de entradas": cantidad_entradas, "número de factura": factura })
        imprimir_factura(factura, nombre, apellido, email, numero_de_tramite, cantidad_entradas)
    elif eventos[indice][5]["disponibles"] == 0:
        print("El evento de ", eventos[indice][0], " está agotado.")
    else:
        print("No hay suficientes entradas disponibles.")
    guardar_venta_en_archivo(nombre, apellido, email, numero_de_tramite, cantidad_entradas, factura)
    guardar_eventos_en_archivo(eventos)


def cancelar_entrada(eventos, ventas,  email, numero_de_tramite, indice, cantidad):
    """Cancela entradas vendidas de un evento, si no se excede la cantidad total de entradas vendidas"""

    for comprador in ventas:
        if comprador["email"] == email and comprador["número de trámite"] == numero_de_tramite:
            if cantidad > comprador["número de entradas"]:
                print("No puede cancelar más entradas de las que compró.")
            else:
                comprador["número de entradas"] -= cantidad
                eventos[indice][5]["disponibles"] + cantidad <= eventos[indice][5]["total"]
                eventos[indice][5]["disponibles"] += cantidad
                print("Canceladas ", cantidad)
                guardar_eventos_en_archivo(eventos)
        else:
            print("No hay entradas vendidas bajo ese mail o numero de factura.")


def ver_entradas_vendidas(eventos):
    """Muestra la cantidad de entradas vendidas por evento"""

    print("\nEntradas vendidas por evento:")
    for evento in eventos:
        vendidas = evento[5]["total"] - evento[5]["disponibles"]
        print(evento[0], " -> ", vendidas, " vendidas ", evento[5]["disponibles"], "disponibles")


def analisis_datos(eventos):
    """Realiza un análisis de datos sobre las ventas de entradas"""

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


def busqueda_artista(eventos, artista):
    """Busca eventos por artista y los muestra"""

    artista_encontrado = [evento for evento in eventos if artista.lower() in evento[0].lower()]
    if artista_encontrado:
        titulo = "\nEventos encontrados: "
        print(titulo.ljust(40, "━"))
        print(f"{'Artista':<20} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas disponibles':<9}")
        for evento in artista_encontrado: 
            print(f"{evento[0]:<20} {evento[1]:<20} {evento[2]:<12} {evento[3]:<7} ${evento[4]:<7} {evento[5]['disponibles']:<9}")
    else:
        print("No se encontraron eventos para", artista)


# MENÚS PRINCIPALES


def mostrar_menu():
    """Muestra el menú principal"""

    titulo = "\n 🎟️   MENÚ PRINCIPAL  "
    print(titulo.ljust(40, "━"))
    print("1. Administración de eventos")
    print("2. Administración de entradas")
    print("3. Ver ventas registradas")
    print("4. Salir")



def menu_eventos(eventos):
    """Muestra el menú de administración de eventos"""

    titulo = "\n 🎟️   MENÚ EVENTOS  "
    print(titulo.ljust(40, "━"))
    print("1. Mostrar eventos")
    print("2. Buscar evento por artista")
    print("3. Crear un evento")
    print("4. Modificar un evento")
    print("5. Eliminar un evento")
    print("6. Volver al menú principal")
    print("".ljust(40, "━"))
    print("\n")

    opcion_eventos = validar_numero(input("Elija una opción: "))-1
    while opcion_eventos < 0 or opcion_eventos > 5:
        opcion_eventos = validar_numero(input("Opción inválida. Ingrese una opción válida: "))-1
    if opcion_eventos == 0:
        mostrar_eventos(eventos)
    elif opcion_eventos == 1:
        artista = validar_no_es_vacio(input("Ingrese el nombre del artista a buscar: "))
        busqueda_artista(eventos, artista)
    elif opcion_eventos == 2:
        artista = validar_no_es_vacio(input("Ingrese el nombre del artista: "))
        estadio = validar_no_es_vacio(input("Ingrese el nombre del estadio: "))
        fecha = validar_fecha(input("Ingrese la fecha del evento (YYYY-MM-DD): "))
        hora = validar_hora(input("Ingrese la hora del evento (HH:MM): "))
        precio = validar_numero(input("Ingrese el precio de la entrada: "))
        cantidad = validar_numero(input("Ingrese la cantidad de entradas disponibles: "))
        crear_evento(eventos, artista, estadio, fecha, hora, precio, cantidad)
    elif opcion_eventos == 3:
        mostrar_eventos(eventos)
        indice = validar_indice(eventos, input("Seleccione el evento a modificar: "))
        continuar = True
        while continuar:
            print("1. Artista\n2. Estadio\n3. Fecha\n4. Hora\n5. Precio\n6. Cantidad de entradas\n7. Salir")
            opcion_mod = validar_numero(input("¿Qué desea modificar?: ")) - 1
            while opcion_mod < 0 or opcion_mod > 6: 
                opcion_mod = validar_numero(input("Opción inválida. Ingrese una opción válida: ")) - 1
            if opcion_mod != 6: 
                nuevo_valor = input("Ingrese el nuevo valor: ")
                modificar_evento(eventos, indice, opcion_mod, nuevo_valor)
            else:
                continuar = False
    elif opcion_eventos == 4:
        mostrar_eventos(eventos)
        indice = validar_indice(eventos, input("Ingrese el índice del evento a eliminar: "))
        eliminar_evento(eventos, indice)
    if opcion_eventos != 5:
        menu_eventos(eventos)


def menu_entradas(eventos):
    """Muestra el menú de administración de entradas"""

    titulo = "\n 🎟️   MENÚ ENTRADAS  "
    print(titulo.ljust(40, "━"))
    print("1. Vender entrada")
    print("2. Cancelar entrada")
    print("3. Ver entradas vendidas")
    print("4. Análisis de datos")
    print("5. Volver al menú principal")
    print("".ljust(40, "━"))
    print("\n")

    opcion_entradas = validar_numero(input("Elija una opción: "))-1
    while opcion_entradas < 0 or opcion_entradas > 4:
        opcion_entradas = validar_numero(input("Opción inválida. Ingrese una opción válida: "))-1
    if opcion_entradas == 0:
        mostrar_eventos(eventos)
        indice = validar_indice(eventos, input("Ingrese el índice del evento: "))
        nombre = validar_no_es_vacio(input("Ingrese su nombre: "))
        apellido = validar_no_es_vacio(input("Ingrese su apellido: "))
        email = validar_email(input("Ingrese su email: "))
        numero_de_tramite = validar_numero_tramite(input("Ingrese su número de trámite: "))
        cantidad_entradas = validar_numero(input("Cantidad de entradas a vender: "))
        vender_entrada(eventos, indice, nombre, apellido, email, numero_de_tramite, cantidad_entradas)
    elif opcion_entradas == 1:
        mostrar_eventos(eventos)
        email = validar_email(input("Ingrese su email: "))
        numero_de_tramite = validar_numero_tramite(input("Ingrese su número de trámite: "))
        indice = validar_indice(eventos, input("Ingrese el índice del evento: "))
        cantidad = validar_numero(input("Cantidad de entradas a cancelar: "))
        cancelar_entrada(email, numero_de_tramite, indice, cantidad)
    elif opcion_entradas == 2:
        ver_entradas_vendidas(eventos)
    elif opcion_entradas == 3:
        analisis_datos(eventos)
    elif opcion_entradas == 4:
        print("Volviendo al menú principal")
    if opcion_entradas != 4:
        menu_entradas(eventos)


# PROGRAMA PRINCIPAL


eventos = cargar_eventos_desde_archivo()
print("\n")
titulo = "  SISTEMA DE GESTIÓN DE EVENTOS  "
print(titulo.center(100, "━"))
mostrar_menu()
print("".ljust(40, "━"))
print("\n")
opcion = validar_numero(input("Elija una opción: "))-1

while opcion != 3:
    if opcion == 0:
        menu_eventos(eventos)
    elif opcion == 1:
        menu_entradas(eventos)
    elif opcion == 2:
        mostrar_ventas_guardadas()
    else:
        print("Opción inválida. Intente nuevamente.")
    mostrar_menu()
    print("".ljust(40, "━"))
    opcion = validar_numero(input("Elija una opción: "))-1

print("¡Chau!")
