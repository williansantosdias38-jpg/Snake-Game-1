import pygame
import random
import sys

# Inicializacao
pygame.init()

# Configuracoes da tela
LARGURA = 600
ALTURA = 400
TAMANHO_BLOCO = 20

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Snake Neon")

# Cores
FUNDO = (12, 18, 32)
FUNDO_CLARO = (18, 27, 46)
GRADE = (31, 43, 70)
PAINEL = (22, 33, 56)
BRANCO = (245, 248, 255)
TEXTO_SUAVE = (174, 188, 215)
AZUL = (54, 154, 255)
AZUL_CLARO = (116, 198, 255)
VERDE = (51, 222, 136)
VERDE_ESCURO = (25, 140, 86)
VERMELHO = (255, 83, 94)
VERMELHO_CLARO = (255, 154, 122)
CINZA = (98, 111, 136)
CINZA_ESCURO = (48, 58, 78)
SOMBRA = (5, 8, 14)

# Fontes
fonte = pygame.font.SysFont("Arial", 24, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 18)
fonte_titulo = pygame.font.SysFont("Arial", 42, bold=True)

# Relogio
clock = pygame.time.Clock()

# Obstaculo
obstaculo = pygame.Rect(280, 180, 40, 40)


def desenhar_fundo():
    tela.fill(FUNDO)

    for y in range(0, ALTURA, TAMANHO_BLOCO):
        cor = FUNDO_CLARO if (y // TAMANHO_BLOCO) % 2 == 0 else FUNDO
        pygame.draw.rect(tela, cor, (0, y, LARGURA, TAMANHO_BLOCO))

    for x in range(0, LARGURA, TAMANHO_BLOCO):
        pygame.draw.line(tela, GRADE, (x, 0), (x, ALTURA), 1)

    for y in range(0, ALTURA, TAMANHO_BLOCO):
        pygame.draw.line(tela, GRADE, (0, y), (LARGURA, y), 1)


def desenhar_texto_centralizado(texto, fonte_usada, cor, y):
    superficie = fonte_usada.render(texto, True, cor)
    retangulo = superficie.get_rect(center=(LARGURA // 2, y))
    tela.blit(superficie, retangulo)


def mostrar_pontuacao(pontos):
    painel = pygame.Rect(12, 10, 154, 38)
    pygame.draw.rect(tela, SOMBRA, painel.move(3, 4), border_radius=10)
    pygame.draw.rect(tela, PAINEL, painel, border_radius=10)
    pygame.draw.rect(tela, AZUL_CLARO, painel, width=2, border_radius=10)

    texto = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto, (26, 17))


def desenhar_comida(x, y):
    centro = (x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO // 2)
    pygame.draw.circle(tela, VERMELHO, centro, 10)
    pygame.draw.circle(tela, VERMELHO_CLARO, (centro[0] - 3, centro[1] - 4), 4)
    pygame.draw.circle(tela, (120, 255, 160), (centro[0] + 5, centro[1] - 9), 3)


def desenhar_obstaculo():
    pygame.draw.rect(tela, SOMBRA, obstaculo.move(4, 5), border_radius=8)
    pygame.draw.rect(tela, CINZA_ESCURO, obstaculo, border_radius=8)
    pygame.draw.rect(tela, CINZA, obstaculo.inflate(-8, -8), border_radius=5)


def desenhar_cobra(cobra, dx, dy):
    for i, bloco in enumerate(cobra):
        x, y = bloco
        retangulo = pygame.Rect(x + 1, y + 1, TAMANHO_BLOCO - 2, TAMANHO_BLOCO - 2)
        cor = AZUL_CLARO if i == len(cobra) - 1 else AZUL
        pygame.draw.rect(tela, cor, retangulo, border_radius=7)
        pygame.draw.rect(tela, (25, 92, 170), retangulo, width=2, border_radius=7)

    cabeca_x, cabeca_y = cobra[-1]
    olho1 = (cabeca_x + 6, cabeca_y + 7)
    olho2 = (cabeca_x + 14, cabeca_y + 7)

    if dx < 0:
        olho1 = (cabeca_x + 6, cabeca_y + 6)
        olho2 = (cabeca_x + 6, cabeca_y + 14)
    elif dx > 0:
        olho1 = (cabeca_x + 14, cabeca_y + 6)
        olho2 = (cabeca_x + 14, cabeca_y + 14)
    elif dy < 0:
        olho1 = (cabeca_x + 6, cabeca_y + 6)
        olho2 = (cabeca_x + 14, cabeca_y + 6)
    elif dy > 0:
        olho1 = (cabeca_x + 6, cabeca_y + 14)
        olho2 = (cabeca_x + 14, cabeca_y + 14)

    pygame.draw.circle(tela, BRANCO, olho1, 3)
    pygame.draw.circle(tela, BRANCO, olho2, 3)
    pygame.draw.circle(tela, FUNDO, olho1, 1)
    pygame.draw.circle(tela, FUNDO, olho2, 1)


def nova_comida():
    comida_x = round(random.randrange(0, LARGURA - TAMANHO_BLOCO) / 20) * 20
    comida_y = round(random.randrange(0, ALTURA - TAMANHO_BLOCO) / 20) * 20

    while pygame.Rect(comida_x, comida_y, TAMANHO_BLOCO, TAMANHO_BLOCO).colliderect(obstaculo):
        comida_x = round(random.randrange(0, LARGURA - TAMANHO_BLOCO) / 20) * 20
        comida_y = round(random.randrange(0, ALTURA - TAMANHO_BLOCO) / 20) * 20

    return comida_x, comida_y


def game_over(pontos):
    desenhar_fundo()

    caixa = pygame.Rect(105, 95, 390, 210)
    pygame.draw.rect(tela, SOMBRA, caixa.move(6, 8), border_radius=18)
    pygame.draw.rect(tela, PAINEL, caixa, border_radius=18)
    pygame.draw.rect(tela, VERMELHO, caixa, width=3, border_radius=18)

    desenhar_texto_centralizado("GAME OVER", fonte_titulo, VERMELHO, 145)
    desenhar_texto_centralizado(f"Pontuacao final: {pontos}", fonte, BRANCO, 198)
    desenhar_texto_centralizado("ENTER para jogar de novo", fonte_pequena, TEXTO_SUAVE, 244)
    desenhar_texto_centralizado("ESC para sair", fonte_pequena, TEXTO_SUAVE, 270)

    pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_RETURN:
                    jogo()


def jogo():
    x = 100
    y = 100

    dx = TAMANHO_BLOCO
    dy = 0

    cobra = []
    tamanho_cobra = 1

    comida_x, comida_y = nova_comida()
    pontos = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and dx == 0:
                    dx = -TAMANHO_BLOCO
                    dy = 0

                elif evento.key == pygame.K_RIGHT and dx == 0:
                    dx = TAMANHO_BLOCO
                    dy = 0

                elif evento.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -TAMANHO_BLOCO

                elif evento.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = TAMANHO_BLOCO

        x += dx
        y += dy

        # Colisao com bordas
        if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:
            game_over(pontos)

        desenhar_fundo()
        desenhar_comida(comida_x, comida_y)
        desenhar_obstaculo()

        # Corpo da cobra
        cabeca = [x, y]
        cobra.append(cabeca)

        if len(cobra) > tamanho_cobra:
            del cobra[0]

        # Colisao consigo mesma
        for bloco in cobra[:-1]:
            if bloco == cabeca:
                game_over(pontos)

        desenhar_cobra(cobra, dx, dy)

        # Colisao com obstaculo
        cabeca_rect = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)

        if cabeca_rect.colliderect(obstaculo):
            game_over(pontos)

        # Comeu comida
        if x == comida_x and y == comida_y:
            comida_x, comida_y = nova_comida()
            tamanho_cobra += 1
            pontos += 10

        mostrar_pontuacao(pontos)

        pygame.display.update()
        clock.tick(10)


jogo()
