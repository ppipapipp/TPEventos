from datetime import datetime

# FUNCIONES DE ARCHIVOS Y GUARDADO DE DATOS
import os

EVENTOS_FILE = "eventos.txt"
VENTAS_FILE = "ventas.txt"
TEMP_FILE = "temp.txt"


def evento_seleccionado(linea):
    """Convierte una línea de texto en un dict evento o devuelve None si formato inválido."""
    linea = linea.strip()
    if linea == " ":
        return None
    partes = linea.split(";")
    artista, estadio, fecha, hora, precio, total, disponibles = partes
    try:
        return {
            "artista": artista,
            "estadio": estadio,
            "fecha": fecha, 
            "hora": hora,     
            "precio": int(precio),
            "entradas": {
                "total": int(total),
                "disponibles": int(disponibles)
            }
        }
    except ValueError:
        return None
#.-.
def evento_a_linea(evento):
    """Convierte un dict evento en la línea del archivo."""
    return f"{evento['artista']};{evento['estadio']};{evento['fecha']};{evento['hora']};{evento['precio']};{evento['entradas']['total']};{evento['entradas']['disponibles']}"

def cantidad_de_eventos():
    """Cuenta cuántas líneas válidas de evento hay en el archivo (sin cargarlas)."""
    cuenta = 0
    try:
        arch = open("eventos.txt", "rt")
        linea = arch.readline()
        while linea != "":
            if evento_seleccionado(linea) is not None:
                cuenta += 1
    except FileNotFoundError:
        return 0
    except OSError as e:
        print("Error al contar eventos:", e)
        return 0
    return cuenta

def obtener_evento_por_indice(indice_a_buscar):
    """Devuelve el evento (dict) correspondiente al índice (0-based) o None si no existe."""
    try:
        arch = open("eventos.txt", "rt")
        linea = arch.readline()
        indice = 1
        while linea != "":
            if indice == indice_a_buscar:
                arch.close()
                return linea.strip()
            linea = arch.readline()
            indice += 1
            evento = evento_seleccionado(linea)
            if evento is not None:
                if numero_linea == indice_a_buscar:
                    return evento
                numero_linea += 1
    except FileNotFoundError:
        return None
    except OSError as e:
        print("Error al leer eventos:", e)
        return None
    return None

# -----------------------
# Mostrar / Buscar
# -----------------------

