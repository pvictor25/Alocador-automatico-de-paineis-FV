import sys
import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtCore as QtCore

class MainWindow(QtWidgets.QMainWindow):


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Alocador automático de Painéis Fotovoltaicos")
        self.setMinimumSize(QtCore.QSize(600, 400))

        # 1. CRIAR O GERENCIADOR DE TELAS (STACKED WIDGET)
        self.telas = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.telas)

        # 2. CONSTRUIR AS TELAS
        self.criar_tela_inicial()
        self.criar_tela_novo_projeto()
        self.criar_tela_modo_simplificado()

        # 3. ADICIONAR AS TELAS AO GERENCIADOR
        # Tela Inicial será o índice 0, Tela de Novo Projeto será o índice 1
        self.telas.addWidget(self.tela_inicial)
        self.telas.addWidget(self.tela_novo_projeto)
        self.telas.addWidget(self.tela_modo_simplificado)


    def criar_tela_inicial(self):
        """Monta a primeira tela (Menu Inicial)"""
        self.tela_inicial = QtWidgets.QWidget()
        self.tela_inicial.setStyleSheet("background-color: #f1edda;")

        # Componentes de texto
        self.titulo_inicio = QtWidgets.QLabel("Bem-vindo ao Alocador de Painéis!")
        self.instrucao_inicio = QtWidgets.QLabel("Inicie um novo projeto ou abra um arquivo existente para começar.")

        self.titulo_inicio.setStyleSheet("QLabel { color: #4d85ef; font-family: 'Arial'; font-size: 26px; font-weight: bold; }")
        self.instrucao_inicio.setStyleSheet("QLabel { color: #04132f; font-family: 'Arial'; font-size: 14px; }")
        self.titulo_inicio.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.instrucao_inicio.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Botões
        self.botao_criar = QtWidgets.QPushButton("Criar novo projeto")
        self.botao_abrir = QtWidgets.QPushButton("Abrir projeto existente")
        self.botao_criar.setFixedSize(200, 80) 
        self.botao_abrir.setFixedSize(200, 80) 

        # Estilização dos botões
        estilo_botoes_inicio = """
            QPushButton {
                background-color: #4d85ef; color: white; font-size: 16px; font-weight: bold;
                border-radius: 10px; padding: 10px;
            }
            QPushButton:hover { background-color: #3172ec; }
        """
        self.botao_criar.setStyleSheet(estilo_botoes_inicio)
        self.botao_abrir.setStyleSheet(estilo_botoes_inicio)

        botao_sair = QtWidgets.QPushButton("Sair do Programa")
        botao_sair.setFixedSize(120, 30)
        botao_sair.setStyleSheet("""
            QPushButton { background-color: #fe9e9a; color: #04132f; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #fe554d; }
        """)

        # CONEXÃO DO BOTÃO
        self.botao_criar.clicked.connect(lambda: self.telas.setCurrentIndex(1))

        botao_sair.clicked.connect(QtWidgets.QApplication.instance().quit)

        # Organização dos Layouts da Tela Inicial
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

        layout_principal.addWidget(botao_sair, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_principal.addStretch(1)

        self.tela_inicial.setLayout(layout_principal)


    def criar_tela_novo_projeto(self):
        """Monta a segunda tela (Formulário / Configuração do Projeto)"""
        self.tela_novo_projeto = QtWidgets.QWidget()
        self.tela_novo_projeto.setStyleSheet("background-color: #f1edda;")
        
        # Componentes de texto
        self.titulo_modo = QtWidgets.QLabel("Selecione o modo de criação do projeto")
        self.instrucao_modo = QtWidgets.QLabel("O modo simplificado realiza o dimensionamento a partir de um retângulo, já o modo avançado realiza o dimensionamento a partir de geometrias complexas.")

        self.titulo_modo.setStyleSheet("QLabel { color: #4d85ef; font-family: 'Arial'; font-size: 24px; font-weight: bold; }")
        self.instrucao_modo.setStyleSheet("QLabel { color: #04132f; font-family: 'Arial'; font-size: 14px; }")
        self.titulo_modo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.instrucao_modo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.instrucao_modo.setWordWrap(True)

        # Botões
        self.botao_modo_simp = QtWidgets.QPushButton("Modo simplificado")
        self.botao_modo_avan = QtWidgets.QPushButton("Modo avançado")
        self.botao_modo_simp.setFixedSize(200, 80) 
        self.botao_modo_avan.setFixedSize(200, 80) 

        # Estilização dos botões
        estilo_botoes_modo = """
            QPushButton {
                background-color: #4d85ef; color: white; font-size: 16px; font-weight: bold;
                border-radius: 10px; padding: 10px;
            }
            QPushButton:hover { background-color: #3172ec; }
        """
        self.botao_modo_simp.setStyleSheet(estilo_botoes_modo)
        self.botao_modo_avan.setStyleSheet(estilo_botoes_modo)

        # Botão para voltar 
        botao_voltar = QtWidgets.QPushButton("← Voltar")
        botao_voltar.setFixedSize(60, 30)
        botao_voltar.setStyleSheet("""
            QPushButton { background-color: #e4ddb9; color: #04132f; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #eec7ba; }
        """)
        
        # CONEXÃO DO BOTÃO VOLTAR: Mudar de volta para o índice 0
        botao_voltar.clicked.connect(lambda: self.telas.setCurrentIndex(0))
        # CONEXÃO DO BOTÃO AVANÇAR: Mudar para o índice 2
        self.botao_modo_simp.clicked.connect(lambda: self.telas.setCurrentIndex(2))

        layout_modo = QtWidgets.QVBoxLayout()

        # Organização dos Layouts da Tela Inicial
        layout_modo.addWidget(
            botao_voltar, alignment=QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
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
        self.tela_modo_simplificado = QtWidgets.QWidget()
        self.tela_modo_simplificado.setStyleSheet("background-color: #f1edda;")

        layout_simplificado = QtWidgets.QVBoxLayout()

        # Botão para voltar 
        botao_voltar = QtWidgets.QPushButton("← Voltar")
        botao_voltar.setFixedSize(60, 30)
        botao_voltar.setStyleSheet("""
            QPushButton { background-color: #e4ddb9; color: #04132f; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #eec7ba; }
        """)
        
        # CONEXÃO DO BOTÃO VOLTAR
        botao_voltar.clicked.connect(lambda: self.telas.setCurrentIndex(1))

        # Estilo das Caixas com Borda Sutil
        estilo_caixas = """
            QGroupBox {
                border-radius: 8px;
                margin-top: 15px;
                font-weight: bold;
                font-size: 14px;
                color: #04132f;
                background-color: #d6c770;  
                border: 1px solid #bfae7a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                left: 10px;
            }
            QGroupBox QLabel {
                background-color: transparent;
            }
        """

        # --- 1. CONFIGURAÇÃO DA CAIXA DO TELHADO ---
        caixa_dim_telhado = QtWidgets.QGroupBox()
        caixa_dim_telhado.setStyleSheet(estilo_caixas)
        lbl_telhado = QtWidgets.QLabel("Dimensões do telhado (m)")
        lbl_telhado.setStyleSheet("color: #04132f; font-weight: bold;")
        
        # Layout interno da caixa do telhado
        layout_interno_telhado = QtWidgets.QVBoxLayout()
        layout_interno_telhado.setContentsMargins(5, 5, 5, 5) # Margem interna para o texto não colar na borda
        layout_interno_telhado.addWidget(lbl_telhado)
        
        # Vincula o layout à caixa do telhado
        caixa_dim_telhado.setLayout(layout_interno_telhado)


        # --- 2. CONFIGURAÇÃO DA CAIXA DOS PAINÉIS ---
        caixa_dim_paineis = QtWidgets.QGroupBox()
        caixa_dim_paineis.setStyleSheet(estilo_caixas)
        lbl_paineis = QtWidgets.QLabel("Dimensões dos painéis (m)")
        lbl_paineis.setStyleSheet("color: #04132f; font-weight: bold;")
        
        # Layout interno da caixa dos painéis
        layout_interno_paineis = QtWidgets.QVBoxLayout()
        layout_interno_paineis.setContentsMargins(5, 5, 5, 5)
        layout_interno_paineis.addWidget(lbl_paineis)
        
        # Vincula o layout à caixa dos painéis
        caixa_dim_paineis.setLayout(layout_interno_paineis)


        # --- 3. CONFIGURAÇÃO DA CAIXA DO GRÁFICO (PLOT) ---
        caixa_plot = QtWidgets.QGroupBox()
        caixa_plot.setStyleSheet("""
            QGroupBox {
                border-radius: 8px;
                margin-top: 15px;
                font-weight: bold;
                font-size: 14px;
                color: #04132f;
                background-color: #ffffff;
                border: 1px solid #cbd5e1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                left: 10px;
            }
        """)

        # --- 4. MONTAGEM DO LAYOUT DA TELA ---
        # Botão voltar no topo esquerdo
        layout_simplificado.addWidget(
            botao_voltar, alignment=QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        layout_simplificado.addSpacing(10)

        # Coloca as duas caixas estruturadas lado a lado
        layout_caixas = QtWidgets.QHBoxLayout()
        layout_caixas.addWidget(caixa_dim_telhado)
        layout_caixas.addWidget(caixa_dim_paineis)

        # Junta tudo no layout principal vertical da tela
        layout_simplificado.addLayout(layout_caixas)
        layout_simplificado.addWidget(caixa_plot, stretch=1) # stretch=1 faz a área do gráfico expandir no espaço que sobrar

        self.tela_modo_simplificado.setLayout(layout_simplificado)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()