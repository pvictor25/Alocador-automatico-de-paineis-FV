import math
import pandas as pd


def _para_float(val):
    """Converte valor numérico ou string com ponto/vírgula para float com segurança."""
    if isinstance(val, str):
        return float(val.replace(",", ".").strip())
    return float(val)


def checar_quina(x, y, w_tel, l_tel, dist_quina=1.0):
    """Verifica se o ponto (x,y) respeita o afastamento das 4 quinas."""
    x = _para_float(x)
    y = _para_float(y)
    w_tel = _para_float(w_tel)
    l_tel = _para_float(l_tel)
    dist_quina = _para_float(dist_quina)

    quinas = [(0, 0), (w_tel, 0), (0, l_tel), (w_tel, l_tel)]
    for q_x, q_y in quinas:
        dist = math.sqrt((x - q_x)**2 + (y - q_y)**2)
        if dist < dist_quina:
            return False
    return True


def dimensionar(
    w_telhado,
    l_telhado,
    w_placa,
    l_placa,
    borda=0.5,
    espacamento=0.05,
    dist_quina=1.0,
):
    """Gera um DataFrame com as coordenadas de todos os painéis válidos."""
    w_telhado = _para_float(w_telhado)
    l_telhado = _para_float(l_telhado)
    w_placa = _para_float(w_placa)
    l_placa = _para_float(l_placa)
    borda = _para_float(borda)
    espacamento = _para_float(espacamento)
    dist_quina = _para_float(dist_quina)

    dados_paineis = []
    id_painel = 1

    x_inicial = borda
    y_inicial = borda

    y = y_inicial
    while y + l_placa <= l_telhado - borda:
        x = x_inicial
        while x + w_placa <= w_telhado - borda:

            # Coordenadas exatas dos 4 vértices do painel atual
            inf_esq = (x, y)
            inf_dir = (x + w_placa, y)
            sup_esq = (x, y + l_placa)
            sup_dir = (x + w_placa, y + l_placa)

            # Validação se todos os cantos respeitam o afastamento
            cantos = [inf_esq, inf_dir, sup_esq, sup_dir]
            placa_valida = True
            for c_x, c_y in cantos:
                if not checar_quina(
                    c_x, c_y, w_telhado, l_telhado, dist_quina=dist_quina
                ):
                    placa_valida = False
                    break

            # Se a placa for válida, salva as coordenadas
            if placa_valida:
                dados_paineis.append({
                    "painel": f"painel-{id_painel}",
                    "x_inf_esq": inf_esq[0],
                    "y_inf_esq": inf_esq[1],
                    "x_inf_dir": inf_dir[0],
                    "y_inf_dir": inf_dir[1],
                    "x_sup_esq": sup_esq[0],
                    "y_sup_esq": sup_esq[1],
                    "x_sup_dir": sup_dir[0],
                    "y_sup_dir": sup_dir[1],
                })
                id_painel += 1

            x += w_placa + espacamento
        y += l_placa + espacamento

    return pd.DataFrame(dados_paineis)
