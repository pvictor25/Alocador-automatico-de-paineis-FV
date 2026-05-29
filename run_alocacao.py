"""Script de execução para o dimensionamento fotovoltaico."""

import algoritmo_de_alocacao_1 as aloc
import interface_grafica as ig

# Constantes globais do projeto (Configuração do Telhado e Placas)
LARGURA_TELHADO = 17.5
COMPRIMENTO_TELHADO = 7.2
LARGURA_PLACA = 1.134
COMPRIMENTO_PLACA = 2.382


# 1. Gerando o DataFrame para Orientação Retrato
df_retrato = aloc.dimensionar(
    w_telhado=LARGURA_TELHADO,
    l_telhado=COMPRIMENTO_TELHADO,
    w_placa=LARGURA_PLACA,
    l_placa=COMPRIMENTO_PLACA
)

# 2. Gerando o DataFrame para Orientação Paisagem (inverte as dimensões)
df_paisagem = aloc.dimensionar(
    w_telhado=LARGURA_TELHADO,
    l_telhado=COMPRIMENTO_TELHADO,
    w_placa=COMPRIMENTO_PLACA,
    l_placa=LARGURA_PLACA
)

# 3. Salvando a quantidade total de painéis de cada orientação em variáveis
total_paineis_retrato = len(df_retrato)
total_paineis_paisagem = len(df_paisagem)

# Exibindo os totais armazenados
print(f"Total na orientação Retrato: {total_paineis_retrato}")
print(f"Total na orientação Paisagem: {total_paineis_paisagem}")

# 4. Chamando a função de plotagem externa para exibir os resultados
ig.plotar_janela_independente(
    df_retrato=df_retrato,
    df_paisagem=df_paisagem,
    w_tel=LARGURA_TELHADO,
    l_tel=COMPRIMENTO_TELHADO
)