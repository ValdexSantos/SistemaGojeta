import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definição dos universos para cada variável (0 a 10)
x_estacionamento = np.linspace(0, 10, 101)
x_acessibilidade = np.linspace(0, 10, 101)
x_limpeza = np.linspace(0, 10, 101)
x_estrutura = np.linspace(0, 10, 101)

# Criação das variáveis fuzzy de entrada
estacionamento = ctrl.Antecedent(x_estacionamento, 'Estacionamento')
acessibilidade = ctrl.Antecedent(x_acessibilidade, 'Acessibilidade')
limpeza = ctrl.Antecedent(x_limpeza, 'Limpeza')

# Criação da variável fuzzy de saída
estrutura = ctrl.Consequent(x_estrutura, 'Estrutura')

# Definição das funções de pertinência para "Estacionamento"
estacionamento['Ruim'] = fuzz.trapmf(x_estacionamento, [0, 0, 2, 4])
estacionamento['Regular'] = fuzz.trapmf(x_estacionamento, [2, 4, 6, 8])
estacionamento['Bom'] = fuzz.trapmf(x_estacionamento, [6, 8, 10, 10])

# Definição das funções de pertinência para "Acessibilidade"
acessibilidade['Ruim'] = fuzz.trapmf(x_acessibilidade, [0, 0, 2, 4])
acessibilidade['Regular'] = fuzz.trapmf(x_acessibilidade, [2, 4, 6, 8])
acessibilidade['Boa'] = fuzz.trapmf(x_acessibilidade, [6, 8, 10, 10])

# Definição das funções de pertinência para "Limpeza"
limpeza['Ruim'] = fuzz.trapmf(x_limpeza, [0, 0, 2, 4])
limpeza['Regular'] = fuzz.trapmf(x_limpeza, [2, 4, 6, 8])
limpeza['Boa'] = fuzz.trapmf(x_limpeza, [6, 8, 10, 10])

# Definição das funções de pertinência para o output "Estrutura"
estrutura['Péssima'] = fuzz.trapmf(x_estrutura, [0, 0, 2, 3.5])
estrutura['Ruim'] = fuzz.trimf(x_estrutura, [2, 3.5, 5])
estrutura['Regular'] = fuzz.trimf(x_estrutura, [3.5, 5, 6.5])
estrutura['Boa'] = fuzz.trimf(x_estrutura, [5, 6.5, 8])
estrutura['Ótima'] = fuzz.trapmf(x_estrutura, [6.5, 8, 10, 10])

# ====================================================================
# Definição das 27 regras conforme a configuração MATLAB
# Os índices das funções de pertinência seguem:
# Inputs:
#   1 -> "Ruim", 2 -> "Regular", 3 -> "Bom"/"Boa" (conforme cada input)
# Output ("Estrutura"):
#   1 -> "Péssima", 2 -> "Ruim", 3 -> "Regular", 4 -> "Boa", 5 -> "Ótima"
# ====================================================================

