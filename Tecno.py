# ====================================================================================================
# SECCIÓN 1: IMPORTACIONES Y CONFIGURACIÓN INICIAL
# ====================================================================================================

# 1.1. Importar módulos necesarios
import pygame  # Importa la librería Pygame para el desarrollo de juegos.
import sys  # Importa el módulo sys para funciones relacionadas con el sistema (ej. salir del programa).
import random  # Importa el módulo random para generar números y selecciones aleatorias.

# 1.2. Inicialización de Pygame
pygame.init()  # Inicializa todos los módulos de Pygame. Esto es MANDATORIO al principio.
pygame.font.init()  # Inicializa el módulo de fuentes para poder usar texto en el juego.

# 1.3. Definiciones de colores (en formato RGB)
BLANCO = (255, 255, 255)  # Color blanco puro.
NEGRO = (0, 0, 0)  # Color negro puro.
ROJO = (255, 0, 0)  # Color rojo puro.
VERDE = (0, 255, 0)  # Color verde puro.
AZUL = (0, 0, 255)  # Color azul puro.
GRIS = (200, 200, 200)  # Un tono de gris claro.
AZUL_CIELO = (135, 206, 235)  # Un tono de azul para el cielo.

# 1.4. Configuración de las dimensiones de la pantalla del juego
ANCHO_PANTALLA = 800  # Ancho de la ventana del juego en píxeles.
ALTO_PANTALLA = 600  # Alto de la ventana del juego en píxeles.

# 1.5. Configuración de la pantalla del juego
# Crea la ventana del juego con el tamaño especificado. Esto inicializa el "display".
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
# Establece el título de la ventana del juego.
pygame.display.set_caption("Tecno-Escape: El Laberinto de Bits")

# 1.6. Configuración del reloj del juego para controlar los FPS (fotogramas por segundo)
reloj = pygame.time.Clock()  # Crea un objeto Clock para controlar la velocidad de actualización del juego.

# 1.7. Configuración de fuentes para mostrar texto
# Define una fuente para el texto normal del juego (preguntas, opciones, etc.).
fuente_normal = pygame.font.SysFont('Arial', 30)
# Define una fuente más grande para mensajes importantes (victoria, derrota).
fuente_grande = pygame.font.SysFont('Arial', 50)

# ====================================================================================================
# SECCIÓN 2: CARGA DE IMÁGENES Y RECURSOS
# ====================================================================================================

# Las imágenes deben estar en la misma carpeta que el script o en una subcarpeta especificada.
try:
    # 2.1. Carga y escala las imágenes de fondo para los diferentes escenarios
    # .convert() optimiza la imagen para la pantalla del juego.
    imagen_fondo1 = pygame.image.load('fondo1.png').convert()
    imagen_fondo1 = pygame.transform.scale(imagen_fondo1, (ANCHO_PANTALLA, ALTO_PANTALLA))

    imagen_fondo2 = pygame.image.load('fondo2.png').convert()
    imagen_fondo2 = pygame.transform.scale(imagen_fondo2, (ANCHO_PANTALLA, ALTO_PANTALLA))

    imagen_fondo3 = pygame.image.load('fondo3.png').convert()
    imagen_fondo3 = pygame.transform.scale(imagen_fondo3, (ANCHO_PANTALLA, ALTO_PANTALLA))

    # Almacena todos los fondos en una lista para acceder a ellos fácilmente.
    fondos_escenario = [imagen_fondo1, imagen_fondo2, imagen_fondo3]

    # 2.2. Carga y escala la imagen del jugador
    # .convert_alpha() se usa para imágenes con transparencia (como PNGs).
    imagen_jugador = pygame.image.load('rob.png').convert_alpha()
    imagen_jugador = pygame.transform.scale(imagen_jugador, (130,130))

    # 2.3. Carga y escala las imágenes de los diferentes tipos de obstáculos
    imagen_mouse = pygame.image.load('mouse.png').convert_alpha()
    imagen_teclado = pygame.image.load('teclado.png').convert_alpha()
    imagen_monitor = pygame.image.load('monitor.png').convert_alpha()
    imagen_usb = pygame.image.load('usb.png').convert_alpha()

    # 2.4. Carga y escala la imagen de la meta
    imagen_meta = pygame.image.load('meta.png').convert_alpha()
    imagen_meta = pygame.transform.scale(imagen_meta, (100, 100))

except pygame.error as e:
    # Captura cualquier error si una imagen no se encuentra o no se puede cargar.
    print(f"Error al cargar una imagen: {e}")
    pygame.quit()  # Cierra Pygame.
    sys.exit()  # Sale del programa.


