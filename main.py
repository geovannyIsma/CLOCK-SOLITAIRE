import pygame
import random
import os
import math

# Configuración inicial
pygame.init()
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.key = f"{value}_{suit}"
        self.back = True

    def flip(self):
        self.back = False

deck = []
k_hands = {}
move_count = 0
card = 13
resultado = ""

def initialize_deck(self):
    global deck
    suits = ['brillo', 'trebol', 'corazon_negro', 'corazon_rojo']
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    self.deck.clear()

    for suit in suits:
        for value in values:
            self.deck.append(Card(suit, value))

def shuffle(self):
    for _ in range(9):
        self.american_shuffle()


def american_shuffle(self):
    global deck
    mitad = len(deck) // 2
    temp_deck = []
    left = deck[:mitad]
    right = deck[mitad:]

    while left or right:
        for _ in range(random.randint(1, 5)):
            if left:
                temp_deck.append(left.pop(0))
        for _ in range(random.randint(1, 5)):
            if right:
                temp_deck.append(right.pop(0))

    deck.clear()
    deck.extend(temp_deck)

def clock_dealing():
    global k_hands
    global deck
    k_hands.clear()
    for i in range(1, 14):
        hand = []
        for _ in range(4):
            if len(deck) > 0:
                hand.append(deck.pop(0))
        k_hands[i] = hand
        print(f"Mano {i}: {', '.join(f'{card.suit}{card.value}' for card in hand)}")
    return k_hands

def verify_lost():
    global k_hands, move_count
    if move_count == 52:
        return False
    if all(card.back for card in k_hands[13] if card.value == 'K'):
        return True
    return False

def verify_win():
    global k_hands, move_count
    if move_count == 52:
        return True

def get_hand_index(self, value):
    hand_indices = {
        'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,
        '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
        'J': 11, 'Q': 12, 'K': 13
    }
    return hand_indices.get(value, 1)

def play_game():
    global k_hands, move_count, resultado, running
    if verify_lost():
        running = False
        resultado = "Perdiste"
    if verify_win():
        running = False
        resultado = "Ganaste"

    card_in_game = k_hands[13][0]
    card_in_game.flip()
    hand = get_hand_index(card_in_game.value)
    k_hands[hand].append(card_in_game)
    k_hands[13].remove(card_in_game)
    move_count += 1
    return hand

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