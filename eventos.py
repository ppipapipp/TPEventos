from datetime import datetime

#falta: 
# chequear que esté todo bien programado
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
                    eventos.append({
                        "artista": artista,
                        "estadio": estadio,
                        "fecha": fecha,
                        "hora": hora,
                        "precio": int(precio),
                        "entradas": {"total": int(total), "disponibles": int(disponibles)}
                    })
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


def guardar_eventos_en_archivo(eventos): #REEMPLAZA TODOS LOS ARCHIVOS
    """Guarda los eventos en 'eventos.txt'"""

    try:
        arch = open("eventos.txt", "wt")
        for evento in eventos:
            arch.write(f"{evento['artista']};{evento['estadio']};{evento['fecha']};{evento['hora']};{evento['precio']};{evento['entradas']['total']};{evento['entradas']['disponibles']}\n")
    except OSError as mensaje:
        print("ERROR al guardar los eventos:", mensaje)
    else:
        print("Evento guardado correctamente.")
    finally:
        try:
            arch.close()
        except NameError:
            pass


def guardar_nuevo_evento(evento): #AGREGÁ NADA MÁS UN REGISTRO
    """Guarda los eventos en 'eventos.txt'"""

    try:
        arch = open("eventos.txt", "at")
        arch.write(f"{evento['artista']};{evento['estadio']};{evento['fecha']};{evento['hora']};{evento['precio']};{evento['entradas']['total']};{evento['entradas']['disponibles']}\n")
    except OSError as mensaje:
        print("ERROR al guardar los eventos:", mensaje)
    else:
        print("Evento guardado correctamente.")
    finally:
        try:
            arch.close()
        except NameError:
            pass


def guardar_venta_en_archivo(venta):
    """Guarda una venta en 'ventas.txt'"""

    try:
        arch = open("ventas.txt", "at")
        arch.write(f"{venta['indice']};{venta['nombre']};{venta['apellido']};{venta['email']};{venta['numero_tramite']};{venta['numero_entradas']};{venta['numero_factura']}\n")
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
    """Carga las ventas desde 'ventas.txt' y las devuelve como lista"""

    ventas = []
    try:
        arch = open("ventas.txt", "rt")
        for linea in arch:
            linea = linea.strip()
            if linea:
                partes = linea.split(";")
                if len(partes) == 7:
                    indice, nombre, apellido, email, tramite, cantidad, factura = partes
                    ventas.append({
                        "indice": int(indice),
                        "nombre": nombre,
                        "apellido": apellido,
                        "email": email,
                        "numero_tramite": tramite,
                        "numero_entradas": int(cantidad),
                        "numero_factura": int(factura)
                    })
                else:
                    print("Línea inválida:", linea)
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return ventas



# FUNCIONES DE VALIDACIÓN


def validar_no_es_vacio(cadena):
    """Valida que la cadena no esté vacía"""

    while cadena.strip() == "": 
        cadena = input("El valor no puede estar vacío. Ingrese nuevamente: ").strip()
    return cadena


def validar_indice(cant_eventos, indice):
    """Valida que el índice ingresado sea válido para la lista de eventos"""

    indice = validar_no_es_vacio(indice)
    while not indice.isdigit() or int(indice) <= 0 or int(indice) > cant_eventos:
        indice = input("Ingrese un índice válido: ")
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
    """Valida que el numero_tramite tenga 15 dígitos"""

    validar_numero(numero_de_tramite)
    while len(str(numero_de_tramite)) != 15:
        numero_de_tramite = validar_numero(input("Número de trámite inválido. Ingrese su número de trámite de 15 dígitos: "))
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

    if len(eventos) > 0:
        titulo = "\n▶   LISTA DE EVENTOS "
        print(titulo.ljust(40, "━"))
        print(f"{'N°':<3} {'Artista':<20} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas disponibles':<9}")
        for i, evento in enumerate(eventos): 
            print(f"{i+1:<3} {evento['artista']:<20} {evento['estadio']:<20} {evento['fecha']:<12} {evento['hora']:<7} ${evento['precio']:<7} {evento['entradas']['disponibles']:<9}")
    else:
        print("No hay eventos registrados.")
    print("\n")


