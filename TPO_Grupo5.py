from datetime import datetime

# FUNCIONES DE ARCHIVOS Y GUARDADO DE DATOS

def guardar_nuevo_evento(evento):
    """Guarda solo un registro en eventos en 'eventos.txt'"""

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
        arch.write(f"{venta['indice']};{venta['nombre']};{venta['apellido']};{venta['email']};{venta['numero_dni']};{venta['numero_entradas']};{venta['numero_factura']}\n")
    except OSError as mensaje:
        print("ERROR al registrar la venta:", mensaje)
    else:
        print("Venta registrada correctamente.")
    finally:
        try:
            arch.close()
        except NameError:
            pass


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
    return int(indice) - 1


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


def validar_numero_dni(numero_dni):
    """Valida que el numero_dni tenga 8 dígitos"""

    validar_numero(numero_dni)
    while len(str(numero_dni)) != 8:
        numero_dni = validar_numero(input("Número de DNI inválido. Ingrese un número de 8 dígitos: "))
    return numero_dni


def validar_email(email):
    """Valida que el email ingresado tenga un formato básico válido"""

    validar_no_es_vacio(email)
    while "@" not in email or "." not in email.split("@")[-1]:
        email = input("Email inválido. Ingrese un email válido: ")
    return email


# FUNCIONES RECURSIVAS PARA CÁLCULOS

def contar_entradas_vendidas_recursivo(arch, acumulador=0):
    """Cuenta recursivamente el total de entradas vendidas leyendo el archivo línea por línea"""
    
    linea = arch.readline()
    if linea == "":
        return acumulador
    
    linea = linea.strip()
    if linea:
        partes = linea.split(";")
        if len(partes) == 7:
            try:
                total = int(partes[5])
                disponibles = int(partes[6])
                vendidas = total - disponibles
                return contar_entradas_vendidas_recursivo(arch, acumulador + vendidas)
            except ValueError:
                return contar_entradas_vendidas_recursivo(arch, acumulador)
    return contar_entradas_vendidas_recursivo(arch, acumulador)


def calcular_recaudacion_recursivo(arch, acumulador=0):
    """Calcula recursivamente la recaudación total leyendo el archivo línea por línea"""
    linea = arch.readline()
    if linea == "":
        return acumulador
    
    linea = linea.strip()
    if linea:
        partes = linea.split(";")
        if len(partes) == 7:
            try:
                precio = int(partes[4])
                total = int(partes[5])
                disponibles = int(partes[6])
                vendidas = total - disponibles
                recaudado = vendidas * precio
                return calcular_recaudacion_recursivo(arch, acumulador + recaudado)
            except ValueError:
                return calcular_recaudacion_recursivo(arch, acumulador)
    return calcular_recaudacion_recursivo(arch, acumulador)


def encontrar_mas_vendido_recursivo(arch, max_vendidas=0, artista_max=""):
    """Encuentra recursivamente el evento con más entradas vendidas"""
    linea = arch.readline()
    if linea == "":
        return max_vendidas, artista_max
    
    linea = linea.strip()
    if linea:
        partes = linea.split(";")
        if len(partes) == 7:
            try:
                artista = partes[0]
                total = int(partes[5])
                disponibles = int(partes[6])
                vendidas = total - disponibles
                if vendidas > max_vendidas:
                    return encontrar_mas_vendido_recursivo(arch, vendidas, artista)
            except ValueError:
                pass
    return encontrar_mas_vendido_recursivo(arch, max_vendidas, artista_max)


def contar_eventos_recursivo(arch, contador=0):
    """Cuenta recursivamente la cantidad de eventos en el archivo"""
    linea = arch.readline()
    if linea == "":
        return contador
    
    linea = linea.strip()
    if linea:
        partes = linea.split(";")
        if len(partes) == 7:
            return contar_eventos_recursivo(arch, contador + 1)
    return contar_eventos_recursivo(arch, contador)


def obtener_max_factura_recursivo(arch, max_actual=0):
    """Obtiene recursivamente el número de factura máximo"""
    linea = arch.readline()
    if linea == "":
        return max_actual
    
    linea = linea.strip()
    if linea:
        partes = linea.split(";")
        if len(partes) == 7:
            try:
                factura = int(partes[6])
                if factura > max_actual:
                    return obtener_max_factura_recursivo(arch, factura)
            except ValueError:
                pass
    return obtener_max_factura_recursivo(arch, max_actual)