def mostrar_eventos():
    """Muestra todos los eventos leyendo línea por línea."""
    try:
        arch = open("eventos.txt", "rt")
        titulo = "\n▶   LISTA DE EVENTOS "
        print(titulo.ljust(40, "━"))
        print(f"{'N°':<3} {'Artista':<20} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas disponibles':<9}")
        print("━" * 90)

        linea = arch.readline()
        numero = 1

        while linea != "":
            linea = linea.strip()
            partes = linea.split(";")

            if len(partes) == 7:
                artista, estadio, fecha, hora, precio, total, disponibles = partes

                print(f"{numero:<3} {artista:<20} {estadio:<20} {fecha:<12} {hora:<7} ${precio:<8} {disponibles}")

                numero += 1
            linea = arch.readline()
        arch.close()
        print("\n")
    except FileNotFoundError as mensaje:
        print("No se pudo abrir el archivo:", mensaje)
    except OSError as mensaje:
            print("No se puede leer el archivo:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass


#en busqueda artista, ver el tema de como se imprimen los eventos encontrados
def busqueda_artista(artista):
    """Busca eventos por artista y los muestra"""
    try:
        arch= open("eventos.txt", "rt")
        linea=arch.readline()
        artista = artista.lower()
        encontrado = False 
        while linea!="":
            evento = evento_seleccionado(linea)
            if artista in evento['artista'].lower():
                encontrado = True
                titulo = "\n▶  Eventos encontrados: "
                print(titulo.ljust(40, "━"))
                print(f"{'Artista':<20} {'Estadio':<20} {'Fecha':<12} {'Hora':<7} {'Precio':<8} {'Entradas disponibles':<9}")
                print(f"{evento['artista']:<20} {evento['estadio']:<20} {evento['fecha']:<12} {evento['hora']:<7} ${evento['precio']:<7} {evento['entradas']['disponibles']:<9}")
            linea=arch.readline() 
        #podemos usar if not ya que encontrado es booliano
        if not encontrado: 
            print("No se encontraron eventos para", artista)
    except FileNotFoundError as mensaje:
        print("No se pudo abrir el archivo:", mensaje)
    except OSError as mensaje:
            print("No se puede leer el archivo:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass

# -----------------------
# Crear (append)
# -----------------------

def crear_evento(artista, estadio, fecha, hora, precio, cantidad):
    """Agrega un nuevo evento al final del archivo (append)."""
    # Verificar si ya existe un evento con mismo artista y misma fecha (scan línea por línea)
    try:
        arch = open("eventos.txt", "rt")
        linea = arch.readline()
        while linea != " ":
            e = evento_seleccionado(linea)
            if e is not None and e['artista'] == artista and e['fecha'] == fecha:
                print("Error, ya existe un evento con ese artista en esa fecha.")
                return
    except FileNotFoundError:
        # si no existe el archivo, lo creamos luego al escribir
        pass
    except OSError as err:
        print("Error al leer eventos:", err)
        return

    nuevo_evento = {
        "artista": artista,
        "estadio": estadio,
        "fecha": fecha,
        "hora": hora,
        "precio": precio,
        "entradas": {"total": cantidad, "disponibles": cantidad}
    }

    try:
        with open(EVENTOS_FILE, "at", encoding="utf-8") as f:
            f.write(evento_a_linea(nuevo_evento) + "\n")
        print("Evento creado con éxito.")
    except OSError as err:
        print("ERROR al guardar el evento:", err)

# -----------------------
# Modificar / Eliminar (stream + temp)
# -----------------------

def modificar_evento_en_archivo(indice_objetivo, campo, nuevo_valor):
    """
    Modifica un atributo del evento en la línea índice_objetivo (0-based entre líneas válidas).
    campo: 'artista', 'estadio', 'fecha', 'hora', 'precio', 'total_entradas'
    """
    encontrado = False
    numero_linea = 0
    try:
        entrada = open("eventos.txt","rt")
        salida = open("temp.txt","wt")
        k = 0
        for linea in entrada:
            evento = evento_seleccionado(linea)
            if evento is None:
                salida.write(linea)  # copia línea no válida tal cual
                continue
            if numero_linea == indice_objetivo:
                encontrado = True
                # aplicar modificación
                if campo == 'artista':
                    evento['artista'] = nuevo_valor.strip() or evento['artista']
                elif campo == 'estadio':
                    evento['estadio'] = nuevo_valor.strip() or evento['estadio']
                elif campo == 'fecha':
                    try:
                        datetime.strptime(nuevo_valor, "%Y-%m-%d")
                        evento['fecha'] = nuevo_valor
                    except Exception:
                        print("Formato de fecha inválido. No se modificó.")
                elif campo == 'hora':
                    try:
                        datetime.strptime(nuevo_valor, "%H:%M")
                        evento['hora'] = nuevo_valor
                    except Exception:
                        print("Formato de hora inválido. No se modificó.")
                elif campo == 'precio':
                    try:
                        evento['precio'] = int(nuevo_valor)
                    except ValueError:
                        print("Precio inválido. No se modificó.")
                elif campo == 'total_entradas':
                    try:
                        nuevo_total = int(nuevo_valor)
                        vendidas = evento['entradas']['total'] - evento['entradas']['disponibles']
                        if nuevo_total < vendidas:
                            print("La nueva cantidad no puede ser menor a las entradas ya vendidas. No se modificó.")
                        else:
                            diferencia = nuevo_total - evento['entradas']['total']
                            evento['entradas']['total'] = nuevo_total
                            evento['entradas']['disponibles'] += diferencia
                    except ValueError:
                        print("Cantidad inválida. No se modificó.")
                # escribir línea modificada
                salida.write(evento_a_linea(evento) + "\n")
            else:
                salida.write(linea)
            if evento is not None:
                numero_linea += 1
    
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except OSError as mensaje:
        print("ERROR: ", mensaje)
    else:
        print("Copia finalizada. Líneas copiadas:", k)
    finally:
        try:
            entrada.close( )
            salida.close( )
        except NameError:
            pass

    if not encontrado:
        try:
            os.remove(TEMP_FILE)
        except OSError:
            pass
        print("Índice no encontrado. No se hicieron cambios.")
        return

    try:
        os.replace(TEMP_FILE, EVENTOS_FILE)  # atómico en muchos SO
    except OSError as e:
        print("Error al reemplazar archivo:", e)
        return

    print("Evento modificado con éxito.")

def eliminar_evento_en_archivo(indice_objetivo):
    """Elimina la línea de evento correspondiente al índice (0-based entre líneas válidas)."""
    encontrado = False
    numero_linea = 0
    try:
        with open(EVENTOS_FILE, "rt", encoding="utf-8") as entrada, open(TEMP_FILE, "wt", encoding="utf-8") as salida:
            for linea in entrada:
                evento = evento_seleccionado(linea)
                if evento is None:
                    salida.write(linea)
                    continue
                if numero_linea == indice_objetivo:
                    encontrado = True
                    # omitimos escribirla --> la eliminamos
                else:
                    salida.write(linea)
                numero_linea += 1
    except FileNotFoundError:
        print("No existe el archivo de eventos.")
        return
    except OSError as e:
        print("Error al eliminar evento:", e)
        return

    if not encontrado:
        try:
            os.remove(TEMP_FILE)
        except OSError:
            pass
        print("Índice no encontrado. No se eliminó nada.")
        return

    try:
        os.replace(TEMP_FILE, EVENTOS_FILE)
    except OSError as e:
        print("Error al reemplazar archivo:", e)
        return

    print("Evento eliminado con éxito.")

# -----------------------
# VENTAS (sin cargar todo)
# -----------------------

def guardar_venta_en_archivo(venta):
    """Agrega una venta (o cancelación como venta negativa) al archivo ventas.txt"""
    try:
        with open(VENTAS_FILE, "at", encoding="utf-8") as f:
            # formato: indice;nombre;apellido;email;numero_de_DNI;numero_entradas;numero_factura
            f.write(f"{venta['indice']};{venta['nombre']};{venta['apellido']};{venta['email']};{venta['numero_de_DNI']};{venta['numero_entradas']};{venta['numero_factura']}\n")
    except OSError as e:
        print("ERROR al registrar la venta:", e)
    else:
        print("Venta registrada correctamente.")

def obtener_siguiente_factura():
    """Calcula el número de factura siguiente buscando el max en ventas.txt sin cargar todo."""
    max_factura = 0
    try:
        with open(VENTAS_FILE, "rt", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea == " ":
                    continue
                partes = linea.split(";")
                if len(partes) != 7:
                    continue
                try:
                    factura = int(partes[6])
                    if factura > max_factura:
                        max_factura = factura
                except ValueError:
                    continue
    except FileNotFoundError:
        return 1
    except OSError as e:
        print("Error al leer ventas:", e)
        return max_factura + 1
    return max_factura + 1

def buscar_venta_por_email_factura(email, factura):
    """Busca una venta que coincida con email y número de factura. Devuelve dict o None."""
    try:
        arch = open("eventos.txt", "rt")
        while linea != " ":
                linea = linea.strip()
                partes = linea.split(";")
                if len(partes) != 7:
                    continue
                try:
                    indice = int(partes[0])
                    nombre = partes[1]
                    apellido = partes[2]
                    email_cl = partes[3]
                    numero_de_DNI = partes[4]
                    num_entradas = int(partes[5])
                    num_factura = int(partes[6])
                except ValueError:
                    continue
                if email_cl == email and num_factura == factura:
                    return {"indice": indice, "nombre": nombre, "apellido": apellido, "email": email_cl, "numero_de_DNI": numero_de_DNI, "numero_entradas": num_entradas, "numero_factura": num_factura}
    except FileNotFoundError:
        return None
    except OSError as e:
        print("Error al leer ventas:", e)
        return None
    return None

def mostrar_ventas_guardadas():
    """Muestra ventas leyendo ventas.txt línea por línea (no devuelve lista)."""
    tiene = False
    print("\n▶   LISTA DE VENTAS ".ljust(40, "━"))
    header = f"{'N°':<3} {'Nombre':<15} {'Apellido':<15} {'Email':<25} {'Trámite':<18} {'Entradas':<9} {'Factura':<9}"
    print(header)
    num = 0
    try:
        entrada = open("eventos.txt","rt")
        for linea in entrada:
            linea = linea.strip()
            if linea == " ":
                continue
            partes = linea.split(";")
            if len(partes) != 7:
                continue
            try:
                num += 1
                nombre = partes[1]
                apellido = partes[2]
                email = partes[3]
                numero_de_DNI = partes[4]
                cantidad = partes[5]
                factura = partes[6]
                tiene = True
                print(f"{num:<3} {nombre:<15} {apellido:<15} {email:<25} {numero_de_DNI:<18} {cantidad:<9} {factura:<9}")
            except Exception:
                continue
    except FileNotFoundError:
        print("No hay ventas registradas.")
        return
    except OSError as e:
        print("Error al leer ventas:", e)
        return

    if not tiene:
        print("No hay ventas registradas.")
    print("\n")

# -----------------------
# Operaciones de venta y cancelación
# -----------------------

def vender_entrada_por_indice(indice_evento, nombre, apellido, email, numero_de_DNI, cantidad_entradas):
    """Vende entradas de un evento identificado por índice (0-based). No carga eventos en memoria."""
    try:
        cantidad_entradas = int(cantidad_entradas)
    except ValueError:
        print("Cantidad inválida.")
        return

    if cantidad_entradas > 6:
        print("No se pueden vender más de 6 entradas por persona.")
        return

    # Buscamos el evento y simultáneamente creamos un temp con la línea modificada
    encontrado = False
    num_evento = 0
    factura = obtener_siguiente_factura()

    try:
        with open(EVENTOS_FILE, "rt", encoding="utf-8") as entrada, open(TEMP_FILE, "wt", encoding="utf-8") as salida:
            for linea in entrada:
                evento = evento_seleccionado(linea)
                if evento is None:
                    salida.write(linea)
                    continue
                if num_evento == indice_evento:
                    encontrado = True
                    if evento['entradas']['disponibles'] >= cantidad_entradas:
                        evento['entradas']['disponibles'] -= cantidad_entradas
                        salida.write(evento_a_linea(evento) + "\n")
                        venta = {
                            "indice": indice_evento,
                            "nombre": nombre,
                            "apellido": apellido,
                            "email": email,
                            "numero_de_DNI": numero_de_DNI,
                            "numero_entradas": cantidad_entradas,
                            "numero_factura": factura
                        }
                        # registramos la venta (append)
                        guardar_venta_en_archivo(venta)
                        # imprimimos factura
                        imprimir_factura(factura, nombre, apellido, email, numero_de_DNI, cantidad_entradas)
                        print(f"Vendidas {cantidad_entradas} entradas para {evento['artista']}.")
                    elif evento['entradas']['disponibles'] == 0:
                        salida.write(linea)  # sin cambios
                        print("El evento está agotado.")
                    else:
                        salida.write(linea)
                        print("No hay suficientes entradas disponibles.")
                else:
                    salida.write(linea)
                num_evento += 1
    except FileNotFoundError:
        print("No existe el archivo de eventos.")
        return
    except OSError as e:
        print("Error al procesar la venta:", e)
        return

    if not encontrado:
        try:
            os.remove(TEMP_FILE)
        except OSError:
            pass
        print("Índice de evento no encontrado. No se realizó la venta.")
        return

    try:
        os.replace(TEMP_FILE, EVENTOS_FILE)
    except OSError as e:
        print("Error al guardar cambios en eventos:", e)
        return

def cancelar_entrada_por_email_factura(email, numero_de_DNI, factura, cantidad):
    """Cancela entradas: busca la venta por email+factura y, si existe y cantidad válida, registra la cancelación y actualiza stock."""
    try:
        factura = int(factura)
        cantidad = int(cantidad)
    except ValueError:
        print("Factura o cantidad inválida.")
        return

    venta = buscar_venta_por_email_factura(email, factura)
    if venta is None:
        print("No hay entradas vendidas bajo ese mail o número de factura.")
        return

    if cantidad > abs(venta['numero_entradas']):  # numero_entradas >0 para venta original
        print("No puede cancelar más entradas de las que compró.")
        return

    indice_evento = venta['indice']

    # Primero actualizamos el archivo de eventos (sumamos stock)
    encontrado = False
    num_evento = 0
    try:
        with open(EVENTOS_FILE, "rt", encoding="utf-8") as entrada, open(TEMP_FILE, "wt", encoding="utf-8") as salida:
            for linea in entrada:
                evento = evento_seleccionado(linea)
                if evento is None:
                    salida.write(linea)
                    continue
                if num_evento == indice_evento:
                    encontrado = True
                    evento['entradas']['disponibles'] += cantidad
                    salida.write(evento_a_linea(evento) + "\n")
                else:
                    salida.write(linea)
                num_evento += 1
    except FileNotFoundError:
        print("No existe archivo de eventos.")
        return
    except OSError as e:
        print("Error al actualizar eventos en la cancelación:", e)
        return

    if not encontrado:
        try:
            os.remove(TEMP_FILE)
        except OSError:
            pass
        print("Evento vinculado a la venta no encontrado.")
        return

    try:
        os.replace(TEMP_FILE, EVENTOS_FILE)
    except OSError as e:
        print("Error al guardar eventos:", e)
        return

    # Segundo: registrar la cancelación como una venta con numero_entradas negativo
    nueva_venta = {
        "indice": indice_evento,
        "nombre": venta['nombre'],
        "apellido": venta['apellido'],
        "email": email,
        "numero_de_DNI": numero_de_DNI,
        "numero_entradas": -cantidad,
        "numero_factura": factura
    }
    guardar_venta_en_archivo(nueva_venta)
    print(f"Se cancelaron {cantidad} entradas del evento correctamente.")

# -----------------------
# Utilidades de validación (adaptadas)
# -----------------------

def validar_no_es_vacio(cadena):
    cadena = cadena or ""
    while cadena.strip() == "":
        cadena = input("El valor no puede estar vacío. Ingrese nuevamente: ").strip()
    return cadena

def validar_indice(cant_eventos, indice_texto):
    """Valida que índice sea entero entre 1 y cant_eventos. Devuelve índice 0-based."""
    indice_texto = validar_no_es_vacio(indice_texto)
    while not indice_texto.isdigit() or int(indice_texto) <= 0 or int(indice_texto) > cant_eventos:
        indice_texto = input("Ingrese un índice válido: ")
    return int(indice_texto) - 1

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
    valor = validar_no_es_vacio(valor)
    while not valor.isdigit() or int(valor) <= 0:
        valor = input("El valor debe ser un número positivo. Ingrese nuevamente: ")
    return int(valor)

def validar_hora(hora):
    hora = validar_no_es_vacio(hora)
    while True:
        try:
            datetime.strptime(hora, "%H:%M")
            return hora
        except Exception:
            hora = input("Error, formato de hora inválido. Ingrese nuevamente (HH:MM): ")

def validar_numero_de_DNI(numero_de_DNI):
    numero_de_DNI = validar_no_es_vacio(numero_de_DNI)
    while not numero_de_DNI.isdigit() or len(str(numero_de_DNI)) != 15:
        numero_de_DNI = input("Número de trámite inválido. Ingrese su número de trámite de 15 dígitos: ")
    return numero_de_DNI

def validar_email(email):
    email = validar_no_es_vacio(email)
    while "@" not in email or "." not in email.split("@")[-1]:
        email = input("Email inválido. Ingrese un email válido: ")
    return email

# -----------------------
# Impresión de factura
# -----------------------

def imprimir_factura(factura, nombre, apellido, email, numero_de_DNI, cantidad_entradas):
    print("\n" + " FACTURA ".center(40, "━"))
    print("Número de factura: ", factura)
    print("Nombre: ", nombre)
    print("Apellido: ", apellido)
    print("Email: ", email)
    print("Número de DNI: ", numero_de_DNI)
    print("Cantidad de entradas compradas: ", cantidad_entradas)
    print("".ljust(40, "━") + "\n")

# -----------------------
# Menús (adaptados para no cargar listas)
# -----------------------

def mostrar_menu():
    titulo = "\n ★   MENÚ PRINCIPAL  "
    print(titulo.ljust(40, "━"))
    print("1. Administración de eventos")
    print("2. Administración de entradas")
    print("3. Ver ventas registradas")
    print("4. Salir")

def menu_eventos():
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

    if opcion_eventos == 0:
        mostrar_eventos()
    elif opcion_eventos == 1:
        artista = validar_no_es_vacio(input("Ingrese el nombre del artista a buscar: "))
        busqueda_artista(artista)
    elif opcion_eventos == 2:
        artista = validar_no_es_vacio(input("Ingrese el nombre del artista: "))
        estadio = validar_no_es_vacio(input("Ingrese el nombre del estadio: "))
        fecha = validar_fecha(input("Ingrese la fecha del evento (YYYY-MM-DD): "))
        hora = validar_hora(input("Ingrese la hora del evento (HH:MM): "))
        precio = validar_numero(input("Ingrese el precio de la entrada: "))
        cantidad = validar_numero(input("Ingrese la cantidad de entradas disponibles: "))
        crear_evento(artista, estadio, fecha, hora, precio, cantidad)
    elif opcion_eventos == 3:
        total = cantidad_de_eventos()
        if total == 0:
            print("No hay eventos para modificar.")
        else:
            mostrar_eventos()
            indice = validar_indice(total, input("Seleccione el evento a modificar: "))
            print("\nOpciones: 1.Artista 2.Estadio 3.Fecha 4.Hora 5.Precio 6.Cantidad de entradas 7.Salir")
            opcion_mod = validar_numero(input("¿Qué desea modificar?: ")) - 1
            while opcion_mod < 0 or opcion_mod > 6:
                opcion_mod = validar_numero(input("Opción inválida. Ingrese una opción válida: ")) - 1
            if opcion_mod != 6:
                nuevo_valor = input("Ingrese el nuevo valor: ")
                campos = {0: 'artista', 1: 'estadio', 2: 'fecha', 3: 'hora', 4: 'precio', 5: 'total_entradas'}
                modificar_evento_en_archivo(indice, campos[opcion_mod], nuevo_valor)
    elif opcion_eventos == 4:
        total = cantidad_de_eventos()
        if total == 0:
            print("No hay eventos para eliminar.")
        else:
            mostrar_eventos()
            indice = validar_indice(total, input("Ingrese el índice del evento a eliminar: "))
            eliminar_evento_en_archivo(indice)
    if opcion_eventos != 5:
        print("\n")
        menu_eventos()

def menu_entradas():
    titulo = "\n ★   MENÚ ENTRADAS  "
    print(titulo.ljust(40, "━"))
    print("1. Vender entrada")
    print("2. Cancelar entrada")
    print("3. Ver entradas vendidas (por evento)")
    print("4. Análisis de datos")
    print("5. Ver ventas registradas")
    print("6. Volver al menú principal")
    print("".ljust(40, "━"))
    print("\n")

    opcion_entradas = validar_numero(input("Elija una opción: ")) - 1
    print("\n")
    while opcion_entradas < 0 or opcion_entradas > 5:
        opcion_entradas = validar_numero(input("Opción inválida. Ingrese una opción válida: ")) - 1

    if opcion_entradas == 0:
        mostrar_eventos()
        total = cantidad_de_eventos()
        if total == 0:
            print("No hay eventos para vender entradas.")
        else:
            indice = validar_indice(total, input("Ingrese el índice del evento: "))
            print("\n")
            nombre = validar_no_es_vacio(input("Ingrese su nombre: "))
            apellido = validar_no_es_vacio(input("Ingrese su apellido: "))
            email = validar_email(input("Ingrese su email: "))
            numero_de_DNI = validar_numero_de_DNI(input("Ingrese su número de DNI: "))
            cantidad_entradas = validar_numero(input("Cantidad de entradas a vender: "))
            vender_entrada_por_indice(indice, nombre, apellido, email, numero_de_DNI, cantidad_entradas)
    elif opcion_entradas == 1:
        email = validar_email(input("Ingrese su email: "))
        numero_de_DNI = validar_numero_de_DNI(input("Ingrese su número de DNI: "))
        factura = validar_numero(input("Ingrese su número de factura: "))
        cantidad = validar_numero(input("Cantidad de entradas a cancelar: "))
        cancelar_entrada_por_email_factura(email, numero_de_DNI, factura, cantidad)
    elif opcion_entradas == 2:
        # Ver entradas vendidas por evento (leyendo eventos sin lista)
        print("\n  ENTRADAS VENDIDAS POR EVENTO ".ljust(60, "━"))
        try:
            with open(EVENTOS_FILE, "rt", encoding="utf-8") as f:
                for linea in f:
                    e = evento_seleccionado(linea)
                    if e is not None:
                        vendidas = e['entradas']['total'] - e['entradas']['disponibles']
                        print(f"{e['artista']:<25} {vendidas:<15} {e['entradas']['disponibles']:<15}")
        except FileNotFoundError:
            print("No hay eventos registrados.")
        except OSError as e:
            print("Error al leer eventos:", e)
    elif opcion_entradas == 3:
        # Analisis de datos: hay que recorrer los eventos y computar sumas sin cargar lista.
        total_eventos = 0
        total_vendidas = 0
        total_recaudado = 0
        max_vendidas = 0
        mas_vendidos = []
        try:
            with open(EVENTOS_FILE, "rt", encoding="utf-8") as f:
                for linea in f:
                    e = evento_seleccionado(linea)
                    if e is None:
                        continue
                    total_eventos += 1
                    vendidas = e['entradas']['total'] - e['entradas']['disponibles']
                    total_vendidas += vendidas
                    total_recaudado += vendidas * e['precio']
                    if vendidas > max_vendidas:
                        max_vendidas = vendidas
                        mas_vendidos = [e]
                    elif vendidas == max_vendidas:
                        mas_vendidos.append(e)
        except FileNotFoundError:
            print("No hay eventos registrados.")
            return
        except OSError as e:
            print("Error al leer eventos:", e)
            return

        if total_eventos == 0 or total_vendidas == 0:
            print("No se han vendido entradas aún.")
            return

        promedio = total_vendidas / total_eventos
        titulo = "\n▶   ANÁLISIS DE DATOS "
        print(titulo.ljust(60, "━"))
        print(f"{'Total recaudado:':<35} ${total_recaudado}")
        print(f"{'Total de entradas vendidas:':<35} {total_vendidas}")
        print(f"{'Promedio de entradas vendidas:':<35} {promedio:.2f}")
        print("━" * 60)
        if len(mas_vendidos) > 1:
            print(f"\nEmpate entre {len(mas_vendidos)} eventos más vendidos:")
        else:
            print("\nEvento más vendido:")
        for e in mas_vendidos:
            vendidas = e['entradas']['total'] - e['entradas']['disponibles']
            print(f"- {e['artista']} ({vendidas} entradas vendidas)")
    elif opcion_entradas == 4:
        mostrar_ventas_guardadas()

    if opcion_entradas != 5:
        print("\n")
        menu_entradas()

# -----------------------
# Programa principal
# -----------------------

def main():
    print("\n")
    titulo = "  SISTEMA DE GESTIÓN DE EVENTOS  "
    print(titulo.center(100, "━"))
    mostrar_menu()
    print("".ljust(40, "━"))
    print("\n")
    opcion = validar_numero(input("Elija una opción: ")) - 1
    print("\n")

    while opcion != 3:
        if opcion == 0:
            menu_eventos()
        elif opcion == 1:
            menu_entradas()
        elif opcion == 2:
            mostrar_ventas_guardadas()
        else:
            print("Opción inválida. Intente nuevamente.")
        mostrar_menu()
        print("".ljust(40, "━"))
        print("\n")
        opcion = validar_numero(input("Elija una opción: ")) - 1

    print("¡Chau!")

    main()

