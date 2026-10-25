"""Módulo responsável pela interface gráfica e renderização dos arranjos solares."""

import math
import os
import sys
import tempfile
import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as patches
from matplotlib.path import Path
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import algoritmo_de_alocacao_1 as aloc

_DIRETORIO_ASSETS = os.path.join(tempfile.gettempdir(), "alocador_fv_assets")
os.makedirs(_DIRETORIO_ASSETS, exist_ok=True)

# Definições de conversão e formatação para cada unidade de medida suportada
UNIDADES = {
    "Metros (m)": {
        "sigla": "m",
        "para_m": 1.0,
        "de_m": 1.0,
        "passo_tel": 0.5,
        "passo_mod": 0.01,
    },
    "Centímetros (cm)": {
        "sigla": "cm",
        "para_m": 0.01,
        "de_m": 100.0,
        "passo_tel": 10.0,
        "passo_mod": 1.0,
    },
    "Milímetros (mm)": {
        "sigla": "mm",
        "para_m": 0.001,
        "de_m": 1000.0,
        "passo_tel": 100.0,
        "passo_mod": 10.0,
    },
    "Polegadas (in)": {
        "sigla": "in",
        "para_m": 0.0254,
        "de_m": 1.0 / 0.0254,
        "passo_tel": 12.0,
        "passo_mod": 0.5,
    },
    "Pés (ft)": {
        "sigla": "ft",
        "para_m": 0.3048,
        "de_m": 1.0 / 0.3048,
        "passo_tel": 1.0,
        "passo_mod": 0.1,
    },
}

# Definições dos materiais de telhado disponíveis
MATERIAIS_TELHADO = {
    "Cerâmica / Barro (Colonial)": {
        "descricao": "Telhas cerâmicas tipo colonial/romana com relevo 3D de capas e bicas",
    },
    "Metálico (Trapezoidal / Zinco)": {
        "descricao": "Chapas de aço galvanizado com perfil trapezoidal e reflexo metálico",
    },
    "Fibrocimento (Ondulada)": {
        "descricao": "Telhas onduladas de cimento/ardósia com iluminação cilíndrica",
    },
    "Laje de Concreto": {
        "descricao": "Laje plana de concreto aparente com textura mineral e juntas",
    },
    "Telha Shingle (Asfáltica)": {
        "descricao": "Mantas asfálticas retangulares sobrepostas tipo shingle americano",
    },
    "Telha Sanduíche (Termoacústica)": {
        "descricao": "Chapas isotérmicas termoacústicas claras com nervuras longitudinais",
    },
    "Padrão (Neutro)": {
        "descricao": "Fundo neutro opaco e limpo",
    },
}

# ==============================================================================
# DEFINIÇÃO DAS PALETAS DE CORES (MODO CLARO E MODO ESCURO)
# ==============================================================================
PALETAS = {
    "claro": {
        # Janela e Superfícies
        "bg_janela": "#f8fafc",         # Slate 50: Fundo suave, moderno e limpo
        "bg_card": "#ffffff",           # Branco puro para cartões e caixas
        "borda_card": "#e2e8f0",        # Slate 200: Linhas sutis e elegantes

        # Tipografia
        "cor_titulo": "#1e40af",        # Blue 800: Azul corporativo de alto contraste
        "cor_texto": "#0f172a",         # Slate 900: Texto principal nítido
        "cor_subtexto": "#475569",      # Slate 600: Textos secundários e instruções
        "cor_card_texto": "#0f172a",    # Slate 900 para labels internas

        # Abas Superiores (QTabWidget)
        "bg_tab": "#f1f5f9",            # Slate 100: Barra de abas
        "cor_tab": "#475569",           # Slate 600: Texto de abas inativas
        "cor_tab_selected": "#2563eb",  # Blue 600: Aba selecionada

        # Seletores e Entradas Numéricas (QSpinBox / QComboBox)
        "bg_input": "#ffffff",          # Branco
        "borda_input": "#cbd5e1",       # Slate 300: Borda limpa
        "cor_input_texto": "#0f172a",   # Texto digitado em Slate 900
        "bg_spin_btn": "#f1f5f9",       # Botões de incremento em Slate 100
        "bg_spin_btn_hover": "#e2e8f0", # Hover em Slate 200
        "bg_spin_btn_pressed": "#cbd5e1", # Clique em Slate 300

        # Botões Principais de Ação
        "bg_botao_prim": "#2563eb",     # Blue 600
        "bg_botao_prim_hover": "#1d4ed8", # Blue 700
        "bg_botao_voltar": "#f1f5f9",   # Slate 100
        "cor_botao_voltar": "#334155",  # Slate 700
        "bg_botao_voltar_hover": "#e2e8f0", # Slate 200
        "bg_botao_sair": "#fee2e2",     # Red 100
        "cor_botao_sair": "#dc2626",    # Red 600
        "bg_botao_sair_hover": "#fecaca", # Red 200

        # Botão de Cálculo (Play Verde)
        "bg_botao_calc": "#f0fdf4",     # Emerald 50
        "borda_botao_calc": "#16a34a",  # Emerald 600
        "bg_botao_calc_hover": "#dcfce7", # Emerald 100

        # Botão de Alternância de Tema
        "bg_botao_tema": "#ffffff",
        "borda_botao_tema": "#cbd5e1",
        "bg_botao_tema_hover": "#f1f5f9",
        "cor_icone_tema": "#2563eb",    # Lua azul moderna

        # Gráficos (Matplotlib)
        "bg_plot": "#ffffff",
        "borda_plot": "#e2e8f0",
        "bg_fig": "#ffffff",
        "bg_axes": "#f8fafc",
        "fg_plot": "#0f172a",
        "grid_plot": "#e2e8f0",
        "spine_plot": "#cbd5e1",

        # Elementos Técnicos do Arranjo
        "cor_telhado": "#dc2626",       # Red 600
        "cor_painel_face": "#1d4ed8",   # Blue 700
        "cor_painel_borda": "#93c5fd",  # Blue 300
    },
    "escuro": {
        # Janela e Superfícies
        "bg_janela": "#09090b",         # Zinc 950: Preto profundo refinado
        "bg_card": "#18181b",           # Zinc 900: Cartões escuros
        "borda_card": "#27272a",        # Zinc 800: Divisórias sutis

        # Tipografia
        "cor_titulo": "#60a5fa",        # Blue 400: Azul claro vibrante
        "cor_texto": "#f4f4f5",         # Zinc 100: Texto claro de alto contraste
        "cor_subtexto": "#a1a1aa",      # Zinc 400: Instruções e rótulos
        "cor_card_texto": "#f4f4f5",    # Zinc 100

        # Abas Superiores (QTabWidget)
        "bg_tab": "#121214",            # Zinc 950
        "cor_tab": "#a1a1aa",           # Zinc 400
        "cor_tab_selected": "#60a5fa",  # Blue 400

        # Seletores e Entradas Numéricas (QSpinBox / QComboBox)
        "bg_input": "#09090b",          # Zinc 950
        "borda_input": "#3f3f46",       # Zinc 700
        "cor_input_texto": "#f4f4f5",   # Zinc 100
        "bg_spin_btn": "#27272a",       # Zinc 800
        "bg_spin_btn_hover": "#3f3f46", # Zinc 700
        "bg_spin_btn_pressed": "#52525b", # Zinc 600

        # Botões Principais de Ação
        "bg_botao_prim": "#2563eb",     # Blue 600
        "bg_botao_prim_hover": "#1d4ed8", # Blue 700
        "bg_botao_voltar": "#27272a",   # Zinc 800
        "cor_botao_voltar": "#e4e4e7",  # Zinc 200
        "bg_botao_voltar_hover": "#3f3f46", # Zinc 700
        "bg_botao_sair": "#7f1d1d",     # Red 900
        "cor_botao_sair": "#fecaca",    # Red 200
        "bg_botao_sair_hover": "#991b1b", # Red 800

        # Botão de Cálculo (Play Verde)
        "bg_botao_calc": "#052e16",     # Emerald 950
        "borda_botao_calc": "#22c55e",  # Emerald 500
        "bg_botao_calc_hover": "#14532d", # Emerald 900

        # Botão de Alternância de Tema
        "bg_botao_tema": "#18181b",
        "borda_botao_tema": "#3f3f46",
        "bg_botao_tema_hover": "#27272a",
        "cor_icone_tema": "#fbbf24",    # Sol dourado brilhante

        # Gráficos (Matplotlib)
        "bg_plot": "#18181b",
        "borda_plot": "#27272a",
        "bg_fig": "#18181b",
        "bg_axes": "#121214",
        "fg_plot": "#f4f4f5",
        "grid_plot": "#27272a",
        "spine_plot": "#3f3f46",

        # Elementos Técnicos do Arranjo
        "cor_telhado": "#ef4444",       # Red 500
        "cor_painel_face": "#1e40af",   # Blue 800
        "cor_painel_borda": "#60a5fa",  # Blue 400
    },
}


class DoubleSpinBoxDecimalPonto(QtWidgets.QDoubleSpinBox):
    """Seletor numérico que aceita ponto ou vírgula, convertendo qualquer vírgula para ponto em tempo real."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLocale(QtCore.QLocale(QtCore.QLocale.Language.C))
        self.lineEdit().textChanged.connect(self._ao_mudar_texto)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        """Intercepta a tecla vírgula e a converte diretamente em ponto."""
        if event.text() == ",":
            evento_ponto = QtGui.QKeyEvent(
                event.type(),
                QtCore.Qt.Key.Key_Period,
                event.modifiers(),
                ".",
            )
            super().keyPressEvent(evento_ponto)
            return
        super().keyPressEvent(event)

    def _ao_mudar_texto(self, texto: str):
        """Converte automaticamente qualquer vírgula colada ou inserida para ponto."""
        if "," in texto:
            pos = self.lineEdit().cursorPosition()
            texto_corrigido = texto.replace(",", ".")
            self.lineEdit().blockSignals(True)
            self.lineEdit().setText(texto_corrigido)
            self.lineEdit().setCursorPosition(pos)
            self.lineEdit().blockSignals(False)

    def validate(self, input_text: str, pos: int):
        texto_ajustado = input_text.replace(",", ".")
        return super().validate(texto_ajustado, pos)

    def fixup(self, input_text: str) -> str:
        return input_text.replace(",", ".")

    def valueFromText(self, text: str) -> float:
        try:
            limpo = text.replace(",", ".").replace(self.suffix(), "").strip()
            return float(limpo)
        except Exception:
            return super().valueFromText(text)

    def textFromValue(self, value: float) -> str:
        return f"{value:.{self.decimals()}f}"


class SpinBoxCasasDecimais(QtWidgets.QSpinBox):
    """Seletor de casas decimais delimitado entre 0 e 5, com normalização para o inteiro mais próximo."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(0, 5)
        self.setValue(3)
        self.setKeyboardTracking(False)
        self.setFixedWidth(96)
        self.lineEdit().textChanged.connect(self._ao_mudar_texto)
        self.editingFinished.connect(self.normalizar)

    def focusInEvent(self, event: QtGui.QFocusEvent):
        super().focusInEvent(event)
        QtCore.QTimer.singleShot(0, self.lineEdit().selectAll)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        super().mousePressEvent(event)
        QtCore.QTimer.singleShot(0, self.lineEdit().selectAll)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        """Intercepta a tecla vírgula e a converte diretamente em ponto."""
        if event.text() == ",":
            evento_ponto = QtGui.QKeyEvent(
                event.type(),
                QtCore.Qt.Key.Key_Period,
                event.modifiers(),
                ".",
            )
            super().keyPressEvent(evento_ponto)
            return
        super().keyPressEvent(event)

    def _ao_mudar_texto(self, texto: str):
        """Converte automaticamente qualquer vírgula para ponto."""
        if "," in texto:
            pos = self.lineEdit().cursorPosition()
            texto_corrigido = texto.replace(",", ".")
            self.lineEdit().blockSignals(True)
            self.lineEdit().setText(texto_corrigido)
            self.lineEdit().setCursorPosition(pos)
            self.lineEdit().blockSignals(False)

    def validate(self, input_text: str, pos: int):
        # Permite digitação livre de números quebrados (com ponto ou vírgula) ou fora da faixa
        return QtGui.QValidator.State.Acceptable, input_text.replace(",", "."), pos

    def valueFromText(self, text: str) -> int:
        try:
            txt = text.replace(",", ".").strip()
            val_float = float(txt)
            return max(0, min(5, int(math.floor(val_float + 0.5))))
        except Exception:
            return self.value()

    def textFromValue(self, val: int) -> str:
        return str(val)

    def normalizar(self):
        """Converte números quebrados ou fora da faixa para o inteiro mais próximo permitido [0, 5]."""
        try:
            texto = self.lineEdit().text().replace(",", ".").strip()
            val_float = float(texto)
            val_norm = max(0, min(5, int(math.floor(val_float + 0.5))))
        except Exception:
            val_norm = self.value()

        if self.value() != val_norm:
            self.setValue(val_norm)
        self.lineEdit().setText(str(val_norm))