def mostrar_ventas(ventas):
    """Muestra la lista de ventas registradas"""

    try:
        hay_ventas = ventas[0]
        titulo = "\n📄   LISTA DE VENTAS "
        print(titulo.ljust(40, "━"))
        print(f"{'N°':<3} {'Nombre':<15} {'Apellido':<15} {'Email':<25} {'Trámite':<18} {'Entradas':<9} {'Factura':<9}")
        for i, venta in enumerate(ventas):
            print(f"{i+1:<3} {venta['nombre']:<15} {venta['apellido']:<15} {venta['email']:<25} {venta['numero_tramite']:<18} {venta['numero_entradas']:<9} {venta['numero_factura']:<9}")
    except IndexError:
        print("No hay ventas registradas.")



def crear_evento(eventos, artista, estadio, fecha, hora, precio, cantidad):
    """Crea un nuevo evento si no existe otro con el mismo artista en la misma fecha"""

    for evento in eventos:
        if evento['artista'] == artista and evento['fecha'] == fecha:
            print("Error, ya existe un evento con ese artista en esa fecha.")
            return
    nuevo_evento = {
        "artista": artista,
        "estadio": estadio,
        "fecha": fecha,
        "hora": hora,
        "precio": precio,
        "entradas": {"total": cantidad, "disponibles": cantidad}
    }
    guardar_nuevo_evento(nuevo_evento)
    print("Evento creado con éxito.")
    



def modificar_evento(eventos, indice, opcion, nuevo_valor):
    """Modifica un atributo específico de un evento"""

    # opcion: 0 Artista, 1 Estadio, 2 Fecha, 3 Hora, 4 Precio, 5 Cantidad de entradas
    if opcion == 0:   # Artista
        eventos[indice]['artista'] = validar_no_es_vacio(nuevo_valor)
    elif opcion == 1:   # Estadio
        eventos[indice]['estadio'] = validar_no_es_vacio(nuevo_valor)
    elif opcion == 2:   # Fecha
        eventos[indice]['fecha'] = validar_fecha(nuevo_valor)
    elif opcion == 3:   # Hora
        eventos[indice]['hora'] = validar_hora(nuevo_valor)
    elif opcion == 4:   # Precio
        eventos[indice]['precio'] = validar_numero(nuevo_valor)
    elif opcion == 5:   # Cantidad de entradas
        nuevo_valor = validar_numero(nuevo_valor)
        vendidas = eventos[indice]['entradas']["total"] - eventos[indice]['entradas']["disponibles"]
        while nuevo_valor < vendidas:
            nuevo_valor = validar_numero(input("La nueva cantidad no puede ser menor a las entradas ya vendidas. Ingrese nuevamente: "))
        diferencia = nuevo_valor - eventos[indice]['entradas']["total"]
        eventos[indice]['entradas']["total"] = nuevo_valor
        eventos[indice]['entradas']["disponibles"] += diferencia
    print("\n")
    print("Evento modificado con éxito.")
    guardar_eventos_en_archivo(eventos)


def eliminar_evento(eventos, indice):
    """Elimina un evento de la lista de eventos"""

    eliminado = eventos.pop(indice)
    print("Evento eliminado: ", eliminado['artista'])
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


def obtener_siguiente_factura(ventas):
    """Devuelve el numero_factura siguiente (max+1) a partir de ventas en memoria"""
    if len(ventas) == 0:
        max_factura = 0
    else:
        max_factura = max(v["numero_factura"] for v in ventas)
    return max_factura + 1


def vender_entrada(eventos, indice, nombre, apellido, email, numero_de_tramite, cantidad_entradas):
    """Vende entradas de un evento, si hay suficientes disponibles, 
    en caso de acabarse se notifica que el evento está agotado"""    

    datos_compradores = []
    
    while cantidad_entradas > 6:
        print("No se pueden vender más de 6 entradas por persona.")
        cantidad_entradas = validar_numero(input("Ingrese la cantidad de entradas a vender (máximo 6): "))

    evento = eventos[indice]
    if evento['entradas']["disponibles"] >= cantidad_entradas:
        ventas_actuales = mostrar_ventas_guardadas()
        factura = obtener_siguiente_factura(ventas_actuales)
        venta = {
            "indice": indice,
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "numero_tramite": numero_de_tramite,
            "numero_entradas": cantidad_entradas,
            "numero_factura": factura
        }
        evento['entradas']["disponibles"] -= cantidad_entradas
        print("Vendidas ", cantidad_entradas, " entradas para " , evento['artista'])
        imprimir_factura(factura, nombre, apellido, email, numero_de_tramite, cantidad_entradas)
        datos_compradores.append({"nombre": nombre, "apellido": apellido, "email": email, "numero_tramite": numero_de_tramite, "numero_entradas": cantidad_entradas, "numero_factura": factura})
    elif evento['entradas']["disponibles"] == 0:
        print("El evento de ", evento['artista'], " está agotado.")
        return
    else:
        print("No hay suficientes entradas disponibles.")
        return

    guardar_venta_en_archivo(venta)
    guardar_eventos_en_archivo(eventos)


