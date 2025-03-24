from sympy import symbols, sympify

def parse_expression(expressao, variaveis):
    simbolos = symbols(variaveis)
    expr = sympify(expressao)
    coeficientes = {str(var): expr.coeff(var) for var in simbolos}
    constante = expr.subs({var: 0 for var in simbolos})
    return coeficientes, constante