import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Validador de Ponto", layout="wide")
st.title("📋 Verificação de Batidas Faltantes")

uploaded_file = st.file_uploader("Envie o relatório de ponto (.csv ou .xlsx)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Leitura do arquivo
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("---")
    st.subheader("Pré-visualização dos dados")
    st.dataframe(df.head())

    # Regra de verificação (exemplo com 4 batidas esperadas)
    batidas_esperadas = st.number_input("Batidas esperadas por dia", min_value=1, max_value=6, value=4)

    if st.button("Identificar Batidas Faltantes"):
        # Garante a ordenação
        df = df.sort_values(by=['cpf', 'data', 'horario'])

        # Agrupa e conta
        resumo = df.groupby(['cpf', 'nome', 'data']).agg(
            total_batidas=('horario', 'count'),
            horarios=('horario', lambda x: ', '.join(map(str, x)))
        ).reset_index()

        inconsistencias = resumo[resumo['total_batidas'] < batidas_esperadas].copy()
        inconsistencias['batidas_faltantes'] = batidas_esperadas - inconsistencias['total_batidas']

        st.error(f"Foram encontradas {len(inconsistencias)} inconsistências!")
        st.dataframe(inconsistencias[['cpf', 'nome', 'data', 'total_batidas', 'batidas_faltantes', 'horarios']])
