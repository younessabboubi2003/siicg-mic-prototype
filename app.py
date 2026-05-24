import io
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Prototype SIICG - MIC",
    page_icon="📊",
    layout="wide",
)

PRIMARY = "#1F3A5F"
ACCENT = "#00A6D6"

st.markdown(
    f"""
    <style>
    .main {{background-color:#F7F9FC;}}
    .block-container {{padding-top: 1.8rem;}}
    .metric-card {{
        background:white; padding:18px; border-radius:16px;
        box-shadow:0 4px 14px rgba(31,58,95,0.10);
        border-left:5px solid {ACCENT};
    }}
    .title {{color:{PRIMARY}; font-weight:800; font-size:34px;}}
    .subtitle {{color:#5B677A; font-size:16px;}}
    .green {{color:#138A36; font-weight:700;}}
    .orange {{color:#C77700; font-weight:700;}}
    .red {{color:#C1121F; font-weight:700;}}
    </style>
    """,
    unsafe_allow_html=True,
)

DEFAULT_FILE = "kpi_mic_sample.csv"


@st.cache_data
def load_default_data():
    return pd.read_csv(DEFAULT_FILE)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    required = [
        "programme", "code_kpi", "intitule", "type", "frequence", "valeur",
        "cible", "unite", "responsable", "mois", "commentaire"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Colonnes manquantes dans le fichier importé : {', '.join(missing)}")
        st.stop()
    df["valeur"] = pd.to_numeric(df["valeur"], errors="coerce")
    df["cible"] = pd.to_numeric(df["cible"], errors="coerce")
    return df


def performance_ratio(row):
    # For delay indicators, lower is better.
    if "délai" in str(row["intitule"]).lower() or "delai" in str(row["intitule"]).lower():
        return row["cible"] / row["valeur"] if row["valeur"] else 0
    return row["valeur"] / row["cible"] if row["cible"] else 0


def alert_status(ratio):
    if ratio >= 0.90:
        return "VERT"
    if ratio >= 0.75:
        return "ORANGE"
    return "ROUGE"


def alert_level(status, ratio):
    if status == "VERT":
        return "N0 - Surveillance"
    if status == "ORANGE":
        return "N1 - Alerte Directeur"
    if ratio >= 0.60:
        return "N2 - Alerte SG"
    return "N3 - Alerte Ministre"


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["taux_realisation"] = df.apply(performance_ratio, axis=1)
    df["taux_realisation_pct"] = (df["taux_realisation"] * 100).round(1)
    df["statut"] = df["taux_realisation"].apply(alert_status)
    df["niveau_alerte"] = df.apply(lambda r: alert_level(r["statut"], r["taux_realisation"]), axis=1)
    df["ecart"] = df["valeur"] - df["cible"]
    return df


def status_emoji(status):
    return {"VERT": "🟢", "ORANGE": "🟠", "ROUGE": "🔴"}.get(status, "⚪")


def generate_report(df: pd.DataFrame) -> str:
    date_str = datetime.now().strftime("%d/%m/%Y")
    nb_red = (df["statut"] == "ROUGE").sum()
    nb_orange = (df["statut"] == "ORANGE").sum()
    nb_green = (df["statut"] == "VERT").sum()
    avg_perf = df["taux_realisation_pct"].mean().round(1)
    critical = df[df["statut"] == "ROUGE"].sort_values("taux_realisation")

    lines = [
        "RAPPORT MENSUEL DE PERFORMANCE - PROTOTYPE DOCG / MIC",
        f"Date de génération : {date_str}",
        "",
        "1. Synthèse exécutive",
        f"Le taux moyen de réalisation des KPI suivis est de {avg_perf}%.",
        f"Répartition des alertes : {nb_green} vertes, {nb_orange} oranges, {nb_red} rouges.",
        "",
        "2. Points d'attention prioritaires",
    ]

    if critical.empty:
        lines.append("Aucun KPI en zone rouge sur la période analysée.")
    else:
        for _, r in critical.iterrows():
            lines.append(
                f"- {r['code_kpi']} | {r['intitule']} : {r['valeur']} {r['unite']} "
                f"vs cible {r['cible']} {r['unite']} ({r['taux_realisation_pct']}%) — {r['niveau_alerte']}"
            )

    lines += [
        "",
        "3. Recommandations DOCG",
        "- Organiser une Revue de Performance Mensuelle avec les responsables des KPI rouges.",
        "- Formaliser un plan d'action correctif sous 15 jours pour chaque écart critique.",
        "- Fiabiliser les sources de données via un dictionnaire KPI et des data owners.",
        "- Consolider les commentaires analytiques avant arbitrage SG / CPP.",
    ]
    return "\n".join(lines)


st.markdown('<div class="title">Prototype Streamlit — SIICG / MIC</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Tableau de bord interactif pour le contrôle de gestion et le pilotage de la performance publique</div>',
    unsafe_allow_html=True,
)
st.divider()

with st.sidebar:
    st.image("https://dummyimage.com/600x180/1F3A5F/ffffff&text=MIC+Performance+Cockpit", use_column_width=True)
    st.header("Paramètres")
    uploaded = st.file_uploader("Importer un fichier KPI CSV ou Excel", type=["csv", "xlsx"])
    st.caption("Le fichier doit contenir les colonnes : programme, code_kpi, intitule, type, frequence, valeur, cible, unite, responsable, mois, commentaire.")

if uploaded is not None:
    if uploaded.name.endswith(".csv"):
        raw_df = pd.read_csv(uploaded)
    else:
        raw_df = pd.read_excel(uploaded)
else:
    raw_df = load_default_data()

df = enrich(normalize_columns(raw_df))

programmes = ["Tous"] + sorted(df["programme"].unique().tolist())
selected_programme = st.sidebar.selectbox("Programme", programmes)
selected_status = st.sidebar.multiselect("Statut d'alerte", ["VERT", "ORANGE", "ROUGE"], default=["VERT", "ORANGE", "ROUGE"])

filtered = df.copy()
if selected_programme != "Tous":
    filtered = filtered[filtered["programme"] == selected_programme]
filtered = filtered[filtered["statut"].isin(selected_status)]

col1, col2, col3, col4 = st.columns(4)
col1.metric("KPI suivis", len(filtered))
col2.metric("Performance moyenne", f"{filtered['taux_realisation_pct'].mean():.1f}%" if len(filtered) else "0%")
col3.metric("Alertes rouges", int((filtered["statut"] == "ROUGE").sum()))
col4.metric("Programmes", filtered["programme"].nunique())

st.subheader("Cockpit stratégique")

c1, c2 = st.columns([1.3, 1])
with c1:
    fig = px.bar(
        filtered.sort_values("taux_realisation_pct"),
        x="taux_realisation_pct",
        y="code_kpi",
        orientation="h",
        color="statut",
        color_discrete_map={"VERT": "#138A36", "ORANGE": "#F4A261", "ROUGE": "#C1121F"},
        hover_data=["intitule", "programme", "valeur", "cible", "unite", "responsable"],
        title="Taux de réalisation par KPI",
    )
    fig.update_layout(height=520, xaxis_title="% de réalisation", yaxis_title="KPI")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig2 = px.pie(
        filtered,
        names="statut",
        title="Répartition des alertes",
        color="statut",
        color_discrete_map={"VERT": "#138A36", "ORANGE": "#F4A261", "ROUGE": "#C1121F"},
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Tableau de pilotage détaillé")
display = filtered[[
    "programme", "code_kpi", "intitule", "type", "valeur", "cible", "unite",
    "taux_realisation_pct", "statut", "niveau_alerte", "responsable", "commentaire"
]].copy()
display["statut"] = display["statut"].apply(lambda s: f"{status_emoji(s)} {s}")
st.dataframe(display, use_container_width=True, hide_index=True)

st.subheader("Analyse DOCG automatique")
red_df = filtered[filtered["statut"] == "ROUGE"]
orange_df = filtered[filtered["statut"] == "ORANGE"]

if len(red_df) > 0:
    st.error(f"{len(red_df)} KPI en zone rouge : arbitrage prioritaire et plan d'action requis.")
    for _, r in red_df.iterrows():
        st.markdown(f"- **{r['code_kpi']} — {r['intitule']}** : {r['taux_realisation_pct']}% de réalisation. Responsable : {r['responsable']}.")
elif len(orange_df) > 0:
    st.warning(f"{len(orange_df)} KPI en zone orange : suivi renforcé recommandé.")
else:
    st.success("Tous les KPI filtrés sont en zone verte.")

st.subheader("Génération du rapport mensuel")
report = generate_report(filtered)
st.text_area("Rapport généré automatiquement", report, height=300)
st.download_button(
    "Télécharger le rapport mensuel DOCG (.txt)",
    data=report.encode("utf-8"),
    file_name="rapport_mensuel_docg_mic.txt",
    mime="text/plain",
)

csv_buffer = io.StringIO()
filtered.to_csv(csv_buffer, index=False)
st.download_button(
    "Exporter les données enrichies (.csv)",
    data=csv_buffer.getvalue().encode("utf-8"),
    file_name="kpi_mic_enrichis.csv",
    mime="text/csv",
)

st.divider()
st.caption("Prototype académique PFE — démonstrateur Streamlit. Objectif : matérialiser le passage du reporting statique au pilotage dynamique, alerté et actionnable.")