def obter_caminho_seta(apontar_para_cima: bool, tema_escuro: bool) -> str:
    """Gera e retorna o caminho de um ícone PNG de seta para os seletores numéricos."""
    direcao = "cima" if apontar_para_cima else "baixo"
    modo = "escuro" if tema_escuro else "claro"
    nome = f"seta_{direcao}_{modo}.png"
    caminho = os.path.join(_DIRETORIO_ASSETS, nome).replace("\\", "/")

    pix = QtGui.QPixmap(16, 16)
    pix.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(pix)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
    painter.setPen(QtCore.Qt.PenStyle.NoPen)

    paleta = PALETAS["escuro" if tema_escuro else "claro"]
    cor = QtGui.QColor(paleta["cor_input_texto"])
    painter.setBrush(QtGui.QBrush(cor))

    path = QtGui.QPainterPath()
    if apontar_para_cima:
        path.moveTo(8, 4)
        path.lineTo(13, 11)
        path.lineTo(3, 11)
    else:
        path.moveTo(3, 5)
        path.lineTo(13, 5)
        path.lineTo(8, 12)
    path.closeSubpath()

    painter.drawPath(path)
    painter.end()
    pix.save(caminho)
    return caminho


def obter_caminho_check() -> str:
    """Gera e retorna o caminho de um ícone PNG de checkmark para as caixas de seleção."""
    nome = "check_branco.png"
    caminho = os.path.join(_DIRETORIO_ASSETS, nome).replace("\\", "/")

    pix = QtGui.QPixmap(16, 16)
    pix.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(pix)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

    pen = QtGui.QPen(
        QtGui.QColor("#ffffff"),
        2.2,
        QtCore.Qt.PenStyle.SolidLine,
        QtCore.Qt.PenCapStyle.RoundCap,
        QtCore.Qt.PenJoinStyle.RoundJoin,
    )
    painter.setPen(pen)

    path = QtGui.QPainterPath()
    path.moveTo(3.5, 8.5)
    path.lineTo(6.5, 12.0)
    path.lineTo(12.5, 4.5)

    painter.drawPath(path)
    painter.end()
    pix.save(caminho)
    return caminho


def criar_icone_play(cor: str = "#22c55e", tamanho: int = 24) -> QtGui.QIcon:
    """Cria um ícone vetorial de Play verde para o botão de alocação."""
    pixmap = QtGui.QPixmap(tamanho, tamanho)
    pixmap.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
    painter.setPen(QtCore.Qt.PenStyle.NoPen)
    painter.setBrush(QtGui.QBrush(QtGui.QColor(cor)))

    path = QtGui.QPainterPath()
    path.moveTo(6, 4)
    path.lineTo(20, 12)
    path.lineTo(6, 20)
    path.closeSubpath()

    painter.drawPath(path)
    painter.end()
    return QtGui.QIcon(pixmap)


def detectar_tema_sistema() -> bool:
    """Verifica se o sistema operacional está utilizando o modo escuro."""
    try:
        app = QtWidgets.QApplication.instance()
        if app and hasattr(app, "styleHints"):
            hints = app.styleHints()
            if hasattr(hints, "colorScheme"):
                return hints.colorScheme() == QtCore.Qt.ColorScheme.Dark
    except Exception:
        pass

    if sys.platform == "win32":
        try:
            import winreg

            chave = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            )
            valor, _ = winreg.QueryValueEx(chave, "AppsUseLightTheme")
            winreg.CloseKey(chave)
            return valor == 0
        except Exception:
            pass

    return False


def criar_icone_sol(cor: str = "#f59e0b", tamanho: int = 26) -> QtGui.QIcon:
    """Cria um ícone vetorial de Sol para alternar ao tema claro."""
    pixmap = QtGui.QPixmap(tamanho, tamanho)
    pixmap.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

    qcor = QtGui.QColor(cor)
    pen = QtGui.QPen(
        qcor, 2, QtCore.Qt.PenStyle.SolidLine, QtCore.Qt.PenCapStyle.RoundCap
    )
    painter.setPen(pen)
    painter.setBrush(QtGui.QBrush(qcor))
    painter.drawEllipse(8, 8, 10, 10)

    raios = [
        (13, 2, 13, 5),
        (13, 21, 13, 24),
        (2, 13, 5, 13),
        (21, 13, 24, 13),
        (5, 5, 7, 7),
        (19, 19, 21, 21),
        (5, 21, 7, 19),
        (19, 7, 21, 5),
    ]
    for x1, y1, x2, y2 in raios:
        painter.drawLine(x1, y1, x2, y2)

    painter.end()
    return QtGui.QIcon(pixmap)


def criar_icone_lua(cor: str = "#4d85ef", tamanho: int = 26) -> QtGui.QIcon:
    """Cria um ícone vetorial de Lua para alternar ao tema escuro."""
    pixmap = QtGui.QPixmap(tamanho, tamanho)
    pixmap.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

    path = QtGui.QPainterPath()
    path.addEllipse(3, 3, 20, 20)
    sub = QtGui.QPainterPath()
    sub.addEllipse(9, 1, 18, 18)
    crescente = path.subtracted(sub)

    painter.setPen(QtCore.Qt.PenStyle.NoPen)
    painter.setBrush(QtGui.QBrush(QtGui.QColor(cor)))
    painter.drawPath(crescente)
    painter.end()
    return QtGui.QIcon(pixmap)


def gerar_patche_telhado(w_tel: float, l_tel: float, cor: str = "red"):
    """Cria o retângulo que representa o perímetro físico do telhado."""
    return patches.Rectangle(
        (0, 0),
        w_tel,
        l_tel,
        fill=False,
        edgecolor=cor,
        linewidth=2.0,
        zorder=2.5,
        label="Borda do Telhado",
    )


# Cache global em memória para as texturas dos módulos solares
_CACHE_TEXTURA_PAINEL = {"retrato": None, "paisagem": None}


def criar_textura_painel(orientacao_paisagem: bool = False) -> np.ndarray:
    """Gera a matriz RGB fotorrealista de um módulo fotovoltaico de alta eficiência.

    O preenchimento de silício monocristalino azul marinho/safira domina >92% da área visível,
    com moldura fina de alumínio anodizado, gaps ultrafinos entre células e busbars discretos.
    """
    if orientacao_paisagem:
        nx, ny = 360, 180
        n_col, n_lin = 12, 6
    else:
        nx, ny = 180, 360
        n_col, n_lin = 6, 12

    img = np.zeros((ny, nx, 3), dtype=np.float32)

    # 1. Moldura de alumínio anodizado fina e sofisticada (3 pixels, ~1.6% da dimensão)
    cor_moldura = np.array([0.65, 0.68, 0.72], dtype=np.float32)
    cor_luz = np.array([0.82, 0.85, 0.89], dtype=np.float32)
    cor_sombra = np.array([0.38, 0.40, 0.44], dtype=np.float32)

    img[:, :] = cor_moldura
    esp_frame = 3

    # Chanfros perimetrais de iluminação da moldura
    img[:1, :] = cor_luz
    img[:, :1] = cor_luz
    img[-1:, :] = cor_sombra
    img[:, -1:] = cor_sombra

    # 2. Área ativa do laminado fotovoltaico
    x0, x1 = esp_frame, nx - esp_frame
    y0, y1 = esp_frame, ny - esp_frame

    # Fundo do encapsulante/backsheet escuro sutil entre células
    img[y0:y1, x0:x1] = [0.06, 0.08, 0.12]

    w_cel = (x1 - x0) / n_col
    h_cel = (y1 - y0) / n_lin

    # Cor base do silício monocristalino com tratamento antirreflexo (ARC azul marinho safira)
    cor_silicio = np.array([0.08, 0.18, 0.38], dtype=np.float32)
    gap = 1

    for c in range(n_col):
        for l in range(n_lin):
            cx0 = int(round(x0 + c * w_cel)) + gap
            cx1 = int(round(x0 + (c + 1) * w_cel)) - gap
            cy0 = int(round(y0 + l * h_cel)) + gap
            cy1 = int(round(y0 + (l + 1) * h_cel)) - gap

            cw = cx1 - cx0
            ch = cy1 - cy0
            if cw > 0 and ch > 0:
                cel = np.zeros((ch, cw, 3), dtype=np.float32)
                grad_y = np.linspace(0.93, 1.07, ch)[:, None, None]
                grad_x = np.linspace(0.96, 1.04, cw)[None, :, None]
                cel[:, :] = cor_silicio * grad_y * grad_x

                # Cantos ultra-sutis de corte monocristalino (apenas 1 pixel para não roubar azul)
                if cw > 6 and ch > 6:
                    cel[0, 0] = [0.06, 0.08, 0.12]
                    cel[0, -1] = [0.06, 0.08, 0.12]
                    cel[-1, 0] = [0.06, 0.08, 0.12]
                    cel[-1, -1] = [0.06, 0.08, 0.12]

                # Multi-busbar finíssimo (linhas metálicas suaves de 1px)
                cor_bb = np.array([0.65, 0.72, 0.82], dtype=np.float32)
                pos_bb = [0.20, 0.40, 0.60, 0.80]
                if not orientacao_paisagem:
                    for frac in pos_bb:
                        bx = int(round(cw * frac))
                        if 0 <= bx < cw:
                            cel[:, bx] = cel[:, bx] * 0.5 + cor_bb * 0.5
                else:
                    for frac in pos_bb:
                        by = int(round(ch * frac))
                        if 0 <= by < ch:
                            cel[by, :] = cel[by, :] * 0.5 + cor_bb * 0.5

                img[cy0:cy1, cx0:cx1] = cel

    # 3. Divisão central sutil de módulos Half-Cell
    if not orientacao_paisagem:
        meio_y = int((y0 + y1) / 2)
        img[meio_y - 1 : meio_y + 1, x0:x1] = [0.06, 0.08, 0.12]
    else:
        meio_x = int((x0 + x1) / 2)
        img[y0:y1, meio_x - 1 : meio_x + 1] = [0.06, 0.08, 0.12]

    # 4. Brilho especular sutil do vidro temperado antirreflexo
    yy, xx = np.mgrid[y0:y1, x0:x1]
    diag = (xx - x0) / (x1 - x0) + (yy - y0) / (y1 - y0)
    brilho = 0.04 * np.exp(-((diag - 0.9) ** 2) / 0.20)
    for c_i in range(3):
        img[y0:y1, x0:x1, c_i] = np.clip(img[y0:y1, x0:x1, c_i] + brilho, 0.0, 1.0)

    return np.clip(img, 0.0, 1.0)