# FUNCIONES PRINCIPALES

def mostrar_eventos():
    """Muestra la lista de eventos disponibles leyendo línea por línea"""
    try:
        arch = open("eventos.txt", "rt")
        titulo = "\n▶   LISTA DE EVENTOS "
        print(titulo.ljust(40, "━"))
        print(f"{'N°':<3} {'Artista':<20} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas disponibles':<9}")
        
        linea = arch.readline()
        encontrado = False
        
        while linea != "":
            linea = linea.strip()
            if linea:
                partes = linea.split(";")
                if len(partes) == 7:
                    artista, estadio, fecha, hora, precio, total, disponibles = partes
                    if artista.lower() in artista.lower():
                        print(f"{artista:<20} {estadio:<20} {fecha:<12} {hora:<7} ${precio:<7} {disponibles:<9}")
                        encontrado = True
            linea = arch.readline()
        
        if not encontrado:
            print("No se encontraron eventos para", artista)
        
        arch.close()
    except FileNotFoundError:
        print("No se encontraron eventos para", artista)
    except OSError as mensaje:
        print("Error al leer el archivo:", mensaje)


def mostrar_ventas():
    """Muestra la lista de ventas registradas leyendo línea por línea"""
    try:
        arch = open("ventas.txt", "rt")
        titulo = "\n▶   LISTA DE VENTAS "
        print(titulo.ljust(40, "━"))
        print(f"{'N°':<3} {'Nombre':<15} {'Apellido':<15} {'Email':<25} {'Trámite':<18} {'Entradas':<9} {'Factura':<9}")
        
        linea = arch.readline()
        numero = 1
        tiene_ventas = False
        
        while linea != "":
            linea = linea.strip()
            if linea:
                partes = linea.split(";")
                if len(partes) == 7:
                    numero, nombre, apellido, email, dni, cantidad, factura = partes
                    print(f"{numero:<3} {nombre:<15} {apellido:<15} {email:<25} {dni:<18} {cantidad:<9} {factura:<9}")
                    numero += 1
                    tiene_ventas = True
            linea = arch.readline()
        
        if not tiene_ventas:
            print("No hay ventas registradas.")
        print("\n")
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
        print("No hay ventas registradas.\n")
    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass


def contar_eventos():
    """Cuenta cuántos eventos hay en el archivo usando recursividad"""
    try:
        arch = open("eventos.txt", "rt")
        cantidad = contar_eventos_recursivo(arch)
        arch.close()
        return cantidad
    except FileNotFoundError:
        return 0
    except OSError:
        return 0


def crear_evento(artista, estadio, fecha, hora, precio, cantidad):
    """Crea un nuevo evento si no existe otro con el mismo artista en la misma fecha"""
    existe = False
    
    try:
        arch = open("eventos.txt", "rt")
        linea = arch.readline()
        
        while linea != "":
            linea = linea.strip()
            if linea:
                partes = linea.split(";")
                if len(partes) == 7:
                    artista_archivo = partes[0]
                    fecha_archivo = partes[2]
                    if artista_archivo.lower() == artista.lower() and fecha_archivo == fecha:
                        existe = True
                        break
            linea = arch.readline()
        arch.close()
    except FileNotFoundError:
        pass
    except OSError as mensaje:
        print("Error al leer el archivo:", mensaje)
        return
    
    if existe:
        print("Error, ya existe un evento con ese artista en esa fecha.")
        return 

    nuevo_evento = {"artista": artista, "estadio": estadio, "fecha": fecha, "hora": hora, "precio": precio, "entradas": {"total": cantidad, "disponibles": cantidad}}
    guardar_nuevo_evento(nuevo_evento)
    print("Evento creado con éxito.")


