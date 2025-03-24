import pulp
from optimization.expression_parser import parse_expression

def resolver_problema_otimizacao(variaveis, tipo, objetivo, restricoes):
    problema = pulp.LpProblem("Problema_de_Otimizacao", pulp.LpMaximize if tipo == "max" else pulp.LpMinimize)
    vars_pulp = {var: pulp.LpVariable(var, lowBound=0) for var in variaveis}

    coeficientes_obj, constante_obj = parse_expression(objetivo, variaveis)
    objetivo_pulp = constante_obj
    for var in variaveis:
        objetivo_pulp += coeficientes_obj.get(var, 0) * vars_pulp[var]
    problema += objetivo_pulp, "Z"

    for restricao in restricoes:
        if "<=" in restricao:
            expr, valor = restricao.split("<=")
            sinal = "<="
        elif ">=" in restricao:
            expr, valor = restricao.split(">=")
            sinal = ">="
        else:
            raise ValueError(f"Formato de restrição inválido: {restricao}")

        coeficientes_res, constante_res = parse_expression(expr, variaveis)
        restricao_pulp = constante_res
        for var in variaveis:
            restricao_pulp += coeficientes_res.get(var, 0) * vars_pulp[var]

        if sinal == "<=":
            problema += restricao_pulp <= float(valor), f"Restricao_{restricoes.index(restricao)}"
        elif sinal == ">=":
            problema += restricao_pulp >= float(valor), f"Restricao_{restricoes.index(restricao)}"

    problema.solve()

    resultados = {var: pulp.value(vars_pulp[var]) for var in variaveis}
    resultados["Z"] = pulp.value(problema.objective)
    resultados["status"] = pulp.LpStatus[problema.status]

    return resultados

def solve_problem(data):
    try:
        parametros = data["dados"]["parametros"]
        variaveis = parametros["variaveis"]
        descricoes = parametros.get("descricoes", variaveis)
        tipo = parametros["tipo"]
        objetivo = parametros["objetivo"]
        restricoes = parametros["restricoes"]

        resultados = resolver_problema_otimizacao(variaveis, tipo, objetivo, restricoes)
        print("Resultados da otimização:", resultados)

        imagem_base64 = None
        if len(variaveis) == 2:
            from graphing.plotter import gerar_grafico
            solucao_otima = [resultados[variaveis[0]], resultados[variaveis[1]]]
            imagem_base64 = gerar_grafico(variaveis, descricoes, restricoes, solucao_otima)

        resposta = {
            "dados": {
                "parametros": parametros,
                "resultado": {
                    "decisao": [f"{var}={resultados[var]:.3f}" for var in variaveis],
                    "Z": float(resultados.get("Z", 0)),
                    "grafico": len(variaveis) == 2,
                    "imagem": imagem_base64
                },
                "mensagem": {
                    "sucesso": True,
                    "texto": f"Otimização concluída com status: {resultados['status']}"
                }
            }
        }

        print("Resposta JSON:", resposta)
        return resposta
    except Exception as e:
        print("Erro em solve_problem:", str(e))
        from utils.error_handler import handle_error
        return handle_error(e, data)