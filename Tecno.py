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

# 1.8. Configuración de juego (HUD, dificultad)
# Vidas, puntaje y niveles
VIDAS_INICIALES = 3
PUNTAJE_POR_SEGUNDO = 5
PUNTAJE_POR_MOUSE = 20
PUNTAJE_POR_RESPUESTA_CORRECTA = 100
PUNTAJE_POR_NIVEL = 500

# Rango de velocidades de obstáculos (se escala con el nivel)
VELOCIDAD_MIN_INICIAL = 2
VELOCIDAD_MAX_INICIAL = 6

# Variables globales que usan los obstáculos al (re)spawnear
velocidad_min = VELOCIDAD_MIN_INICIAL
velocidad_max = VELOCIDAD_MAX_INICIAL

# ====================================================================================================
# SECCIÓN 2: CARGA DE IMÁGENES Y RECURSOS
# ====================================================================================================

# Las imágenes deben estar en la misma carpeta que el script o en una subcarpeta especificada.
def cargar_imagen_segura(path, size=None, use_alpha=True, color_placeholder=AZUL_CIELO):
    try:
        imagen = pygame.image.load(path)
        imagen = imagen.convert_alpha() if use_alpha else imagen.convert()
        if size is not None:
            imagen = pygame.transform.scale(imagen, size)
        return imagen
    except (pygame.error, FileNotFoundError):
        # Placeholder sólido si no existe la imagen
        superficie = pygame.Surface(size if size else (50, 50))
        superficie.fill(color_placeholder)
        return superficie

# 2.1. Carga y escala las imágenes de fondo para los diferentes escenarios
imagen_fondo1 = cargar_imagen_segura('fondo1.png', (ANCHO_PANTALLA, ALTO_PANTALLA), use_alpha=False)
imagen_fondo2 = cargar_imagen_segura('fondo2.png', (ANCHO_PANTALLA, ALTO_PANTALLA), use_alpha=False)
imagen_fondo3 = cargar_imagen_segura('fondo3.png', (ANCHO_PANTALLA, ALTO_PANTALLA), use_alpha=False)

# Almacena todos los fondos en una lista para acceder a ellos fácilmente.
fondos_escenario = [imagen_fondo1, imagen_fondo2, imagen_fondo3]

# 2.2. Carga y escala la imagen del jugador
imagen_jugador = cargar_imagen_segura('rob.png', (130, 130), use_alpha=True)

# 2.3. Carga y escala las imágenes de los diferentes tipos de obstáculos
imagen_mouse = cargar_imagen_segura('mouse.png', (50, 50), use_alpha=True)
imagen_teclado = cargar_imagen_segura('teclado.png', (50, 50), use_alpha=True)
imagen_monitor = cargar_imagen_segura('monitor.png', (50, 50), use_alpha=True)
imagen_usb = cargar_imagen_segura('usb.png', (50, 50), use_alpha=True)

# 2.4. Carga y escala la imagen de la meta
imagen_meta = cargar_imagen_segura('meta.png', (100, 100), use_alpha=True)


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
        self.velocidad = random.randrange(velocidad_min, velocidad_max + 1)  # Velocidad de caída según dificultad.

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
            self.velocidad = random.randrange(velocidad_min, velocidad_max + 1)  # Nueva velocidad con dificultad.


# 3.3. Clase Meta: Representa el objetivo final del juego.
class Meta(pygame.sprite.Sprite):
    def __init__(self):
        """Constructor de la clase Meta."""
        super().__init__()  # Llama al constructor de la clase padre.
        self.image = imagen_meta  # Asigna la imagen de la meta.
        self.rect = self.image.get_rect()  # Obtiene el rectángulo del sprite.

        # Posición de la meta en el extremo superior derecho de la pantalla.
        self.rect.top = 10  # A 10 píxeles del borde superior.
        self.rect.right = ANCHO_PANTALLA - 10  # A 10 píxeles del borde derecho.


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


# 5.1.1. Función para dibujar el HUD (puntaje, vidas, nivel)
def dibujar_hud(pantalla, puntaje, vidas, nivel):
    texto_puntaje = fuente_normal.render(f"Puntos: {puntaje}", True, BLANCO)
    texto_vidas = fuente_normal.render(f"Vidas: {vidas}", True, BLANCO)
    texto_nivel = fuente_normal.render(f"Nivel: {nivel}", True, BLANCO)

    pantalla.blit(texto_puntaje, (10, 10))
    pantalla.blit(texto_vidas, (10, 45))
    pantalla.blit(texto_nivel, (10, 80))


# 5.1.2. Pantalla de fin (victoria/derrota) con opción de volver al menú
def mostrar_pantalla_fin(mensaje, puntaje):
    en_fin = True
    while en_fin:
        pantalla.blit(fondos_escenario[0], (0, 0))
        titulo = fuente_grande.render(mensaje, True, BLANCO)
        puntaje_txt = fuente_normal.render(f"Puntaje final: {puntaje}", True, BLANCO)
        instr = fuente_normal.render("ENTER: menú  |  ESC: salir", True, BLANCO)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 - 40)))
        pantalla.blit(puntaje_txt, puntaje_txt.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2)))
        pantalla.blit(instr, instr.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 + 50)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_fin = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 'menu'
                if event.key == pygame.K_ESCAPE:
                    return 'salir'