def modificar_evento(indice_objetivo, opcion, nuevo_valor):
    """Modifica un atributo específico de un evento"""
    try:
        entrada = open("eventos.txt", "rt")
        salida = open("temp.txt", "wt")
        numero_linea = 0
        encontrado = False
        
        linea = entrada.readline()
        while linea != "":
            linea_limpia = linea.strip()
            if linea_limpia:
                partes = linea_limpia.split(";")
                if len(partes) == 7:
                    if numero_linea == indice_objetivo:
                        encontrado = True
                        artista, estadio, fecha, hora, precio, total, disponibles = partes
                        
                        # Artista
                        if opcion == 0:
                            artista = validar_no_es_vacio(nuevo_valor)
                        # Estadio
                        elif opcion == 1:
                            estadio = validar_no_es_vacio(nuevo_valor)
                        # Fecha
                        elif opcion == 2:
                            fecha = validar_fecha(nuevo_valor)
                        # Hora
                        elif opcion == 3:
                            hora = validar_hora(nuevo_valor)
                        # Precio
                        elif opcion == 4:
                            precio = str(validar_numero(nuevo_valor))
                        # Cantidad de entradas
                        elif opcion == 5:
                            nuevo_total = validar_numero(nuevo_valor)
                            vendidas = int(total) - int(disponibles)
                            if nuevo_total < vendidas:
                                print("La nueva cantidad no puede ser menor a las entradas ya vendidas.")
                                salida.write(linea)
                            else:
                                diferencia = nuevo_total - int(total)
                                total = str(nuevo_total)
                                disponibles = str(int(disponibles) + diferencia)
                        
                        salida.write(f"{artista};{estadio};{fecha};{hora};{precio};{total};{disponibles}\n")
                    else:
                        salida.write(linea)
                    numero_linea += 1
                else:
                    salida.write(linea)
            else:
                salida.write(linea)
            linea = entrada.readline()
        
        entrada.close()
        salida.close()
        
        if encontrado:
            try:
                import os
                os.remove("eventos.txt")
                os.rename("temp.txt", "eventos.txt")
                print("\nEvento modificado con éxito.")
            except OSError as mensaje:
                print("Error al guardar cambios:", mensaje)
        else:
            import os
            os.remove("temp.txt")
            print("Evento no encontrado.")
            
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except OSError as mensaje:
        print("Error al modificar:", mensaje)


def eliminar_evento(indice_objetivo):
    """Elimina un evento de la lista de eventos"""
    try:
        entrada = open("eventos.txt", "rt")
        salida = open("temp.txt", "wt")
        numero_linea = 0
        encontrado = False
        artista_eliminado = ""
        
        linea = entrada.readline()
        while linea != "":
            linea_limpia = linea.strip()
            if linea_limpia:
                partes = linea_limpia.split(";")
                if len(partes) == 7:
                    if numero_linea == indice_objetivo:
                        encontrado = True
                        artista_eliminado = partes[0]
                    else:
                        salida.write(linea)
                    numero_linea += 1
                else:
                    salida.write(linea)
            else:
                salida.write(linea)
            linea = entrada.readline()
        
        entrada.close()
        salida.close()
        
        if encontrado:
            try:
                import os
                os.remove("eventos.txt")
                os.rename("temp.txt", "eventos.txt")
                print("Evento eliminado:", artista_eliminado)
            except OSError as mensaje:
                print("Error al guardar cambios:", mensaje)
        else:
            import os
            os.remove("temp.txt")
            print("Evento no encontrado.")
            
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except OSError as mensaje:
        print("Error al eliminar:", mensaje)


def obtener_siguiente_factura():
    """Devuelve el numero_factura siguiente usando recursividad"""
    try:
        arch = open("ventas.txt", "rt")
        max_factura = obtener_max_factura_recursivo(arch)
        arch.close()
        return max_factura + 1
    except FileNotFoundError:
        return 1
    except OSError:
        return 1


def imprimir_factura(factura, nombre, apellido, email, numero_dni, cantidad_entradas):
    """Imprime la factura de la compra realizada"""
    print("\n"+" FACTURA ".center(40, "━"))
    print("Número de factura: ", factura)
    print("Nombre: ", nombre)
    print("Apellido: ", apellido)
    print("Email: ", email)
    print("Número de trámite: ", numero_dni)
    print("Cantidad de entradas compradas: ", cantidad_entradas)
    print("".ljust(40, "━")+"\n")


