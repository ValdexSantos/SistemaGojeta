import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Importa as funções dos subsistemas
from subsistema_fuzzy import compute_estrutura
from subsystem_servico import compute_servico

# Definição dos universos de discurso para o sistema principal
# Variáveis de entrada: "Serviço" e "Estrutura" (faixa de 0 a 10)
x_servico = np.linspace(0, 10, 101)
x_estrutura = np.linspace(0, 10, 101)
# Variável de saída: "Gorjeta" (faixa de 0 a 15)
x_gorjeta = np.linspace(0, 15, 101)

# Criação das variáveis fuzzy dos inputs
servico = ctrl.Antecedent(x_servico, 'Serviço')
estrutura = ctrl.Antecedent(x_estrutura, 'Estrutura')

# Criação da variável fuzzy do output
gorjeta = ctrl.Consequent(x_gorjeta, 'Gorjeta')

# Definição das funções de pertinência para "Serviço"
servico['Ruim'] = fuzz.trapmf(x_servico, [0, 0, 2, 5])
servico['Regular'] = fuzz.trimf(x_servico, [2, 5, 8])
servico['Bom'] = fuzz.trapmf(x_servico, [5, 8, 10, 10])

# Definição das funções de pertinência para "Estrutura"
estrutura['Ruim'] = fuzz.trapmf(x_estrutura, [0, 0, 3, 5])
estrutura['Regular'] = fuzz.trapmf(x_estrutura, [3, 5, 6, 8])
estrutura['Boa'] = fuzz.trapmf(x_estrutura, [6, 8, 10, 10])

# Definição das funções de pertinência para "Gorjeta"
gorjeta['Muito baixa'] = fuzz.trimf(x_gorjeta, [0, 0, 3.755])
gorjeta['Baixa'] = fuzz.trimf(x_gorjeta, [0, 3.75, 7.5])
gorjeta['Média'] = fuzz.trimf(x_gorjeta, [3.75, 7.5, 11.25])
gorjeta['Alta'] = fuzz.trimf(x_gorjeta, [7.5, 11.25, 15])
gorjeta['Muito alta'] = fuzz.trimf(x_gorjeta, [11.25, 15, 15])

# ====================================================================
# Definição das 9 regras segundo a especificação:
#
# Regra 1: Se Serviço é Ruim e Estrutura é Ruim       => Gorjeta é Muito baixa
# Regra 2: Se Serviço é Ruim e Estrutura é Regular    => Gorjeta é Baixa
# Regra 3: Se Serviço é Ruim e Estrutura é Boa        => Gorjeta é Média
# Regra 4: Se Serviço é Regular e Estrutura é Ruim      => Gorjeta é Baixa
# Regra 5: Se Serviço é Regular e Estrutura é Regular   => Gorjeta é Média
# Regra 6: Se Serviço é Regular e Estrutura é Boa       => Gorjeta é Alta
# Regra 7: Se Serviço é Bom e Estrutura é Ruim          => Gorjeta é Média
# Regra 8: Se Serviço é Bom e Estrutura é Regular       => Gorjeta é Alta
# Regra 9: Se Serviço é Bom e Estrutura é Boa           => Gorjeta é Muito alta
# ====================================================================

rule1 = ctrl.Rule(servico['Ruim'] & estrutura['Ruim'], gorjeta['Muito baixa'])
rule2 = ctrl.Rule(servico['Ruim'] & estrutura['Regular'], gorjeta['Baixa'])
rule3 = ctrl.Rule(servico['Ruim'] & estrutura['Boa'], gorjeta['Média'])
rule4 = ctrl.Rule(servico['Regular'] & estrutura['Ruim'], gorjeta['Baixa'])
rule5 = ctrl.Rule(servico['Regular'] & estrutura['Regular'], gorjeta['Média'])
rule6 = ctrl.Rule(servico['Regular'] & estrutura['Boa'], gorjeta['Alta'])
rule7 = ctrl.Rule(servico['Bom'] & estrutura['Ruim'], gorjeta['Média'])
rule8 = ctrl.Rule(servico['Bom'] & estrutura['Regular'], gorjeta['Alta'])
rule9 = ctrl.Rule(servico['Bom'] & estrutura['Boa'], gorjeta['Muito alta'])

# Criação do sistema de controle fuzzy e da simulação
gorjeta_system = ctrl.ControlSystem([
    rule1, rule2, rule3,
    rule4, rule5, rule6,
    rule7, rule8, rule9
])
gorjeta_sim = ctrl.ControlSystemSimulation(gorjeta_system)


def compute_gorjeta(servico_val, estrutura_val):
    """
    Calcula a saída do sistema principal fuzzy "Gorjeta" a partir
    dos valores de entrada: serviço e estrutura.
    """
    gorjeta_sim.input['Serviço'] = servico_val
    gorjeta_sim.input['Estrutura'] = estrutura_val
    gorjeta_sim.compute()
    return gorjeta_sim.output['Gorjeta']


def compute_integrated_gorjeta(atendimento_val, comida_val, estacionamento_val, acessibilidade_val, limpeza_val):
    """
    Calcula a gorjeta integrada utilizando os dois subsistemas:
      - Subsistema de Serviço (entradas: Atendimento e Comida)
      - Subsistema de Estrutura (entradas: Estacionamento, Acessibilidade e Limpeza)

    Em seguida, utiliza as saídas desses subsistemas como entradas
    para o sistema principal de Gorjeta.

    Retorna o valor defuzzificado da gorjeta.
    """
    # Calcula a saída do subsistema de Serviço
    servico_val = compute_servico(atendimento_val, comida_val)
    # Calcula a saída do subsistema de Estrutura
    estrutura_val = compute_estrutura(estacionamento_val, acessibilidade_val, limpeza_val)

    # Calcula a gorjeta com base nas saídas dos dois subsistemas
    gorjeta_val = compute_gorjeta(servico_val, estrutura_val)

    return gorjeta_val


if __name__ == '__main__':
    # Exemplo de uso do sistema principal integrado

    # Entradas para o subsistema de Serviço
    atendimento_ex = 4.0
    comida_ex = 7.0

    # Entradas para o subsistema de Estrutura
    estacionamento_ex = 5.0
    acessibilidade_ex = 7.0
    limpeza_ex = 3.0

    resultado = compute_integrated_gorjeta(atendimento_ex, comida_ex,
                                           estacionamento_ex, acessibilidade_ex, limpeza_ex)
    print("Valor da Gorjeta:", resultado)
