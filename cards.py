# cards.py
import pygame

ANCHO_CARTA, ALTO_CARTA = 100, 150

imagenes_cartas = {}

class Mazo:
    def __init__(self, simbolo, color):
        self.simbolo = simbolo
        self.color = color
        self.oculta = True
        self.carta = self.cargar_carta("atras")

    def cargar_carta(self, nombre):
        carta = pygame.image.load(f"Sprites/{nombre}.png")
        return pygame.transform.scale(carta, (ANCHO_CARTA, ALTO_CARTA))

    def mostrar(self):
        self.oculta = False
        self.carta = self.cargar_carta(f"{self.simbolo.lower()}_{self.color.lower()}")

    def ocultar(self):
        self.oculta = True
        self.carta = self.cargar_carta("atras")

def crear_mazo():
    simbolos = [str(i) for i in range(2, 11)] + ["A", "J", "Q", "K"]
    colores = ["brillo", "trebol", "corazon_negro", "corazon_rojo"]
    return [Mazo(simbolo, color) for simbolo in simbolos for color in colores]

talia = crear_mazo()