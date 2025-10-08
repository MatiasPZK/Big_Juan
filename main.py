import pygame
import random
import sys
import time
import os

pygame.init()

ANCHO, ALTO = 800, 500
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("🎰 Big Juan | EsimBET 🎰")

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)

fuente = pygame.font.Font(None, 50)
fuente_peque = pygame.font.Font(None, 30)

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

imagenes = [
    pygame.image.load(os.path.join(ASSETS_DIR, "frutas", "chilli.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "frutas", "dog.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "frutas", "guitar.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "frutas", "hat.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "frutas", "J_icon.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "frutas", "money.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "frutas", "Q_icon.png")),
]

imagenes = [pygame.transform.scale(img, (100, 100)) for img in imagenes]

bg_path = os.path.join(ASSETS_DIR, "bg.png")
fondo = pygame.image.load(bg_path)
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

try:
    spin_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "sounds", "spin.mp3"))
    win_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "sounds", "win.mp3"))
except:
    spin_sound = None
    win_sound = None

puntos = 10

reloj = pygame.time.Clock()

def mostrar_texto(texto, color, y, tamaño=50):
    fuente_local = pygame.font.Font(None, tamaño)
    texto_render = fuente_local.render(texto, True, color)
    rect = texto_render.get_rect(center=(ANCHO // 2, y))
    ventana.blit(texto_render, rect)

def animar_giro():
    if spin_sound: spin_sound.play()
    for _ in range(20):
        ventana.blit(fondo, (0, 0))
        resultado = [random.choice(imagenes) for _ in range(3)]
        for i, img in enumerate(resultado):
            x = 250 + i * 120
            ventana.blit(img, (x, 200))
        mostrar_texto("🎰 GIRANDO 🎰", AMARILLO, 100)
        pygame.display.flip()
        pygame.time.wait(170)

def main():
    global puntos
    corriendo = True
    jugando = False

    while corriendo:
        ventana.blit(fondo, (0, 0))
        mostrar_texto("BIG JUAN DELUXE", AMARILLO, 60)
        mostrar_texto(f"Plata: {puntos}$", BLANCO, 120, 30)
        mostrar_texto("Presioná ESPACIO para girar", VERDE, 420, 30)
        mostrar_texto("ESC para salir", ROJO, 460, 25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    corriendo = False
                if event.key == pygame.K_SPACE:
                    jugando = True

        if jugando:
            animar_giro()
            resultado = [random.choice(imagenes) for _ in range(3)]
            ventana.blit(fondo, (0, 0))
            for i, img in enumerate(resultado):
                x = 250 + i * 120
                ventana.blit(img, (x, 200))

            if resultado[0] == resultado[1] == resultado[2]:
                puntos += 10
                mostrar_texto("💥 JACKPOT +10 💥", VERDE, 100)
                if win_sound: win_sound.play()
            elif resultado[0] == resultado[1] or resultado[1] == resultado[2] or resultado[0] == resultado[2]:
                puntos += 3
                mostrar_texto("✨ Ganaste +3 ✨", BLANCO, 100)
            else:
                puntos -= 2
                mostrar_texto("😢 Jaja, no sacaste nada -2", ROJO, 100)

            mostrar_texto(f"Puntos: {puntos}", BLANCO, 350, 30)
            pygame.display.flip()
            time.sleep(1.5)
            jugando = False

            if puntos <= 0:
                ventana.blit(fondo, (0, 0))
                mostrar_texto("❌ Le debes al FMI ❌", ROJO, ALTO // 2)
                mostrar_texto("R para reiniciar o ESC para salir", AMARILLO, ALTO // 2 + 50, 30)
                pygame.display.flip()
                esperando = True
                while esperando:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                            if event.key == pygame.K_r:
                                puntos = 10
                                esperando = False

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