def cancelar_entrada(eventos, ventas, email, numero_de_tramite, factura, cantidad):
    """Cancela entradas vendidas de un evento, usando los datos de la venta existente."""

    venta_encontrada = None
    i = 0
    while i < len(ventas):
        venta = ventas[i]
      
        if venta['email'] == email and venta['numero_factura'] == factura:
            venta_encontrada = venta

        i = i + 1

    if venta_encontrada is None:
        print("No hay entradas vendidas bajo ese mail o número de factura.")
    else:
        indice_evento = venta_encontrada['indice']
        nombre = venta_encontrada['nombre']
        apellido = venta_encontrada['apellido']
        entradas_compradas = venta_encontrada['numero_entradas']
        nueva_venta = {
            "indice": indice_evento,
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "numero_tramite": numero_de_tramite,
            "numero_entradas": -cantidad,
            "numero_factura": factura
        }

        if cantidad > entradas_compradas:
            print("No puede cancelar más entradas de las que compró.")
        else:
            eventos[indice_evento]['entradas']["disponibles"] += cantidad
            guardar_venta_en_archivo(nueva_venta)
            guardar_eventos_en_archivo(eventos)
            print(f"Se cancelaron {cantidad} entradas del evento '{eventos[indice_evento]['artista']}' correctamente.")


def ver_entradas_vendidas(eventos):
    """Muestra la cantidad de entradas vendidas por evento"""

    print("\nEntradas vendidas por evento:")
    for evento in eventos:
        vendidas = evento['entradas']["total"] - evento['entradas']["disponibles"]
        print(evento['artista'], " -> ", vendidas, " vendidas ", evento['entradas']['disponibles'], "disponibles")


def analisis_datos(eventos):
    """Realiza un análisis de datos sobre las ventas de entradas"""

    if len(eventos) == 0:
        print("No hay eventos registrados.")
        return
    total_vendidas = sum(evento['entradas']["total"] - evento['entradas']["disponibles"] for evento in eventos)
    total_recaudado = sum((evento['entradas']["total"] - evento['entradas']["disponibles"]) * evento['precio'] for evento in eventos)
    promedio = total_vendidas / len(eventos) if len(eventos) > 0 else 0
    max_vendidas = max(map(lambda evento: evento['entradas']["total"] - evento['entradas']["disponibles"], eventos))
    mas_vendidos = list(filter(lambda evento: (evento['entradas']["total"] - evento['entradas']["disponibles"]) == max_vendidas, eventos))
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
            print(f"- {e['artista']} ({max_vendidas} entradas vendidas)")


def busqueda_artista(eventos, artista):
    """Busca eventos por artista y los muestra"""

    artista_encontrado = list(filter(lambda evento: artista.lower() in evento['artista'].lower(), eventos))
    if artista_encontrado:
        titulo = "\n▶  Eventos encontrados: "
        print(titulo.ljust(40, "━"))
        print(f"{'Artista':<20} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas disponibles':<9}")
        for evento in artista_encontrado: 
            print(f"{evento['artista']:<20} {evento['estadio']:<20} {evento['fecha']:<12} {evento['hora']:<7} ${evento['precio']:<7} {evento['entradas']['disponibles']:<9}")
    else:
        print("No se encontraron eventos para", artista)


# MENÚS PRINCIPALES


def mostrar_menu():
    """Muestra el menú principal"""

    titulo = "\n ★   MENÚ PRINCIPAL  "
    print(titulo.ljust(40, "━"))
    print("1. Administración de eventos")
    print("2. Administración de entradas")
    print("3. Ver ventas registradas")
    print("4. Salir")
    



