import sys, pygame, os, math
from pygame.locals import *
import cards
import random

pygame.init()

ANCHO, ALTO = 1920, 1080
ANCHO_CARTA, ALTO_CARTA = 120, 180
RADIO = 400

tamaño = ANCHO, ALTO
pantalla = pygame.display.set_mode(tamaño)
pygame.display.set_caption("Solitario del Reloj 0.1 beta")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Ajusta el centro del reloj para que esté más centrado verticalmente
CENTRO_X, CENTRO_Y = ANCHO // 2, ALTO // 2 - 100

# Desplaza las posiciones una a la derecha
posicion_hora = [
    (
        CENTRO_X + RADIO * math.cos((i + 1) * (2 * math.pi / 12) - math.pi / 2),
        CENTRO_Y + RADIO * math.sin((i + 1) * (2 * math.pi / 12) - math.pi / 2)
    )
    for i in range(12)
]
posicion_hora.append((CENTRO_X, CENTRO_Y))

imagen_fondo = pygame.image.load(os.path.join("Sprites", "fondo.jpg"))
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))

lista_horas = {simbolo: i for i, simbolo in
               enumerate(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'])}


def cargar_imagenes_cartas():
    dir_sprites = "Sprites"
    for nombre_archivo in os.listdir(dir_sprites):
        if nombre_archivo.endswith(".png"):
            nombre, _ = nombre_archivo.split(".")
            imagen = pygame.image.load(os.path.join(dir_sprites, nombre_archivo))
            cards.imagenes_cartas[nombre] = pygame.transform.scale(imagen, (ANCHO_CARTA, ALTO_CARTA))

    cards.carta_atras = cards.imagenes_cartas.get("atras", pygame.Surface((ANCHO_CARTA, ALTO_CARTA)))
    if "atras" not in cards.imagenes_cartas:
        cards.carta_atras.fill(NEGRO)


cargar_imagenes_cartas()


def dibujar_cartas(ancho, alto, hora):
    # Dibuja todas las cartas excepto la última (la carta superior)
    for carta in reloj[hora][1:]:
        superficie_carta = carta.carta
        rect_carta = superficie_carta.get_rect()
        rect_mitad = pygame.Rect(0, 0, min(cards.carta_atras.get_width(), rect_carta.width),
                                 min(cards.carta_atras.get_height(), rect_carta.height))
        pantalla.blit(superficie_carta.subsurface(rect_mitad), (ancho, alto))
        ancho += 12  # Cambia el desplazamiento horizontal a positivo
        alto -= 5  # Cambia el desplazamiento vertical a negativo

    # Dibuja únicamente la carta superior (si existe)
    if reloj[hora]:
        pantalla.blit(reloj[hora][0].carta, (ancho, alto))


def dibujar_tablero():
    for i in range(13):
        dibujar_cartas(posicion_hora[i][0], posicion_hora[i][1], i)


def barajeo_americano(mazo):
    mitad = len(mazo) // 2
    izquierda = mazo[:mitad]
    derecha = mazo[mitad:]
    mazo_barajeado = []

    while izquierda or derecha:
        for _ in range(random.randint(1, 5)):
            if izquierda:
                mazo_barajeado.append(izquierda.pop(0))
        for _ in range(random.randint(1, 5)):
            if derecha:
                mazo_barajeado.append(derecha.pop(0))

    return mazo_barajeado


def barajar_cartas():
    global reloj
    reloj = [[] for _ in range(13)]
    for _ in range(10):  # Realizar el barajeo americano 10 veces
        cards.talia = barajeo_americano(cards.talia)
    for i, carta in enumerate(cards.talia):
        reloj[i // 4].append(carta)
        carta.ocultar()
    reloj[12][0].mostrar()
    global hora_llena
    hora_llena = [False] * 13


def verificar_si_lleno(ite):
    if ite != 12:
        hora_llena[ite] = len(reloj[ite]) == 4 and all(not carta.oculta for carta in reloj[ite])
    else:
        hora_llena[ite] = len(reloj[ite]) == 4 and all(
            not carta.oculta and carta.simbolo == "K" for carta in reloj[ite])


def ganar():
    pantalla.fill(NEGRO)
    imagen_ganar = pygame.image.load("Sprites/gano.png")
    imagen_ganar = pygame.transform.scale(imagen_ganar, (ANCHO // 2, ALTO // 2))
    pantalla.blit(imagen_ganar, ((ANCHO - imagen_ganar.get_width()) // 2, (ALTO - imagen_ganar.get_height()) // 2))
    pygame.display.flip()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == K_x:
                    pygame.quit()
                    sys.exit()
                if evento.key == K_r:
                    bucle_principal()


def perder():
    pantalla.fill(NEGRO)
    imagen_perder = pygame.image.load("Sprites/perdio.png")
    imagen_perder = pygame.transform.scale(imagen_perder, (ANCHO // 2, ALTO // 2))
    pantalla.blit(imagen_perder, ((ANCHO - imagen_perder.get_width()) // 2, (ALTO - imagen_perder.get_height()) // 2))
    pygame.display.flip()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == K_x:
                    pygame.quit()
                    sys.exit()
                if evento.key == K_r:
                    bucle_principal()

def bucle_principal():
    barajar_cartas()
    perdido = False
    atrapado = False
    Objetivo = None
    pos_temp = None

    while True:
        pantalla.blit(imagen_fondo, (0, 0))
        pos = pygame.mouse.get_pos()
        tecla = pygame.key.get_pressed()

        if not perdido:
            dibujar_tablero()
        else:
            perder()

        if all(hora_llena):
            ganar()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for ite in range(13):
                    if (posicion_hora[ite][0] <= pos[0] <= posicion_hora[ite][0] + ANCHO_CARTA and
                            posicion_hora[ite][1] <= pos[1] <= posicion_hora[ite][1] + ALTO_CARTA and
                            not reloj[ite][0].oculta and not hora_llena[ite]):
                        Objetivo = reloj[ite].pop(0)
                        pos_temp = ite
                        atrapado = True
                        verificar_si_lleno(ite)
                        break
                else:
                    atrapado = False
            if evento.type == pygame.MOUSEBUTTONUP and atrapado:
                for ite in range(13):
                    if (posicion_hora[ite][0] <= pos[0] <= posicion_hora[ite][0] + ANCHO_CARTA and
                            posicion_hora[ite][1] <= pos[1] <= posicion_hora[ite][1] + ALTO_CARTA and
                            lista_horas[Objetivo.simbolo] == ite):
                        reloj[ite].append(Objetivo)
                        reloj[ite][0].mostrar()
                        Objetivo = None
                        verificar_si_lleno(ite)
                        if hora_llena[ite] and ite != 12:
                            for i in range(ite, 13):
                                if i >= 12:
                                    i -= 12
                                reloj[i + 1][0].mostrar()
                        elif hora_llena[ite] and ite == 12:
                            perdido = True
                        break
                else:
                    if pos_temp is not None:
                        reloj[pos_temp].insert(0, Objetivo)
                        hora_llena[pos_temp] = False
                        Objetivo = None
                        pos_temp = None

        if tecla[K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if atrapado and Objetivo:
            pantalla.blit(Objetivo.carta, (pos[0] - 20, pos[1] - 20))

        pygame.display.flip()


bucle_principal()