# 5.2. Función para manejar la lógica de las preguntas de opción múltiple.
def manejar_pregunta():
    """
    Presenta una pregunta de opción múltiple al jugador.
    Devuelve True si la respuesta es correcta, False si es incorrecta.
    """
    pregunta_actual = random.choice(preguntas_tecnologia)  # Elige una pregunta al azar de la lista.
    mostrando_pregunta = True  # Bandera para controlar el bucle de la pregunta.
    tiempo_limite_ms = 10000  # 10 segundos
    inicio = pygame.time.get_ticks()

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

        # 5.2.3. Temporizador visual
        restante_ms = max(0, tiempo_limite_ms - (pygame.time.get_ticks() - inicio))
        segundos = int(restante_ms / 1000)
        texto_timer = fuente_normal.render(f"Tiempo: {segundos}", True, ROJO if segundos <= 3 else BLANCO)
        pantalla.blit(texto_timer, (ANCHO_PANTALLA - 180, 10))
        pygame.display.flip()  # Actualiza la pantalla para mostrar la pregunta y las opciones.

        if restante_ms == 0:
            mostrar_mensaje("¡Tiempo agotado!", ROJO)
            return False

        # 5.2.4. Bucle de eventos para esperar la respuesta del usuario.
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

                # 5.2.5. Verifica la respuesta
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
    en_menu = True
    en_pausa = False

    # HUD y dificultad
    puntaje = 0
    vidas = VIDAS_INICIALES
    nivel = 1
    tiempo_desde_ultimo_nivel = 0  # milisegundos

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
        # Menú de inicio simple
        while en_menu:
            pantalla.blit(fondos_escenario[0], (0, 0))
            titulo = fuente_grande.render("Tecno-Escape", True, BLANCO)
            instruccion = fuente_normal.render("Presiona ENTER para iniciar", True, BLANCO)
            pantalla.blit(titulo, titulo.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 - 40)))
            pantalla.blit(instruccion, instruccion.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2)))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jugando = False
                    en_menu = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    en_menu = False
        # 6.6.1. Controlar la velocidad de fotogramas
        dt_ms = reloj.tick(60)  # Limita a 60 FPS y devuelve ms transcurridos.
        tiempo_desde_ultimo_nivel += dt_ms
        # Puntaje por tiempo
        puntaje += int(PUNTAJE_POR_SEGUNDO * (dt_ms / 1000))

        # 6.6.2. Manejo de eventos del usuario
        for event in pygame.event.get():  # Itera a través de todos los eventos ocurridos.
            if event.type == pygame.QUIT:  # Si el usuario hace clic en el botón de cerrar ventana...
                jugando = False  # ...cambia la bandera para salir del bucle.
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                en_pausa = not en_pausa

        # Pantalla de pausa
        while en_pausa and jugando:
            pausa_txt = fuente_grande.render("Pausa", True, BLANCO)
            instr = fuente_normal.render("Pulsa P para continuar", True, BLANCO)
            pantalla.blit(fondos_escenario[escenario_actual], (0, 0))
            todos_los_sprites.draw(pantalla)
            dibujar_hud(pantalla, puntaje, vidas, nivel)
            pantalla.blit(pausa_txt, pausa_txt.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 - 30)))
            pantalla.blit(instr, instr.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 + 20)))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jugando = False
                    en_pausa = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    en_pausa = False

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
                        vidas -= 1
                        if vidas <= 0:
                            mostrar_mensaje("¡Te quedaste sin vidas!", ROJO)
                            accion = mostrar_pantalla_fin("Game Over", puntaje)
                            if accion == 'menu':
                                return main()
                            else:
                                jugando = False
                        else:
                            mostrar_mensaje(f"Respuesta incorrecta. Vidas: {vidas}", ROJO)
                    else:
                        puntaje += PUNTAJE_POR_RESPUESTA_CORRECTA

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
                    puntaje += PUNTAJE_POR_MOUSE
                    print("Chocaste con un mouse, sigues adelante!")

        # 6.6.6. Detección de colisión con la meta (condición de victoria)
        # Se pasa [meta] como una lista para que spritecollide lo trate como un grupo con un solo elemento.
        colision_meta = pygame.sprite.spritecollide(jugador, [meta], False)
        if colision_meta:  # Si el jugador colisiona con la meta.
            puntaje += PUNTAJE_POR_NIVEL * nivel
            mostrar_mensaje("¡Felicidades, has llegado a la meta!", VERDE)
            accion = mostrar_pantalla_fin("¡Victoria!", puntaje)
            if accion == 'menu':
                # Reiniciar estado para volver al menú
                return main()
            else:
                jugando = False

        # 6.6.7. Dibujar / Renderizar
        pantalla.blit(fondos_escenario[escenario_actual], (0, 0))  # Dibuja el fondo de pantalla actual.
        todos_los_sprites.draw(pantalla)  # Dibuja todos los sprites en la pantalla.
        # Dibujar HUD
        dibujar_hud(pantalla, puntaje, vidas, nivel)

        # Escalado de dificultad por tiempo (cada ~20s aumenta nivel)
        if tiempo_desde_ultimo_nivel >= 20000:
            tiempo_desde_ultimo_nivel = 0
            nivel += 1
            # Aumentar ligeramente velocidades globales
            global velocidad_min, velocidad_max
            velocidad_min = min(velocidad_min + 1, 10)
            velocidad_max = min(velocidad_max + 1, 14)
            # Recalibrar velocidades actuales de obstáculos (opcional)
            for obs in obstaculos:
                obs.velocidad = random.randrange(velocidad_min, velocidad_max + 1)

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