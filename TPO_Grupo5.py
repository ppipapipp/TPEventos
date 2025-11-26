from datetime import datetime
import os 
import json 

# FUNCIONES DE ARCHIVOS Y GUARDADO DE DATOS

def guardar_nuevo_evento(evento):
    """Guarda un registro en formato JSON Line en 'eventos.jsonl'"""
    try:
        arch = open("eventos.jsonl", "a") 
        json.dump(evento, arch) 
        arch.write("\n") 
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
    """Guarda una venta en 'operaciones.jsonl' en formato JSON"""
    try:
        arch = open("operaciones.jsonl", "a")
        json.dump(venta, arch)
        arch.write("\n")
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


def validar_indice(indice):
    """Valida que el índice ingresado sea válido para la lista de eventos"""
    indice = validar_numero(indice)
    maximo = contar_eventos()
    while indice < 1 or indice > maximo:
        indice = input("Ingrese un índice válido: ")
        indice = validar_numero(indice) 
    return int(indice)


def validar_fecha(fecha):
    """Valida que la fecha ingresada tenga el formato YYYY-MM-DD y no sea pasada"""
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
        
        if not valido:
            fecha = input("Ingrese nuevamente (YYYY-MM-DD): ")
    return fecha


def validar_numero(valor):
    """Valida que el valor ingresado sea un número positivo"""
    if type(valor) is str:
        valor = validar_no_es_vacio(valor)
    
    while not str(valor).isdigit() or int(valor) <= 0:
        valor = input("El valor debe ser un número positivo. Ingrese nuevamente: ")
        valor = validar_no_es_vacio(valor)
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
    numero_dni = validar_numero(numero_dni)
    while len(str(numero_dni)) != 8:
        numero_dni = validar_numero(input("Número de DNI inválido. Ingrese un número de 8 dígitos: "))
    return numero_dni


def validar_email(email):
    """Valida que el email ingresado tenga un formato básico válido"""
    validar_no_es_vacio(email)
    while "@" not in email or "." not in email.split("@")[-1]:
        email = input("Email inválido. Ingrese un email válido: ")
    return email


# FUNCIONES ANÁLISIS DE DATOS


def contar_entradas_vendidas(arch, acumulador=0):
    """Cuenta recursivamente sumando las ventas de todos los sectores"""

    linea = arch.readline()

    if linea == "":
        return acumulador
    
    linea = linea.strip()
    if linea:
        try:
            registro = json.loads(linea)
            sectores = registro['sectores']
            vendidas_evento = 0
            
            for datos_sector in sectores.values():
                total = datos_sector['cantidad']
                disponibles = datos_sector.get('disponibles', total)
                vendidas_evento += (total - disponibles)
            
            return contar_entradas_vendidas(arch, acumulador + vendidas_evento)
        except (ValueError):
            return contar_entradas_vendidas(arch, acumulador)
    return contar_entradas_vendidas(arch, acumulador)


def calcular_recaudacion(arch, acumulador=0):
    """Calcula recursivamente la recaudación total sumando precio*vendidas por sector"""

    linea = arch.readline()

    if linea == "":
        return acumulador
    
    linea = linea.strip()
    if linea:
        try:
            registro = json.loads(linea)
            sectores = registro['sectores']
            recaudado_evento = 0
            
            for datos_sector in sectores.values():
                precio = datos_sector['precio']
                total = datos_sector['cantidad']
                disponibles = datos_sector.get('disponibles', total)
                vendidas = total - disponibles
                recaudado_evento += (vendidas * precio)
                
            return calcular_recaudacion(arch, acumulador + recaudado_evento)
        except (ValueError):
            return calcular_recaudacion(arch, acumulador)
    return calcular_recaudacion(arch, acumulador)


def encontrar_mas_vendido(arch, max_vendidas=0, artista_max=""):
    """Encuentra el evento con más entradas vendidas sumando sus sectores"""

    linea = arch.readline()

    if linea == "":
        return max_vendidas, artista_max
    
    linea = linea.strip()
    if linea:
        try:
            registro = json.loads(linea)
            artista = registro['artista']
            sectores = registro['sectores']
            vendidas_totales = 0
            
            for datos_sector in sectores.values():
                total = datos_sector['cantidad']
                disponibles = datos_sector.get('disponibles', total)
                vendidas_totales += (total - disponibles)
            
            if vendidas_totales > max_vendidas:
                return encontrar_mas_vendido(arch, vendidas_totales, artista)
        except (ValueError):
            pass
    return encontrar_mas_vendido(arch, max_vendidas, artista_max)