def vender_entrada(indice_objetivo, nombre, apellido, email, numero_dni, cantidad_entradas):
    """Vende entradas de un evento, si hay suficientes disponibles"""
    while cantidad_entradas > 6:
        print("No se pueden vender más de 6 entradas por persona.")
        cantidad_entradas = validar_numero(input("Ingrese la cantidad de entradas a vender (máximo 6): "))

    try:
        entrada = open("eventos.txt", "rt")
        salida = open("temp.txt", "wt")
        numero_linea = 0
        encontrado = False
        venta_realizada = False
        
        linea = entrada.readline()
        while linea != "":
            linea_limpia = linea.strip()
            if linea_limpia:
                partes = linea_limpia.split(";")
                if len(partes) == 7:
                    if numero_linea == indice_objetivo:
                        encontrado = True
                        artista, estadio, fecha, hora, precio, total, disponibles = partes
                        disponibles_int = int(disponibles)
                        
                        if disponibles_int >= cantidad_entradas:
                            disponibles_int -= cantidad_entradas
                            salida.write(f"{artista};{estadio};{fecha};{hora};{precio};{total};{disponibles_int}\n")
                            
                            factura = obtener_siguiente_factura()
                            venta = {"indice": indice_objetivo, "nombre": nombre, "apellido": apellido, "email": email, "numero_dni": numero_dni, "numero_entradas": cantidad_entradas, "numero_factura": factura}
                            guardar_venta_en_archivo(venta)
                            
                            print("Vendidas", cantidad_entradas, "entradas para", artista)
                            imprimir_factura(factura, nombre, apellido, email, numero_dni, cantidad_entradas)
                            venta_realizada = True
                        elif disponibles_int == 0:
                            print("El evento de", artista, "está agotado.")
                            salida.write(linea)
                        else:
                            print("No hay suficientes entradas disponibles.")
                            salida.write(linea)
                    else:
                        salida.write(linea)
                    numero_linea += 1
                else:
                    salida.write(linea)
            else:
                salida.write(linea)
            linea = entrada.readline()
        
        entrada.close()
        salida.close()
        
        if encontrado and venta_realizada:
            try:
                import os
                os.remove("eventos.txt")
                os.rename("temp.txt", "eventos.txt")
            except OSError as mensaje:
                print("Error al guardar cambios:", mensaje)
        else:
            import os
            os.remove("temp.txt")
            if not encontrado:
                print("Evento no encontrado.")
                
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except OSError as mensaje:
        print("Error al vender:", mensaje)


def buscar_venta(email, factura):
    """Busca una venta por email y factura, devuelve el índice y cantidad"""
    try:
        arch = open("ventas.txt", "rt")
        linea = arch.readline()
        
        while linea != "":
            linea = linea.strip()
            if linea:
                partes = linea.split(";")
                if len(partes) == 7:
                    indice, nombre, apellido, email_v, dni, cantidad, factura_v = partes
                    if email_v == email and int(factura_v) == factura:
                        arch.close()
                        return int(indice), int(cantidad), nombre, apellido
            linea = arch.readline()
        
        arch.close()
        return None, None, None, None
    except FileNotFoundError:
        return None, None, None, None
    except OSError:
        return None, None, None, None


def cancelar_entrada(email, numero_dni, factura, cantidad):
    """Cancela entradas vendidas de un evento"""
    indice_evento, entradas_compradas, nombre, apellido = buscar_venta(email, factura)
    
    if indice_evento is None:
        print("No hay entradas vendidas bajo ese mail o número de factura.")
        return
    
    if cantidad > entradas_compradas:
        print("No puede cancelar más entradas de las que compró.")
        return
    
    # Actualizar archivo de eventos
    try:
        entrada = open("eventos.txt", "rt")
        salida = open("temp.txt", "wt")
        numero_linea = 0
        
        linea = entrada.readline()
        while linea != "":
            linea_limpia = linea.strip()
            if linea_limpia:
                partes = linea_limpia.split(";")
                if len(partes) == 7:
                    if numero_linea == indice_evento:
                        artista, estadio, fecha, hora, precio, total, disponibles = partes
                        disponibles_int = int(disponibles) + cantidad
                        salida.write(f"{artista};{estadio};{fecha};{hora};{precio};{total};{disponibles_int}\n")
                        artista_cancelado = artista
                    else:
                        salida.write(linea)
                    numero_linea += 1
                else:
                    salida.write(linea)
            else:
                salida.write(linea)
            linea = entrada.readline()
        
        entrada.close()
        salida.close()
        
        # Registrar cancelación
        nueva_venta = {"indice": indice_evento, "nombre": nombre, "apellido": apellido, "email": email, "numero_dni": numero_dni, "numero_entradas": -cantidad, "numero_factura": factura}
        guardar_venta_en_archivo(nueva_venta)
        
        print(f"Se cancelaron {cantidad} entradas del evento '{artista_cancelado}' correctamente.")
        
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except OSError as mensaje:
        print("Error al cancelar:", mensaje)


