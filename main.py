#Bem vindo ao código do jogo da cobrinha de @gdelacerda23. Sinta-se livre para entrar em contato comigo se
#quiser conversar sobre o projeto!

#Welcome to the snake game code by @gdelacerda23. Please feel free to contact me if you
#want to talk about the project!

#Módulos necessários
from tkinter import *
import random

#CONSTANTES - você pode brincar com estes valores se quiser!

LARGURA_JOGO = 1100   #largura da janela do jogo
ALTURA_JOGO = 800   #altura da janela do jogo
VELOCIDADE_COBRA = 90    #ATENÇÃO: quanto mais baixo este número, mais rápido é o jogo! Esta é a constante da velocidade da cobra
TAMANHO_ESPACOS = 50    #tamanho de itens como a comida e o tamanho das partes da cobra
PARTES_CORPO = 2         #quantas partes tem o corpo da cobra ao iniciar o jogo
COR_COBRA = "#000080"    #cor da cobra em hexadecimal, nesse caso, deixei com a cor 'Navy Blue'
COR_COMIDA = "#32CD32"   #cor da comida em hexadecimal, nesse caso, deixei com a cor 'Lime Green'
COR_DO_FUNDO = "#1C1C1C" #cor do fundo do jogo, nesse caso, deixei com a cor 'Grey11'



class Cobra:
    def __init__(self):
        self.tamanho_corpo = PARTES_CORPO
        self.coordenadas = []
        self.quadrados = []

        for i in range(0, PARTES_CORPO):
            self.coordenadas.append([0, 0])    #onde a nossa cobrinha aparece na tela

        for x, y in self.coordenadas:
            quadrado = canvas.create_rectangle(x, y, x + TAMANHO_ESPACOS, y + TAMANHO_ESPACOS, fill=COR_COBRA, tag="cobrinha")    #construção da cobrinha
            self.quadrados.append(quadrado)




class Comida:
    def __init__(self):          #a seguir, fazemos uma randomização de onde a comida irá surgir, com o método randint
        x = random.randint(0, (LARGURA_JOGO / TAMANHO_ESPACOS) - 1) * TAMANHO_ESPACOS
        y = random.randint(0, (ALTURA_JOGO / TAMANHO_ESPACOS) - 1) * TAMANHO_ESPACOS

        self.coordenadas = [x, y]

        canvas.create_oval(x, y, x + TAMANHO_ESPACOS, y + TAMANHO_ESPACOS, fill=COR_COMIDA, tag="comida")




def proximo_turno(cobra, comida):
    x, y = cobra.coordenadas[0]

    if direcao == "cima":
        y -= TAMANHO_ESPACOS
    elif direcao == "direita":
        x += TAMANHO_ESPACOS
    elif direcao == "baixo":
        y += TAMANHO_ESPACOS
    elif direcao == "esquerda":
        x -= TAMANHO_ESPACOS

    cobra.coordenadas.insert(0, (x, y))

    quadrado = canvas.create_rectangle(x, y, x + TAMANHO_ESPACOS, y + TAMANHO_ESPACOS, fill=COR_COBRA)    #fazendo a cobrinha aparecer na tela
    cobra.quadrados.insert(0, quadrado)


    #este condicional checa se não está havendo uma sobreposição da cobrinha com a comida
    if x == comida.coordenadas[0] and y == comida.coordenadas[1]:
        global pontuacao #deixando a variável pontuação global

        pontuacao += 1   #adicionamos 1 à pontuação, pois a cobrinha encontrou a comida

        label.config(text="Sua Pontuação: {}".format(pontuacao))

        canvas.delete("comida")

        comida = Comida()

    else:
          #importante: este código executa apenas enquanto a cobrinha ainda não encontrou a comida
        del cobra.coordenadas[-1]

        canvas.delete(cobra.quadrados[-1])

        del cobra.quadrados[-1]

    if checar_colisoes(cobra):
        fim_de_jogo()

    window.after(VELOCIDADE_COBRA, proximo_turno, cobra, comida)


def mudar_direcao(nova_direcao):
    global direcao    #variável global de direção para conseguirmos acessá-la


#aqui, estamos conferindo se o jogador não está tentando fazer a cobrinha se mover para a direção contrária à qual ela já está se movendo
    if nova_direcao == 'esquerda':
        if direcao != 'direita':
            direcao = nova_direcao

    elif nova_direcao == 'direita':
        if direcao != 'esquerda':
            direcao = nova_direcao

    elif nova_direcao == 'cima':
        if direcao != 'baixo':
            direcao = nova_direcao

    elif nova_direcao == 'baixo':
        if direcao != 'cima':
            direcao = nova_direcao




def checar_colisoes(cobra):
    x, y = cobra.coordenadas[0]

    if x < 0 or x >= LARGURA_JOGO:       #checa se a cobrinha saiu da tela
        return True
    elif y < 0 or y >= ALTURA_JOGO:
        return True

    for parte_do_corpo in cobra.coordenadas[1:]:
        if x == parte_do_corpo[0] and y == parte_do_corpo[1]:
            return True

    return False


def fim_de_jogo():     #função que nos fornece nossa tela de fim de jogo
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height()/2, font=('New Times Roman', 60), text="Fim de Jogo!", tag="fim de jogo", fill="#B22222")   #cor escolhida: FireBrick


window = Tk()
window.title("Jogo da Cobrinha")   #título do jogo
window.resizable(False, False)   #com isso, não é possível redimensionar a janela

pontuacao = 0  #inicializando a variável da pontuação
direcao = "direita"    #direção inicial da cobrinha

label = Label(window, text="Sua Pontuação: {}".format(pontuacao), font=('Arial', 30))     #A mensagem que aparece no jogo
label.pack()

canvas = Canvas(window, bg=COR_DO_FUNDO, height=ALTURA_JOGO, width=LARGURA_JOGO)
canvas.pack()

window.update()

largura_janela = window.winfo_width()
altura_janela = window.winfo_height()
largura_tela = window.winfo_screenwidth()
altura_tela = window.winfo_screenheight()

x = int((largura_tela / 2) - (largura_janela / 2))
y = int((altura_tela / 2) - (altura_janela / 2))

window.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

window.bind('<Left>', lambda event: mudar_direcao('esquerda'))
window.bind('<Right>', lambda event: mudar_direcao('direita'))
window.bind('<Up>', lambda event: mudar_direcao('cima'))
window.bind('<Down>', lambda event: mudar_direcao('baixo'))


cobra = Cobra()
comida = Comida()

proximo_turno(cobra, comida)

window.mainloop()