def contar_eventos_recursivo(arch, contador=0):
    """Función recursiva para contar eventos (uso interno)"""
    linea = arch.readline()
    if linea == "": return contador
    linea = linea.strip()
    if linea:
        try:
            json.loads(linea)
            return contar_eventos_recursivo(arch, contador + 1)
        except: pass
    return contar_eventos_recursivo(arch, contador)


def contar_eventos():
    """Cuenta cuántos eventos hay en el archivo usando recursividad"""
    try:
        arch = open("eventos.jsonl", "r")
        cantidad = contar_eventos_recursivo(arch)
        arch.close()
        return cantidad
    except FileNotFoundError as mensaje:
        print("No se encontró el archivo", mensaje)
    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)


def obtener_max_factura(arch, max_actual=0):
    """Obtiene recursivamente el número de factura máximo"""

    linea = arch.readline()

    if linea == "":
        return max_actual
    
    linea = linea.strip()
    if linea:
        try:
            registro = json.loads(linea)
            factura = int(registro['numero_factura'])
            if factura > max_actual:
                return obtener_max_factura(arch, factura)
        except (ValueError):
            pass
    return obtener_max_factura(arch, max_actual)


# FUNCIONES PRINCIPALES


def mostrar_eventos():
    """Muestra todos los eventos con el formato solicitado"""
    try:
        arch = open("eventos.jsonl", "r")
        titulo = "\n▶   LISTA DE EVENTOS "
        print(titulo.ljust(80, "━"))
        print(f"{'N°':<3} {'Artista':<20} {'Estadio':<20} {'Fecha':<12} {'Hora':<7}") 
        print("━" * 80)
        print("\n")
        
        linea = arch.readline()
        numero = 1

        while linea != "":
            linea = linea.strip()
            if linea:
                try:
                    evento = json.loads(linea)       
                    total_disponibles_evento = 0
                    for d in evento['sectores'].values():
                        total_disponibles_evento += d.get('disponibles', d['cantidad'])
                    print(f"{numero}. {evento['artista']:<20} {evento['estadio']:<20} {evento['fecha']:<12} {evento['hora']:<7}")
                    
                    print("   ▶  Sectores: ")
                    for nombre_sec, datos in evento['sectores'].items():
                        total = datos['cantidad']
                        disp = datos.get('disponibles', total) 
                        precio = datos['precio']
                        print(f"   ━ {nombre_sec:<20} Precio: ${precio:<8} Disp: {disp}/{total}")
                    
                    print("\n")
                    numero += 1
                except Exception as e:
                    print(f"Línea inválida: {e}")
            linea = arch.readline()
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


def mostrar_ventas():
    """Muestra la lista de operaciones registradas"""
    try:
        arch = open("operaciones.jsonl", "r")
        titulo = "\n▶   LISTA DE OPERACIONES "
        print(titulo.ljust(80, "━"))
        print(f"{'N°':<3} {'Cliente':<20} {'Sector':<15} {'Factura':<9} {'Cant.':<6}")
        print("━" * 80)
        
        linea = arch.readline()
        numero = 1
        tiene_ventas = False
        
        while linea != "":
            linea = linea.strip()
            if linea:
                try:
                    venta = json.loads(linea)
                    nombre_completo = f"{venta['nombre']} {venta['apellido']}"
                    sector = venta.get('sector', '-')
                    
                    print(f"{numero:<3} {nombre_completo:<20} {sector:<15} {venta['numero_factura']:<9} {venta['numero_entradas']:<6}")
                    numero += 1
                    tiene_ventas = True
                except:
                    pass
            linea = arch.readline()
        
        if not tiene_ventas:
            print("No hay ventas registradas.")
        print("\n")
    except FileNotFoundError as mensaje:
        print("No se encontró el archivo", mensaje)
    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass


def evento_seleccionado(linea):
    """Convierte una línea de texto JSON en un dict evento o devuelve un diccionario vacio"""

    linea = linea.strip()
    if linea == "": 
        return {}
    try:
        return json.loads(linea)
    except:
        return {}


