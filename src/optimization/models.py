# src/optimization/models.py
class OptimizationProblem:
    def __init__(self, variaveis, tipo, objetivo, restricoes):
        self.variaveis = variaveis
        self.tipo = tipo
        self.objetivo = objetivo
        self.restricoes = restricoes