def obter_textura_painel(orientacao_paisagem: bool = False) -> np.ndarray:
    """Retorna a textura fotorrealista do módulo solar a partir do cache."""
    chave = "paisagem" if orientacao_paisagem else "retrato"
    if _CACHE_TEXTURA_PAINEL[chave] is None:
        _CACHE_TEXTURA_PAINEL[chave] = criar_textura_painel(orientacao_paisagem)
    return _CACHE_TEXTURA_PAINEL[chave]


def agrupar_fileiras_modulos(
    df_paineis, limiar_y: float = 0.02, limiar_x_gap: float = 0.25
):
    """Agrupa os módulos em fileiras horizontais e segmentos contíguos para instalação dos trilhos."""
    if df_paineis.empty:
        return []

    df_sorted = df_paineis.sort_values(by=["y_inf_esq", "x_inf_esq"])
    fileiras = []
    fileira_atual = []
    y_ref = None

    for _, row in df_sorted.iterrows():
        y_atual = row["y_inf_esq"]
        if y_ref is None or abs(y_atual - y_ref) <= limiar_y:
            fileira_atual.append(row)
            y_ref = y_atual
        else:
            if fileira_atual:
                fileiras.append(fileira_atual)
            fileira_atual = [row]
            y_ref = y_atual

    if fileira_atual:
        fileiras.append(fileira_atual)

    segmentos = []
    for f in fileiras:
        seg_atual = [f[0]]
        for i in range(1, len(f)):
            gap = f[i]["x_inf_esq"] - f[i - 1]["x_inf_dir"]
            if gap <= limiar_x_gap:
                seg_atual.append(f[i])
            else:
                segmentos.append(seg_atual)
                seg_atual = [f[i]]
        if seg_atual:
            segmentos.append(seg_atual)

    return segmentos


def agrupar_colunas_modulos(
    df_paineis, limiar_x: float = 0.02, limiar_y_gap: float = 0.25
):
    """Agrupa os módulos em colunas verticais e segmentos contíguos para instalação dos trilhos."""
    if df_paineis.empty:
        return []

    df_sorted = df_paineis.sort_values(by=["x_inf_esq", "y_inf_esq"])
    colunas = []
    coluna_atual = []
    x_ref = None

    for _, row in df_sorted.iterrows():
        x_atual = row["x_inf_esq"]
        if x_ref is None or abs(x_atual - x_ref) <= limiar_x:
            coluna_atual.append(row)
            x_ref = x_atual
        else:
            if coluna_atual:
                colunas.append(coluna_atual)
            coluna_atual = [row]
            x_ref = x_atual

    if coluna_atual:
        colunas.append(coluna_atual)

    segmentos = []
    for c in colunas:
        seg_atual = [c[0]]
        for i in range(1, len(c)):
            gap = c[i]["y_inf_esq"] - c[i - 1]["y_sup_esq"]
            if gap <= limiar_y_gap:
                seg_atual.append(c[i])
            else:
                segmentos.append(seg_atual)
                seg_atual = [c[i]]
        if seg_atual:
            segmentos.append(seg_atual)

    return segmentos


def desenhar_estrutura_suporte_e_paineis(
    ax,
    df_paineis,
    fator: float,
    tema_escuro: bool = False,
):
    """Desenha a estrutura metálica de trilhos, grampos de fixação e módulos fotovoltaicos realistas."""
    if df_paineis.empty:
        return

    # Determina orientação a partir do primeiro módulo
    primeiro = df_paineis.iloc[0]
    w_m = primeiro["x_inf_dir"] - primeiro["x_inf_esq"]
    h_m = primeiro["y_sup_esq"] - primeiro["y_inf_esq"]
    eh_paisagem = w_m > h_m

    img_modulo = obter_textura_painel(eh_paisagem)

    # 1. Estrutura metálica de suporte: trilhos contínuos e grampos (clamps)
    ext_trilho = 0.08 * fator
    esp_trilho = 0.05 * fator
    cw = 0.035 * fator
    ch = 0.055 * fator

    cor_trilho_face = "#475569" if tema_escuro else "#94a3b8"
    cor_trilho_borda = "#334155" if tema_escuro else "#64748b"
    cor_trilho_ranhura = "#94a3b8" if tema_escuro else "#f1f5f9"
    cor_clamp_face = "#cbd5e1" if tema_escuro else "#e2e8f0"
    cor_clamp_borda = "#1e293b" if tema_escuro else "#334155"

    if not eh_paisagem:
        # Painéis na VERTICAL (Retrato): trilhos horizontais (eixo X)
        segmentos = agrupar_fileiras_modulos(df_paineis)
        for seg in segmentos:
            x_ini = (seg[0]["x_inf_esq"] * fator) - ext_trilho
            x_fim = (seg[-1]["x_inf_dir"] * fator) + ext_trilho
            y_bot = seg[0]["y_inf_esq"] * fator
            h_seg = (seg[0]["y_sup_esq"] - seg[0]["y_inf_esq"]) * fator

            y_t1 = y_bot + 0.22 * h_seg
            y_t2 = y_bot + 0.78 * h_seg

            for yt in [y_t1, y_t2]:
                # Perfil do trilho metálico horizontal
                ax.add_patch(
                    patches.Rectangle(
                        (x_ini, yt - esp_trilho / 2.0),
                        x_fim - x_ini,
                        esp_trilho,
                        facecolor=cor_trilho_face,
                        edgecolor=cor_trilho_borda,
                        linewidth=0.7,
                        zorder=2.8,
                    )
                )
                # Ranhura longitudinal central
                ax.plot(
                    [x_ini, x_fim],
                    [yt, yt],
                    color=cor_trilho_ranhura,
                    linewidth=0.6,
                    zorder=2.85,
                )

                # Grampo terminal esquerdo (End-clamp)
                x_esq = seg[0]["x_inf_esq"] * fator
                ax.add_patch(
                    patches.Rectangle(
                        (x_esq - cw / 2.0, yt - ch / 2.0),
                        cw,
                        ch,
                        facecolor=cor_clamp_face,
                        edgecolor=cor_clamp_borda,
                        linewidth=0.6,
                        zorder=3.3,
                    )
                )

                # Grampos intermediários entre módulos (Mid-clamps) com parafuso allen
                for i in range(len(seg) - 1):
                    xm = (seg[i]["x_inf_dir"] + seg[i + 1]["x_inf_esq"]) / 2.0 * fator
                    ax.add_patch(
                        patches.Rectangle(
                            (xm - cw / 2.0, yt - ch / 2.0),
                            cw,
                            ch,
                            facecolor=cor_clamp_face,
                            edgecolor=cor_clamp_borda,
                            linewidth=0.6,
                            zorder=3.3,
                        )
                    )
                    ax.plot(
                        [xm],
                        [yt],
                        marker="o",
                        markersize=2.2,
                        color="#09090b",
                        zorder=3.4,
                    )

                # Grampo terminal direito (End-clamp)
                x_dir = seg[-1]["x_inf_dir"] * fator
                ax.add_patch(
                    patches.Rectangle(
                        (x_dir - cw / 2.0, yt - ch / 2.0),
                        cw,
                        ch,
                        facecolor=cor_clamp_face,
                        edgecolor=cor_clamp_borda,
                        linewidth=0.6,
                        zorder=3.3,
                    )
                )
    else:
        # Painéis na HORIZONTAL (Paisagem): trilhos giram 90º e ficam VERTICAIS (eixo Y)
        segmentos_col = agrupar_colunas_modulos(df_paineis)
        for seg in segmentos_col:
            y_ini = (seg[0]["y_inf_esq"] * fator) - ext_trilho
            y_fim = (seg[-1]["y_sup_esq"] * fator) + ext_trilho
            x_esq = seg[0]["x_inf_esq"] * fator
            w_seg = (seg[0]["x_inf_dir"] - seg[0]["x_inf_esq"]) * fator

            # 2 trilhos verticais que cruzam o lado longo do módulo
            x_t1 = x_esq + 0.22 * w_seg
            x_t2 = x_esq + 0.78 * w_seg

            for xt in [x_t1, x_t2]:
                # Perfil do trilho metálico vertical
                ax.add_patch(
                    patches.Rectangle(
                        (xt - esp_trilho / 2.0, y_ini),
                        esp_trilho,
                        y_fim - y_ini,
                        facecolor=cor_trilho_face,
                        edgecolor=cor_trilho_borda,
                        linewidth=0.7,
                        zorder=2.8,
                    )
                )
                # Ranhura vertical central
                ax.plot(
                    [xt, xt],
                    [y_ini, y_fim],
                    color=cor_trilho_ranhura,
                    linewidth=0.6,
                    zorder=2.85,
                )

                # Grampo terminal inferior (End-clamp horizontalizado)
                y_bot = seg[0]["y_inf_esq"] * fator
                ax.add_patch(
                    patches.Rectangle(
                        (xt - ch / 2.0, y_bot - cw / 2.0),
                        ch,
                        cw,
                        facecolor=cor_clamp_face,
                        edgecolor=cor_clamp_borda,
                        linewidth=0.6,
                        zorder=3.3,
                    )
                )

                # Grampos intermediários entre módulos da coluna
                for i in range(len(seg) - 1):
                    ym = (seg[i]["y_sup_esq"] + seg[i + 1]["y_inf_esq"]) / 2.0 * fator
                    ax.add_patch(
                        patches.Rectangle(
                            (xt - ch / 2.0, ym - cw / 2.0),
                            ch,
                            cw,
                            facecolor=cor_clamp_face,
                            edgecolor=cor_clamp_borda,
                            linewidth=0.6,
                            zorder=3.3,
                        )
                    )
                    ax.plot(
                        [xt],
                        [ym],
                        marker="o",
                        markersize=2.2,
                        color="#09090b",
                        zorder=3.4,
                    )

                # Grampo terminal superior (End-clamp horizontalizado)
                y_top = seg[-1]["y_sup_esq"] * fator
                ax.add_patch(
                    patches.Rectangle(
                        (xt - ch / 2.0, y_top - cw / 2.0),
                        ch,
                        cw,
                        facecolor=cor_clamp_face,
                        edgecolor=cor_clamp_borda,
                        linewidth=0.6,
                        zorder=3.3,
                    )
                )

    # 2. Módulos Fotovoltaicos fotorrealistas
    cor_moldura_vetorial = "#64748b" if tema_escuro else "#475569"
    for _, row in df_paineis.iterrows():
        x1 = row["x_inf_esq"] * fator
        y1 = row["y_inf_esq"] * fator
        x2 = row["x_inf_dir"] * fator
        y2 = row["y_sup_esq"] * fator

        # Textura fotorrealista do módulo solar
        ax.imshow(
            img_modulo,
            extent=[x1, x2, y1, y2],
            origin="lower",
            zorder=3.0,
            aspect="auto",
            interpolation="bilinear",
        )

        # Moldura nítida de alumínio perimetral (linha fina sutil)
        ax.add_patch(
            patches.Rectangle(
                (x1, y1),
                x2 - x1,
                y2 - y1,
                fill=False,
                edgecolor=cor_moldura_vetorial,
                linewidth=0.45,
                zorder=3.1,
            )
        )