def obtener_info_estadio_por_id(id_requerido):
    """Busca el estadio en estadios.jsonl por número de línea (ID)"""
    try:
        arch = open("estadios.jsonl", "r")
        linea = arch.readline()
        contador = 1
        while linea != "":
            linea = linea.strip()
            if linea:
                try:
                    if contador == id_requerido:
                        estadio_data = json.loads(linea)
                        arch.close()
                        return estadio_data['estadio'], estadio_data['sectores']
                    contador += 1
                except: pass
            linea = arch.readline()
        arch.close()
    except FileNotFoundError as mensaje:
        print("No se encontró el archivo", mensaje)
    return False


def crear_evento(artista, id_estadio, fecha, hora):
    """Crea un nuevo evento buscando el estadio por ID"""
    
    nombre_estadio, sectores_estadio = obtener_info_estadio_por_id(id_estadio)
    
    if nombre_estadio == "":
        print("Error: ID de estadio no válido.")
        return

    #Validar duplicados
    existe = False
    try:
        arch = open("eventos.jsonl", "r")
        linea = arch.readline()
        while linea != "":
            linea = linea.strip()
            if linea:
                try:
                    evento = json.loads(linea)
                    if evento['artista'].lower() == artista.lower() and evento['fecha'] == fecha:
                        existe = True
                        break
                except: pass
            linea = arch.readline()
        arch.close()
    except FileNotFoundError as mensaje:
        print("No se encontró el archivo eventos.jsonl", mensaje)
        pass

    if existe:
        print("Error, ya existe un evento con ese artista en esa fecha.")
        return 
    
    sectores_evento = {}
    for nombre_sec, datos in sectores_estadio.items():
        sectores_evento[nombre_sec] = {
            "precio": datos['precio'],
            "cantidad": datos['cantidad'],
            "disponibles": datos['cantidad'] 
        }

    nuevo_evento = {
        "artista": artista, 
        "estadio": nombre_estadio,
        "fecha": fecha, 
        "hora": hora, 
        "sectores": sectores_evento
    }
    
    guardar_nuevo_evento(nuevo_evento)
    print(f"Evento creado con éxito en {nombre_estadio}.")



def modificar_evento(indice, opcion):
    """Modifica un atributo específico de un evento usando json"""
    try:
        entrada = open("eventos.jsonl", "r")
        salida = open("eventos2.jsonl", "w")
        linea = entrada.readline()
        nro_actual = 1
        
        while linea != "":
            linea_limpia = linea.strip()
            if linea_limpia:
                try:
                    evento = json.loads(linea_limpia) 
                    
                    if nro_actual == indice:
                        modificado = False
                        
                        # Modificar nombre
                        if opcion == 0:      
                            nuevo = validar_no_es_vacio(input("Nuevo artista: "))
                            evento["artista"] = nuevo
                            modificado = True
                        
                        # Modificar fecha
                        elif opcion == 1:  
                            nuevo = validar_fecha(input("Nueva fecha (YYYY-MM-DD): "))
                            evento["fecha"] = nuevo
                            modificado = True

                        # Modificar hora
                        elif opcion == 2: 
                            nuevo = validar_hora(input("Nueva hora (HH:MM): "))
                            evento["hora"] = nuevo
                            modificado = True

                        # Modificar precio
                        elif opcion == 3:
                            lista_sectores = list(evento["sectores"].keys())
                            print("\nSectores disponibles:")
                            for i, sec in enumerate(lista_sectores):
                                print(f"{i+1}. {sec}")
                            
                            idx_sector = validar_numero(input("\nIngrese el número del sector: ")) - 1
                            
                            if 0 <= idx_sector < len(lista_sectores):
                                nom_sector = lista_sectores[idx_sector]
                                nuevo_p = validar_numero(input(f"Nuevo precio para {nom_sector}: "))
                                evento["sectores"][nom_sector]["precio"] = nuevo_p
                                modificado = True
                            else: 
                                print("Número de sector inválido.")

                        # Modificar cant entradas
                        elif opcion == 4:
                            lista_sectores = list(evento["sectores"].keys())
                            print("\nSectores disponibles:")
                            for i, sec in enumerate(lista_sectores):
                                print(f"{i+1}. {sec}")
                            
                            idx_sector = validar_numero(input("\nIngrese el número del sector: ")) - 1
                            
                            if 0 <= idx_sector < len(lista_sectores):
                                nom_sector = lista_sectores[idx_sector]
                                nuevo_t = validar_numero(input(f"Nueva cantidad total para {nom_sector}: "))
                                datos = evento["sectores"][nom_sector]
                                disp_actual = datos.get("disponibles", datos["cantidad"])
                                vendidas = datos["cantidad"] - disp_actual
                                
                                if nuevo_t < vendidas:
                                    print(f"No se puede reducir a {nuevo_t}, ya se vendieron {vendidas}.")
                                else:
                                    diferencia = nuevo_t - datos["cantidad"]
                                    evento["sectores"][nom_sector]["cantidad"] = nuevo_t
                                    evento["sectores"][nom_sector]["disponibles"] = disp_actual + diferencia
                                    modificado = True
                            else: 
                                print("Número de sector inválido.")

                        if modificado:
                            json.dump(evento, salida)
                            salida.write("\n")
                        else:
                            salida.write(linea)
                    else:
                        salida.write(linea)
                    nro_actual += 1
                except:
                    salida.write(linea) 
            else:
                salida.write(linea)
            linea = entrada.readline()
        print("\nModificación finalizada.")
    except FileNotFoundError as mensaje:
        print("No se encontró eventos.jsonl", mensaje)
    except OSError as mensaje:
        print("Error de archivo", mensaje)
    finally:
        try: 
            entrada.close()
            salida.close()
        except: 
            pass            
    try: 
        os.replace("eventos2.jsonl", "eventos.jsonl")
    except: 
        pass


