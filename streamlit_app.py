# import streamlit as st

# st.title("🎈 My new app")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )


import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# --- Conexão com Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/drive"]

# Substitua pelo caminho do seu arquivo JSON de credenciais
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
client = gspread.authorize(creds)

# Substitua pelo ID da sua planilha
sheet = client.open_by_key("15HwvTeGf07Z-C5pA3884MTJve_dwv8X58CwnNjHu89Y")
worksheet = sheet.sheet1  # primeira aba

# --- Ler dados existentes ---
dados = worksheet.get_all_values()
df = pd.DataFrame(dados[1:], columns=dados[0])  # Ignora cabeçalho

# --- Interface Streamlit ---
st.title("Formulário de Seleção")

# Dropdown com 1ª coluna
coluna1 = df.columns[0]
empresas = df[coluna1].tolist()
empresa_selecionada = st.selectbox(f"Escolha {coluna1}", empresas)

# Botões (radio) com 2ª coluna
coluna2 = df.columns[1]
opcoes = df[coluna2].tolist()
opcao_selecionada = st.radio(f"Escolha {coluna2}", opcoes)

# Botão enviar
if st.button("Enviar"):
    # Salvar no Google Sheets
    worksheet.append_row([datetime.now().strftime("%d/%m/%Y %H:%M:%S"), empresa_selecionada, opcao_selecionada])
    st.success(f"Registrado: {empresa_selecionada} / {opcao_selecionada}")