def gerar_patche_painel(
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
    tema_escuro: bool = False,
):
    """Cria o retângulo que representa um painel fotovoltaico (método de apoio)."""
    paleta = PALETAS["escuro" if tema_escuro else "claro"]
    largura = x_max - x_min
    altura = y_max - y_min
    face = paleta["cor_painel_face"]
    edge = paleta["cor_painel_borda"]
    return patches.Rectangle(
        (x_min, y_min),
        largura,
        altura,
        facecolor=face,
        alpha=0.92,
        edgecolor=edge,
        linewidth=0.9,
        zorder=3.0,
    )


def calcular_contorno_area_util(
    w_disp: float,
    l_disp: float,
    borda_disp: float,
    dist_quina_disp: float,
    n_pts: int = 24,
):
    """Calcula os vértices ordenados da área utilizável no sentido horário."""
    if w_disp <= 2 * borda_disp or l_disp <= 2 * borda_disp:
        return []

    if dist_quina_disp <= borda_disp:
        return [
            (borda_disp, l_disp - borda_disp),
            (w_disp - borda_disp, l_disp - borda_disp),
            (w_disp - borda_disp, borda_disp),
            (borda_disp, borda_disp),
        ]

    d_max_w = (w_disp - 2 * borda_disp) / 2.0
    d_max_l = (l_disp - 2 * borda_disp) / 2.0
    d_max = min(d_max_w, d_max_l)

    if dist_quina_disp**2 <= borda_disp**2:
        return [
            (borda_disp, l_disp - borda_disp),
            (w_disp - borda_disp, l_disp - borda_disp),
            (w_disp - borda_disp, borda_disp),
            (borda_disp, borda_disp),
        ]

    d = min(math.sqrt(dist_quina_disp**2 - borda_disp**2), d_max)
    if d <= 0:
        return [
            (borda_disp, l_disp - borda_disp),
            (w_disp - borda_disp, l_disp - borda_disp),
            (w_disp - borda_disp, borda_disp),
            (borda_disp, borda_disp),
        ]

    razao = max(0.0, min(1.0, borda_disp / dist_quina_disp))
    pts = []

    # 1. Quina Superior Esquerda: centro (0, l_disp)
    for t in np.linspace(-np.arccos(razao), -np.arcsin(razao), n_pts):
        pts.append((dist_quina_disp * np.cos(t), l_disp + dist_quina_disp * np.sin(t)))

    # 2. Quina Superior Direita: centro (w_disp, l_disp)
    for t in np.linspace(np.pi + np.arcsin(razao), np.pi + np.arccos(razao), n_pts):
        pts.append((w_disp + dist_quina_disp * np.cos(t), l_disp + dist_quina_disp * np.sin(t)))

    # 3. Quina Inferior Direita: centro (w_disp, 0)
    for t in np.linspace(np.pi - np.arccos(razao), np.pi - np.arcsin(razao), n_pts):
        pts.append((w_disp + dist_quina_disp * np.cos(t), dist_quina_disp * np.sin(t)))

    # 4. Quina Inferior Esquerda: centro (0, 0)
    for t in np.linspace(np.arcsin(razao), np.arccos(razao), n_pts):
        pts.append((dist_quina_disp * np.cos(t), dist_quina_disp * np.sin(t)))

    return pts


def criar_patch_area_nao_utilizavel(
    w_disp: float,
    l_disp: float,
    borda_disp: float,
    dist_quina_disp: float,
):
    """Cria um PathPatch unificado com recorte que preenche a área não utilizável com vermelho translúcido."""
    verts_ext = [
        (0.0, 0.0),
        (w_disp, 0.0),
        (w_disp, l_disp),
        (0.0, l_disp),
        (0.0, 0.0),
    ]
    codes_ext = [
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.CLOSEPOLY,
    ]

    pts_util = calcular_contorno_area_util(
        w_disp, l_disp, borda_disp, dist_quina_disp
    )

    if pts_util:
        verts_furo = pts_util + [pts_util[0]]
        codes_furo = [Path.MOVETO] + [Path.LINETO] * (len(pts_util) - 1) + [Path.CLOSEPOLY]
        path_completo = Path(verts_ext + verts_furo, codes_ext + codes_furo)
    else:
        path_completo = Path(verts_ext, codes_ext)

    return patches.PathPatch(
        path_completo,
        facecolor="#ef4444",
        alpha=0.32,
        edgecolor="none",
        zorder=1.0,
    )


def criar_patch_linha_area_util(pts_util, cor_telhado: str):
    """Cria o contorno fino e tracejado que delimita a área utilizável."""
    if not pts_util:
        return None
    verts = pts_util + [pts_util[0]]
    codes = [Path.MOVETO] + [Path.LINETO] * (len(pts_util) - 1) + [Path.CLOSEPOLY]
    return patches.PathPatch(
        Path(verts, codes),
        fill=False,
        edgecolor=cor_telhado,
        linestyle="--",
        linewidth=1.3,
        zorder=2.0,
    )


def desenhar_arcos_quinas(
    ax,
    w_disp: float,
    l_disp: float,
    dist_quina_disp: float,
    cor_telhado: str,
    n_pts: int = 30,
):
    """Exibe os arcos/semicírculos que determinam a distância de segurança nas 4 quinas."""
    if dist_quina_disp <= 0:
        return

    quinas = [
        (0.0, 0.0, 0.0, np.pi / 2.0),
        (w_disp, 0.0, np.pi / 2.0, np.pi),
        (w_disp, l_disp, np.pi, 3.0 * np.pi / 2.0),
        (0.0, l_disp, 3.0 * np.pi / 2.0, 2.0 * np.pi),
    ]

    for qx, qy, t1, t2 in quinas:
        th = np.linspace(t1, t2, n_pts)
        xs = qx + dist_quina_disp * np.cos(th)
        ys = qy + dist_quina_disp * np.sin(th)
        ax.plot(
            xs,
            ys,
            color=cor_telhado,
            linestyle="--",
            linewidth=1.3,
            zorder=2.0,
        )


def gerar_textura_realista(
    material: str,
    w_m: float,
    l_m: float,
    tema_escuro: bool = False,
) -> np.ndarray:
    """Gera uma matriz RGB procedural de alta definição e 100% opaca com iluminação e relevo do material."""
    max_pts = 600
    dpi_m = min(45.0, max_pts / max(w_m, l_m, 1.0))
    nx = max(32, int(w_m * dpi_m))
    ny = max(32, int(l_m * dpi_m))
    x = np.linspace(0, w_m, nx)
    y = np.linspace(0, l_m, ny)
    X, Y = np.meshgrid(x, y)
    np.random.seed(42)

    if "Cerâmica" in material:
        passo_x = 0.22
        onda = np.sin(2.0 * np.pi * X / passo_x)
        luz_onda = 0.72 + 0.28 * onda
        passo_y = 0.40
        y_rel = (Y % passo_y) / passo_y
        sombra_y = np.where(y_rel < 0.07, 0.68 + 0.32 * (y_rel / 0.07), 1.0)
        ruido = np.random.normal(0, 0.025, (ny, nx))
        fator = np.clip(luz_onda * sombra_y + ruido, 0.35, 1.25)
        if tema_escuro:
            r, g, b = 0.68, 0.26, 0.10
        else:
            r, g, b = 0.84, 0.38, 0.16
        return np.dstack([np.clip(r * fator, 0, 1), np.clip(g * fator, 0, 1), np.clip(b * fator, 0, 1)])

    elif "Metálico" in material:
        passo_x = 0.25
        x_rel = (X % passo_x) / passo_x
        perfil = np.piecewise(
            x_rel,
            [
                x_rel < 0.25,
                (x_rel >= 0.25) & (x_rel < 0.40),
                (x_rel >= 0.40) & (x_rel < 0.85),
                x_rel >= 0.85,
            ],
            [
                lambda t: 1.15,
                lambda t: 1.15 - 0.45 * ((t - 0.25) / 0.15),
                lambda t: 0.70,
                lambda t: 0.70 + 0.45 * ((t - 0.85) / 0.15),
            ],
        )
        ruido = np.random.normal(0, 0.015, (ny, nx))
        fator = np.clip(perfil + ruido, 0.4, 1.3)
        if tema_escuro:
            r, g, b = 0.34, 0.39, 0.46
        else:
            r, g, b = 0.66, 0.72, 0.78
        return np.dstack([np.clip(r * fator, 0, 1), np.clip(g * fator, 0, 1), np.clip(b * fator, 0, 1)])

    elif "Fibrocimento" in material:
        passo_x = 0.16
        onda = np.sin(2.0 * np.pi * X / passo_x)
        luz_onda = 0.82 + 0.22 * onda
        passo_y = 1.80
        y_rel = (Y % passo_y) / passo_y
        sombra_y = np.where(y_rel < 0.03, 0.75 + 0.25 * (y_rel / 0.03), 1.0)
        ruido = np.random.normal(0, 0.03, (ny, nx))
        fator = np.clip(luz_onda * sombra_y + ruido, 0.4, 1.2)
        if tema_escuro:
            r, g, b = 0.42, 0.41, 0.40
        else:
            r, g, b = 0.68, 0.67, 0.65
        return np.dstack([np.clip(r * fator, 0, 1), np.clip(g * fator, 0, 1), np.clip(b * fator, 0, 1)])

    elif "Laje" in material:
        passo_grelha = 2.50
        dist_x = np.minimum(X % passo_grelha, passo_grelha - (X % passo_grelha))
        dist_y = np.minimum(Y % passo_grelha, passo_grelha - (Y % passo_grelha))
        junta = np.where((dist_x < 0.04) | (dist_y < 0.04), 0.78, 1.0)
        ruido1 = np.random.normal(0, 0.04, (ny, nx))
        ruido2 = np.random.normal(0, 0.02, (ny, nx))
        fator = np.clip(junta + ruido1 + ruido2, 0.4, 1.2)
        if tema_escuro:
            r, g, b = 0.35, 0.36, 0.38
        else:
            r, g, b = 0.76, 0.78, 0.80
        return np.dstack([np.clip(r * fator, 0, 1), np.clip(g * fator, 0, 1), np.clip(b * fator, 0, 1)])

    elif "Shingle" in material:
        passo_y = 0.15
        passo_x = 0.32
        linha_idx = np.floor(Y / passo_y).astype(int)
        offset_x = (linha_idx % 2) * (passo_x / 2.0)
        x_alinhado = X + offset_x
        dist_junta_x = np.minimum(x_alinhado % passo_x, passo_x - (x_alinhado % passo_x))
        junta_x = np.where(dist_junta_x < 0.02, 0.65, 1.0)
        y_rel = (Y % passo_y) / passo_y
        sombra_y = np.where(y_rel < 0.12, 0.60 + 0.40 * (y_rel / 0.12), 0.95 + 0.08 * (1.0 - y_rel))
        ruido = np.random.normal(0, 0.035, (ny, nx))
        fator = np.clip(sombra_y * junta_x + ruido, 0.35, 1.25)
        if tema_escuro:
            r, g, b = 0.25, 0.27, 0.30
        else:
            r, g, b = 0.45, 0.47, 0.52
        return np.dstack([np.clip(r * fator, 0, 1), np.clip(g * fator, 0, 1), np.clip(b * fator, 0, 1)])

    elif "Sanduíche" in material:
        passo_x = 0.30
        x_rel = (X % passo_x) / passo_x
        perfil = np.piecewise(
            x_rel,
            [
                x_rel < 0.15,
                (x_rel >= 0.15) & (x_rel < 0.25),
                (x_rel >= 0.25) & (x_rel < 0.90),
                x_rel >= 0.90,
            ],
            [
                lambda t: 1.18,
                lambda t: 1.18 - 0.35 * ((t - 0.15) / 0.10),
                lambda t: 0.83,
                lambda t: 0.83 + 0.35 * ((t - 0.90) / 0.10),
            ],
        )
        ruido = np.random.normal(0, 0.01, (ny, nx))
        fator = np.clip(perfil + ruido, 0.5, 1.3)
        if tema_escuro:
            r, g, b = 0.28, 0.32, 0.38
        else:
            r, g, b = 0.90, 0.92, 0.94
        return np.dstack([np.clip(r * fator, 0, 1), np.clip(g * fator, 0, 1), np.clip(b * fator, 0, 1)])

    else:
        # Padrão (Neutro)
        val = 0.18 if tema_escuro else 0.96
        return np.ones((ny, nx, 3)) * val