def eliminar_evento(indice):
    """Elimina un evento de la lista de eventos"""
    try: 
        entrada = open("eventos.jsonl","r")
        salida = open("eventos2.jsonl","w")
        linea = entrada.readline()
        numero = 1
        while linea != "":
            if numero != indice:
                salida.write(linea)
            
            if linea.strip():
                numero += 1
            
            linea = entrada.readline()
        print("Evento eliminado con exito")
    except FileNotFoundError as mensaje:
        print("No se encontro eventos.jsonl", mensaje)
    except OSError as mensaje:
        print("Error al eliminar el evento:", mensaje)
    finally:
        try:
            entrada.close()
            salida.close()
        except:
            pass
    try:
        os.replace("eventos2.jsonl","eventos.jsonl")
    except OSError as mensaje:
        print("Error al reemplazar archivo:", mensaje)
            

def obtener_siguiente_factura():
    """Devuelve el numero_factura siguiente usando recursividad"""
    try:
        arch = open("operaciones.jsonl", "r")
        max_factura = obtener_max_factura(arch)
        arch.close()
        return max_factura + 1
    except FileNotFoundError as mensaje:
        print("No se encontró el archivo", mensaje)
    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)


def imprimir_factura(factura, nombre, apellido, email, dni, cantidad, sector, monto_unitario):
    """Imprime la factura de la compra realizada"""
    print("\n"+" FACTURA ".center(40, "━"))
    print(f"Factura N°: {factura}")
    print(f"Cliente: {nombre} {apellido}")
    print(f"DNI: {dni}")
    print(f"Email: {email}")
    print(f"Sector: {sector}")
    print(f"Cantidad: {cantidad}")
    print(f"Total: ${cantidad * monto_unitario}")
    print("".ljust(40, "━")+"\n")


