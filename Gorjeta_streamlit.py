import streamlit as st
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Importa a função integrada para o cálculo da gorjeta
from sistema_gorjeta import compute_integrated_gorjeta

# Configuração da página
st.set_page_config(page_title="Sistema de Previsão de Gorjeta", layout="centered")

st.title("Sistema Integrado de Previsão de Gorjeta")
st.write("Ajuste os parâmetros abaixo para avaliar a experiência e visualizar a gorjeta final de forma interativa:")

# Parâmetros para o Subsistema de Serviço
st.sidebar.header("Parâmetros do Subsistema de Serviço")
atendimento = st.sidebar.slider("Atendimento", 0.0, 10.0, 5.0, step=0.1)
comida = st.sidebar.slider("Comida", 0.0, 10.0, 5.0, step=0.1)

# Parâmetros para o Subsistema de Estrutura
st.sidebar.header("Parâmetros do Subsistema de Estrutura")
estacionamento = st.sidebar.slider("Estacionamento", 0.0, 10.0, 5.0, step=0.1)
acessibilidade = st.sidebar.slider("Acessibilidade", 0.0, 10.0, 5.0, step=0.1)
limpeza = st.sidebar.slider("Limpeza", 0.0, 10.0, 5.0, step=0.1)

# Cálculo automático da gorjeta integrado
computed_value = compute_integrated_gorjeta(
    atendimento, comida, estacionamento, acessibilidade, limpeza
)
st.success(f"Valor da Gorjeta Calculada: {computed_value:.2f}")


def plot_gorjeta_membership(gorjeta_value=None):
    """
    Plota as funções de pertinência para a variável 'Gorjeta' e, se fornecido,
    destaca o valor calculado com uma linha vertical tracejada.
    """
    # Define o universo para a variável Gorjeta (0 a 15)
    x = np.linspace(0, 15, 101)

    # Define as funções de pertinência conforme a especificação
    mf_muito_baixa = fuzz.trimf(x, [0, 0, 3.755])
    mf_baixa = fuzz.trimf(x, [0, 3.75, 7.5])
    mf_media = fuzz.trimf(x, [3.75, 7.5, 11.25])
    mf_alta = fuzz.trimf(x, [7.5, 11.25, 15])
    mf_muito_alta = fuzz.trimf(x, [11.25, 15, 15])

    # Cria o gráfico
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, mf_muito_baixa, 'b', linewidth=1.5, label='Muito baixa')
    ax.plot(x, mf_baixa, 'g', linewidth=1.5, label='Baixa')
    ax.plot(x, mf_media, 'r', linewidth=1.5, label='Média')
    ax.plot(x, mf_alta, 'c', linewidth=1.5, label='Alta')
    ax.plot(x, mf_muito_alta, 'm', linewidth=1.5, label='Muito alta')

    # Se o valor calculado foi fornecido, destaque-o no gráfico
    if gorjeta_value is not None:
        ax.axvline(x=gorjeta_value, color='k', linestyle='--', label='Gorjeta Calculada')
        ax.text(gorjeta_value + 0.3, 0.1, f'{gorjeta_value:.2f}', color='black')

    ax.set_title('Funções de Pertinência da Gorjeta')
    ax.set_xlabel('Gorjeta')
    ax.set_ylabel('Grau de Pertinência')
    ax.legend(loc='upper left')
    ax.grid(True)

    return fig


st.header("Gráfico da Pertinência da Gorjeta")
fig = plot_gorjeta_membership(computed_value)
st.pyplot(fig)

st.markdown("""
---
**Como Funciona:**
- **Subsistema de Serviço:** Avalia os parâmetros "Atendimento" e "Comida".
- **Subsistema de Estrutura:** Utiliza "Estacionamento", "Acessibilidade" e "Limpeza".
- **Sistema Principal (Gorjeta):** Integra as saídas dos dois subsistemas para gerar o valor final da gorjeta.
""")
