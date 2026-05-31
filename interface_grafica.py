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

        # 3. ADICIONAR AS TELAS AO GERENCIADOR
        # Tela Inicial será o índice 0, Tela de Novo Projeto será o índice 1
        self.telas.addWidget(self.tela_inicial)
        self.telas.addWidget(self.tela_novo_projeto)

    def criar_tela_inicial(self):
        """Monta a primeira tela (Menu Inicial)"""
        self.tela_inicial = QtWidgets.QWidget()
        self.tela_inicial.setStyleSheet("background-color: #f1edda;")

        # Componentes de texto
        self.titulo_inicio = QtWidgets.QLabel("Bem-vindo ao Alocador de Painéis!")
        self.instrucao_inicio = QtWidgets.QLabel("Inicie um novo projeto ou abra um arquivo existente para começar.")

        self.titulo_inicio.setStyleSheet("QLabel { color: #4d85ef; font-family: 'Arial'; font-size: 22px; font-weight: bold; }")
        self.instrucao_inicio.setStyleSheet("QLabel { color: #04132f; font-family: 'Arial'; font-size: 12px; font-weight: bold; }")
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

        # CONEXÃO DO BOTÃO: Mudar para a tela de índice 1
        self.botao_criar.clicked.connect(lambda: self.telas.setCurrentIndex(1))

        # Organização dos Layouts da Tela Inicial
        layout_principal = QtWidgets.QVBoxLayout()
        layout_principal.addStretch(2)
        layout_principal.addWidget(self.titulo_inicio)
        layout_principal.addWidget(self.instrucao_inicio)
        layout_principal.addSpacing(15)
        
        layout_botoes = QtWidgets.QHBoxLayout()
        layout_botoes.addWidget(self.botao_criar)
        layout_botoes.addWidget(self.botao_abrir)
        layout_principal.addLayout(layout_botoes)
        
        layout_principal.addStretch(2)
        self.tela_inicial.setLayout(layout_principal)

    def criar_tela_novo_projeto(self):
        """Monta a segunda tela (Formulário / Configuração do Projeto)"""
        self.tela_novo_projeto = QtWidgets.QWidget()
        self.tela_novo_projeto.setStyleSheet("background-color: #f1edda;")

        layout_modo = QtWidgets.QVBoxLayout()
        
        # Componentes de texto
        self.titulo_modo = QtWidgets.QLabel("Selecione o modo de criação do projeto")
        self.instrucao_modo = QtWidgets.QLabel("O modo simplificado realiza o dimensionamento a partir de um retângulo, \njá o modo avançado realiza o dimensionamento a partir de geometrias complexas.")

        self.titulo_modo.setStyleSheet("QLabel { color: #4d85ef; font-family: 'Arial'; font-size: 22px; font-weight: bold; }")
        self.instrucao_modo.setStyleSheet("QLabel { color: #04132f; font-family: 'Arial'; font-size: 12px; }")
        self.titulo_modo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.instrucao_modo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

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

        # Botão para voltar à tela inicial caso o usuário queira
        botao_voltar = QtWidgets.QPushButton("← Voltar")
        botao_voltar.setFixedSize(60, 30)
        botao_voltar.setStyleSheet("""
            QPushButton { background-color: #e4ddb9; color: #04132f; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #eec7ba; }
        """)
        
        # CONEXÃO DO BOTÃO VOLTAR: Mudar de volta para o índice 0
        botao_voltar.clicked.connect(lambda: self.telas.setCurrentIndex(0))
        # CONEXÃO DO BOTÃO AVANÇAR: Mudar para o índice 2
        self.botao_modo_simp.clicked.connect(lambda: self.telas.setCurrentIndex(0))

        # Adicionando componentes no layout da segunda tela
        layout_modo.addWidget(self.titulo_modo)
        layout_modo.addWidget(self.instrucao_modo)

        # Organização dos Layouts da Tela Inicial
        layout_modo = QtWidgets.QVBoxLayout()
        layout_modo.addStretch(1)
        layout_modo.addWidget(self.titulo_modo)
        layout_modo.addWidget(self.instrucao_modo)
        layout_modo.addSpacing(15)

        layout_botoes_modo = QtWidgets.QHBoxLayout()
        layout_botoes_modo.addWidget(self.botao_modo_simp)
        layout_botoes_modo.addWidget(self.botao_modo_avan)
        layout_modo.addLayout(layout_botoes_modo)

        
        #layout_modo.addSpacing(30)
        
        # Aqui você poderá futuramente colocar seus inputs de dimensionamento...
        layout_modo.addStretch(1) 
        
        layout_modo.addWidget(botao_voltar, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tela_novo_projeto.setLayout(layout_modo)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()