def vender_entrada(indice_objetivo, nombre, apellido, email, numero_dni, cantidad_entradas):
    """Vende entradas seleccionando el sector específico"""

    while cantidad_entradas > 6:
        print("No se pueden vender más de 6 entradas por persona.")
        cantidad_entradas = validar_numero(input("Ingrese la cantidad de entradas a vender (máximo 6): "))

    encontrado = False
    venta_realizada = False

    try:
        entrada = open("eventos.jsonl", "r")
        salida = open("eventos2.jsonl", "w")
        
        numero_linea = 1 
        linea = entrada.readline()

        while linea != "":
            linea_limpia = linea.strip()
            if linea_limpia:
                try:
                    evento = json.loads(linea_limpia)
                    
                    if numero_linea == indice_objetivo:
                        encontrado = True
                        print(f"\nSectores disponibles para {evento['artista']}:")
                        sectores = evento['sectores']
                        lista_sectores = []
                        numero = 0
                        
                        for nom, dat in sectores.items():
                            disp = dat.get('disponibles', dat['cantidad'])
                            numero += 1
                            print(f"{numero}. {nom}: ${dat['precio']} (Disponibles: {disp})")
                            lista_sectores.append(nom)
                        
                        opcion_sector = validar_numero(input("\nIngrese el número del sector: ")) - 1
                        
                        if 0 <= opcion_sector < len(lista_sectores):
                            sector_elegido = lista_sectores[opcion_sector]
                            datos_sector = sectores[sector_elegido]
                            disponibles = datos_sector.get('disponibles', datos_sector['cantidad'])
                            
                            if disponibles >= cantidad_entradas:
                                datos_sector['disponibles'] = disponibles - cantidad_entradas
                                evento['sectores'][sector_elegido] = datos_sector
                                
                                json.dump(evento, salida)
                                salida.write("\n")

                                factura = obtener_siguiente_factura()
                                venta = {
                                    "indice": indice_objetivo, 
                                    "nombre": nombre, 
                                    "apellido": apellido, 
                                    "email": email,
                                    "numero_dni": numero_dni, 
                                    "numero_entradas": cantidad_entradas, 
                                    "numero_factura": factura,
                                    "sector": sector_elegido
                                }
                                guardar_venta_en_archivo(venta)

                                print("Venta exitosa.")
                                imprimir_factura(factura, nombre, apellido, email, numero_dni, cantidad_entradas, sector_elegido, datos_sector['precio'])
                                venta_realizada = True
                            else:
                                print(f"No hay suficientes entradas en {sector_elegido}.")
                                salida.write(linea) #Sin cambios
                        else:
                            print("Número de sector inválido.")
                            salida.write(linea) #Sin cambios
                    else:
                        salida.write(linea)
                    
                    numero_linea += 1
                except:
                    salida.write(linea)
            else:
                salida.write(linea)

            linea = entrada.readline()

    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
        return
    except OSError as mensaje:
        print("Error al vender:", mensaje)
        return
    finally:
        try:
            entrada.close()
            salida.close()
        except:
            pass

    if encontrado and venta_realizada:
        try:
            os.replace("eventos2.jsonl", "eventos.jsonl")
        except OSError:
            print("Error al guardar cambios en archivo.")
    else:
        try:
            os.remove("eventos2.jsonl")
        except: 
            pass
        if not encontrado:
            print("Evento no encontrado.")



def buscar_venta(email, factura):
    """Busca una venta en el JSON por email y factura y devuelve datos incluyendo sector"""
    try:
        arch = open("operaciones.jsonl", "r")
        linea = arch.readline()
        
        while linea != "":
            linea = linea.strip()
            if linea:
                try:
                    venta = json.loads(linea)
                    if venta['email'] == email and int(venta['numero_factura']) == factura:
                        return venta['indice'], venta['numero_entradas'], venta['nombre'], venta['apellido'], venta.get('sector')
                except:
                    pass
            linea = arch.readline()
        return False
    except OSError:
        print("Error en la lectura del archivo")
    finally:
        try:
            arch.close()
        except:
            pass 


def cancelar_entrada(email, numero_dni, factura, cantidad):
    """Cancela entradas devolviéndolas al sector correspondiente"""
    
    indice_evento, entradas_compradas, nombre, apellido, sector_venta = buscar_venta(email, factura)
    
    if indice_evento is False:
        print("No hay entradas vendidas bajo ese mail o número de factura.")
        return
    
    if int(cantidad) > int(entradas_compradas):
        print("No puede cancelar más entradas de las que compró.")
        return
    
    if sector_venta == "":
        print("Esta venta no tiene sector registrado (formato antiguo). No se puede procesar devolución automática.")
        return

    try:
        entrada = open("eventos.jsonl", "r")
        salida = open("eventos2.jsonl", "w")
        numero_linea = 1
        
        linea = entrada.readline()
        while linea != "":
            linea_limpia = linea.strip()
            if linea_limpia:
                try:
                    evento = json.loads(linea_limpia)
                    
                    if numero_linea == indice_evento:
                        if sector_venta in evento['sectores']:
                            datos = evento['sectores'][sector_venta]
                            disp = datos.get('disponibles', datos['cantidad'])
                            evento['sectores'][sector_venta]['disponibles'] = disp + cantidad
                            
                            json.dump(evento, salida)
                            salida.write("\n")
                            print(f"Se devolvieron {cantidad} entradas al sector {sector_venta}.")
                        else:
                            print("El sector original ya no existe en el evento.")
                            salida.write(linea)
                    else:
                        salida.write(linea)
                    
                    numero_linea += 1
                except:
                    salida.write(linea)
            else:
                salida.write(linea)
            linea = entrada.readline()

        nueva_venta = {
            "indice": indice_evento, 
            "nombre": nombre, 
            "apellido": apellido, 
            "email": email, 
            "numero_dni": numero_dni, 
            "numero_entradas": -cantidad, 
            "numero_factura": factura,
            "sector": sector_venta
        }
        guardar_venta_en_archivo(nueva_venta)
        
    except OSError as mensaje:
        print("Error al cancelar:", mensaje)
    finally:
        try:
            entrada.close()
            salida.close()
        except:
            pass
    
    try:
        os.replace("eventos2.jsonl", "eventos.jsonl")
    except OSError:
        pass


