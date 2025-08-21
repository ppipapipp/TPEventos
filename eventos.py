from datetime import datetime

#DECLARACIÓN DE VARIABLES

eventos = [
    ["Taylor", "Estadio Nacional", "2023-10-01", "20:00", 50000, 1000, 1000],
    ["Coldplay", "Estadio Nacional", "2023-11-01", "21:00", 60000, 1500, 1500],
    ["Bad_bunny", "Estadio Nacional", "2023-12-01", "22:00", 70000, 2000, 2000]
]

#FUNCIONES

def mostrar_eventos():
    print("\n📋   LISTA DE EVENTOS  ━━━━━━━━━━━━━━━━")
    for i, evento in enumerate(eventos): #NO SÉ SI SE PUEDE USAR ENUMERATE
        print(i+1,". Artista: ", evento[0], " Estadio: ", evento[1], " Fecha: ", evento[2], " Hora: ", evento[3], " Precio: $", evento[4], " Entradas disponibles: ", evento[6])
    if not eventos:
        print("No hay eventos registrados.")


def crear_evento(artista, estadio, fecha, hora, precio, cantidad):
    evento = [artista, estadio, fecha, hora, precio, cantidad, cantidad]
    eventos.append(evento)
    print("Evento creado con éxito.")


def modificar_evento(indice, opcion, nuevo_valor):
    #FUNCIONA MAL, ME DEJA MODIFICAR AUNQUE NO EXISTA EL INDICE, NO VA CON EL MISMO INDICE PORQUE EN LA LISTA EMPIEZA EN 0 Y EN EL MENU EN 1, Y NO LO MODIFICA DE TODAS FORMAS
    if 0 <= indice < len(eventos):
        if opcion == 1:   # Artista
            eventos[indice][0] = nuevo_valor
        elif opcion == 2: # Estadio
            eventos[indice][1] = nuevo_valor
        elif opcion == 3: # Fecha
            eventos[indice][2] = nuevo_valor
        elif opcion == 4: # Hora
            eventos[indice][3] = nuevo_valor
        elif opcion == 5: # Precio
            eventos[indice][4] = int(nuevo_valor)
        elif opcion == 6: # Cantidad de entradas
            nuevas = int(nuevo_valor)
            diferencia = nuevas - eventos[indice][5]
            eventos[indice][5] = nuevas
            eventos[indice][6] += diferencia
        print("Evento modificado.")
    else:
        print("Índice de evento inválido.") 

def eliminar_evento(indice):
    #PROBABLEMENTE PASE LO MISMO QUE CON MODIFICAR, NO SE SI VA A FUNCIONAR BIEN
    if 0 <= indice+1 < len(eventos):
        eliminado = eventos.pop(indice)
        print(f"Evento eliminado: {eliminado[0]}")
    else:
        print("Índice de evento inválido.")


def vender_entrada(indice, cantidad):
        #PROBABLEMENTE PASE LO MISMO QUE CON MODIFICAR, NO SE SI VA A FUNCIONAR BIEN
    if 0 <= indice+1 < len(eventos):
        if eventos[indice][6] >= cantidad:
            eventos[indice][6] -= cantidad
            print("Vendidas ", cantidad, " entradas para " , eventos[indice][0])
        else:
            print("No hay suficientes entradas disponibles.")
    else:
        print("Índice de evento inválido.") #ME DEJA VENDER AUNQUE NO EXISTA EL INDICE


def cancelar_entrada(indice, cantidad):
        #PROBABLEMENTE PASE LO MISMO QUE CON MODIFICAR, NO SE SI VA A FUNCIONAR BIEN
    if 0 <= indice+1 < len(eventos):
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
    promedio = total_vendidas / len(eventos)
    mas_vendido = max(eventos, key=lambda x: x[5] - x[6])

    print("\nAnálisis de datos:")
    print("Total entradas vendidas: ",total_vendidas)
    print(f"Promedio de entradas vendidas por evento: {promedio:.2f}")
    print("Evento más vendido: ", mas_vendido[0] , (mas_vendido[5] - mas_vendido[6], " entradas vendidas"))


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
opcion = input("Elija una opción: ")

while opcion != "9":
    
    if opcion == "1":
        mostrar_eventos()

    elif opcion == "2":
        artista = input("Ingrese el nombre del artista: ")
        estadio = input("Ingrese el nombre del estadio: ")
        fecha = input("Ingrese la fecha del evento (YYYY-MM-DD): ")
        hora = input("Ingrese la hora del evento (HH:MM): ")
        precio = int(input("Ingrese el precio de la entrada: "))
        cantidad = int(input("Ingrese la cantidad de entradas disponibles: "))
        crear_evento(artista, estadio, fecha, hora, precio, cantidad)

    elif opcion == "3":
        mostrar_eventos()
        indice = int(input("Ingrese el índice del evento a modificar: "))
        print("1. Artista\n2. Estadio\n3. Fecha\n4. Hora\n5. Precio\n6. Cantidad de entradas")
        opcion_mod = int(input("¿Qué desea modificar?: "))
        nuevo_valor = input("Ingrese el nuevo valor: ")
        modificar_evento(indice, opcion_mod, nuevo_valor)

    elif opcion == "4":
        mostrar_eventos()
        indice = int(input("Ingrese el índice del evento a eliminar: "))
        eliminar_evento(indice)

    elif opcion == "5":
        mostrar_eventos()
        indice = int(input("Ingrese el índice del evento: "))
        cantidad = int(input("Cantidad de entradas a vender: "))
        vender_entrada(indice, cantidad)

    elif opcion == "6":
        mostrar_eventos()
        indice = int(input("Ingrese el índice del evento: "))
        cantidad = int(input("Cantidad de entradas a cancelar: "))
        cancelar_entrada(indice, cantidad)

    elif opcion == "7":
        ver_entradas_vendidas()

    elif opcion == "8":
        analisis_datos()

    elif opcion == "9": #HACER QUE SE VEA EL CHAU ANTES DE IRTE
        print("¡Chau!")

    else:
        print("Opción inválida. Intente nuevamente.")
    
    mostrar_menu()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    opcion = input("Elija una opción: ")