# ====================================================================================================
# SECCIÓN 3: DEFINICIÓN DE CLASES DE OBJETOS DEL JUEGO (SPRITES)
# ====================================================================================================

# 3.1. Clase Jugador: Representa el sprite controlable por el usuario.
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        """Constructor de la clase Jugador."""
        super().__init__()  # Llama al constructor de la clase padre (pygame.sprite.Sprite).
        self.image = imagen_jugador  # Asigna la imagen cargada al sprite del jugador.
        self.rect = self.image.get_rect()  # Obtiene el rectángulo que define la posición y tamaño del sprite.

        # Posición inicial del jugador en el centro inferior de la pantalla.
        self.rect.centerx = ANCHO_PANTALLA // 2  # Centra horizontalmente.
        self.rect.bottom = ALTO_PANTALLA - 10  # A 10 píxeles del borde inferior.
        self.velocidad = 5  # Define la velocidad de movimiento del jugador en píxeles por fotograma.

    def update(self):
        """
        Actualiza la posición del jugador en cada fotograma del juego
        según la entrada del teclado y lo mantiene dentro de los límites de la pantalla.
        """
        keys = pygame.key.get_pressed()  # Obtiene el estado de todas las teclas (presionadas o no).

        # Movimiento horizontal:
        if keys[pygame.K_LEFT]:  # Si la tecla de flecha izquierda está presionada...
            self.rect.x -= self.velocidad  # ...mueve el jugador a la izquierda.
        if keys[pygame.K_RIGHT]:  # Si la tecla de flecha derecha está presionada...
            self.rect.x += self.velocidad  # ...mueve el jugador a la derecha.

        # Movimiento vertical:
        if keys[pygame.K_UP]:  # Si la tecla de flecha arriba está presionada...
            self.rect.y -= self.velocidad  # ...mueve el jugador hacia arriba.
        if keys[pygame.K_DOWN]:  # Si la tecla de flecha abajo está presionada...
            self.rect.y += self.velocidad  # ...mueve el jugador hacia abajo.

        # 3.1.1. Limitar el movimiento del jugador dentro de los bordes de la pantalla
        if self.rect.right > ANCHO_PANTALLA:  # Si el borde derecho del jugador excede el ancho de la pantalla...
            self.rect.right = ANCHO_PANTALLA  # ...ajusta su posición al borde.
        if self.rect.left < 0:  # Si el borde izquierdo del jugador es menor que 0...
            self.rect.left = 0  # ...ajusta su posición al borde izquierdo.
        if self.rect.bottom > ALTO_PANTALLA:  # Si el borde inferior del jugador excede el alto de la pantalla...
            self.rect.bottom = ALTO_PANTALLA  # ...ajusta su posición al borde inferior.
        if self.rect.top < 0:  # Si el borde superior del jugador es menor que 0...
            self.rect.top = 0  # ...ajusta su posición al borde superior.


# 3.2. Clase Obstaculo: Representa los dispositivos informáticos que bajan por la pantalla.
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, tipo_obstaculo):
        """
        Constructor de la clase Obstaculo.
        Recibe 'tipo_obstaculo' para asignar la imagen correcta y determinar su comportamiento.
        """
        super().__init__()  # Llama al constructor de la clase padre.
        self.tipo = tipo_obstaculo  # Guarda el tipo de obstáculo (ej. "mouse", "teclado").

        # 3.2.1. Asigna la imagen y escala según el tipo de obstáculo
        if self.tipo == "mouse":
            self.image = pygame.transform.scale(imagen_mouse, (50, 50))
        elif self.tipo == "teclado":
            self.image = pygame.transform.scale(imagen_teclado, (50, 50))
        elif self.tipo == "monitor":
            self.image = pygame.transform.scale(imagen_monitor, (50, 50))
        elif self.tipo == "usb":
            self.image = pygame.transform.scale(imagen_usb, (50, 50))
        else:  # En caso de un tipo no reconocido, usa una imagen por defecto o un color.
            self.image = pygame.Surface([50, 50])
            self.image.fill(AZUL_CIELO)  # Color de respaldo si no hay imagen.

        self.rect = self.image.get_rect()  # Obtiene el rectángulo del sprite.

        # 3.2.2. Posición inicial aleatoria en la parte superior fuera de la pantalla.
        self.rect.x = random.randrange(ANCHO_PANTALLA - self.rect.width)  # Posición X aleatoria.
        self.rect.y = random.randrange(-100, -40)  # Posición Y inicial por encima de la pantalla.
        self.velocidad = random.randrange(1, 8)  # Velocidad de caída aleatoria.

    def update(self):
        """
        Actualiza la posición del obstáculo en cada fotograma, moviéndolo hacia abajo.
        Si sale de la pantalla, lo resetea en la parte superior.
        """
        self.rect.y += self.velocidad  # Mueve el obstáculo hacia abajo.

        # 3.2.3. Reiniciar el obstáculo si sale de la pantalla
        if self.rect.top > ALTO_PANTALLA + 10:  # Si el obstáculo está completamente fuera de la pantalla por abajo...
            self.rect.x = random.randrange(
                ANCHO_PANTALLA - self.rect.width)  # ...lo mueve a una nueva posición X aleatoria.
            self.rect.y = random.randrange(-100, -40)  # ...y lo coloca de nuevo por encima de la pantalla.
            self.velocidad = random.randrange(1, 8)  # ...y le asigna una nueva velocidad aleatoria.


