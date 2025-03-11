from pyDatalog import pyDatalog
import re
import sys

pyDatalog.create_terms('Producto, Categoria, Precio, Caracteristica, recomendar, X, Y, Z, W')

# Asegurar codificación UTF-8
sys.stdin.reconfigure(encoding='utf-8')

# Base de conocimiento ampliada con nuevos ítems y subcategorías
+ Producto('Humidificador', 'Electrodomestico', 50, 'Mejora calidad del aire')
+ Producto('Ventilador', 'Electrodomestico', 30, 'Enfria ambientes')
+ Producto('Sistema de Sonido', 'Electronica', 200, 'Mejora experiencia auditiva')
+ Producto('Aire Acondicionado', 'Electrodomestico', 300, 'Regula temperatura')
+ Producto('Purificador de Aire', 'Electrodomestico', 150, 'Elimina contaminantes del aire')
+ Producto('Calefactor', 'Electrodomestico', 120, 'Genera calor para invierno')
+ Producto('Lampara Inteligente', 'Electronica', 40, 'Iluminacion controlada por voz')
+ Producto('Robot Aspirador', 'Electrodomestico', 250, 'Limpieza automatica del hogar')
+ Producto('Cafetera Automatica', 'Electrodomestico', 100, 'Prepara cafe automaticamente')
+ Producto('Televisor 4K', 'Electronica', 600, 'Alta resolucion de imagen')
+ Producto('Escritorio de madera', 'Mobiliario', 200, 'Espacio de trabajo comodo')
+ Producto('Silla ergonomica', 'Mobiliario', 150, 'Mejora la postura')
+ Producto('Colchon ortopedico', 'Mobiliario', 500, 'Mejora la calidad del sueño')
+ Producto('Cortinas blackout', 'Decoracion', 80, 'Bloquea la luz para mejor descanso')
+ Producto('Cuadro decorativo', 'Decoracion', 60, 'Aporta estilo a la habitacion')

# Reglas de recomendación
recomendar(X, Y) <= Producto(X, Y, Z, W)


# Interpretación de lenguaje natural

def interpretar_categoria(texto):
    texto = texto.lower()

    categorias = {
        'Electrodomestico': ['aire', 'ventilacion', 'clima', 'frio', 'calor', 'enfriar', 'calentar', 'humidificador',
                             'ventilador', 'purificador', 'calefactor', 'cafetera', 'robot'],
        'Electronica': ['musica', 'sonido', 'audio', 'imagen', 'pantalla', 'video', 'televisor', 'lampara'],
        'Mobiliario': ['mueble', 'silla', 'cama', 'escritorio', 'colchon', 'mesa'],
        'Decoracion': ['decoracion', 'cuadro', 'cortinas', 'ambiente', 'estilo']
    }

    for categoria, palabras_clave in categorias.items():
        if any(palabra in texto for palabra in palabras_clave):
            return categoria
    return None


# Función para obtener información detallada de un producto
def obtener_informacion_producto(nombre_producto):
    nombre_producto = nombre_producto.lower()

    # Usar pyDatalog directamente para consultar la base de datos
    # Primero hacemos una búsqueda exacta
    productos = Producto(X, Y, Z, W)
    for prod in productos:
        nombre, categoria, precio, caracteristica = prod
        if nombre.lower() == nombre_producto:
            return (nombre, categoria, precio, caracteristica)

    # Si no se encuentra una coincidencia exacta, hacemos una búsqueda parcial
    for prod in productos:
        nombre, categoria, precio, caracteristica = prod
        if nombre_producto in nombre.lower():
            return (nombre, categoria, precio, caracteristica)

    return None


# Función para recomendar productos según la preferencia del usuario
def obtener_recomendacion(categoria):
    resultado = recomendar(X, categoria)
    return [x[0] for x in resultado] if resultado else []


# Simulación de consulta del usuario con bucle para múltiples consultas
if __name__ == "__main__":
    print("Bienvenido al asistente de compras para productos del hogar.")
    while True:
        try:
            preferencia = input("¿Qué tipo de producto buscas? (Escribe 'salir' para finalizar): ").strip()
            if preferencia.lower() == 'salir':
                print("Gracias por usar el asistente de compras. ¡Hasta luego!")
                break

            categoria_interpretada = interpretar_categoria(preferencia)

            if categoria_interpretada:
                recomendaciones = obtener_recomendacion(categoria_interpretada)
                if recomendaciones:
                    print(f"Basado en tu preferencia, te recomendamos: {', '.join(recomendaciones)}")
                    producto_seleccionado = input(
                        "Escribe el nombre del producto que deseas ver más detalles: ").strip()
                    informacion_producto = obtener_informacion_producto(producto_seleccionado)

                    if informacion_producto:
                        nombre, categoria, precio, caracteristica = informacion_producto
                        print(f"\nInformación del producto seleccionado:")
                        print(f"Nombre: {nombre}")
                        print(f"Categoría: {categoria}")
                        print(f"Precio: ${precio}")
                        print(f"Característica: {caracteristica}\n")
                    else:
                        print("Producto no encontrado. Asegúrate de escribir el nombre correctamente.\n")
                        print("Opciones disponibles: ", ', '.join(recomendaciones))

                    # Preguntar si desea buscar otro producto
                    continuar = input("¿Deseas buscar otro producto? (sí/no): ").strip().lower()
                    if continuar != 'sí' and continuar != 'si':
                        print("Gracias por usar el asistente de compras. ¡Hasta luego!")
                        break
                else:
                    print("Lo siento, no tenemos recomendaciones para esa categoría.")
            else:
                print("No comprendí tu solicitud. ¿Puedes ser más específico?")
        except UnicodeDecodeError:
            print("Error de codificación. Intenta ingresar tu consulta nuevamente.")