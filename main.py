from random import randint
import pygame
import sys
from pygame.locals import *

ancho = 900
alto = 480
lista_enemigo = []


class NaveEspacial(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_nave = pygame.image.load('img/nave.png')
        self.imagen_explosion = pygame.image.load('img/explosion.png')
        self.rect = self.imagen_nave.get_rect()
        self.rect.centerx = ancho / 2
        self.rect.centery = alto - 30
        self.velocidad = 10

        self.lista_disparo = []
        self.vida = True

        self.sonido_disparo = pygame.mixer.Sound('music/disparo.mp3')
        self.sonido_explosion = pygame.mixer.Sound('music/explosion.mp3')

    def movimiento_derecha(self):
        self.rect.right += self.velocidad
        self.__movimiento()

    def movimiento_izquierda(self):
        self.rect.left -= self.velocidad
        self.__movimiento()

    def __movimiento(self):
        if self.vida:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right > 870:
                self.rect.right = 840

    def disparar(self, x, y):
        proyectil = Proyectil(x, y, 'img/bala.png', True)
        self.lista_disparo.append(proyectil)
        self.sonido_disparo.play()

    def dibujar(self, superficie):
        superficie.blit(self.imagen_nave, self.rect)

    def destruccion(self):
        self.sonido_explosion.play()
        self.vida = False
        self.velocidad = 0
        self.imagen_nave = self.imagen_explosion


class Invasor(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, distancia):
        pygame.sprite.Sprite.__init__(self)
        self.invasor_a = pygame.image.load('img/invasor_a.png')
        self.invasor_b = pygame.image.load('img/invasor_b.png')
        self.invasor_c = pygame.image.load('img/invasor_c.png')
        self.invasor_d = pygame.image.load('img/invasor_d.png')

        self.lista_invasores = [self.invasor_a, self.invasor_b, self.invasor_c, self.invasor_d]
        self.pos_imagen = 0

        self.imagen_invasor = self.lista_invasores[self.pos_imagen]
        self.rect = self.imagen_invasor.get_rect()

        self.lista_disparo = []
        self.velocidad_disparo = 5
        self.rect.top = pos_y
        self.rect.left = pos_x
        self.rango_disparo = 10
        self.tiempo_cambio = 1
        self.conquista = False
        self.contador = 0
        self.derecha = True
        self.max_descenso = self.rect.top + 40
        self.limite_derecha = pos_x + distancia
        self.limite_izquierda = pos_x - distancia

    def dibujar(self, superficie):
        self.imagen_invasor = self.lista_invasores[self.pos_imagen]
        superficie.blit(self.imagen_invasor, self.rect)

    def comportamiento(self, tiempo):
        if not self.conquista:
            self.__movimientos()
            self.__ataque()
            if self.tiempo_cambio == tiempo:
                self.pos_imagen += 1
                self.tiempo_cambio += 1

                if self.pos_imagen > len(self.lista_invasores) - 1:
                    self.pos_imagen = 0

    def __movimientos(self):
        if self.contador < 1:
            self.__movimiento_lateral()
        else:
            self.__descenso()

    def __movimiento_lateral(self):
        if self.derecha:
            self.rect.left = self.rect.left + self.velocidad_disparo
            if self.rect.left > self.limite_derecha:
                self.derecha = False
                self.contador += 1
        else:
            self.rect.left = self.rect.left - self.velocidad_disparo
            if self.rect.left < self.limite_izquierda:
                self.derecha = True

    def __descenso(self):

        if self.max_descenso == self.rect.top:
            self.contador = 0
            self.max_descenso = self.rect.top + 40
        else:
            self.rect.top += 1

    def __ataque(self):
        if randint(0, 100) == self.rango_disparo:
            self.__disparar()

    def __disparar(self):
        x, y = self.rect.center
        proyectil = Proyectil(x, y, 'img/bomba.png', False)
        self.lista_disparo.append(proyectil)


class Proyectil(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, ruta, personaje):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_proyectil = pygame.image.load(ruta)
        self.rect = self.imagen_proyectil.get_rect()
        self.velocidad_disparo = 5
        self.rect.top = pos_y
        self.rect.left = pos_x
        self.disparo_personaje = personaje

    def trayectoria(self):
        if self.disparo_personaje:
            self.rect.top = self.rect.top - self.velocidad_disparo
        else:
            self.rect.top = self.rect.top + self.velocidad_disparo

    def dibujar(self, superficie):
        superficie.blit(self.imagen_proyectil, self.rect)


def cargar_enemigos():
    posx = 100
    for x in range(1, 5):
        enemigo = Invasor(posx, 100, 40)
        lista_enemigo.append(enemigo)
        posx = posx + 200

    posx = 100
    for x in range(1, 5):
        enemigo = Invasor(posx, 0, 40)
        lista_enemigo.append(enemigo)
        posx = posx + 200

    posx = 100
    for x in range(1, 5):
        enemigo = Invasor(posx, -100, 40)
        lista_enemigo.append(enemigo)
        posx = posx + 200


def detener_todo():
    for enemigo in lista_enemigo:
        for disparo in enemigo.lista_disparo:
            enemigo.lista_disparo.remove(disparo)
        enemigo.conquista = True


def space_invader():
    pygame.init()
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Space Invader")
    imagen_fondo = pygame.image.load('img/fondo.png')
    pygame.mixer.music.load('music/fondo.mp3')
    pygame.mixer.music.play(100)
    fuente = pygame.font.SysFont('Arial', 30)
    texto = fuente.render("Fin del Juego", False, (120, 100, 40))
    jugador = NaveEspacial()
    cargar_enemigos()
    en_juego = True

    reloj = pygame.time.Clock()

    while True:
        reloj.tick(60)
        tiempo = int(pygame.time.get_ticks() / 1000)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if en_juego:
                if evento.type == KEYDOWN:
                    if evento.key == K_LEFT:
                        jugador.movimiento_izquierda()
                    elif evento.key == K_RIGHT:
                        jugador.movimiento_derecha()
                    elif evento.key == K_SPACE:
                        x, y = jugador.rect.center
                        jugador.disparar(x, y)

        ventana.blit(imagen_fondo, (0, 0))
        jugador.dibujar(ventana)

        if len(jugador.lista_disparo) > 0:
            for x in jugador.lista_disparo:
                x.dibujar(ventana)
                x.trayectoria()
                if x.rect.top < -10:
                    jugador.lista_disparo.remove(x)
                else:
                    for enemigo in lista_enemigo:
                        if x.rect.colliderect(enemigo.rect):
                            lista_enemigo.remove(enemigo)
                            jugador.lista_disparo.remove(x)
        if len(lista_enemigo) > 0:
            for enemigo in lista_enemigo:
                enemigo.comportamiento(tiempo)
                enemigo.dibujar(ventana)

                if enemigo.rect.colliderect(jugador.rect):
                    jugador.destruccion()
                    en_juego = False
                    detener_todo()

                if len(enemigo.lista_disparo) > 0:
                    for x in enemigo.lista_disparo:
                        x.dibujar(ventana)
                        x.trayectoria()
                        if x.rect.colliderect(jugador.rect):
                            jugador.destruccion()
                            en_juego = False
                            detener_todo()
                        if x.rect.top > 900:
                            enemigo.lista_disparo.remove(x)
                        else:
                            for disparo in jugador.lista_disparo:
                                if x.rect.colliderect(disparo.rect):
                                    jugador.lista_disparo.remove(disparo)
                                    enemigo.lista_disparo.remove(x)

        if not en_juego:
            pygame.mixer.music.fadeout(3000)
            ventana.blit(texto, (300, 300))
        pygame.display.update()


if __name__ == '__main__':
    space_invader()



