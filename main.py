import pygame
import random
import os
import math

# Configuración inicial
pygame.init()

# Tamaño de ventana y cartas
WIDTH, HEIGHT = 1920, 1080  # Resolución Full HD
CARD_WIDTH, CARD_HEIGHT = 120, 180  # Tamaño de las cartas ajustado

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clock Solitaire")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Diccionario para almacenar las cartas
card_images = {}
card_back = None

# Coordenadas de las pilas en forma de reloj
RADIUS = 320 # Radio del círculo aumentado para más espacio
CLOCK_POSITIONS = [
    (
        WIDTH // 2 + RADIUS * math.cos(i * (2 * math.pi / 12) - math.pi / 2),
        # Ajuste para comenzar en la parte superior
        HEIGHT // 2 + RADIUS * math.sin(i * (2 * math.pi / 12) - math.pi / 2)
    )
    for i in range(12)
]
CENTER_POSITION = (WIDTH // 2, HEIGHT // 2)  # Posición central para el Rey

# Crear pilas
piles = [[] for _ in range(13)]

# Cargar imagen de fondo
background_image = pygame.image.load(os.path.join("Sprites", "fondo.jpg"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Función para cargar imágenes
def load_card_images():
    global card_back
    sprites_dir = "Sprites"

    for file_name in os.listdir(sprites_dir):
        if file_name.endswith(".png"):
            name, _ = file_name.split(".")  # Quita la extensión
            image = pygame.image.load(os.path.join(sprites_dir, file_name))
            card_images[name] = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))

    # Cargar y redimensionar la parte trasera de las cartas
    if "atras" in card_images:
        card_back = card_images["atras"]
    else:
        card_back = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        card_back.fill(BLACK)  # Si no hay imagen de reverso, usamos un rectángulo negro

# Función para barajar y distribuir cartas
def shuffle_deck():
    deck = []
    for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
        for suit in ['brillo', 'trebol', 'corazon_negro', 'corazon_rojo']:
            key = f"{value}_{suit}"
            if key in card_images:
                deck.append(key)

    random.shuffle(deck)
    for i, card in enumerate(deck):
        piles[i % 13].append(card)

# Dibujar pilas de cartas con rotación
def draw_piles():
    for i, pile in enumerate(CLOCK_POSITIONS + [CENTER_POSITION]):
        if piles[i]:  # Si la pila tiene cartas
            card = piles[i][-1]  # La carta superior
            x, y = pile

            # Calcular el ángulo para inclinar la carta
            angle = (i * (360 / 12)) % 360 if i < 12 else 0  # Las cartas centrales no rotan

            # Rotar la imagen de la carta
            rotated_image = pygame.transform.rotate(card_images[card], -angle)  # Invertir signo para giro antihorario
            rect = rotated_image.get_rect(center=(x, y))

            # Dibujar la carta
            screen.blit(rotated_image, rect.topleft)
        else:  # Mostrar reverso si está vacío
            x, y = pile
            screen.blit(card_back, (x - CARD_WIDTH // 2, y - CARD_HEIGHT // 2))


# Lógica principal
def main():
    global card_images, card_back
    running = True
    clock = pygame.time.Clock()

    load_card_images()  # Cargar imágenes
    shuffle_deck()  # Barajar y distribuir cartas

    while running:
        screen.blit(background_image, (0, 0))  # Dibuja la imagen de fondo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dibujar elementos del juego
        draw_piles()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()