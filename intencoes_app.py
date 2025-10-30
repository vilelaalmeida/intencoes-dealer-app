import streamlit as st
import pandas as pd
import requests
from io import BytesIO

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

    # --- Botão de download (CSV) ---
    csv = df.to_csv(index=True).encode('utf-8')
    st.download_button(
        label="📥 Baixar relatório em CSV",
        data=csv,
        file_name=f"intencoes_{dealer}.csv",
        mime='text/csv'
    )

    # --- Envio por e-mail (SendGrid) ---
    import os
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY") # substitua pela sua chave real

    if st.button("📧 Enviar por e-mail"):
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=True, sheet_name="Intenções")

        # Envia o arquivo para o e-mail
        data = {
            "personalizations": [{"to": [{"email": "vilelaalmeida@icloud.com"}]}],
            "from": {"email": "noreply@ladata.com"},
            "subject": f"Intenções de compra - Dealer {dealer}",
            "content": [{"type": "text/plain", "value": f"Segue o relatório do dealer {dealer} em anexo."}],
            "attachments": [{
                # Corrigido: precisa converter o arquivo em base64 (não decode latin1)
                "content": buffer.getvalue().encode('base64').decode(),
                "filename": f"intencoes_{dealer}.xlsx",
                "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }]
        }

        r = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json"
            },
            json=data
        )

        if r.status_code == 202:
            st.success("📨 E-mail enviado com sucesso!")
        else:
            st.error(f"Erro ao enviar e-mail: {r.text}")

