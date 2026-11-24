# Programa em Python para criar o Jogo da Cobrinha (Snake Game)

from tkinter import *
import random
import os

# Inicializando dimensões e configurações do jogo
LARGURA = 500
ALTURA = 500
VELOCIDADE = 180
TAMANHO_ESPACO = 20
TAMANHO_CORPO = 2
COR_COBRA = "#20E36B"
COR_COBRA_CLARA = "#72FFAD"
COR_COBRA_ESCURA = "#087B39"
COR_CABECA = "#00F58A"
COR_COMIDA = "#FF4057"
COR_FUNDO = "#07130D"


def desenhar_grade():
    """Desenha uma grade suave para identificar claramente cada quadrado."""
    for y in range(0, ALTURA, TAMANHO_ESPACO):
        for x in range(0, LARGURA, TAMANHO_ESPACO):
            cor = "#0B2114" if ((x // TAMANHO_ESPACO + y // TAMANHO_ESPACO) % 2 == 0) else "#0D2818"
            tela.create_rectangle(x, y, x + TAMANHO_ESPACO, y + TAMANHO_ESPACO,
                                  fill=cor, outline="#183C24", width=1,
                                  tag="grade")


def desenhar_segmento(cobra, x, y, indice, ultima_posicao=None):
    """Cria um quadrado 3D. O primeiro segmento é a cabeça e recebe olhos."""
    margem = 2

    # Sombra deslocada dá profundidade aos segmentos.
    tela.create_rectangle(x + 3, y + 4,
                          x + TAMANHO_ESPACO + 1,
                          y + TAMANHO_ESPACO + 2,
                          fill="#031008", outline="", tag="cobra")

    cor = COR_CABECA if indice == 0 else COR_COBRA
    tela.create_rectangle(x + margem, y + margem,
                          x + TAMANHO_ESPACO - margem,
                          y + TAMANHO_ESPACO - margem,
                          fill=cor, outline="#C1FFD8", width=1,
                          tag="cobra")

    # Faces superior/esquerda claras e inferior/direita escuras.
    tela.create_polygon(x + margem, y + margem,
                        x + TAMANHO_ESPACO - margem, y + margem,
                        x + TAMANHO_ESPACO - margem - 3, y + margem + 3,
                        x + margem + 3, y + margem + 3,
                        fill=COR_COBRA_CLARA, outline="", tag="cobra")
    tela.create_polygon(x + TAMANHO_ESPACO - margem, y + margem,
                        x + TAMANHO_ESPACO - margem, y + TAMANHO_ESPACO - margem,
                        x + TAMANHO_ESPACO - margem - 3, y + TAMANHO_ESPACO - margem - 3,
                        x + TAMANHO_ESPACO - margem - 3, y + margem + 3,
                        fill=COR_COBRA_ESCURA, outline="", tag="cobra")

    if indice == 0:
        if direcao == "direita":
            olhos = [(x + 13, y + 6), (x + 13, y + 13)]
        elif direcao == "esquerda":
            olhos = [(x + 5, y + 6), (x + 5, y + 13)]
        elif direcao == "cima":
            olhos = [(x + 6, y + 5), (x + 13, y + 5)]
        else:
            olhos = [(x + 6, y + 13), (x + 13, y + 13)]

        for olho_x, olho_y in olhos:
            tela.create_oval(olho_x - 2, olho_y - 2,
                             olho_x + 2, olho_y + 2,
                             fill="#FFFFFF", outline="#082414", tag="cobra")
            tela.create_oval(olho_x - 0.8, olho_y - 0.8,
                             olho_x + 0.8, olho_y + 0.8,
                             fill="#000000", outline="", tag="cobra")


class Cobra:

    def __init__(self):
        self.tamanho_corpo = TAMANHO_CORPO
        self.coordenadas = [[0, 0] for _ in range(TAMANHO_CORPO)]
        self.quadrados = []

        desenhar_cobra(self, self.coordenadas)


class Comida:

    def __init__(self, cobra):
        espacos_ocupados = {tuple(parte) for parte in cobra.coordenadas}
        espacos_livres = []

        for y in range(0, ALTURA, TAMANHO_ESPACO):
            for x in range(0, LARGURA, TAMANHO_ESPACO):
                if (x, y) not in espacos_ocupados:
                    espacos_livres.append([x, y])

        if not espacos_livres:
            self.coordenadas = [-TAMANHO_ESPACO, -TAMANHO_ESPACO]
            return

        self.coordenadas = random.choice(espacos_livres)

        # Comida esférica em 3D.
        tela.create_oval(self.coordenadas[0] + 4, self.coordenadas[1] + 5,
                         self.coordenadas[0] + 18, self.coordenadas[1] + 19,
                         fill="#A70F29", outline="", tag="comida")
        tela.create_oval(self.coordenadas[0] + 2, self.coordenadas[1] + 2,
                         self.coordenadas[0] + 16, self.coordenadas[1] + 16,
                         fill=COR_COMIDA, outline="#FF9BA8", width=1,
                         tag="comida")
        tela.create_oval(self.coordenadas[0] + 5, self.coordenadas[1] + 5,
                         self.coordenadas[0] + 9, self.coordenadas[1] + 9,
                         fill="#FFD0D6", outline="", tag="comida")


def desenhar_cobra(cobra, posicoes):
    tela.delete("cobra")
    for indice, (x, y) in enumerate(posicoes):
        desenhar_segmento(cobra, x, y, indice)


def animar_movimento(cobra, antigas, novas, etapa=0, total=6):
    """Atualiza diretamente os segmentos, sem acumular callbacks."""
    desenhar_cobra(cobra, novas)


def proximo_turno(cobra, comida):
    global turno_agendado

    turno_agendado = None

    if pausado:
        turno_agendado = janela.after(VELOCIDADE, proximo_turno, cobra, comida)
        return

    x, y = cobra.coordenadas[0]

    if direcao == "cima":
        y -= TAMANHO_ESPACO
    elif direcao == "baixo":
        y += TAMANHO_ESPACO
    elif direcao == "esquerda":
        x -= TAMANHO_ESPACO
    elif direcao == "direita":
        x += TAMANHO_ESPACO

    antigas = [parte[:] for parte in cobra.coordenadas]
    cobra.coordenadas.insert(0, [x, y])

    cresceu = (x == comida.coordenadas[0] and y == comida.coordenadas[1])

    if cresceu:
        global pontuacao, pontuacao_maxima
        pontuacao += 1
        if pontuacao > pontuacao_maxima:
            pontuacao_maxima = pontuacao
            salvar_recorde()
        atualizar_pontuacao()
        tela.delete("comida")
        comida = Comida(cobra)
    else:
        del cobra.coordenadas[-1]

    novas = [parte[:] for parte in cobra.coordenadas]
    animar_movimento(cobra, antigas, novas)

    if verificar_colisoes(cobra):
        janela.after(140, fim_de_jogo)
    else:
        turno_agendado = janela.after(VELOCIDADE, proximo_turno, cobra, comida)


def mudar_direcao(nova_direcao):
    global direcao

    if nova_direcao == "esquerda" and direcao != "direita":
        direcao = nova_direcao
    elif nova_direcao == "direita" and direcao != "esquerda":
        direcao = nova_direcao
    elif nova_direcao == "cima" and direcao != "baixo":
        direcao = nova_direcao
    elif nova_direcao == "baixo" and direcao != "cima":
        direcao = nova_direcao


def atualizar_pontuacao():
    rotulo.config(text="Pontos: {}  |  Pontuação máxima: {}".format(pontuacao, pontuacao_maxima))


def carregar_recorde():
    try:
        with open(CAMINHO_RECORDE, "r", encoding="utf-8") as arquivo:
            return int(arquivo.read().strip())
    except (OSError, ValueError):
        return 0


def salvar_recorde():
    try:
        with open(CAMINHO_RECORDE, "w", encoding="utf-8") as arquivo:
            arquivo.write(str(pontuacao_maxima))
    except OSError:
        pass


def alternar_pausa():
    global pausado
    pausado = not pausado

    if pausado:
        botao_pausa.config(text="▶ Continuar")
        tela.create_text(LARGURA // 2, ALTURA // 2,
                         text="PAUSADO",
                         font=("consolas", 42, "bold"),
                         fill="#FFFFFF",
                         tag="pausa")
    else:
        botao_pausa.config(text="Ⅱ Pausar")
        tela.delete("pausa")


def verificar_colisoes(cobra):
    x, y = cobra.coordenadas[0]

    if x < 0 or x >= LARGURA:
        return True
    if y < 0 or y >= ALTURA:
        return True

    for parte_corpo in cobra.coordenadas[1:]:
        if x == parte_corpo[0] and y == parte_corpo[1]:
            return True

    return False


def fim_de_jogo():
    global pontuacao_maxima
    if pontuacao > pontuacao_maxima:
        pontuacao_maxima = pontuacao
        salvar_recorde()
        atualizar_pontuacao()

    tela.delete(ALL)
    tela.create_rectangle(0, 0, LARGURA, ALTURA, fill=COR_FUNDO, outline="")
    tela.create_text(tela.winfo_width() / 2,
                     tela.winfo_height() / 2,
                     font=("consolas", 45, "bold"),
                     text="FIM DE JOGO",
                     fill="#FF4057",
                     tag="fim_de_jogo")


# Definindo a janela do jogo
janela = Tk()
janela.title("Jogo da Cobrinha 3D")

pontuacao = 0
pontuacao_maxima = 0
pausado = False
turno_agendado = None
CAMINHO_RECORDE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recorde.txt")
pontuacao_maxima = carregar_recorde()
direcao = "baixo"

painel = Frame(janela)
painel.pack(fill=X)

rotulo = Label(painel, text="Pontos: 0  |  Pontuação máxima: 0",
               font=("consolas", 16), anchor="w")
rotulo.pack(side=LEFT, padx=10, pady=5)

botao_pausa = Button(painel, text="Ⅱ Pausar", command=alternar_pausa,
                     font=("consolas", 12), width=12)
botao_pausa.pack(side=RIGHT, padx=10, pady=5)
atualizar_pontuacao()

tela = Canvas(janela, bg=COR_FUNDO,
              height=ALTURA, width=LARGURA,
              highlightthickness=3, highlightbackground="#20E36B")
tela.pack()

janela.update()

desenhar_grade()

largura_janela = janela.winfo_width()
altura_janela = janela.winfo_height()
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

x = int((largura_tela / 2) - (largura_janela / 2))
y = int((altura_tela / 2) - (altura_janela / 2))

janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

janela.bind("<Left>", lambda event: mudar_direcao("esquerda"))
janela.bind("<Right>", lambda event: mudar_direcao("direita"))
janela.bind("<Up>", lambda event: mudar_direcao("cima"))
janela.bind("<Down>", lambda event: mudar_direcao("baixo"))
janela.bind("<p>", lambda event: alternar_pausa())
janela.bind("<P>", lambda event: alternar_pausa())

cobra = Cobra()
comida = Comida(cobra)

proximo_turno(cobra, comida)

janela.mainloop()