# 3.3. Clase Meta: Representa el objetivo final del juego.
class Meta(pygame.sprite.Sprite):
    def __init__(self):
        """Constructor de la clase Meta."""
        super().__init__()  # Llama al constructor de la clase padre.
        self.image = imagen_meta  # Asigna la imagen de la meta.
        self.rect = self.image.get_rect()  # Obtiene el rectángulo del sprite.

        # Posición de la meta en el extremo superior derecho de la pantalla.
        self.rect.top = 10  # A 10 píxeles del borde superior.
        self.rect.right = ANCHO_PANTALLA - 350  # A 10 píxeles del borde derecho.


# ====================================================================================================
# SECCIÓN 4: DEFINICIÓN DEL BANCO DE PREGUNTAS
# ====================================================================================================

# Lista de diccionarios, donde cada diccionario representa una pregunta.
# Cada pregunta tiene:
# - "pregunta": El texto de la pregunta.
# - "opciones": Una lista de cadenas con las posibles respuestas.
# - "correcta": El índice (0, 1, 2, 3) de la opción correcta en la lista "opciones".
preguntas_tecnologia = [
    {
        "pregunta": "¿Qué es la CPU?",
        "opciones": ["Unidad de Procesamiento Central", "Disco duro", "Memoria RAM", "Tarjeta gráfica"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué significa 'bug' en programación?",
        "opciones": ["Un atajo de teclado", "Un error en el código", "Una función matemática", "Un tipo de dato"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué componente almacena datos a largo plazo?",
        "opciones": ["RAM", "Placa madre", "Disco duro", "Procesador"],
        "correcta": 2
    },
    {
        "pregunta": "¿Qué es la RAM?",
        "opciones": ["Un tipo de cable", "Memoria de acceso aleatorio", "Un disco duro externo",
                     "La velocidad del procesador"],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuál es el atajo de teclado para copiar?",
        "opciones": ["Ctrl + V", "Ctrl + Z", "Ctrl + C", "Ctrl + P"],
        "correcta": 2
    }
]


# ====================================================================================================
# SECCIÓN 5: FUNCIONES AUXILIARES (MENSAJES Y MANEJO DE PREGUNTAS)
# ====================================================================================================

# 5.1. Función para mostrar mensajes temporales en pantalla (victoria, derrota)
def mostrar_mensaje(mensaje, color):
    """
    Muestra un mensaje centrado en la pantalla durante 2 segundos.
    mensaje: La cadena de texto a mostrar.
    color: La tupla RGB del color del texto.
    """
    texto = fuente_grande.render(mensaje, True, color)  # Renderiza el texto con la fuente grande y el color.
    rect = texto.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))  # Centra el rectángulo del texto.
    pantalla.blit(texto, rect)  # Dibuja el texto en la pantalla.
    pygame.display.flip()  # Actualiza toda la pantalla para mostrar el mensaje.
    pygame.time.wait(2000)  # Pausa el juego por 2000 milisegundos (2 segundos).


