import re
import unicodedata
from datetime import date
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Plusoft - Nomenclatura Padrão", layout="centered")

st.title("📋 Plusoft - Nomenclatura Padrão")
st.markdown("Preencha os campos abaixo para gerar a nomenclatura padronizada da campanha CRM.")

# Função para normalizar texto (acentos, espaços, caracteres especiais)
def normalize_text(text):
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = text.replace(" ", "_")
    return text

# Inicializa histórico
if "history" not in st.session_state:
    st.session_state.history = []

# Layout em colunas
col1, col2 = st.columns(2)

with col1:
    data_input = st.date_input("Data da campanha:", value=date.today())
    canal = st.selectbox(
        "Canal:",
        ["Email", "SMS", "SMS - Com LP", "Push", "WhatsApp", "Social (Meta-Face)", "Extração"]
    )
    tipo_campanha = st.selectbox("Tipo de Campanha:", ["Pontual", "Recorrente"])
    responsavel = st.selectbox("Responsável:", ["Interno", "Externo"])

with col2:
    marca = st.text_input("Marca/Bandeira:")
    publico = st.text_input("Público:")
    plano_envio = st.text_input("Plano/Nome de Envio:")

# Converte data para formato aaaammdd
data = data_input.strftime("%Y%m%d")

# Mapeamentos
canal_abbr = {
    "Email": "emkt",
    "SMS": "sms",
    "SMS - Com LP": "lpg",
    "Push": "psh",
    "WhatsApp": "wts",
    "Social (Meta-Face)": "soc",
    "Extração": "ext"
}

responsavel_abbr = {"Interno": "int", "Externo": "ext"}

# Prévia dinâmica
channel = canal_abbr.get(canal, "")
responsible = responsavel_abbr.get(responsavel, "")
brand = normalize_text(marca)
audience = normalize_text(publico)
send_name = normalize_text(plano_envio)

preview = f"{data}-{channel}-{tipo_campanha}-{responsible}-{brand}-{audience}-{send_name}".lower()
st.markdown(f"🧩 **Prévia da Nomenclatura:** `{preview}`")

# Validação dinâmica
invalid_fields = []
pattern = r"^[a-zA-Z0-9_\-ç]+$"

if marca and not re.match(pattern, brand):
    invalid_fields.append("Marca/Bandeira")
if publico and not re.match(pattern, audience):
    invalid_fields.append("Público")
if plano_envio and not re.match(pattern, send_name):
    invalid_fields.append("Plano/Nome de Envio")

if invalid_fields:
    st.warning(f"⚠️ Campos inválidos: {', '.join(invalid_fields)} — use apenas letras, números, traços ou underline.")

# Geração
if st.button("Gerar Nomenclatura"):
    if invalid_fields:
        st.error("❌ Corrija os campos inválidos antes de gerar a nomenclatura.")
    else:
        result = preview
        st.success("✅ Nomenclatura gerada com sucesso!")
        st.code(result, language="text")

        # Salva no histórico
        st.session_state.history.append(result)

        # Botão de cópia (funcional com JavaScript)
        components.html(f"""
        <button style="
            background-color:#0077cc;
            color:white;
            border:none;
            border-radius:5px;
            padding:8px 16px;
            cursor:pointer;
        " onclick="navigator.clipboard.writeText('{result}');
        alert('Nomenclatura copiada para a área de transferência!');">
        📋 Copiar Resultado
        </button>
        """, height=60)

        st.toast("Nomenclatura gerada!")

# Histórico das últimas nomenclaturas
if st.session_state.history:
    st.markdown("### 🕒 Histórico recente")
    for item in reversed(st.session_state.history[-5:]):
        st.code(item)