def menu_eventos():
    """Muestra el menú de administración de eventos"""

    eventos = cargar_eventos_desde_archivo()

    titulo = "\n ★   MENÚ EVENTOS  "
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
    print("\n")
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
        print("\n")
        indice = validar_indice(len(eventos), input("Seleccione el evento a modificar: "))
        print("\n")
        continuar = True
        while continuar:
            print("1. Artista\n2. Estadio\n3. Fecha\n4. Hora\n5. Precio\n6. Cantidad de entradas\n7. Salir")
            print("\n")
            opcion_mod = validar_numero(input("¿Qué desea modificar?: ")) - 1
            while opcion_mod < 0 or opcion_mod > 6: 
                opcion_mod = validar_numero(input("Opción inválida. Ingrese una opción válida: ")) - 1
            if opcion_mod != 6: 
                print("\n")
                nuevo_valor = input("Ingrese el nuevo valor: ")
                print("\n")
                modificar_evento(eventos, indice, opcion_mod, nuevo_valor)
                print("\n")
            else:
                continuar = False
    elif opcion_eventos == 4:
        mostrar_eventos(eventos)
        print("\n")
        indice = validar_indice(len(eventos), input("Ingrese el índice del evento a eliminar: "))
        print("\n")
        eliminar_evento(eventos, indice)
    if opcion_eventos != 5:
        print("\n")
        menu_eventos()


def menu_entradas():
    """Muestra el menú de administración de entradas"""

    ventas = mostrar_ventas_guardadas()
    eventos = cargar_eventos_desde_archivo()

    titulo = "\n ★   MENÚ ENTRADAS  "
    print(titulo.ljust(40, "━"))
    print("1. Vender entrada")
    print("2. Cancelar entrada")
    print("3. Ver entradas vendidas")
    print("4. Análisis de datos")
    print("5. Volver al menú principal")
    print("".ljust(40, "━"))
    print("\n")

    opcion_entradas = validar_numero(input("Elija una opción: "))-1
    print("\n")
    while opcion_entradas < 0 or opcion_entradas > 4:
        opcion_entradas = validar_numero(input("Opción inválida. Ingrese una opción válida: "))-1
    if opcion_entradas == 0:
        mostrar_eventos(eventos)
        indice = validar_indice(len(eventos), input("Ingrese el índice del evento: "))
        print("\n")
        nombre = validar_no_es_vacio(input("Ingrese su nombre: "))
        apellido = validar_no_es_vacio(input("Ingrese su apellido: "))
        email = validar_email(input("Ingrese su email: "))
        numero_de_tramite = validar_numero_tramite(input("Ingrese su número de tramite: "))
        cantidad_entradas = validar_numero(input("Cantidad de entradas a vender: "))
        vender_entrada(eventos, indice, nombre, apellido, email, numero_de_tramite, cantidad_entradas)
    elif opcion_entradas == 1:
        email = validar_email(input("Ingrese su email: "))
        numero_de_tramite = validar_numero_tramite(input("Ingrese su número de tramite: "))
        factura = validar_numero(input("Ingrese su número de factura: "))
        cantidad = validar_numero(input("Cantidad de entradas a cancelar: "))
        cancelar_entrada(eventos, ventas, email, numero_de_tramite, factura, cantidad)
        ventas = mostrar_ventas_guardadas()
    elif opcion_entradas == 2:
        ver_entradas_vendidas(eventos)
    elif opcion_entradas == 3:
        analisis_datos(eventos)
    if opcion_entradas != 4:
        menu_entradas()
        


# PROGRAMA PRINCIPAL


print("\n")
titulo = "  SISTEMA DE GESTIÓN DE EVENTOS  "
print(titulo.center(100, "━"))
mostrar_menu()
print("".ljust(40, "━"))
print("\n")
opcion = validar_numero(input("Elija una opción: "))-1
print("\n")

while opcion != 3:
    if opcion == 0:
        menu_eventos()
    elif opcion == 1:
        menu_entradas()
    elif opcion == 2:
        ventas = mostrar_ventas_guardadas()
        mostrar_ventas(ventas)
    else:
        print("Opción inválida. Intente nuevamente.")
    mostrar_menu()
    print("".ljust(40, "━"))
    print("\n")
    opcion = validar_numero(input("Elija una opción: "))-1

print("¡Chau!")
