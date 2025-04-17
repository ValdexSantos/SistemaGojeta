import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definição dos universos de discurso (0 a 10 com 101 pontos)
x_atendimento = np.linspace(0, 10, 101)
x_comida = np.linspace(0, 10, 101)
x_servico = np.linspace(0, 10, 101)

# Criação das variáveis fuzzy de entrada
atendimento = ctrl.Antecedent(x_atendimento, 'Atendimento')
comida = ctrl.Antecedent(x_comida, 'Comida')

# Criação da variável fuzzy de saída
servico = ctrl.Consequent(x_servico, 'Serviço')

# Definição das funções de pertinência para "Atendimento"
atendimento['Ruim'] = fuzz.trapmf(x_atendimento, [0, 0, 3, 5])
atendimento['Regular'] = fuzz.trapmf(x_atendimento, [3, 5, 6, 8])
atendimento['Bom'] = fuzz.trapmf(x_atendimento, [6, 8, 10, 10])

# Definição das funções de pertinência para "Comida"
comida['Ruim'] = fuzz.trapmf(x_comida, [0, 0, 3, 5])
comida['Regular'] = fuzz.trapmf(x_comida, [3, 5, 6, 8])
comida['Boa'] = fuzz.trapmf(x_comida, [6, 8, 10, 10])

# Definição das funções de pertinência para o output "Serviço"
servico['Péssimo'] = fuzz.trapmf(x_servico, [0, 0, 2, 3.5])
servico['Ruim'] = fuzz.trimf(x_servico, [2, 3.5, 5])
servico['Regular'] = fuzz.trimf(x_servico, [3.5, 5, 6.5])
servico['Bom'] = fuzz.trimf(x_servico, [5, 6.5, 8])
servico['Ótimo'] = fuzz.trapmf(x_servico, [6.5, 8, 10, 10])

# ====================================================================
# Definição das 9 regras conforme a especificação:
#
# Regra 1: Se Atendimento é Ruim e Comida é Ruim      => Serviço é Péssimo
# Regra 2: Se Atendimento é Ruim e Comida é Regular   => Serviço é Ruim
# Regra 3: Se Atendimento é Ruim e Comida é Boa       => Serviço é Regular
# Regra 4: Se Atendimento é Regular e Comida é Ruim     => Serviço é Ruim
# Regra 5: Se Atendimento é Regular e Comida é Regular  => Serviço é Regular
# Regra 6: Se Atendimento é Regular e Comida é Boa      => Serviço é Bom
# Regra 7: Se Atendimento é Bom e Comida é Ruim         => Serviço é Regular
# Regra 8: Se Atendimento é Bom e Comida é Regular      => Serviço é Bom
# Regra 9: Se Atendimento é Bom e Comida é Boa          => Serviço é Ótimo
# ====================================================================

rule1 = ctrl.Rule(atendimento['Ruim'] & comida['Ruim'], servico['Péssimo'])
rule2 = ctrl.Rule(atendimento['Ruim'] & comida['Regular'], servico['Ruim'])
rule3 = ctrl.Rule(atendimento['Ruim'] & comida['Boa'], servico['Regular'])
rule4 = ctrl.Rule(atendimento['Regular'] & comida['Ruim'], servico['Ruim'])
rule5 = ctrl.Rule(atendimento['Regular'] & comida['Regular'], servico['Regular'])
rule6 = ctrl.Rule(atendimento['Regular'] & comida['Boa'], servico['Bom'])
rule7 = ctrl.Rule(atendimento['Bom'] & comida['Ruim'], servico['Regular'])
rule8 = ctrl.Rule(atendimento['Bom'] & comida['Regular'], servico['Bom'])
rule9 = ctrl.Rule(atendimento['Bom'] & comida['Boa'], servico['Ótimo'])

# Criação do sistema de controle e da simulação
servico_system = ctrl.ControlSystem([
    rule1, rule2, rule3,
    rule4, rule5, rule6,
    rule7, rule8, rule9
])
servico_simulation = ctrl.ControlSystemSimulation(servico_system)


def compute_servico(atendimento_val, comida_val):
    """
    Calcula a saída do subsistema fuzzy "Serviço" a partir dos valores de:
      - Atendimento
      - Comida
    Retorna o valor defuzzificado.
    """
    servico_simulation.input['Atendimento'] = atendimento_val
    servico_simulation.input['Comida'] = comida_val

    servico_simulation.compute()

    return servico_simulation.output['Serviço']


if __name__ == '__main__':
    # Exemplo de uso do subsistema
    exemplo_atendimento = 4.0  # Valor para "Atendimento"
    exemplo_comida = 7.0  # Valor para "Comida"

    resultado = compute_servico(exemplo_atendimento, exemplo_comida)
    print("Saída do subsistema de Serviço:", resultado)