def ver_entradas_vendidas():
    """Muestra la cantidad de entradas vendidas por evento"""
    try:
        arch = open("eventos.txt", "rt")
        titulo = "\n  ENTRADAS VENDIDAS POR EVENTO "
        print(titulo.ljust(60, "━"))
        print(f"{'Artista':<25} {'Vendidas':<15} {'Disponibles':<15}")
        
        linea = arch.readline()
        tiene_eventos = False
        
        while linea != "":
            linea = linea.strip()
            if linea:
                partes = linea.split(";")
                if len(partes) == 7:
                    artista, estadio, fecha, hora, precio, total, disponibles = partes
                    vendidas = int(total) - int(disponibles)
                    print(f"{artista:<25} {vendidas:<15} {disponibles:<15}")
                    tiene_eventos = True
            linea = arch.readline()
        
        if not tiene_eventos:
            print("No hay eventos registrados.")
        print("\n")
        arch.close()
    except FileNotFoundError:
        print("No hay eventos registrados.\n")
    except OSError as mensaje:
        print("Error al leer el archivo:", mensaje)


def analisis_datos():
    """Realiza un análisis de datos sobre las ventas de entradas usando recursividad"""
    cantidad_eventos = contar_eventos()
    
    if cantidad_eventos == 0:
        print("No hay eventos registrados.")
        return
    
    try:
        # Calcular total vendidas
        arch = open("eventos.txt", "rt")
        total_vendidas = contar_entradas_vendidas_recursivo(arch)
        arch.close()
        
        if total_vendidas == 0:
            print("No se han vendido entradas aún.")
            return
        
        # Calcular recaudación
        arch = open("eventos.txt", "rt")
        total_recaudado = calcular_recaudacion_recursivo(arch)
        arch.close()
        
        # Calcular promedio
        promedio = total_vendidas / cantidad_eventos
        
        # Encontrar evento más vendido
        arch = open("eventos.txt", "rt")
        max_vendidas, artista_max = encontrar_mas_vendido_recursivo(arch)
        arch.close()
        
        titulo = "\n▶   ANÁLISIS DE DATOS "
        print(titulo.ljust(60, "━"))
        print(f"{'Total recaudado:':<35} ${total_recaudado}")
        print(f"{'Total de entradas vendidas:':<35} {total_vendidas}")
        print(f"{'Promedio de entradas vendidas:':<35} {promedio:.2f}")
        print("━" * 60)
        print("\nEvento más vendido:")
        print(f"- {artista_max} ({max_vendidas} entradas vendidas)")
        print("\n")
        
    except FileNotFoundError:
        print("No hay eventos registrados.")
    except OSError as mensaje:
        print("Error al leer el archivo:", mensaje)