def aplicar_textura_material_telhado(
    ax,
    w_tel: float,
    l_tel: float,
    w_disp: float,
    l_disp: float,
    material: str,
    tema_escuro: bool = False,
):
    """Renderiza a textura física realista e 100% opaca do material do telhado."""
    # Se for Padrão (Neutro), preenche com cor sólida limpa
    if material == "Padrão (Neutro)":
        cor_solida = "#27272a" if tema_escuro else "#f8fafc"
        ax.add_patch(
            patches.Rectangle(
                (0.0, 0.0),
                w_disp,
                l_disp,
                facecolor=cor_solida,
                edgecolor="none",
                zorder=0.5,
            )
        )
        return

    # Gera a textura procedimental realista em alta resolução
    img = gerar_textura_realista(
        material=material,
        w_m=w_tel,
        l_m=l_tel,
        tema_escuro=tema_escuro,
    )

    # Renderiza a imagem do material opaca ocupando exatamente o perímetro do telhado
    ax.imshow(
        img,
        extent=[0.0, w_disp, 0.0, l_disp],
        origin="lower",
        zorder=0.5,
        aspect="auto",
        interpolation="bilinear",
    )


def desenhar_eixo(
    ax,
    df_paineis,
    w_tel: float,
    l_tel: float,
    titulo: str,
    borda: float = 0.5,
    dist_quina: float = 1.0,
    material: str = "Cerâmica / Barro (Colonial)",
    tema_escuro: bool = False,
    unidade: str = "Metros (m)",
    mostrar_area_util: bool = True,
):
    """Preenche e configura um eixo com o arranjo de painéis na unidade selecionada."""
    dados_u = UNIDADES.get(unidade, UNIDADES["Metros (m)"])
    fator = dados_u["de_m"]
    sigla = dados_u["sigla"]

    w_disp = w_tel * fator
    l_disp = l_tel * fator
    borda_disp = borda * fator
    dist_quina_disp = dist_quina * fator

    paleta = PALETAS["escuro" if tema_escuro else "claro"]
    cor_telhado = paleta["cor_telhado"]

    # 0. Textura realista 100% opaca do material do telhado
    aplicar_textura_material_telhado(
        ax,
        w_tel=w_tel,
        l_tel=l_tel,
        w_disp=w_disp,
        l_disp=l_disp,
        material=material,
        tema_escuro=tema_escuro,
    )

    # 1. Delimitação da área útil (sombreamento vermelho, linha tracejada e arcos de quina)
    if mostrar_area_util:
        patch_nao_util = criar_patch_area_nao_utilizavel(
            w_disp, l_disp, borda_disp, dist_quina_disp
        )
        if patch_nao_util is not None:
            ax.add_patch(patch_nao_util)

        pts_util = calcular_contorno_area_util(
            w_disp, l_disp, borda_disp, dist_quina_disp
        )
        patch_linha_util = criar_patch_linha_area_util(pts_util, cor_telhado)
        if patch_linha_util is not None:
            ax.add_patch(patch_linha_util)

        desenhar_arcos_quinas(ax, w_disp, l_disp, dist_quina_disp, cor_telhado)

    # 2. Perímetro externo físico do telhado (linha sólida)
    ax.add_patch(gerar_patche_telhado(w_disp, l_disp, cor=cor_telhado))

    # 3. Estrutura metálica de suporte e painéis fotovoltaicos fotorrealistas
    desenhar_estrutura_suporte_e_paineis(
        ax, df_paineis, fator=fator, tema_escuro=tema_escuro
    )

    margem = 1.0 * fator
    ax.set_xlim(-margem, w_disp + margem)
    ax.set_ylim(-margem, l_disp + margem)
    ax.set_aspect("equal", adjustable="box")

    fg = paleta["fg_plot"]
    bg = paleta["bg_axes"]
    grid_cor = paleta["grid_plot"]
    spine_cor = paleta["spine_plot"]

    ax.set_facecolor(bg)
    ax.set_title(
        f"{titulo}: {len(df_paineis)} Painéis",
        color=fg,
        fontsize=11,
        fontweight="bold",
    )
    ax.set_xlabel(f"Largura ({sigla})", color=fg)
    ax.set_ylabel(f"Comprimento ({sigla})", color=fg)
    ax.tick_params(colors=fg)

    for spine in ax.spines.values():
        spine.set_color(spine_cor)

    ax.grid(True, linestyle="--", alpha=0.5, color=grid_cor)


class CanvasJanela(FigureCanvas):
    """Componente de plotagem embutido no PyQt6."""

    def __init__(self, largura: int = 8, altura: int = 4, dpi: int = 100):
        self.fig = Figure(figsize=(largura, altura), dpi=dpi)
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        self.texto_qtd = None
        super().__init__(self.fig)

    def atualizar_grafico(
        self,
        df_retrato,
        df_paisagem,
        w_tel: float,
        l_tel: float,
        borda: float = 0.5,
        dist_quina: float = 1.0,
        material: str = "Cerâmica / Barro (Colonial)",
        tema_escuro: bool = False,
        unidade: str = "Metros (m)",
        mostrar_area_util: bool = True,
    ):
        """Limpa o canvas e renderiza as duas orientações simultaneamente."""
        self.ax1.clear()
        self.ax2.clear()

        if self.texto_qtd:
            try:
                self.texto_qtd.remove()
            except Exception:
                pass
            self.texto_qtd = None

        paleta = PALETAS["escuro" if tema_escuro else "claro"]
        bg_fig = paleta["bg_fig"]
        fg_texto = paleta["fg_plot"]
        self.fig.patch.set_facecolor(bg_fig)

        desenhar_eixo(
            self.ax1,
            df_retrato,
            w_tel,
            l_tel,
            "Orientação Retrato",
            borda=borda,
            dist_quina=dist_quina,
            material=material,
            tema_escuro=tema_escuro,
            unidade=unidade,
            mostrar_area_util=mostrar_area_util,
        )
        desenhar_eixo(
            self.ax2,
            df_paisagem,
            w_tel,
            l_tel,
            "Orientação Paisagem",
            borda=borda,
            dist_quina=dist_quina,
            material=material,
            tema_escuro=tema_escuro,
            unidade=unidade,
            mostrar_area_util=mostrar_area_util,
        )

        texto_base = (
            f"Comparativo Técnico | Retrato: {len(df_retrato)} painéis "
            f"vs. Paisagem: {len(df_paisagem)} painéis"
        )
        self.texto_qtd = self.fig.text(
            0.5,
            0.02,
            texto_base,
            ha="center",
            fontsize=10,
            fontweight="bold",
            color=fg_texto,
        )

        self.fig.tight_layout()
        self.fig.subplots_adjust(bottom=0.14)
        self.draw()


