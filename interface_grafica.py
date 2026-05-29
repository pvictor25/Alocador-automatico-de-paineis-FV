"""Módulo responsável pela renderização gráfica dos arranjos solares."""

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def gerar_patche_telhado(w_tel, l_tel):
    """Cria o retângulo que representa o perímetro do telhado."""
    return patches.Rectangle(
        (0, 0),
        w_tel,
        l_tel,
        fill=False,
        color="red",
        linewidth=2,
        label="Borda do Telhado"
    )


def gerar_patche_painel(x_min, y_min, x_max, y_max):
    """Cria o retângulo que representa um painel fotovoltaico."""
    largura = x_max - x_min
    altura = y_max - y_min
    return patches.Rectangle(
        (x_min, y_min),
        largura,
        altura,
        facecolor="blue",
        alpha=0.6,
        edgecolor="black"
    )


def desenhar_eixo(ax, df_paineis, w_tel, l_tel, titulo):
    """Preenche e configura um eixo específico com o arranjo de painéis."""
    # Desenha o telhado
    ax.add_patch(gerar_patche_telhado(w_tel, l_tel))

    # Desenha os painéis
    for _, row in df_paineis.iterrows():
        ax.add_patch(
            gerar_patche_painel(
                x_min=row["x_inf_esq"],
                y_min=row["y_inf_esq"],
                x_max=row["x_inf_dir"],
                y_max=row["y_sup_esq"]
            )
        )

    # Configurações de layout do subgráfico
    ax.set_xlim(-1, w_tel + 1)
    ax.set_ylim(-1, l_tel + 1)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(f"{titulo}: {len(df_paineis)} Painéis")
    ax.set_xlabel("Largura (m)")
    ax.set_ylabel("Comprimento (m)")
    ax.grid(True, linestyle="--", alpha=0.5)


def plotar_janela_independente(df_retrato, df_paisagem, w_tel, l_tel):
    """Abre uma janela padrão do Matplotlib com os dois arranjos lado a lado."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Renderiza cada lado
    desenhar_eixo(ax1, df_retrato, w_tel, l_tel, "Orientação Retrato")
    desenhar_eixo(ax2, df_paisagem, w_tel, l_tel, "Orientação Paisagem")

    # Texto informativo centralizado na base da janela
    texto_base = (
        f"Comparativo Técnico | Retrato: {len(df_retrato)} painéis "
        f"vs. Paisagem: {len(df_paisagem)} painéis"
    )
    fig.text(
        0.5, 0.02,
        texto_base,
        ha="center",
        fontsize=12,
        fontweight="bold"
    )

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.show()


class CanvasJanela(FigureCanvas):
    """Componente de plotagem para ser embutido dentro do PySide6."""

    def __init__(self, largura=10, altura=5, dpi=100):
        self.fig = Figure(figsize=(largura, altura), dpi=dpi)
        # Cria os dois subplots lado a lado (1 linha, 2 colunas)
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        self.texto_qtd = None
        super().__init__(self.fig)

    def atualizar_grafico(self, df_retrato, df_paisagem, w_tel, l_tel):
        """Limpa o canvas e renderiza as duas orientações simultaneamente."""
        self.ax1.clear()
        self.ax2.clear()

        if self.texto_qtd:
            self.texto_qtd.remove()

        # Desenha os arranjos nos eixos correspondentes
        desenhar_eixo(self.ax1, df_retrato, w_tel, l_tel, "Orientação Retrato")
        desenhar_eixo(self.ax2, df_paisagem, w_tel, l_tel, "Orientação Paisagem")

        # Atualiza o texto global inferior
        texto_base = (
            f"Comparativo Técnico | Retrato: {len(df_retrato)} painéis "
            f"vs. Paisagem: {len(df_paisagem)} painéis"
        )
        self.texto_qtd = self.fig.text(
            0.5, 0.02,
            texto_base,
            ha="center",
            fontsize=11,
            fontweight="bold"
        )

        self.fig.tight_layout()
        self.fig.subplots_adjust(bottom=0.15)
        self.draw()