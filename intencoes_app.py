import streamlit as st
import pandas as pd

# --- Configuração da página ---
st.set_page_config(page_title="Planejamento de Intenção de Compra", page_icon="🧾")

# --- Cabeçalho corporativo ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=100)
with col2:
    st.title("Planejamento de Intenção de Compra")

st.markdown("Aplicativo desenvolvido pela **LA Data** para coleta e consolidação de intenções de compra de tratores.")
st.divider()

# --- Entrada do dealer ---
dealer = st.text_input("Digite o nome ou ID do dealer:")

# --- Produtos e meses ---
produtos = ["Trator 10", "Trator 20"]
meses = ["Março", "Abril", "Maio"]

# --- Coleta dos dados ---
intencoes = {}

for produto in produtos:
    st.subheader(produto)
    intencoes[produto] = {}
    for mes in meses:
        intencoes[produto][mes] = st.number_input(
            f"Quantidade prevista para {mes}:",
            min_value=0,
            step=1,
            key=f"{produto}_{mes}"
        )

# --- Geração do DataFrame ---
df = pd.DataFrame(intencoes).T
df["Total Produto"] = df.sum(axis=1)
df.loc["Total Mês"] = df.sum()

# --- Botão para exibir relatório ---
if st.button("Gerar relatório"):
    st.success(f"Relatório gerado para o dealer **{dealer}**")
    st.dataframe(df)

    # Botão de download
    csv = df.to_csv(index=True).encode('utf-8')
    st.download_button(
        label="📥 Baixar relatório em CSV",
        data=csv,
        file_name=f"intencoes_{dealer}.csv",
        mime='text/csv'
    )