# 5.2. Función para manejar la lógica de las preguntas de opción múltiple.
def manejar_pregunta():
    """
    Presenta una pregunta de opción múltiple al jugador.
    Devuelve True si la respuesta es correcta, False si es incorrecta.
    """
    pregunta_actual = random.choice(preguntas_tecnologia)  # Elige una pregunta al azar de la lista.
    mostrando_pregunta = True  # Bandera para controlar el bucle de la pregunta.

    while mostrando_pregunta:
        pantalla.fill(AZUL)  # Limpia la pantalla con un fondo negro para la pregunta.

        # 5.2.1. Muestra el texto de la pregunta
        texto_pregunta = fuente_normal.render(pregunta_actual["pregunta"], True, BLANCO)  # Renderiza la pregunta.
        rect_pregunta = texto_pregunta.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 100))  # Centra.
        pantalla.blit(texto_pregunta, rect_pregunta)  # Dibuja la pregunta.

        # 5.2.2. Muestra las opciones numeradas
        y_pos = ALTO_PANTALLA // 2 - 20  # Posición Y inicial para la primera opción.
        for i, opcion in enumerate(pregunta_actual["opciones"]):  # Itera sobre las opciones.
            texto_opcion = fuente_normal.render(f"{i + 1}. {opcion}", True,
                                                GRIS)  # Renderiza la opción (ej. "1. Opción").
            rect_opcion = texto_opcion.get_rect(left=ANCHO_PANTALLA // 2 - 200,
                                                top=y_pos + i * 50)  # Posiciona la opción.
            pantalla.blit(texto_opcion, rect_opcion)  # Dibuja la opción.

        pygame.display.flip()  # Actualiza la pantalla para mostrar la pregunta y las opciones.

        # 5.2.3. Bucle de eventos para esperar la respuesta del usuario.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Si el usuario cierra la ventana...
                pygame.quit()  # ...cierra Pygame.
                sys.exit()  # ...sale del programa.
            elif evento.type == pygame.KEYDOWN:  # Si se presiona una tecla...
                opcion_elegida = -1  # Variable para almacenar el índice de la opción elegida.

                # Mapea las teclas numéricas a los índices de las opciones.
                if evento.key == pygame.K_1:
                    opcion_elegida = 0
                elif evento.key == pygame.K_2:
                    opcion_elegida = 1
                elif evento.key == pygame.K_3:
                    opcion_elegida = 2
                elif evento.key == pygame.K_4:
                    opcion_elegida = 3

                # 5.2.4. Verifica la respuesta
                if opcion_elegida != -1:  # Si se presionó una tecla numérica válida...
                    if opcion_elegida == pregunta_actual["correcta"]:  # ...y es la respuesta correcta...
                        print("Respuesta correcta. ¡Continúas el juego!")
                        return True  # ...devuelve True para continuar el juego.
                    else:  # ...si no es la respuesta correcta...
                        print("Respuesta incorrecta. Fin del juego.")
                        mostrar_mensaje("¡Respuesta incorrecta! Fin del juego.", ROJO)  # Muestra mensaje de derrota.
                        return False  # ...devuelve False para terminar el juego.


# ====================================================================================================
# SECCIÓN 6: FUNCIÓN PRINCIPAL DEL JUEGO (GAME LOOP)
# ====================================================================================================