rule1 = ctrl.Rule(estacionamento['Ruim'] & acessibilidade['Ruim'] & limpeza['Ruim'], estrutura['Péssima'])
rule2 = ctrl.Rule(estacionamento['Ruim'] & acessibilidade['Ruim'] & limpeza['Regular'], estrutura['Péssima'])
rule3 = ctrl.Rule(estacionamento['Ruim'] & acessibilidade['Ruim'] & limpeza['Boa'], estrutura['Ruim'])
rule4 = ctrl.Rule(estacionamento['Ruim'] & acessibilidade['Regular'] & limpeza['Ruim'], estrutura['Péssima'])
rule5 = ctrl.Rule(estacionamento['Ruim'] & acessibilidade['Regular'] & limpeza['Regular'], estrutura['Regular'])
rule6 = ctrl.Rule(estacionamento['Ruim'] & acessibilidade['Regular'] & limpeza['Boa'], estrutura['Regular'])
rule7 = ctrl.Rule(estacionamento['Ruim'] & acessibilidade['Boa'] & limpeza['Ruim'], estrutura['Ruim'])
rule8 = ctrl.Rule(estacionamento['Ruim'] & acessibilidade['Boa'] & limpeza['Regular'], estrutura['Regular'])
rule9 = ctrl.Rule(estacionamento['Ruim'] & acessibilidade['Boa'] & limpeza['Boa'], estrutura['Boa'])
rule10 = ctrl.Rule(estacionamento['Regular'] & acessibilidade['Ruim'] & limpeza['Ruim'], estrutura['Péssima'])
rule11 = ctrl.Rule(estacionamento['Regular'] & acessibilidade['Ruim'] & limpeza['Regular'], estrutura['Regular'])
rule12 = ctrl.Rule(estacionamento['Regular'] & acessibilidade['Ruim'] & limpeza['Boa'], estrutura['Regular'])
rule13 = ctrl.Rule(estacionamento['Regular'] & acessibilidade['Regular'] & limpeza['Ruim'], estrutura['Ruim'])
rule14 = ctrl.Rule(estacionamento['Regular'] & acessibilidade['Regular'] & limpeza['Regular'], estrutura['Regular'])
rule15 = ctrl.Rule(estacionamento['Regular'] & acessibilidade['Regular'] & limpeza['Boa'], estrutura['Boa'])
rule16 = ctrl.Rule(estacionamento['Regular'] & acessibilidade['Boa'] & limpeza['Ruim'], estrutura['Ruim'])
rule17 = ctrl.Rule(estacionamento['Regular'] & acessibilidade['Boa'] & limpeza['Regular'], estrutura['Boa'])
rule18 = ctrl.Rule(estacionamento['Regular'] & acessibilidade['Boa'] & limpeza['Boa'], estrutura['Ótima'])
rule19 = ctrl.Rule(estacionamento['Bom'] & acessibilidade['Ruim'] & limpeza['Ruim'], estrutura['Péssima'])
rule20 = ctrl.Rule(estacionamento['Bom'] & acessibilidade['Ruim'] & limpeza['Regular'], estrutura['Regular'])
rule21 = ctrl.Rule(estacionamento['Bom'] & acessibilidade['Ruim'] & limpeza['Boa'], estrutura['Boa'])
rule22 = ctrl.Rule(estacionamento['Bom'] & acessibilidade['Regular'] & limpeza['Ruim'], estrutura['Ruim'])
rule23 = ctrl.Rule(estacionamento['Bom'] & acessibilidade['Regular'] & limpeza['Regular'], estrutura['Boa'])
rule24 = ctrl.Rule(estacionamento['Bom'] & acessibilidade['Regular'] & limpeza['Boa'], estrutura['Ótima'])
rule25 = ctrl.Rule(estacionamento['Bom'] & acessibilidade['Boa'] & limpeza['Ruim'], estrutura['Regular'])
rule26 = ctrl.Rule(estacionamento['Bom'] & acessibilidade['Boa'] & limpeza['Regular'], estrutura['Ótima'])
rule27 = ctrl.Rule(estacionamento['Bom'] & acessibilidade['Boa'] & limpeza['Boa'], estrutura['Ótima'])

# Criação do sistema de controle e sua simulação
sistema = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9,
    rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18,
    rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27
])
fuzzy_simulation = ctrl.ControlSystemSimulation(sistema)


def compute_estrutura(estacionamento_val, acessibilidade_val, limpeza_val):
    """
    Calcula a saída do subsistema fuzzy ("Estrutura")
    a partir dos valores de entrada definidos para:
      - Estacionamento
      - Acessibilidade
      - Limpeza
    Retorna o valor defuzzificado.
    """
    fuzzy_simulation.input['Estacionamento'] = estacionamento_val
    fuzzy_simulation.input['Acessibilidade'] = acessibilidade_val
    fuzzy_simulation.input['Limpeza'] = limpeza_val

    fuzzy_simulation.compute()

    return fuzzy_simulation.output['Estrutura']


if __name__ == '__main__':
    # Exemplo de uso do subsistema
    val_estacionamento = 5.0  # valor para "Estacionamento"
    val_acessibilidade = 7.0  # valor para "Acessibilidade"
    val_limpeza = 3.0  # valor para "Limpeza"

    resultado = compute_estrutura(val_estacionamento, val_acessibilidade, val_limpeza)
    print("Saída do subsistema (Estrutura):", resultado)
