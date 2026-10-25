# Conferidor de vencimentos · app de exemplo da aula (dados fictícios)
import io
from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Conferidor de vencimentos", page_icon="📋")
st.title("Conferidor de vencimentos")
st.caption("Envie uma planilha com as colunas nome, conselho e vencimento. Dados fictícios.")

EXEMPLO = """nome,conselho,vencimento
Ana Pereira,COREN,2026-11-09
Zeca Gomes,CRM,2027-05-13
Lia Souza,CRF,2026-11-19
Rui Lima,COREN,2026-10-20
"""

arquivo = st.file_uploader("Planilha (CSV ou Excel)", type=["csv", "xlsx"])
if arquivo is None:
    st.info("Sem arquivo? Veja com os dados de exemplo abaixo.")
    df = pd.read_csv(io.StringIO(EXEMPLO))
elif arquivo.name.endswith(".xlsx"):
    df = pd.read_excel(arquivo)
else:
    df = pd.read_csv(arquivo)

df["vencimento"] = pd.to_datetime(df["vencimento"]).dt.date
dias = st.slider("Avisar quem vence nos próximos (dias)", 7, 90, 30)
df["faltam_dias"] = df["vencimento"].apply(lambda d: (d - date.today()).days)
df["situação"] = df["faltam_dias"].apply(
    lambda n: "vencido" if n < 0 else (f"vence em {n} dias" if n <= dias else "em dia"))

c1, c2, c3 = st.columns(3)
c1.metric("Vencidos", int((df["faltam_dias"] < 0).sum()))
c2.metric(f"Vencem em até {dias} dias", int(df["faltam_dias"].between(0, dias).sum()))
c3.metric("Em dia", int((df["faltam_dias"] > dias).sum()))

st.dataframe(df.sort_values("vencimento"), use_container_width=True, hide_index=True)
