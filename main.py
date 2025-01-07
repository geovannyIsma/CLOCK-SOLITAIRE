import pygame
import random
import os
import math
import time

# Configuración inicial
pygame.init()


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.key = f"{value}_{suit}"
        self.back = True
        self.pos = (0, 0)  # Posición actual
        self.target_pos = (0, 0)  # Posición objetivo para animación
        self.moving = False
        self.angle = 0

    def flip(self):
        self.back = False

    def set_position(self, pos):
        self.pos = pos
        self.target_pos = pos

    def move_to(self, target):
        self.target_pos = target
        self.moving = True

    def update_position(self, speed=0.1):
        if self.moving:
            dx = self.target_pos[0] - self.pos[0]
            dy = self.target_pos[1] - self.pos[1]
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 1:
                self.pos = self.target_pos
                self.moving = False
                return True

            self.pos = (
                self.pos[0] + dx * speed,
                self.pos[1] + dy * speed
            )
        return False


class ClockSolitaire:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.CARD_WIDTH = 120
        self.CARD_HEIGHT = 180
        self.RADIUS = 320

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Clock Solitaire")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Calcular posiciones del reloj
        self.CLOCK_POSITIONS = [
            (
                width // 2 + self.RADIUS * math.cos(i * (2 * math.pi / 12) - math.pi / 2),
                height // 2 + self.RADIUS * math.sin(i * (2 * math.pi / 12) - math.pi / 2)
            )
            for i in range(12)
        ]
        self.CENTER_POSITION = (width // 2, height // 2)

        self.deck = []
        self.k_hands = {}
        self.move_count = 0
        self.current_hand = 13
        self.game_state = "playing"  # "playing", "won", "lost"
        self.waiting_for_click = True
        self.animation_in_progress = False

        self.card_images = {}
        self.card_back = None
        self.background = None

        self.load_assets()
        self.initialize_game()

    def load_assets(self):
        # Cargar imágenes
        sprites_dir = "Sprites"
        for file_name in os.listdir(sprites_dir):
            if file_name.endswith(".png"):
                name = file_name[:-4]
                image = pygame.image.load(os.path.join(sprites_dir, file_name))
                self.card_images[name] = pygame.transform.scale(
                    image, (self.CARD_WIDTH, self.CARD_HEIGHT)
                )

        self.card_back = self.card_images.get("atras")
        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join("Sprites", "fondo.jpg")),
            (self.WIDTH, self.HEIGHT)
        )

    def initialize_game(self):
        # Inicializar mazo
        suits = ['brillo', 'trebol', 'corazon_negro', 'corazon_rojo']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

        self.deck = [Card(v, s) for s in suits for v in values]
        self.shuffle()
        self.deal_cards()

    def shuffle(self):
        for _ in range(9):
            mitad = len(self.deck) // 2
            temp_deck = []
            left = self.deck[:mitad]
            right = self.deck[mitad:]

            while left or right:
                for _ in range(random.randint(1, 5)):
                    if left:
                        temp_deck.append(left.pop(0))
                for _ in range(random.randint(1, 5)):
                    if right:
                        temp_deck.append(right.pop(0))

            self.deck = temp_deck

    def deal_cards(self):
        self.k_hands.clear()
        for i in range(1, 14):
            hand = []
            pos = self.CENTER_POSITION if i == 13 else self.CLOCK_POSITIONS[i - 1]
            angle = 0 if i == 13 else ((i - 1) * -30)

            for _ in range(4):
                if self.deck:
                    card = self.deck.pop(0)
                    card.set_position(pos)
                    card.angle = angle
                    hand.append(card)
            self.k_hands[i] = hand

    def get_hand_index(self, value):
        hand_indices = {
            'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
            'J': 11, 'Q': 12, 'K': 13
        }
        return hand_indices.get(value, 1)

    def verify_win(self):
        return self.move_count >= 52

    def verify_lost(self):
        if not self.k_hands.get(13):
            return False
        return all(card.back for card in self.k_hands[13] if card.value == 'K')

    def make_move(self):
        if self.game_state != "playing" or not self.k_hands[self.current_hand]:
            return False

        card = self.k_hands[self.current_hand][0]
        card.flip()
        next_hand = self.get_hand_index(card.value)

        # Establecer posición objetivo para la animación
        target_pos = self.CENTER_POSITION if next_hand == 13 else self.CLOCK_POSITIONS[next_hand - 1]
        target_angle = 0 if next_hand == 13 else ((next_hand - 1) * -30)

        card.move_to(target_pos)
        card.angle = target_angle

        # Mover la carta a la nueva mano
        self.k_hands[next_hand].append(card)
        self.k_hands[self.current_hand].pop(0)

        self.move_count += 1
        self.current_hand = next_hand
        self.animation_in_progress = True

        # Verificar condiciones de victoria/derrota
        if self.verify_win():
            self.game_state = "won"
        elif self.verify_lost():
            self.game_state = "lost"

        return True

    def draw_card(self, card, pos, angle=0):
        image = self.card_images[card.key] if not card.back else self.card_back
        rotated = pygame.transform.rotate(image, angle)
        rect = rotated.get_rect(center=pos)
        self.screen.blit(rotated, rect)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Dibujar todas las cartas en cada mano
        for hand_index, hand in self.k_hands.items():
            for card in hand:
                self.draw_card(card, card.pos, card.angle)

        # Dibujar estado del juego
        font = pygame.font.Font(None, 74)
        if self.game_state == "won":
            text = font.render("¡Ganaste!", True, self.WHITE)
        elif self.game_state == "lost":
            text = font.render("¡Perdiste!", True, self.WHITE)
        else:
            text = font.render(f"Movimientos: {self.move_count}", True, self.WHITE)

        self.screen.blit(text, (20, 20))

    def update(self):
        if self.animation_in_progress:
            self.animation_in_progress = any(
                card.update_position() for hand in self.k_hands.values() for card in hand
            )

    def handle_click(self, pos):
        if not self.animation_in_progress and self.waiting_for_click:
            self.waiting_for_click = False
            return self.make_move()
        return False


def main():
    game = ClockSolitaire(1920, 1080)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.handle_click(event.pos)

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()