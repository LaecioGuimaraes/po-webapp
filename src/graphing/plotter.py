import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
from optimization.expression_parser import parse_expression

def gerar_grafico(variaveis, descricoes, restricoes, solucao_otima):
    plt.figure(figsize=(8, 6))
    plt.title("Espaço de Soluções")
    plt.xlabel(descricoes[0])
    plt.ylabel(descricoes[1])
    plt.grid(True)

    # Inicializa os limites dos eixos
    x_min, x_max = 0, 1  # Valores iniciais pequenos
    y_min, y_max = 0, 1  # Valores iniciais pequenos

    # Ajusta os limites com base nas restrições
    for restricao in restricoes:
        if "<=" in restricao or ">=" in restricao:
            if "<=" in restricao:
                expr, valor = restricao.split("<=")
            elif ">=" in restricao:
                expr, valor = restricao.split(">=")

            coeficientes, constante = parse_expression(expr, variaveis)
            a = float(coeficientes.get(variaveis[0], 0))
            b = float(coeficientes.get(variaveis[1], 0))
            c = float(valor) - float(constante)

            if b != 0:
                # Calcula os valores de y para x_min e x_max
                y_vals_xmin = (c - a * x_min) / b
                y_vals_xmax = (c - a * x_max) / b

                # Atualiza os limites de y
                y_min = min(y_min, y_vals_xmin, y_vals_xmax)
                y_max = max(y_max, y_vals_xmin, y_vals_xmax)

            if a != 0:
                # Calcula os valores de x para y_min e y_max
                x_vals_ymin = (c - b * y_min) / a
                x_vals_ymax = (c - b * y_max) / a

                # Atualiza os limites de x
                x_min = min(x_min, x_vals_ymin, x_vals_ymax)
                x_max = max(x_max, x_vals_ymin, x_vals_ymax)

    # Garante que os limites não sejam negativos (se as restrições permitirem)
    x_min = max(x_min, 0)
    y_min = max(y_min, 0)

    # Adiciona uma margem para melhor visualização
    margem = 0.1  # 10% de margem
    x_min -= margem * (x_max - x_min)
    x_max += margem * (x_max - x_min)
    y_min -= margem * (y_max - y_min)
    y_max += margem * (y_max - y_min)

    x = np.linspace(x_min, x_max, 400)
    y = np.linspace(y_min, y_max, 400)

    # Lista para armazenar as áreas factíveis
    areas_factiveis = []

    # Plota as restrições
    for restricao in restricoes:
        if "<=" in restricao or ">=" in restricao:
            if "<=" in restricao:
                expr, valor = restricao.split("<=")
            elif ">=" in restricao:
                expr, valor = restricao.split(">=")

            coeficientes, constante = parse_expression(expr, variaveis)
            a = float(coeficientes.get(variaveis[0], 0))
            b = float(coeficientes.get(variaveis[1], 0))
            c = float(valor) - float(constante)

            if b != 0:
                y_vals = (c - a * x) / b
                plt.plot(x, y_vals, label=restricao)
                # Armazena a área factível para cada restrição
                if "<=" in restricao:
                    areas_factiveis.append((a, b, c, 'leq'))
                elif ">=" in restricao:
                    areas_factiveis.append((a, b, c, 'geq'))

    # Preenche a região factível
    if areas_factiveis:
        # Define os limites da região factível
        y_min_region = np.zeros_like(x)
        y_max_region = np.full_like(x, 1e6)  # Usamos um valor grande, mas finito, em vez de np.inf

        for a, b, c, tipo in areas_factiveis:
            if b != 0:
                y_restricao = (c - a * x) / b
                if tipo == 'leq':
                    y_max_region = np.minimum(y_max_region, y_restricao)
                elif tipo == 'geq':
                    y_min_region = np.maximum(y_min_region, y_restricao)

        # Verifica se há uma região factível
        condicao = np.logical_and(y_max_region > y_min_region, y_max_region != np.inf)
        if np.any(condicao):
            plt.fill_between(x, y_min_region, y_max_region, where=condicao, color='gray', alpha=0.6, label='Região Factível')

    # Plota a solução ótima, se existir
    if solucao_otima:
        plt.scatter(solucao_otima[0], solucao_otima[1], color='red', label="Solução Ótima")

    plt.subplots_adjust(bottom=0.25)

    # Mover a legenda para abaixo do gráfico
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=2)

    # Define os limites dos eixos
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    # Salva o gráfico em um buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')  # bbox_inches='tight' para evitar cortes
    buffer.seek(0)

    # Codifica a imagem em Base64
    imagem_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return imagem_base64