import re
from datetime import date
import streamlit as st

st.set_page_config(page_title="Plusoft - Nomenclatura Padrão", layout="centered")

st.title("📋 Plusoft - Nomenclatura Padrão")
st.markdown("Preencha os campos abaixo para gerar a nomenclatura padronizada da campanha CRM.")

# Campo de data com calendário
data_input = st.date_input("Data da campanha:", value=date.today())
data = data_input.strftime("%Y%m%d")  # Converte para o formato aaaammdd

canal = st.selectbox(
    "Canal:",
    ["Email", "SMS", "SMS - Com LP", "Push", "WhatsApp", "Social (Meta-Face)", "Extração"]
)

tipo_campanha = st.selectbox(
    "Tipo de Campanha:",
    ["Pontual", "Recorrente"]
)

responsavel = st.selectbox(
    "Responsável:",
    ["Interno", "Externo"]
)

marca = st.text_input("Marca/Bandeira:")
publico = st.text_input("Público:")
plano_envio = st.text_input("Plano/Nome de Envio:")

# Botão de gerar nomenclatura
if st.button("Gerar Nomenclatura"):
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

    responsavel_abbr = {
        "Interno": "int",
        "Externo": "ext"
    }

    # Abreviações e formatações
    channel = canal_abbr.get(canal, "")
    responsible = responsavel_abbr.get(responsavel, "")
    brand = marca.replace(" ", "_")
    audience = publico.replace(" ", "_")
    send_name = plano_envio.replace(" ", "_")

    # Validação dos campos de texto
    if not re.match(r"^[a-zA-Z0-9_\-ç]+$", brand) or \
       not re.match(r"^[a-zA-Z0-9_\-ç]+$", audience) or \
       not re.match(r"^[a-zA-Z0-9_\-ç]+$", send_name):
        st.error("❌ Os campos 'Marca/Bandeira', 'Público' e 'Plano/Nome de Envio' devem conter apenas letras, números e traços.")
        st.stop()

    # Resultado final
    result = f"{data}-{channel}-{tipo_campanha}-{responsible}-{brand}-{audience}-{send_name}".lower()
    st.success("✅ Nomenclatura gerada com sucesso!")
    st.code(result, language="text")

    # Botão copiar
    st.button("📋 Copiar Resultado", on_click=lambda: st.toast("Copie o texto manualmente (função nativa do navegador)."))
