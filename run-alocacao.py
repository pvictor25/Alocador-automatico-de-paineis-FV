import pandas as pd
import algoritmo_de_alocacao_1 as aloc

LARGURA_TELHADO = 12.0
COMPRIMENTO_TELHADO = 8.0
LARGURA_PLACA = 1.1
COMPRIMENTO_PLACA = 2.2

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

# Exibindo os resultados formatados
print(
    f"Total Retrato: {len(df_retrato)} placas | "
    f"Total Paisagem: {len(df_paisagem)} placas\n"
)
print("Amostra do DataFrame Orientação Retrato:")
print(df_retrato.head())