def ver_entradas_vendidas():
    """Muestra la cantidad de entradas vendidas por evento detallado por sector"""
    try:
        arch = open("eventos.jsonl", "r")
        titulo = "\n   ENTRADAS VENDIDAS "
        print(titulo.ljust(70, "━"))
        
        linea = arch.readline()
        tiene_eventos = False
        
        while linea != "":
            linea = linea.strip()
            if linea:
                try:
                    evento = json.loads(linea)
                    print(f"Evento: {evento['artista']} ({evento['estadio']})")
                    print(f"{'Sector':<20} {'Vendidas':<10} {'Disponibles':<12}")
                    
                    for nom, datos in evento['sectores'].items():
                        total = datos['cantidad']
                        disp = datos.get('disponibles', total)
                        vendidas = total - disp
                        print(f"{nom:<20} {vendidas:<10} {disp:<12}")
                    print("-" * 42)
                    tiene_eventos = True
                except:
                    pass
            linea = arch.readline()
        
        if not tiene_eventos:
            print("No hay eventos registrados.")
        print("\n")
    except FileNotFoundError as mensaje:
        print("No se encontró el archivo", mensaje)
    finally:
        try:
            arch.close()
        except:
            pass


def analisis_datos():
    """Realiza un análisis de datos sobre las ventas de entradas"""
    cantidad_eventos = contar_eventos()
    
    if cantidad_eventos == 0:
        print("No hay eventos registrados.")
        return
    
    try:
        # Calcular total vendidas
        arch = open("eventos.jsonl", "r")
        total_vendidas = contar_entradas_vendidas(arch)
        arch.close()
        
        if total_vendidas == 0:
            print("No se han vendido entradas aún.")
            return
        
        # Calcular recaudación
        arch = open("eventos.jsonl", "r")
        total_recaudado = calcular_recaudacion(arch)
        arch.close()
        
        # Calcular promedio
        promedio = total_vendidas / cantidad_eventos
        
        # Encontrar evento más vendido
        arch = open("eventos.jsonl", "r")
        max_vendidas, artista_max = encontrar_mas_vendido(arch)
        arch.close()
        
        titulo = "\n▶   ANÁLISIS DE DATOS "
        print(titulo.ljust(60, "━"))
        print(f"{'Total recaudado:':<35} ${total_recaudado}")
        print(f"{'Total de entradas vendidas:':<35} {total_vendidas}")
        print(f"{'Promedio de entradas vendidas:':<35} {promedio:.2f}")
        print("━" * 60)
        print("\nEvento más vendido:")
        print(f"- {artista_max} ({max_vendidas} entradas vendidas totales)")
        print("\n")
        
    except FileNotFoundError:
        print("No se encontró el archivo", mensaje)
    except OSError as mensaje:
        print("Error al leer el archivo:", mensaje)


def busqueda_artista(artista):
    """Busca eventos por artista y los muestra"""
    try:
        arch= open("eventos.jsonl", "r")
        linea=arch.readline()
        artista = artista.lower()
        encontrado = False 
        while linea!="":
            evento = evento_seleccionado(linea)
            if evento and artista in evento['artista'].lower():
                encontrado = True
                titulo = "\n▶   ARTISTA ENCONTRADO: "
                print(titulo.ljust(80, "━"))
                print(f"{'━':<3} {'Artista':<20} {'Estadio':<15} {'Fecha':<9} {'Hora':>8}")
                print("━" * 80)
                print(f"{evento['artista']:>16} {evento['estadio']:>19} {evento['fecha']:>14} {evento['hora']:>8}")
                print("Sectores:")
                for nom, datos in evento['sectores'].items():
                    print(f" ━ {nom}: ${datos['precio']}")
                print("\n")
            linea=arch.readline() 
        if not encontrado: 
            print("No se encontraron eventos para", artista)
    except FileNotFoundError as mensaje:
        print("No se encontró el archivo", mensaje)
    finally:
        try:
            arch.close()
        except:
            pass


