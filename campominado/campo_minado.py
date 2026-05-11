import tkinter as tk
from tkinter import messagebox
import random

# CONFIGURAÇÕES
LINHAS = 8
COLUNAS = 8
MINAS = 10
TAMANHO_BOTAO = 4

class CampoMinado:

    def __init__(self, root):

        self.root = root
        self.root.title("Campo Minado")

        self.frame_jogo = tk.Frame(self.root)
        self.frame_jogo.pack(pady=10)

        # BOTÃO RECOMEÇAR
        self.botao_recomecar = tk.Button(
            self.root,
            text="🔄 Recomeçar",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.reiniciar_jogo
        )

        self.botao_recomecar.pack(pady=10)

        self.iniciar_jogo()

    def iniciar_jogo(self):

        self.tabuleiro = []
        self.botoes = []
        self.bandeiras = set()

        self.criar_tabuleiro()
        self.colocar_minas()
        self.calcular_numeros()
        self.criar_interface()

    def criar_tabuleiro(self):

        self.tabuleiro = [
            [0 for _ in range(COLUNAS)]
            for _ in range(LINHAS)
        ]

    def colocar_minas(self):

        minas = 0

        while minas < MINAS:

            linha = random.randint(0, LINHAS - 1)
            coluna = random.randint(0, COLUNAS - 1)

            if self.tabuleiro[linha][coluna] != -1:

                self.tabuleiro[linha][coluna] = -1
                minas += 1

    def calcular_numeros(self):

        for linha in range(LINHAS):
            for coluna in range(COLUNAS):

                if self.tabuleiro[linha][coluna] == -1:
                    continue

                minas_vizinhas = 0

                for i in range(max(0, linha - 1), min(LINHAS, linha + 2)):
                    for j in range(max(0, coluna - 1), min(COLUNAS, coluna + 2)):

                        if self.tabuleiro[i][j] == -1:
                            minas_vizinhas += 1

                self.tabuleiro[linha][coluna] = minas_vizinhas

    def criar_interface(self):

        for linha in range(LINHAS):

            linha_botoes = []

            for coluna in range(COLUNAS):

                botao = tk.Button(
                    self.frame_jogo,
                    width=TAMANHO_BOTAO,
                    height=2,
                    font=("Arial", 12, "bold")
                )

                # CLIQUE ESQUERDO
                botao.config(
                    command=lambda l=linha, c=coluna: self.clicar(l, c)
                )

                # CLIQUE DIREITO
                botao.bind(
                    "<Button-3>",
                    lambda event, l=linha, c=coluna: self.marcar_bomba(l, c)
                )

                botao.grid(row=linha, column=coluna)

                linha_botoes.append(botao)

            self.botoes.append(linha_botoes)

    def clicar(self, linha, coluna):

        botao = self.botoes[linha][coluna]

        # NÃO ABRE SE TIVER BANDEIRA
        if (linha, coluna) in self.bandeiras:
            return

        if botao["state"] == "disabled":
            return

        valor = self.tabuleiro[linha][coluna]

        # BOMBA
        if valor == -1:

            botao.config(text="💣", bg="red")

            self.mostrar_minas()

            messagebox.showerror(
                "Fim de jogo",
                "Você perdeu!"
            )

            self.desativar_botoes()

        else:

            cores = {
                1: "blue",
                2: "green",
                3: "red",
                4: "purple",
                5: "brown",
                6: "cyan",
                7: "black",
                8: "gray"
            }

            texto = "" if valor == 0 else str(valor)

            botao.config(
                text=texto,
                bg="lightgray",
                disabledforeground=cores.get(valor, "black"),
                state="disabled"
            )

            if valor == 0:
                self.revelar_zeros(linha, coluna)

        self.verificar_vitoria()

    def marcar_bomba(self, linha, coluna):

        botao = self.botoes[linha][coluna]

        # NÃO MARCA BLOCO ABERTO
        if botao["state"] == "disabled":
            return

        # REMOVE BANDEIRA
        if (linha, coluna) in self.bandeiras:

            botao.config(text="")
            self.bandeiras.remove((linha, coluna))

        # ADICIONA BANDEIRA
        else:

            botao.config(
                text="🚩",
                fg="red"
            )

            self.bandeiras.add((linha, coluna))

    def revelar_zeros(self, linha, coluna):

        for i in range(max(0, linha - 1), min(LINHAS, linha + 2)):
            for j in range(max(0, coluna - 1), min(COLUNAS, coluna + 2)):

                botao = self.botoes[i][j]

                if botao["state"] == "disabled":
                    continue

                if (i, j) in self.bandeiras:
                    continue

                valor = self.tabuleiro[i][j]

                texto = "" if valor == 0 else str(valor)

                botao.config(
                    text=texto,
                    bg="lightgray",
                    state="disabled"
                )

                if valor == 0:
                    self.revelar_zeros(i, j)

    def mostrar_minas(self):

        for linha in range(LINHAS):
            for coluna in range(COLUNAS):

                if self.tabuleiro[linha][coluna] == -1:

                    self.botoes[linha][coluna].config(
                        text="💣",
                        bg="red"
                    )

    def desativar_botoes(self):

        for linha in self.botoes:
            for botao in linha:
                botao.config(state="disabled")

    def verificar_vitoria(self):

        total_revelado = 0

        for linha in range(LINHAS):
            for coluna in range(COLUNAS):

                if self.botoes[linha][coluna]["state"] == "disabled":
                    total_revelado += 1

        if total_revelado == (LINHAS * COLUNAS) - MINAS:

            messagebox.showinfo(
                "Vitória",
                "Parabéns! Você venceu!"
            )

            self.desativar_botoes()

    def reiniciar_jogo(self):

        # REMOVE BOTÕES ANTIGOS
        for widget in self.frame_jogo.winfo_children():
            widget.destroy()

        # RECOMEÇA
        self.iniciar_jogo()


# JANELA
root = tk.Tk()

root.resizable(False, False)

jogo = CampoMinado(root)

root.mainloop()