def busqueda_artista(artista):
    """Busca eventos por artista y los muestra"""
    try:
        arch = open("eventos.txt", "rt")
        titulo = "\n▶  Eventos encontrados: "
        print(titulo.ljust(40, "━"))
        print(f"{'Artista':<20} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas disponibles':<9}")
        
        linea = arch.readline()
    except FileNotFoundError:
        print("No hay eventos registrados.")
    except OSError as mensaje:
        print("Error al leer el archivo:", mensaje)



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

    opcion_eventos = validar_numero(input("Elija una opción: ")) - 1
    print("\n")
    while opcion_eventos < 0 or opcion_eventos > 5:
        opcion_eventos = validar_numero(input("Opción inválida. Ingrese una opción válida: ")) - 1

    # Mostrar eventos
    if opcion_eventos == 0:
        mostrar_eventos()

    # Buscar evento por artista
    elif opcion_eventos == 1:
        artista = validar_no_es_vacio(input("Ingrese el nombre del artista a buscar: "))
        busqueda_artista(artista)

    # Crear evento
    elif opcion_eventos == 2:
        artista = validar_no_es_vacio(input("Ingrese el nombre del artista: "))
        estadio = validar_no_es_vacio(input("Ingrese el nombre del estadio: "))
        fecha = validar_fecha(input("Ingrese la fecha del evento (YYYY-MM-DD): "))
        hora = validar_hora(input("Ingrese la hora del evento (HH:MM): "))
        precio = validar_numero(input("Ingrese el precio de la entrada: "))
        cantidad = validar_numero(input("Ingrese la cantidad de entradas disponibles: "))
        crear_evento(artista, estadio, fecha, hora, precio, cantidad)

    # Modificar evento
    elif opcion_eventos == 3:
        mostrar_eventos()
        cantidad = contar_eventos()
        if cantidad > 0:
            print("\n")
            indice = validar_indice(cantidad, input("Seleccione el evento a modificar: "))
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
                    modificar_evento(indice, opcion_mod, nuevo_valor)
                    print("\n")
                else:
                    continuar = False

    # Eliminar evento
    elif opcion_eventos == 4:
        mostrar_eventos()
        cantidad = contar_eventos()
        if cantidad > 0:
            print("\n")
            indice = validar_indice(cantidad, input("Ingrese el índice del evento a eliminar: "))
            print("\n")
            eliminar_evento(indice)

    # Volver al menú
    if opcion_eventos != 5:
        print("\n")
        menu_eventos()


def menu_entradas():
    """Muestra el menú de administración de entradas"""

    titulo = "\n ★   MENÚ ENTRADAS  "
    print(titulo.ljust(40, "━"))
    print("1. Vender entrada")
    print("2. Cancelar entrada")
    print("3. Ver entradas vendidas")
    print("4. Análisis de datos")
    print("5. Volver al menú principal")
    print("".ljust(40, "━"))
    print("\n")

    opcion_entradas = validar_numero(input("Elija una opción: ")) - 1
    print("\n")
    while opcion_entradas < 0 or opcion_entradas > 4:
        opcion_entradas = validar_numero(input("Opción inválida. Ingrese una opción válida: ")) - 1

    # Vender entrada
    if opcion_entradas == 0:
        mostrar_eventos()
        cantidad = contar_eventos()
        if cantidad > 0:
            indice = validar_indice(cantidad, input("Ingrese el índice del evento: "))
            print("\n")
            nombre = validar_no_es_vacio(input("Ingrese su nombre: "))
            apellido = validar_no_es_vacio(input("Ingrese su apellido: "))
            email = validar_email(input("Ingrese su email: "))
            numero_dni = validar_numero_dni(input("Ingrese su número de DNI: "))
            cantidad_entradas = validar_numero(input("Cantidad de entradas a vender: "))
            vender_entrada(indice, nombre, apellido, email, numero_dni, cantidad_entradas)

    # Cancelar entrada
    elif opcion_entradas == 1:
        email = validar_email(input("Ingrese su email: "))
        numero_dni = validar_numero_dni(input("Ingrese su número de DNI: "))
        factura = validar_numero(input("Ingrese su número de factura: "))
        cantidad = validar_numero(input("Cantidad de entradas a cancelar: "))
        cancelar_entrada(email, numero_dni, factura, cantidad)

    # Ver entradas vendidas
    elif opcion_entradas == 2:
        ver_entradas_vendidas()

    # Análisis de datos
    elif opcion_entradas == 3:
        analisis_datos()

    # Volver al menú
    if opcion_entradas != 4:
        menu_entradas()


# PROGRAMA PRINCIPAL

print("\n")
titulo = "  SISTEMA DE GESTIÓN DE EVENTOS  "
print(titulo.center(100, "━"))
mostrar_menu()
print("".ljust(40, "━"))
print("\n")
opcion = validar_numero(input("Elija una opción: ")) - 1
print("\n")

while opcion != 3:
    # Menú de eventos
    if opcion == 0:
        menu_eventos()

    # Menú de entradas
    elif opcion == 1:
        menu_entradas()

    # Mostrar todas las ventas
    elif opcion == 2:
        mostrar_ventas()
    else:
        print("Opción inválida. Intente nuevamente.")
    
    mostrar_menu()
    print("".ljust(40, "━"))
    print("\n")
    opcion = validar_numero(input("Elija una opción: ")) - 1

print("¡Chau!")