def plotar_janela_independente(
    df_retrato,
    df_paisagem,
    w_tel,
    l_tel,
    borda: float = 0.5,
    dist_quina: float = 1.0,
    material: str = "Cerâmica / Barro (Colonial)",
    mostrar_area_util: bool = True,
):
    """Abre uma janela padrão do Matplotlib com os dois arranjos lado a lado."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    desenhar_eixo(
        ax1,
        df_retrato,
        w_tel,
        l_tel,
        "Orientação Retrato",
        borda=borda,
        dist_quina=dist_quina,
        material=material,
        mostrar_area_util=mostrar_area_util,
    )
    desenhar_eixo(
        ax2,
        df_paisagem,
        w_tel,
        l_tel,
        "Orientação Paisagem",
        borda=borda,
        dist_quina=dist_quina,
        material=material,
        mostrar_area_util=mostrar_area_util,
    )

    texto_base = (
        f"Comparativo Técnico | Retrato: {len(df_retrato)} painéis "
        f"vs. Paisagem: {len(df_paisagem)} painéis"
    )
    fig.text(0.5, 0.02, texto_base, ha="center", fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.show()


class MainWindow(QtWidgets.QMainWindow):
    """Janela principal do Alocador Automático de Painéis Fotovoltaicos."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Alocador automático de Painéis Fotovoltaicos")
        self.setMinimumSize(QtCore.QSize(860, 640))
        self.resize(1020, 740)

        # 1. TEMA, UNIDADE, CASAS DECIMAIS E MATERIAL DO TELHADO
        self.tema_escuro = detectar_tema_sistema()
        self.tema_manual = False
        self.unidade_atual = "Metros (m)"
        self.casas_decimais = 3
        self.material_telhado_atual = "Cerâmica / Barro (Colonial)"
        self.mostrar_area_util = True

        # Cache dos últimos resultados calculados (armazenados em Metros)
        self.ultimo_df_retrato = None
        self.ultimo_df_paisagem = None
        self.ultimo_w_tel = None
        self.ultimo_l_tel = None
        self.ultimo_borda = 0.5
        self.ultimo_dist_quina = 1.0

        # 2. GERENCIADOR DE TELAS (STACKED WIDGET)
        self.telas = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.telas)

        # 3. CONSTRUIR AS TELAS
        self.criar_tela_inicial()
        self.criar_tela_novo_projeto()
        self.criar_tela_modo_simplificado()

        # 4. ADICIONAR AS TELAS AO GERENCIADOR
        self.telas.addWidget(self.tela_inicial)
        self.telas.addWidget(self.tela_novo_projeto)
        self.telas.addWidget(self.tela_modo_simplificado)

        # 5. BOTÃO DE TEMA FIXO NA EXTREMIDADE DA TELA (CANTO SUPERIOR DIREITO)
        self.botao_tema = QtWidgets.QPushButton(self)
        self.botao_tema.setFixedSize(40, 40)
        self.botao_tema.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.botao_tema.clicked.connect(self.alternar_tema)

        # 6. SINCRONIZAÇÃO AUTOMÁTICA COM O SO
        app = QtWidgets.QApplication.instance()
        if app and hasattr(app, "styleHints"):
            hints = app.styleHints()
            if hasattr(hints, "colorSchemeChanged"):
                hints.colorSchemeChanged.connect(self._ao_mudar_tema_sistema)

        # 7. APLICAR TEMA INICIAL E DIMENSIONAMENTO PRELIMINAR
        self.aplicar_tema(self.tema_escuro)
        self.executar_dimensionamento()

    def resizeEvent(self, event):
        """Mantém o botão de tema no canto superior direito da janela."""
        super().resizeEvent(event)
        margem = 14
        self.botao_tema.move(
            self.width() - self.botao_tema.width() - margem, margem
        )
        self.botao_tema.raise_()

    def alternar_tema(self):
        """Alterna manualmente entre tema claro e escuro."""
        self.tema_manual = True
        self.aplicar_tema(not self.tema_escuro)
        self.replotar_resultado_atual()

    def _ao_mudar_tema_sistema(self):
        """Responde às mudanças de tema do SO quando não houver seleção manual."""
        if not self.tema_manual:
            novo_escuro = detectar_tema_sistema()
            if novo_escuro != self.tema_escuro:
                self.aplicar_tema(novo_escuro)
                self.replotar_resultado_atual()

    def replotar_resultado_atual(self):
        """Re-renderiza o arranjo atual com o tema, a unidade, o material e as opções de exibição."""
        if self.ultimo_df_retrato is not None:
            self.canvas.atualizar_grafico(
                df_retrato=self.ultimo_df_retrato,
                df_paisagem=self.ultimo_df_paisagem,
                w_tel=self.ultimo_w_tel,
                l_tel=self.ultimo_l_tel,
                borda=self.ultimo_borda,
                dist_quina=self.ultimo_dist_quina,
                material=self.material_telhado_atual,
                tema_escuro=self.tema_escuro,
                unidade=self.unidade_atual,
                mostrar_area_util=self.mostrar_area_util,
            )

    def criar_tela_inicial(self):
        """Monta a primeira tela (Menu Inicial)."""
        self.tela_inicial = QtWidgets.QWidget()

        self.titulo_inicio = QtWidgets.QLabel("Bem-vindo ao Alocador de Painéis!")
        self.instrucao_inicio = QtWidgets.QLabel(
            "Inicie um novo projeto ou abra um arquivo existente para começar."
        )

        self.titulo_inicio.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.instrucao_inicio.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.botao_criar = QtWidgets.QPushButton("Criar novo projeto")
        self.botao_abrir = QtWidgets.QPushButton("Abrir projeto existente")
        self.botao_criar.setFixedSize(200, 75)
        self.botao_abrir.setFixedSize(200, 75)
        self.botao_criar.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.botao_abrir.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.botao_sair = QtWidgets.QPushButton("Sair do Programa")
        self.botao_sair.setFixedSize(130, 32)
        self.botao_sair.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.botao_criar.clicked.connect(lambda: self.telas.setCurrentIndex(1))
        self.botao_sair.clicked.connect(QtWidgets.QApplication.instance().quit)

        layout_principal = QtWidgets.QVBoxLayout()
        layout_principal.addStretch(3)
        layout_principal.addWidget(self.titulo_inicio)
        layout_principal.addSpacing(10)
        layout_principal.addWidget(self.instrucao_inicio)
        layout_principal.addStretch(1)

        layout_botoes = QtWidgets.QHBoxLayout()
        layout_botoes.addWidget(self.botao_criar)
        layout_botoes.addWidget(self.botao_abrir)
        layout_principal.addLayout(layout_botoes)

        layout_principal.addStretch(3)
        layout_principal.addWidget(
            self.botao_sair, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        layout_principal.addStretch(1)

        self.tela_inicial.setLayout(layout_principal)

    def criar_tela_novo_projeto(self):
        """Monta a segunda tela (Seleção do modo do projeto)."""
        self.tela_novo_projeto = QtWidgets.QWidget()

        self.titulo_modo = QtWidgets.QLabel("Selecione o modo de criação do projeto")
        self.instrucao_modo = QtWidgets.QLabel(
            "O modo simplificado realiza o dimensionamento a partir de um retângulo, "
            "já o modo avançado realiza o dimensionamento a partir de geometrias complexas."
        )

        self.titulo_modo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.instrucao_modo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.instrucao_modo.setWordWrap(True)

        self.botao_modo_simp = QtWidgets.QPushButton("Modo simplificado")
        self.botao_modo_avan = QtWidgets.QPushButton("Modo avançado")
        self.botao_modo_simp.setFixedSize(200, 75)
        self.botao_modo_avan.setFixedSize(200, 75)
        self.botao_modo_simp.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.botao_modo_avan.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.botao_voltar_modo = QtWidgets.QPushButton("← Voltar")
        self.botao_voltar_modo.setFixedSize(70, 32)
        self.botao_voltar_modo.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.botao_voltar_modo.clicked.connect(lambda: self.telas.setCurrentIndex(0))
        self.botao_modo_simp.clicked.connect(lambda: self.telas.setCurrentIndex(2))

        layout_modo = QtWidgets.QVBoxLayout()
        layout_modo.addWidget(
            self.botao_voltar_modo,
            alignment=QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop,
        )

        layout_modo.addStretch(3)
        layout_modo.addWidget(self.titulo_modo)
        layout_modo.addSpacing(10)
        layout_modo.addWidget(self.instrucao_modo)
        layout_modo.addStretch(2)

        layout_botoes_modo = QtWidgets.QHBoxLayout()
        layout_botoes_modo.addWidget(self.botao_modo_simp)
        layout_botoes_modo.addWidget(self.botao_modo_avan)
        layout_modo.addLayout(layout_botoes_modo)
        layout_modo.addStretch(6)

        self.tela_novo_projeto.setLayout(layout_modo)

    def criar_tela_modo_simplificado(self):
        """Monta a terceira tela (Modo Simplificado com menus superiores e botão play)."""
        self.tela_modo_simplificado = QtWidgets.QWidget()

        layout_simplificado = QtWidgets.QVBoxLayout()
        layout_simplificado.setContentsMargins(18, 12, 18, 14)
        layout_simplificado.setSpacing(10)

        # Barra do topo: botão voltar
        layout_topo = QtWidgets.QHBoxLayout()
        self.botao_voltar_simp = QtWidgets.QPushButton("← Voltar")
        self.botao_voltar_simp.setFixedSize(70, 32)
        self.botao_voltar_simp.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.botao_voltar_simp.clicked.connect(lambda: self.telas.setCurrentIndex(1))

        layout_topo.addWidget(self.botao_voltar_simp)
        layout_topo.addStretch(1)
        layout_simplificado.addLayout(layout_topo)

        # --- SEÇÃO SUPERIOR: BOTÃO PLAY À ESQUERDA + MENUS / ABAS ---
        layout_controles = QtWidgets.QHBoxLayout()
        layout_controles.setSpacing(14)

        # 1. BOTÃO DE REALIZAR ALOCAÇÃO (Sempre visível à esquerda com ícone de play verde)
        self.botao_calcular = QtWidgets.QPushButton("Realizar Alocação")
        self.botao_calcular.setObjectName("botao_calcular")
        self.botao_calcular.setFixedSize(185, 68)
        self.botao_calcular.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.botao_calcular.setIcon(criar_icone_play("#22c55e", 24))
        self.botao_calcular.setIconSize(QtCore.QSize(20, 20))
        self.botao_calcular.setToolTip("Executa o cálculo e atualiza o gráfico com as opções configuradas")
        self.botao_calcular.clicked.connect(self.executar_dimensionamento)

        # 2. ABAS SUPERIORES COM DIFERENTES MENUS
        self.abas_configuracao = QtWidgets.QTabWidget()
        self.abas_configuracao.setFixedHeight(84)

        # === MENU 1: Opções de Telhado ===
        self.aba_telhado = QtWidgets.QWidget()
        layout_aba_telhado = QtWidgets.QHBoxLayout(self.aba_telhado)
        layout_aba_telhado.setContentsMargins(14, 6, 14, 6)
        layout_aba_telhado.setSpacing(12)

        self.lbl_larg_telhado = QtWidgets.QLabel("Largura (m):")
        self.input_larg_telhado = DoubleSpinBoxDecimalPonto()
        self.input_larg_telhado.setDecimals(self.casas_decimais)
        self.input_larg_telhado.setRange(0.5, 2000.0)
        self.input_larg_telhado.setSingleStep(0.5)
        self.input_larg_telhado.setValue(17.50)
        self.input_larg_telhado.setSuffix(" m")

        self.lbl_comp_telhado = QtWidgets.QLabel("Comprimento (m):")
        self.input_comp_telhado = DoubleSpinBoxDecimalPonto()
        self.input_comp_telhado.setDecimals(self.casas_decimais)
        self.input_comp_telhado.setRange(0.5, 2000.0)
        self.input_comp_telhado.setSingleStep(0.5)
        self.input_comp_telhado.setValue(7.20)
        self.input_comp_telhado.setSuffix(" m")

        layout_aba_telhado.addWidget(self.lbl_larg_telhado)
        layout_aba_telhado.addWidget(self.input_larg_telhado)
        layout_aba_telhado.addSpacing(10)
        layout_aba_telhado.addWidget(self.lbl_comp_telhado)
        layout_aba_telhado.addWidget(self.input_comp_telhado)
        layout_aba_telhado.addStretch(1)

        # === MENU 2: Opções de Painéis ===
        self.aba_paineis = QtWidgets.QWidget()
        layout_aba_paineis = QtWidgets.QHBoxLayout(self.aba_paineis)
        layout_aba_paineis.setContentsMargins(14, 6, 14, 6)
        layout_aba_paineis.setSpacing(12)

        self.lbl_larg_painel = QtWidgets.QLabel("Largura (m):")
        self.input_larg_painel = DoubleSpinBoxDecimalPonto()
        self.input_larg_painel.setDecimals(self.casas_decimais)
        self.input_larg_painel.setRange(0.01, 50.0)
        self.input_larg_painel.setSingleStep(0.01)
        self.input_larg_painel.setValue(1.134)
        self.input_larg_painel.setSuffix(" m")

        self.lbl_comp_painel = QtWidgets.QLabel("Comprimento (m):")
        self.input_comp_painel = DoubleSpinBoxDecimalPonto()
        self.input_comp_painel.setDecimals(self.casas_decimais)
        self.input_comp_painel.setRange(0.01, 50.0)
        self.input_comp_painel.setSingleStep(0.01)
        self.input_comp_painel.setValue(2.382)
        self.input_comp_painel.setSuffix(" m")

        layout_aba_paineis.addWidget(self.lbl_larg_painel)
        layout_aba_paineis.addWidget(self.input_larg_painel)
        layout_aba_paineis.addSpacing(10)
        layout_aba_paineis.addWidget(self.lbl_comp_painel)
        layout_aba_paineis.addWidget(self.input_comp_painel)
        layout_aba_paineis.addStretch(1)

        # === MENU 3: Configuração de Alocação ===
        self.aba_alocacao = QtWidgets.QWidget()
        layout_aba_alocacao = QtWidgets.QHBoxLayout(self.aba_alocacao)
        layout_aba_alocacao.setContentsMargins(14, 6, 14, 6)
        layout_aba_alocacao.setSpacing(10)

        self.lbl_espacamento = QtWidgets.QLabel("Entre painéis (m):")
        self.lbl_espacamento.setToolTip("Espaçamento livre entre painéis adjacentes")
        self.input_espacamento = DoubleSpinBoxDecimalPonto()
        self.input_espacamento.setDecimals(self.casas_decimais)
        self.input_espacamento.setRange(0.0, 10.0)
        self.input_espacamento.setSingleStep(0.01)
        self.input_espacamento.setValue(0.05)
        self.input_espacamento.setSuffix(" m")
        self.input_espacamento.setToolTip("Espaçamento livre entre painéis adjacentes")

        self.lbl_borda = QtWidgets.QLabel("Bordas (m):")
        self.lbl_borda.setToolTip("Recuo de segurança nas bordas do telhado")
        self.input_dist_borda = DoubleSpinBoxDecimalPonto()
        self.input_dist_borda.setDecimals(self.casas_decimais)
        self.input_dist_borda.setRange(0.0, 50.0)
        self.input_dist_borda.setSingleStep(0.05)
        self.input_dist_borda.setValue(0.50)
        self.input_dist_borda.setSuffix(" m")
        self.input_dist_borda.setToolTip("Recuo de segurança nas bordas do telhado")

        self.lbl_quina = QtWidgets.QLabel("Quinas (m):")
        self.lbl_quina.setToolTip("Afastamento euclidiano de segurança nas 4 quinas do telhado")
        self.input_dist_quina = DoubleSpinBoxDecimalPonto()
        self.input_dist_quina.setDecimals(self.casas_decimais)
        self.input_dist_quina.setRange(0.0, 50.0)
        self.input_dist_quina.setSingleStep(0.10)
        self.input_dist_quina.setValue(1.00)
        self.input_dist_quina.setSuffix(" m")
        self.input_dist_quina.setToolTip("Afastamento euclidiano de segurança nas 4 quinas do telhado")

        layout_aba_alocacao.addWidget(self.lbl_espacamento)
        layout_aba_alocacao.addWidget(self.input_espacamento)
        layout_aba_alocacao.addWidget(self.lbl_borda)
        layout_aba_alocacao.addWidget(self.input_dist_borda)
        layout_aba_alocacao.addWidget(self.lbl_quina)
        layout_aba_alocacao.addWidget(self.input_dist_quina)

        self.check_area_util_aloc = QtWidgets.QCheckBox("Mostrar delimitação da área útil")
        self.check_area_util_aloc.setChecked(self.mostrar_area_util)
        self.check_area_util_aloc.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.check_area_util_aloc.setToolTip(
            "Exibe ou oculta a linha tracejada, os arcos das quinas e o sombreamento da área útil"
        )
        self.check_area_util_aloc.toggled.connect(self.ao_alternar_mostrar_area_util)
        layout_aba_alocacao.addSpacing(10)
        layout_aba_alocacao.addWidget(self.check_area_util_aloc)
        layout_aba_alocacao.addStretch(1)

        # === MENU 4: Configurações Gerais (Material do Telhado, Unidade de Medida e Casas Decimais) ===
        self.aba_configuracoes = QtWidgets.QWidget()
        layout_aba_config = QtWidgets.QHBoxLayout(self.aba_configuracoes)
        layout_aba_config.setContentsMargins(14, 6, 14, 6)
        layout_aba_config.setSpacing(10)

        self.lbl_material = QtWidgets.QLabel("Material do telhado:")
        self.lbl_material.setToolTip("Altera a cor e a textura visual que representam o material do telhado")

        self.combo_material = QtWidgets.QComboBox()
        self.combo_material.addItems(list(MATERIAIS_TELHADO.keys()))
        self.combo_material.setCurrentText(self.material_telhado_atual)
        self.combo_material.currentTextChanged.connect(self.ao_mudar_material_telhado)

        self.lbl_unidade = QtWidgets.QLabel("Unidade:")
        self.lbl_unidade.setToolTip("Define a unidade de comprimento para dimensões e gráficos")

        self.combo_unidade = QtWidgets.QComboBox()
        self.combo_unidade.addItems(list(UNIDADES.keys()))
        self.combo_unidade.setCurrentText(self.unidade_atual)
        self.combo_unidade.currentTextChanged.connect(self.ao_mudar_unidade)

        self.lbl_casas = QtWidgets.QLabel("Casas decimais (0-5):")
        self.lbl_casas.setToolTip("Número de casas decimais após a vírgula (ajustado automaticamente entre 0 e 5)")

        self.spin_casas_decimais = SpinBoxCasasDecimais()
        self.spin_casas_decimais.setFixedWidth(96)
        self.spin_casas_decimais.setValue(self.casas_decimais)
        self.spin_casas_decimais.setToolTip(
            "Delimitado entre 0 e 5. Números quebrados ou fora da faixa são ajustados automaticamente para o mais próximo permitido."
        )
        self.spin_casas_decimais.valueChanged.connect(self.ao_mudar_casas_decimais)

        self.check_area_util_cfg = QtWidgets.QCheckBox("Mostrar delimitação da área útil")
        self.check_area_util_cfg.setChecked(self.mostrar_area_util)
        self.check_area_util_cfg.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.check_area_util_cfg.setToolTip(
            "Exibe ou oculta a linha tracejada, os arcos das quinas e o sombreamento da área útil"
        )
        self.check_area_util_cfg.toggled.connect(self.ao_alternar_mostrar_area_util)

        layout_aba_config.addWidget(self.lbl_material)
        layout_aba_config.addWidget(self.combo_material)
        layout_aba_config.addSpacing(14)
        layout_aba_config.addWidget(self.lbl_unidade)
        layout_aba_config.addWidget(self.combo_unidade)
        layout_aba_config.addSpacing(14)
        layout_aba_config.addWidget(self.lbl_casas)
        layout_aba_config.addWidget(self.spin_casas_decimais)
        layout_aba_config.addSpacing(14)
        layout_aba_config.addWidget(self.check_area_util_cfg)
        layout_aba_config.addStretch(1)

        # Adiciona as abas ao QTabWidget
        self.abas_configuracao.addTab(self.aba_telhado, "Opções de telhado")
        self.abas_configuracao.addTab(self.aba_paineis, "Opções de painéis")
        self.abas_configuracao.addTab(self.aba_alocacao, "Configuração de alocação")
        self.abas_configuracao.addTab(self.aba_configuracoes, "Configurações")

        # Insere o botão de play verde à esquerda e as abas ao lado
        layout_controles.addWidget(
            self.botao_calcular, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        layout_controles.addWidget(self.abas_configuracao, stretch=1)

        layout_simplificado.addLayout(layout_controles)

        # --- 3. CAIXA DO GRÁFICO (CANVAS INTEGRADO) ---
        self.caixa_plot = QtWidgets.QGroupBox()
        layout_plot = QtWidgets.QVBoxLayout()
        layout_plot.setContentsMargins(8, 8, 8, 8)
        self.canvas = CanvasJanela()
        layout_plot.addWidget(self.canvas)
        self.caixa_plot.setLayout(layout_plot)

        layout_simplificado.addWidget(self.caixa_plot, stretch=1)

        self.tela_modo_simplificado.setLayout(layout_simplificado)

    def ao_mudar_material_telhado(self, novo_material: str):
        """Atualiza o material do telhado e re-renderiza o gráfico com a nova textura/cor."""
        if novo_material == self.material_telhado_atual or novo_material not in MATERIAIS_TELHADO:
            return
        self.material_telhado_atual = novo_material
        self.replotar_resultado_atual()

    def ao_alternar_mostrar_area_util(self, ativo: bool):
        """Sincroniza a exibição das bordas da área útil e atualiza o gráfico em tempo real."""
        self.mostrar_area_util = bool(ativo)
        for chk in [self.check_area_util_aloc, self.check_area_util_cfg]:
            if chk.isChecked() != self.mostrar_area_util:
                chk.blockSignals(True)
                chk.setChecked(self.mostrar_area_util)
                chk.blockSignals(False)
        self.replotar_resultado_atual()

    def ao_mudar_casas_decimais(self, novas_casas: int):
        """Atualiza o número de casas decimais em todos os campos numéricos da interface."""
        self.casas_decimais = int(novas_casas)
        campos = [
            self.input_larg_telhado,
            self.input_comp_telhado,
            self.input_larg_painel,
            self.input_comp_painel,
            self.input_espacamento,
            self.input_dist_borda,
            self.input_dist_quina,
        ]
        for spin in campos:
            spin.blockSignals(True)
            spin.setDecimals(self.casas_decimais)
            spin.blockSignals(False)

    def ao_mudar_unidade(self, nova_unidade_nome: str):
        """Converte automaticamente os valores dos campos e a interface para a nova unidade."""
        if nova_unidade_nome == self.unidade_atual or nova_unidade_nome not in UNIDADES:
            return

        unidade_antiga = self.unidade_atual
        self.unidade_atual = nova_unidade_nome

        dados_antiga = UNIDADES[unidade_antiga]
        dados_nova = UNIDADES[nova_unidade_nome]

        # Fator de conversão entre unidades
        fator_conversao = dados_antiga["para_m"] * dados_nova["de_m"]
        sigla = dados_nova["sigla"]

        # 1. Atualiza labels de cada campo
        self.lbl_larg_telhado.setText(f"Largura ({sigla}):")
        self.lbl_comp_telhado.setText(f"Comprimento ({sigla}):")
        self.lbl_larg_painel.setText(f"Largura ({sigla}):")
        self.lbl_comp_painel.setText(f"Comprimento ({sigla}):")
        self.lbl_espacamento.setText(f"Entre painéis ({sigla}):")
        self.lbl_borda.setText(f"Bordas ({sigla}):")
        self.lbl_quina.setText(f"Quinas ({sigla}):")

        # 2. Converte os valores e ajusta as propriedades dos seletores
        campos = [
            (self.input_larg_telhado, 0.5, 2000.0, dados_nova["passo_tel"]),
            (self.input_comp_telhado, 0.5, 2000.0, dados_nova["passo_tel"]),
            (self.input_larg_painel, 0.01, 50.0, dados_nova["passo_mod"]),
            (self.input_comp_painel, 0.01, 50.0, dados_nova["passo_mod"]),
            (self.input_espacamento, 0.0, 10.0, dados_nova["passo_mod"]),
            (self.input_dist_borda, 0.0, 50.0, dados_nova["passo_mod"]),
            (self.input_dist_quina, 0.0, 50.0, dados_nova["passo_mod"]),
        ]

        for spin, min_m, max_m, passo in campos:
            val_atual = spin.value()
            novo_val = val_atual * fator_conversao
            spin.blockSignals(True)
            spin.setDecimals(self.casas_decimais)
            spin.setRange(min_m * dados_nova["de_m"], max_m * dados_nova["de_m"])
            spin.setSingleStep(passo)
            spin.setValue(novo_val)
            spin.setSuffix(f" {sigla}")
            spin.blockSignals(False)

        # 3. Atualiza o gráfico com a nova unidade
        self.replotar_resultado_atual()

    def executar_dimensionamento(self):
        """Lê os parâmetros de entrada, chama o algoritmo de alocação e atualiza o gráfico."""
        try:
            dados_u = UNIDADES.get(self.unidade_atual, UNIDADES["Metros (m)"])
            para_m = dados_u["para_m"]

            def sanitizar_float(spin):
                txt = str(spin.value()).replace(",", ".").strip()
                return float(txt)

            # Converte as entradas do usuário para a unidade física padrão (Metros)
            w_tel = sanitizar_float(self.input_larg_telhado) * para_m
            l_tel = sanitizar_float(self.input_comp_telhado) * para_m
            w_placa = sanitizar_float(self.input_larg_painel) * para_m
            l_placa = sanitizar_float(self.input_comp_painel) * para_m
            espacamento = sanitizar_float(self.input_espacamento) * para_m
            borda = sanitizar_float(self.input_dist_borda) * para_m
            dist_quina = sanitizar_float(self.input_dist_quina) * para_m

            df_retrato = aloc.dimensionar(
                w_telhado=w_tel,
                l_telhado=l_tel,
                w_placa=w_placa,
                l_placa=l_placa,
                borda=borda,
                espacamento=espacamento,
                dist_quina=dist_quina,
            )
            df_paisagem = aloc.dimensionar(
                w_telhado=w_tel,
                l_telhado=l_tel,
                w_placa=l_placa,
                l_placa=w_placa,
                borda=borda,
                espacamento=espacamento,
                dist_quina=dist_quina,
            )

            # Salva o último resultado em metros (unidade física de referência)
            self.ultimo_df_retrato = df_retrato
            self.ultimo_df_paisagem = df_paisagem
            self.ultimo_w_tel = w_tel
            self.ultimo_l_tel = l_tel
            self.ultimo_borda = borda
            self.ultimo_dist_quina = dist_quina

            self.canvas.atualizar_grafico(
                df_retrato=df_retrato,
                df_paisagem=df_paisagem,
                w_tel=w_tel,
                l_tel=l_tel,
                borda=borda,
                dist_quina=dist_quina,
                material=self.material_telhado_atual,
                tema_escuro=self.tema_escuro,
                unidade=self.unidade_atual,
                mostrar_area_util=self.mostrar_area_util,
            )
        except Exception as e:
            print(f"Erro ao dimensionar arranjo: {e}")

    def aplicar_tema(self, escuro: bool):
        """Aplica o tema Claro ou Escuro em todos os elementos da interface conforme as paletas."""
        self.tema_escuro = escuro
        paleta = PALETAS["escuro" if escuro else "claro"]

        if escuro:
            self.botao_tema.setIcon(criar_icone_sol(paleta["cor_icone_tema"]))
            self.botao_tema.setToolTip("Mudar para modo claro")
        else:
            self.botao_tema.setIcon(criar_icone_lua(paleta["cor_icone_tema"]))
            self.botao_tema.setToolTip("Mudar para modo escuro")

        caminho_seta_cima = obter_caminho_seta(True, escuro)
        caminho_seta_baixo = obter_caminho_seta(False, escuro)

        # 1. Telas de Fundo
        estilo_fundo = f"background-color: {paleta['bg_janela']};"
        self.tela_inicial.setStyleSheet(estilo_fundo)
        self.tela_novo_projeto.setStyleSheet(estilo_fundo)
        self.tela_modo_simplificado.setStyleSheet(estilo_fundo)

        # 2. Textos e Títulos
        self.titulo_inicio.setStyleSheet(
            f"color: {paleta['cor_titulo']}; font-family: 'Arial'; font-size: 26px; font-weight: bold;"
        )
        self.instrucao_inicio.setStyleSheet(
            f"color: {paleta['cor_subtexto']}; font-family: 'Arial'; font-size: 14px;"
        )
        self.titulo_modo.setStyleSheet(
            f"color: {paleta['cor_titulo']}; font-family: 'Arial'; font-size: 24px; font-weight: bold;"
        )
        self.instrucao_modo.setStyleSheet(
            f"color: {paleta['cor_subtexto']}; font-family: 'Arial'; font-size: 14px;"
        )

        # 3. Botões Primários
        estilo_botoes_prim = f"""
            QPushButton {{
                background-color: {paleta['bg_botao_prim']}; color: white; font-size: 15px; font-weight: bold;
                border-radius: 10px; padding: 10px; border: none;
            }}
            QPushButton:hover {{ background-color: {paleta['bg_botao_prim_hover']}; }}
        """
        self.botao_criar.setStyleSheet(estilo_botoes_prim)
        self.botao_abrir.setStyleSheet(estilo_botoes_prim)
        self.botao_modo_simp.setStyleSheet(estilo_botoes_prim)
        self.botao_modo_avan.setStyleSheet(estilo_botoes_prim)

        # 4. Botões Voltar
        estilo_voltar = f"""
            QPushButton {{
                background-color: {paleta['bg_botao_voltar']}; color: {paleta['cor_botao_voltar']};
                font-weight: bold; border-radius: 6px; border: 1px solid {paleta['borda_card']};
            }}
            QPushButton:hover {{ background-color: {paleta['bg_botao_voltar_hover']}; }}
        """
        self.botao_voltar_modo.setStyleSheet(estilo_voltar)
        self.botao_voltar_simp.setStyleSheet(estilo_voltar)

        # 5. Botão Sair
        self.botao_sair.setStyleSheet(f"""
            QPushButton {{
                background-color: {paleta['bg_botao_sair']}; color: {paleta['cor_botao_sair']};
                font-weight: bold; border-radius: 6px; border: none;
            }}
            QPushButton:hover {{ background-color: {paleta['bg_botao_sair_hover']}; }}
        """)

        # 6. Botão de Alternância de Tema
        self.botao_tema.setStyleSheet(f"""
            QPushButton {{
                background-color: {paleta['bg_botao_tema']};
                border: 1px solid {paleta['borda_botao_tema']};
                border-radius: 20px;
                padding: 4px;
            }}
            QPushButton:hover {{
                background-color: {paleta['bg_botao_tema_hover']};
            }}
        """)

        # 7. Botão Realizar Alocação (Verde, à esquerda)
        self.botao_calcular.setStyleSheet(f"""
            QPushButton#botao_calcular {{
                background-color: {paleta['bg_botao_calc']};
                color: {paleta['cor_card_texto']};
                font-weight: bold;
                font-size: 14px;
                border: 2px solid {paleta['borda_botao_calc']};
                border-radius: 8px;
                padding: 8px 14px;
            }}
            QPushButton#botao_calcular:hover {{
                background-color: {paleta['bg_botao_calc_hover']};
            }}
            QPushButton#botao_calcular:pressed {{
                background-color: {paleta['borda_botao_calc']};
                color: white;
            }}
        """)

        # 8. Abas Superiores (QTabWidget)
        estilo_abas = f"""
            QTabWidget::pane {{
                border: 1px solid {paleta['borda_card']};
                border-radius: 8px;
                background-color: {paleta['bg_card']};
                top: -1px;
            }}
            QTabBar::tab {{
                background-color: {paleta['bg_tab']};
                color: {paleta['cor_tab']};
                font-weight: bold;
                font-size: 13px;
                padding: 6px 14px;
                border: 1px solid {paleta['borda_card']};
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 4px;
            }}
            QTabBar::tab:selected {{
                background-color: {paleta['bg_card']};
                color: {paleta['cor_tab_selected']};
                border-bottom: 2px solid {paleta['cor_tab_selected']};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {paleta['bg_card']};
                color: {paleta['cor_card_texto']};
            }}
            QTabWidget QWidget {{
                background-color: transparent;
            }}
            QTabWidget QLabel {{
                background-color: transparent;
                color: {paleta['cor_card_texto']};
                font-size: 12px;
                font-weight: bold;
            }}
        """
        self.abas_configuracao.setStyleSheet(estilo_abas)

        # 9. Seletores Numéricos (QDoubleSpinBox e QSpinBox)
        estilo_spinboxes = f"""
            QDoubleSpinBox, QSpinBox {{
                background-color: {paleta['bg_input']};
                color: {paleta['cor_input_texto']};
                border: 1px solid {paleta['borda_input']};
                border-radius: 6px;
                padding-left: 6px;
                padding-right: 26px;
                min-height: 26px;
                font-size: 12px;
                font-weight: bold;
            }}
            QDoubleSpinBox:focus, QSpinBox:focus {{
                border: 1.5px solid {paleta['cor_titulo']};
            }}
            QDoubleSpinBox::up-button, QSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 22px;
                border-left: 1px solid {paleta['borda_input']};
                border-bottom: 1px solid {paleta['borda_input']};
                border-top-right-radius: 5px;
                background-color: {paleta['bg_spin_btn']};
            }}
            QDoubleSpinBox::up-button:hover, QSpinBox::up-button:hover {{
                background-color: {paleta['bg_spin_btn_hover']};
            }}
            QDoubleSpinBox::up-button:pressed, QSpinBox::up-button:pressed {{
                background-color: {paleta['bg_spin_btn_pressed']};
            }}
            QDoubleSpinBox::up-arrow, QSpinBox::up-arrow {{
                image: url("{caminho_seta_cima}");
                width: 9px;
                height: 6px;
            }}
            QDoubleSpinBox::down-button, QSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 22px;
                border-left: 1px solid {paleta['borda_input']};
                border-bottom-right-radius: 5px;
                background-color: {paleta['bg_spin_btn']};
            }}
            QDoubleSpinBox::down-button:hover, QSpinBox::down-button:hover {{
                background-color: {paleta['bg_spin_btn_hover']};
            }}
            QDoubleSpinBox::down-button:pressed, QSpinBox::down-button:pressed {{
                background-color: {paleta['bg_spin_btn_pressed']};
            }}
            QDoubleSpinBox::down-arrow, QSpinBox::down-arrow {{
                image: url("{caminho_seta_baixo}");
                width: 9px;
                height: 6px;
            }}
        """
        self.input_larg_telhado.setStyleSheet(estilo_spinboxes)
        self.input_comp_telhado.setStyleSheet(estilo_spinboxes)
        self.input_larg_painel.setStyleSheet(estilo_spinboxes)
        self.input_comp_painel.setStyleSheet(estilo_spinboxes)
        self.input_espacamento.setStyleSheet(estilo_spinboxes)
        self.input_dist_borda.setStyleSheet(estilo_spinboxes)
        self.input_dist_quina.setStyleSheet(estilo_spinboxes)
        self.spin_casas_decimais.setStyleSheet(estilo_spinboxes)

        # 10. Seletor de Unidades e Material (QComboBox)
        estilo_combobox = f"""
            QComboBox {{
                background-color: {paleta['bg_input']};
                color: {paleta['cor_input_texto']};
                border: 1px solid {paleta['borda_input']};
                border-radius: 6px;
                padding-left: 8px;
                padding-right: 26px;
                min-height: 26px;
                min-width: 130px;
                font-size: 12px;
                font-weight: bold;
            }}
            QComboBox:focus {{
                border: 1.5px solid {paleta['cor_titulo']};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 22px;
                border-left: 1px solid {paleta['borda_input']};
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                background-color: {paleta['bg_spin_btn']};
            }}
            QComboBox::down-arrow {{
                image: url("{caminho_seta_baixo}");
                width: 9px;
                height: 6px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {paleta['bg_card']};
                color: {paleta['cor_card_texto']};
                border: 1px solid {paleta['borda_card']};
                selection-background-color: {paleta['bg_botao_prim']};
                selection-color: white;
            }}
        """
        self.combo_unidade.setStyleSheet(estilo_combobox)
        self.combo_material.setStyleSheet(estilo_combobox)

        # 11. Caixa do Gráfico
        self.caixa_plot.setStyleSheet(f"""
            QGroupBox {{
                border-radius: 8px;
                margin-top: 2px;
                background-color: {paleta['bg_plot']};
                border: 1px solid {paleta['borda_plot']};
            }}
        """)

        # 12. Caixas de Seleção (QCheckBox)
        caminho_check = obter_caminho_check()
        estilo_checkbox = f"""
            QCheckBox {{
                color: {paleta['cor_card_texto']};
                font-size: 12px;
                font-weight: bold;
                spacing: 6px;
                background-color: transparent;
            }}
            QCheckBox::indicator {{
                width: 17px;
                height: 17px;
                border: 1px solid {paleta['borda_input']};
                border-radius: 4px;
                background-color: {paleta['bg_input']};
            }}
            QCheckBox::indicator:hover {{
                border: 1.5px solid {paleta['cor_titulo']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {paleta['bg_botao_prim']};
                border: 1px solid {paleta['bg_botao_prim']};
                image: url("{caminho_check}");
            }}
        """
        self.check_area_util_aloc.setStyleSheet(estilo_checkbox)
        self.check_area_util_cfg.setStyleSheet(estilo_checkbox)


def main():
    """Ponto de entrada para inicialização da aplicação Qt."""
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
