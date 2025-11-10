import re
import unicodedata
from datetime import date
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Plusoft - Nomenclatura Padrão", layout="centered")

st.title("📋 Plusoft - Nomenclatura Padrão (Novo Formato)")
st.markdown("Preencha os campos abaixo para gerar a nomenclatura no formato:\n **AAAAMMDD_BANDEIRA-CANAL-TIPOCAMPANHAS-NOMEAÇÃO**")

# Função para normalizar texto (acentos, espaços, caracteres especiais)
def normalize_text(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = text.strip().replace(" ", "_").lower()
    return text

# Inicializa histórico
if "history" not in st.session_state:
    st.session_state.history = []


data_input = st.date_input("Data da campanha:", value=date.today())
canal = st.selectbox(
    "Canal:",
    ["Email", "SMS", "SMS - Com LP", "Push", "WhatsApp", "Social (Meta-Face)", "Extração", "Multi-Canal"]
)

bandeira = st.text_input("Bandeira / Marca:")
tipo_campanha = st.selectbox("Tipo de Campanha:", ["Pontual", "Recorrente"])
nomeacao = st.text_input("Nomeação:")

# Mapeamentos abreviados
canal_abbr = {
    "Email": "emkt",
    "SMS": "sms",
    "SMS - Com LP": "lpg",
    "Push": "psh",
    "WhatsApp": "wts",
    "Social (Meta-Face)": "soc",
    "Extração": "ext"
}

# Converte e normaliza
data = data_input.strftime("%Y%m%d")
bandeira_norm = normalize_text(bandeira)
canal_norm = canal_abbr.get(canal, "").lower()
tipo_norm = normalize_text(tipo_campanha)
nomeacao_norm = normalize_text(nomeacao)

# Monta prévia dinâmica
preview = f"{data}_{bandeira_norm}-{canal_norm}-{tipo_norm}-{nomeacao_norm}"

# Validação simples
pattern = r"^[a-zA-Z0-9_\-ç]+$"
invalid_fields = []

for campo, valor in {
    "Bandeira": bandeira_norm,
    "Nomeação": nomeacao_norm,
}.items():
    if valor and not re.match(pattern, valor):
        invalid_fields.append(campo)

st.markdown(f"🧩 **Prévia da Nomenclatura:** `{preview}`")

if invalid_fields:
    st.warning(f"⚠️ Campos inválidos: {', '.join(invalid_fields)} — use apenas letras, números, traços ou underline.")

# Geração final
if st.button("Gerar Nomenclatura"):
    if invalid_fields:
        st.error("❌ Corrija os campos inválidos antes de gerar a nomenclatura.")
    else:
        result = preview
        st.success("✅ Nomenclatura gerada com sucesso!")
        st.code(result, language="text")

        # Salva no histórico
        st.session_state.history.append(result)

# Histórico
if st.session_state.history:
    st.markdown("### 🕒 Histórico recente")
    for item in reversed(st.session_state.history[-5:]):
        st.code(item)