# MENÚS PRINCIPALES

def mostrar_menu():
    """Muestra el menú principal"""
    titulo = "\n ★   MENÚ PRINCIPAL  "
    print(titulo.ljust(40, "━"))
    print("1. Administración de eventos")
    print("2. Administración de entradas")
    print("3. Ver lista de operaciones")
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
    
    # Mostrar eventos
    if opcion_eventos == 0:
        mostrar_eventos()

    # Búsqueda por artista
    elif opcion_eventos == 1:
        artista = validar_no_es_vacio(input("Ingrese el nombre del artista a buscar: "))
        busqueda_artista(artista)

    # Crear evento
    elif opcion_eventos == 2:
        artista = validar_no_es_vacio(input("Ingrese el nombre del artista: "))
        
        print("\nEstadios disponibles:")
        try:
            e_arch = open("estadios.jsonl", "r")
            l = e_arch.readline()
            numero = 0
            while l:
                try:
                    datos = json.loads(l)
                    numero+=1
                    print(f"{numero}. {datos['estadio']}")
                except: pass
                l = e_arch.readline()
            e_arch.close()
        except: 
            print("No se pudo leer estadios.jsonl")

        estadio = validar_numero(input("\nIngrese el número del estadio: "))
        fecha = validar_fecha(input("Ingrese la fecha del evento (YYYY-MM-DD): "))
        hora = validar_hora(input("Ingrese la hora del evento (HH:MM): "))
        crear_evento(artista, estadio, fecha, hora)

    # Modificar evento
    elif opcion_eventos == 3:
        mostrar_eventos()
        cantidad = contar_eventos()
        if cantidad > 0:
            indice = validar_indice(input("Seleccione el evento a modificar: "))
            print("\n1. Artista\n2. Fecha\n3. Hora\n4. Modificar PRECIO de un sector\n5. Modificar CANTIDAD de un sector\n6. Salir")
            opcion_mod = validar_numero(input("¿Qué desea modificar?: ")) - 1
            if 0 <= opcion_mod <= 4:
                modificar_evento(indice, opcion_mod)

    # Eliminar evento
    elif opcion_eventos == 4:
        mostrar_eventos()
        cantidad = contar_eventos()
        if cantidad > 0:
            indice = validar_indice(input("Ingrese el índice del evento a eliminar: "))
            eliminar_evento(indice)

    # Volver al menú
    if opcion_eventos != 5:
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

    if opcion_entradas == 0:
        mostrar_eventos()
        cantidad = contar_eventos()
        if cantidad > 0:
            indice = validar_indice(input("Ingrese el índice del evento: "))
            nombre = validar_no_es_vacio(input("Ingrese su nombre: "))
            apellido = validar_no_es_vacio(input("Ingrese su apellido: "))
            email = validar_email(input("Ingrese su email: "))
            numero_dni = validar_numero_dni(input("Ingrese su número de DNI: "))
            cantidad_entradas = validar_numero(input("Cantidad de entradas a vender: "))
            vender_entrada(indice, nombre, apellido, email, numero_dni, cantidad_entradas)

    elif opcion_entradas == 1:
        email = validar_email(input("Ingrese su email: "))
        numero_dni = validar_numero_dni(input("Ingrese su número de DNI: "))
        factura = validar_numero(input("Ingrese su número de factura: "))
        cantidad = validar_numero(input("Cantidad de entradas a cancelar: "))
        cancelar_entrada(email, numero_dni, factura, cantidad)

    elif opcion_entradas == 2:
        ver_entradas_vendidas()

    elif opcion_entradas == 3:
        analisis_datos()

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
    if opcion == 0:
        menu_eventos()
    elif opcion == 1:
        menu_entradas()
    elif opcion == 2:
        mostrar_ventas()
    else:
        print("Opción inválida. Intente nuevamente.")
    
    mostrar_menu()
    print("".ljust(40, "━"))
    print("\n")
    opcion = validar_numero(input("Elija una opción: ")) - 1

print("¡Chau!")