def main():
    """
    Función principal que contiene el bucle del juego y toda la lógica de ejecución.
    """
    jugando = True  # Bandera que controla si el juego está en ejecución.

    # 6.1. Creación de grupos de sprites
    # Grupos para organizar los objetos del juego.
    todos_los_sprites = pygame.sprite.Group()  # Contiene todos los sprites para dibujarlos y actualizarlos.
    obstaculos = pygame.sprite.Group()  # Contiene solo los obstáculos para la detección de colisiones.

    # 6.2. Creación del jugador
    jugador = Jugador()  # Crea una instancia del jugador.
    todos_los_sprites.add(jugador)  # Añade el jugador al grupo de todos los sprites.

    # 6.3. Creación de la meta
    meta = Meta()  # Crea una instancia de la meta.
    todos_los_sprites.add(meta)  # Añade la meta al grupo de todos los sprites.

    # 6.4. Generación inicial de obstáculos
    tipos_obstaculos = ["mouse", "teclado", "usb", "monitor"]  # Tipos de obstáculos disponibles.
    for i in range(10):  # Genera 10 obstáculos iniciales.
        tipo_aleatorio = random.choice(tipos_obstaculos)  # Elige un tipo al azar.
        obstaculo = Obstaculo(tipo_aleatorio)  # Crea el obstáculo con el tipo elegido.
        todos_los_sprites.add(obstaculo)  # Añade al grupo de todos los sprites.
        obstaculos.add(obstaculo)  # Añade al grupo de obstáculos.

    # 6.5. Variables para controlar el cambio de escenario
    escenario_actual = 0  # Inicia en el primer escenario (índice 0).
    # Define los umbrales de altura para cambiar de fondo.
    # A medida que el jugador sube (su coordenada 'y' disminuye), pasará por estos umbrales.
    umbrales_escenario = [ALTO_PANTALLA * 0.7, ALTO_PANTALLA * 0.4]
    # Ejemplo:
    # - Si el jugador sube por encima del 70% de la pantalla (ALTO_PANTALLA * 0.7), cambia a fondo 2.
    # - Si el jugador sube por encima del 40% de la pantalla (ALTO_PANTALLA * 0.4), cambia a fondo 3.

    # 6.6. Bucle principal del juego (Game Loop)
    while jugando:
        # 6.6.1. Controlar la velocidad de fotogramas
        reloj.tick(60)  # Limita el bucle a un máximo de 60 fotogramas por segundo.

        # 6.6.2. Manejo de eventos del usuario
        for event in pygame.event.get():  # Itera a través de todos los eventos ocurridos.
            if event.type == pygame.QUIT:  # Si el usuario hace clic en el botón de cerrar ventana...
                jugando = False  # ...cambia la bandera para salir del bucle.

        # 6.6.3. Actualizar la posición y estado de todos los sprites
        todos_los_sprites.update()  # Llama al método update() de cada sprite en el grupo.

        # 6.6.4. Lógica para cambiar el fondo de pantalla según el avance del jugador
        if jugador.rect.y < umbrales_escenario[0] and escenario_actual == 0:
            escenario_actual = 1  # Cambia al segundo escenario.
            print("Cambiando a escenario 2")

        if len(umbrales_escenario) > 1 and jugador.rect.y < umbrales_escenario[1] and escenario_actual == 1:
            escenario_actual = 2  # Cambia al tercer escenario.
            print("Cambiando a escenario 3")

        # 6.6.5. Detección de colisiones con los obstáculos
        # pygame.sprite.spritecollide(sprite_individual, grupo_sprites, do_kill)
        # do_kill=False significa que los sprites en el grupo no se eliminan al colisionar automáticamente.
        colisiones_obstaculos = pygame.sprite.spritecollide(jugador, obstaculos, False)
        if colisiones_obstaculos:  # Si hubo al menos una colisión con un obstáculo.
            for obstaculo_chocado in colisiones_obstaculos:  # Itera sobre cada obstáculo colisionado.
                # Verifica el tipo de obstáculo para decidir si activar la pregunta.
                if obstaculo_chocado.tipo in ["teclado", "usb"]:  # Si es un teclado o USB (obstáculos peligrosos).
                    # Elimina el obstáculo colisionado para que no cause más colisiones o preguntas.
                    obstaculos.remove(obstaculo_chocado)
                    todos_los_sprites.remove(obstaculo_chocado)

                    # Activa la lógica de la pregunta.
                    if not manejar_pregunta():  # Si la función devuelve False (respuesta INCORRECTA)...
                        jugando = False  # ...el juego termina.

                elif obstaculo_chocado.tipo == "monitor":  # Si choca con un monitor
                    # Opcional: Podrías hacer que el jugador pierda vida, o simplemente que el obstáculo desaparezca.
                    # Por ahora, simplemente lo removemos para que no estorbe.
                    obstaculos.remove(obstaculo_chocado)
                    todos_los_sprites.remove(obstaculo_chocado)
                    print("Chocaste con un monitor, pero sigues adelante!")

                elif obstaculo_chocado.tipo == "mouse":  # Si choca con un mouse (obstáculo seguro).
                    # Simplemente elimina el mouse para que no se quede estorbando, no pasa nada.
                    obstaculos.remove(obstaculo_chocado)
                    todos_los_sprites.remove(obstaculo_chocado)
                    print("Chocaste con un mouse, sigues adelante!")

        # 6.6.6. Detección de colisión con la meta (condición de victoria)
        # Se pasa [meta] como una lista para que spritecollide lo trate como un grupo con un solo elemento.
        colision_meta = pygame.sprite.spritecollide(jugador, [meta], False)
        if colision_meta:  # Si el jugador colisiona con la meta.
            mostrar_mensaje("¡Felicidades, has llegado a la meta!", VERDE)  # Muestra mensaje de victoria.
            jugando = False  # Termina el juego.

        # 6.6.7. Dibujar / Renderizar
        pantalla.blit(fondos_escenario[escenario_actual], (0, 0))  # Dibuja el fondo de pantalla actual.
        todos_los_sprites.draw(pantalla)  # Dibuja todos los sprites en la pantalla.

        # 6.6.8. Actualizar la pantalla
        pygame.display.flip()  # Muestra todo lo que se ha dibujado en la pantalla.


# ====================================================================================================
# SECCIÓN 7: INICIO DEL PROGRAMA
# ====================================================================================================

# Comprueba si el script se está ejecutando directamente (no importado como módulo).
if __name__ == "__main__":
    main()  # Llama a la función principal para iniciar el juego.
    pygame.quit()  # Desinicializa todos los módulos de Pygame.
    sys.exit()  # Sale completamente del programa.