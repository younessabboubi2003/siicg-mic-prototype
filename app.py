import io
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="SIICG — MIC | Executive Performance Cockpit",
    page_icon="assets/logo_mic.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PALETTE
# ============================================================
NAVY = "#1E2A44"
NAVY_2 = "#243B63"
GOLD = "#C8A96B"
TEAL = "#1F7A7A"
RED = "#B91C1C"
ORANGE = "#D97706"
GREEN = "#047857"
LIGHT = "#F7F8FA"
WHITE = "#FFFFFF"
GRAY = "#6B7280"
LGRAY = "#E5E7EB"
SOFT_BLUE = "#EAF3F8"

MIC_LOGO = "assets/logo_mic.png"
DEFAULT_FILE = "kpi_mic_sample.csv"

# ============================================================
# CSS — PREMIUM CONSULTING STYLE
# ============================================================
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    font-family: 'Segoe UI', Arial, sans-serif;
}}

.main {{
    background-color: {LIGHT};
}}

.block-container {{
    padding: 0 2.6rem 2.5rem 2.6rem;
    max-width: 1380px;
}}

.header-band {{
    background: linear-gradient(90deg, {NAVY} 0%, {NAVY_2} 100%);
    padding: 18px 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 3px solid {GOLD};
    margin: -1.8rem -2.6rem 1.4rem -2.6rem;
}}

.header-left {{
    display: flex;
    align-items: center;
    gap: 18px;
}}

.header-logo {{
    height: 52px;
    object-fit: contain;
    background: white;
    border-radius: 6px;
    padding: 5px 12px;
}}

.header-title {{
    color: {WHITE};
    font-size: 22px;
    font-weight: 750;
    line-height: 1.15;
}}

.header-sub {{
    color: {GOLD};
    font-size: 12px;
    margin-top: 4px;
}}

.header-badge {{
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    color: {WHITE};
    font-size: 12px;
    font-weight: 600;
    padding: 8px 14px;
    border-radius: 999px;
}}

.method-box {{
    background: {SOFT_BLUE};
    border-left: 4px solid {TEAL};
    color: {NAVY};
    padding: 14px 18px;
    border-radius: 8px;
    margin: 0 0 1.2rem 0;
    font-size: 14px;
    line-height: 1.5;
}}

.section-title {{
    color: {NAVY};
    font-size: 17px;
    font-weight: 750;
    border-left: 4px solid {GOLD};
    padding-left: 12px;
    margin: 1.4rem 0 0.8rem 0;
}}

.exec-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 1.2rem;
}}

.exec-card {{
    background: {WHITE};
    border: 1px solid {LGRAY};
    border-radius: 12px;
    padding: 18px 18px;
    box-shadow: 0 2px 8px rgba(30,42,68,0.045);
}}

.exec-card .label {{
    font-size: 11px;
    color: {GRAY};
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 8px;
}}

.exec-card .value {{
    font-size: 30px;
    font-weight: 800;
    color: {NAVY};
    line-height: 1;
}}

.exec-card .sub {{
    font-size: 11px;
    color: {GRAY};
    margin-top: 7px;
}}

.exec-card.green {{ border-top: 3px solid {GREEN}; }}
.exec-card.orange {{ border-top: 3px solid {ORANGE}; }}
.exec-card.red {{ border-top: 3px solid {RED}; }}
.exec-card.gold {{ border-top: 3px solid {GOLD}; }}

.decision-card {{
    background: {WHITE};
    border: 1px solid {LGRAY};
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    box-shadow: 0 1px 5px rgba(30,42,68,0.04);
}}

.decision-red {{ border-left: 5px solid {RED}; }}
.decision-orange {{ border-left: 5px solid {ORANGE}; }}
.decision-green {{ border-left: 5px solid {GREEN}; }}

.decision-title {{
    color: {NAVY};
    font-weight: 750;
    font-size: 13px;
}}

.decision-meta {{
    color: {GRAY};
    font-size: 12px;
    margin-top: 4px;
}}

.decision-action {{
    color: {NAVY};
    font-size: 12px;
    margin-top: 7px;
    background: #F9FAFB;
    padding: 7px 10px;
    border-radius: 6px;
}}

.gov-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1rem;
}}

.gov-card {{
    background: {WHITE};
    border: 1px solid {LGRAY};
    border-radius: 10px;
    padding: 14px;
    text-align: center;
}}

.gov-card .gov-label {{
    font-size: 11px;
    color: {GRAY};
    text-transform: uppercase;
    font-weight: 700;
}}

.gov-card .gov-value {{
    color: {NAVY};
    font-size: 16px;
    font-weight: 750;
    margin-top: 6px;
}}

.assistant-panel {{
    background: {WHITE};
    border: 1px solid {LGRAY};
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(30,42,68,0.045);
    margin-top: 0.2rem;
}}

.assistant-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}}

.assistant-title {{
    color: {NAVY};
    font-size: 15px;
    font-weight: 800;
}}

.assistant-badge {{
    background: #ECFDF5;
    color: {GREEN};
    border: 1px solid #A7F3D0;
    font-size: 10px;
    padding: 3px 8px;
    border-radius: 999px;
    font-weight: 800;
}}

.assistant-note {{
    background: #F8FAFC;
    color: {GRAY};
    border-left: 3px solid {GOLD};
    padding: 9px 10px;
    border-radius: 7px;
    font-size: 12px;
    margin-bottom: 12px;
    line-height: 1.45;
}}

.assistant-answer {{
    background: #F9FAFB;
    border: 1px solid {LGRAY};
    border-radius: 10px;
    padding: 12px;
    color: {NAVY};
    font-size: 13px;
    line-height: 1.55;
    margin-top: 10px;
}}

section[data-testid="stSidebar"] {{
    background: {NAVY} !important;
}}

section[data-testid="stSidebar"] * {{
    color: {WHITE} !important;
}}

section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stFileUploader label,
section[data-testid="stSidebar"] .stTextInput label {{
    color: {GOLD} !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}}

.sidebar-logo-wrap {{
    text-align: center;
    padding: 14px 0 8px 0;
    border-bottom: 1px solid rgba(200,169,107,0.35);
    margin-bottom: 16px;
}}

.sidebar-logo {{
    height: 48px;
    object-fit: contain;
    background: white;
    border-radius: 6px;
    padding: 5px 12px;
}}

.sidebar-doc-title {{
    color: {GOLD} !important;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 12px;
    text-align: center;
}}

.stDownloadButton > button {{
    background: {NAVY} !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 650 !important;
    padding: 10px 18px !important;
}}

.stDownloadButton > button:hover {{
    background: {TEAL} !important;
}}

.footer {{
    margin-top: 2rem;
    padding: 12px 0;
    border-top: 1px solid {LGRAY};
    text-align: center;
    font-size: 11px;
    color: {GRAY};
}}

.stTextArea textarea {{
    font-family: 'Courier New', monospace;
    font-size: 12px;
    background: #F9FAFB;
    border: 1px solid {LGRAY};
    border-radius: 8px;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid {LGRAY};
    border-radius: 10px;
    overflow: hidden;
}}

/* Sidebar input readability fix */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] select {{
    color: #1E2A44 !important;
    background-color: #FFFFFF !important;
}}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {{
    color: #1E2A44 !important;
}}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
}}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {{
    background-color: #F8FAFC !important;
    border: 1px dashed #CBD5E1 !important;
}}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {{
    color: #1E2A44 !important;
}}

section[data-testid="stSidebar"] span[data-baseweb="tag"] {{
    border-radius: 8px !important;
    font-weight: 700 !important;
    color: white !important;
}}

.status-chip {{
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    color: white;
    font-size: 11px;
    font-weight: 800;
    margin: 2px 4px 2px 0;
}}

.status-chip.green {{ background: #047857; }}
.status-chip.orange {{ background: #D97706; }}
.status-chip.red {{ background: #B91C1C; }}


/* Cleaner sidebar filter controls */
.sidebar-status-card {{
    border-radius: 10px;
    padding: 9px 10px;
    margin: 6px 0;
    font-weight: 800;
    font-size: 12px;
    letter-spacing: .3px;
    text-align: center;
    color: white;
}}

.sidebar-status-card.vert {{
    background: #047857;
}}

.sidebar-status-card.orange {{
    background: #D97706;
}}

.sidebar-status-card.rouge {{
    background: #B91C1C;
}}

/* KPI TYPE CARDS — visibility fix */
.sidebar-type-card {{
    border-radius: 10px;
    padding: 9px 10px;
    margin: 6px 0;
    font-weight: 800;
    font-size: 12px;
    letter-spacing: .3px;
    text-align: center;
    background: #C8A96B !important;
    color: #1E2A44 !important;
    border: 1px solid #C8A96B !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}}

/* Better readability for Streamlit widgets inside sidebar */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] select {{
    color: #1E2A44 !important;
    background-color: #FFFFFF !important;
}}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
}}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {{
    color: #1E2A44 !important;
}}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {{
    background-color: #F8FAFC !important;
    border: 1px dashed #CBD5E1 !important;
}}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {{
    color: #1E2A44 !important;
}}


/* Documentary repository cards */
.doc-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 12px;
}}

.doc-card {{
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(30,42,68,0.045);
    min-height: 185px;
}}

.doc-title {{
    color: #1E2A44;
    font-weight: 800;
    font-size: 14px;
    margin-bottom: 8px;
}}

.doc-desc {{
    color: #6B7280;
    font-size: 12px;
    line-height: 1.55;
    margin-bottom: 12px;
}}

.doc-badge {{
    display: inline-block;
    padding: 4px 9px;
    border-radius: 999px;
    color: white;
    font-size: 10px;
    font-weight: 800;
    margin-bottom: 10px;
    letter-spacing: .3px;
}}

.doc-badge.reg {{
    background: #1E2A44;
}}

.doc-badge.gov {{
    background: #C8A96B;
    color: #1E2A44;
}}

.doc-badge.cdg {{
    background: #1F7A7A;
}}

.doc-badge.perf {{
    background: #047857;
}}

.doc-badge.circ {{
    background: #D97706;
}}

.doc-badge.ref {{
    background: #6B7280;
}}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
today_str = datetime.now().strftime("%d %B %Y")

st.markdown(f"""
<div class="header-band">
  <div class="header-left">
    <img src="{MIC_LOGO}" class="header-logo" alt="Logo MIC"/>
    <div>
      <div class="header-title">SIICG — Executive Performance Steering Cockpit</div>
      <div class="header-sub">Système d’Information Intégré de Contrôle de Gestion · Ministère de l’Industrie et du Commerce</div>
    </div>
  </div>
  <div class="header-badge">📅 {today_str}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="method-box">
<b>Strategic Performance Steering Cockpit.</b> Le prototype SIICG illustre la transition d’un reporting fragmenté vers une plateforme intégrée de pilotage stratégique capable de transformer les données de performance en mécanismes d’alerte, d’analyse, d’arbitrage et d’aide à la décision pour les instances de gouvernance du Ministère.
</div>
""", unsafe_allow_html=True)

# ============================================================
# DATA FUNCTIONS
# ============================================================
@st.cache_data
def load_default_data():
    return pd.read_csv(DEFAULT_FILE)


def normalize_columns(df):
    df = df.copy()
    required = [
        "programme", "code_kpi", "intitule", "type", "frequence",
        "valeur", "cible", "unite", "responsable", "mois", "commentaire"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Colonnes manquantes : {', '.join(missing)}")
        st.stop()

    df["valeur"] = pd.to_numeric(df["valeur"], errors="coerce")
    df["cible"] = pd.to_numeric(df["cible"], errors="coerce")
    df["type"] = df["type"].astype(str).str.upper().str.strip()
    return df


def performance_ratio(row):
    """
    Pour les KPI de type délai, la logique est inversée :
    plus la valeur réelle est faible, meilleure est la performance.
    """
    label = str(row["intitule"]).lower()
    if "délai" in label or "delai" in label:
        return row["cible"] / row["valeur"] if row["valeur"] else 0
    return row["valeur"] / row["cible"] if row["cible"] else 0


def alert_status(ratio):
    if ratio >= 0.90:
        return "VERT"
    if ratio >= 0.70:
        return "ORANGE"
    return "ROUGE"


def alert_level(status, ratio):
    if status == "VERT":
        return "N0 — Surveillance"
    if status == "ORANGE":
        return "N1 — Alerte Directeur"
    if ratio >= 0.60:
        return "N2 — Alerte SG"
    return "N3 — Alerte Ministre"


def enrich(df):
    df = df.copy()
    df["taux_realisation"] = df.apply(performance_ratio, axis=1)
    df["taux_realisation_pct"] = (df["taux_realisation"] * 100).round(1)
    df["statut"] = df["taux_realisation"].apply(alert_status)
    df["niveau_alerte"] = df.apply(lambda r: alert_level(r["statut"], r["taux_realisation"]), axis=1)
    df["ecart"] = df["valeur"] - df["cible"]
    return df


def status_emoji(status):
    return {"VERT": "🟢", "ORANGE": "🟠", "ROUGE": "🔴"}.get(status, "⚪")


def generate_report(df):
    date_str = datetime.now().strftime("%d/%m/%Y")
    nb_red = (df["statut"] == "ROUGE").sum()
    nb_orange = (df["statut"] == "ORANGE").sum()
    nb_green = (df["statut"] == "VERT").sum()
    avg_perf = df["taux_realisation_pct"].mean().round(1) if len(df) else 0
    critical = df[df["statut"] == "ROUGE"].sort_values("taux_realisation")

    lines = [
        "╔══════════════════════════════════════════════════════════════╗",
        "║   RAPPORT MENSUEL DE PERFORMANCE — DOCG / MIC               ║",
        f"║   Date : {date_str:<52}║",
        "╚══════════════════════════════════════════════════════════════╝",
        "",
        "1. SYNTHÈSE EXÉCUTIVE",
        f"   Taux moyen de réalisation : {avg_perf}%",
        f"   Alertes : {nb_green} vertes · {nb_orange} oranges · {nb_red} rouges",
        "",
        "2. POINTS D'ATTENTION PRIORITAIRES",
    ]

    if critical.empty:
        lines.append("   Aucun KPI en zone rouge sur la période analysée.")
    else:
        for _, r in critical.iterrows():
            lines.append(f"   ⚠  {r['code_kpi']} — {r['intitule']}")
            lines.append(f"      Réalisé : {r['valeur']} {r['unite']} | Cible : {r['cible']} {r['unite']} | Taux : {r['taux_realisation_pct']}%")
            lines.append(f"      Niveau d'alerte : {r['niveau_alerte']} | Responsable : {r['responsable']}")
            lines.append("")

    lines += [
        "3. RECOMMANDATIONS DOCG",
        "   → Organiser la RPM sous 48h pour les KPI en zone rouge.",
        "   → Formaliser un plan d'action correctif sous 15 jours.",
        "   → Fiabiliser les sources via le dictionnaire KPI et les data owners.",
        "   → Consolider les commentaires analytiques avant arbitrage SG / CPP.",
        "",
        "4. GOUVERNANCE DES DONNÉES",
        "   → Vérifier la complétude des sources.",
        "   → Certifier mensuellement les données par les Data Owners.",
        "   → Conserver l'historique des modifications pour auditabilité.",
        "",
        "──────────────────────────────────────────────────────────────",
        "Prototype académique SIICG — PFE EMI × Forvis Mazars × MIC",
    ]

    return "\n".join(lines)


def build_assistant_response(question, data):
    q = str(question).lower().strip()

    if data.empty:
        return "Aucune donnée n’est disponible avec les filtres actuels. Veuillez élargir les filtres pour générer une analyse."

    nb_total = len(data)
    avg = data["taux_realisation_pct"].mean().round(1)
    red = data[data["statut"] == "ROUGE"].sort_values("taux_realisation_pct")
    orange = data[data["statut"] == "ORANGE"].sort_values("taux_realisation_pct")
    green = data[data["statut"] == "VERT"]
    worst = data.sort_values("taux_realisation_pct").head(3)

    if any(k in q for k in ["critique", "critiques", "rouge", "urgence", "risque"]):
        if red.empty:
            return (
                f"**Lecture SIICG :** aucun KPI n’est actuellement en zone rouge sur le périmètre filtré. "
                f"La performance moyenne est de **{avg}%**. Le point de vigilance principal concerne les KPI en zone orange, "
                f"qui doivent être suivis en RPM afin d’éviter une dégradation vers un niveau d’alerte SG."
            )
        lines = ["**KPI critiques identifiés :**"]
        for _, r in red.iterrows():
            lines.append(f"- **{r['code_kpi']} — {r['intitule']}** : {r['taux_realisation_pct']}% · {r['niveau_alerte']} · Responsable : {r['responsable']}")
        lines.append("\n**Décision recommandée :** inscrire ces KPI à l’ordre du jour de la prochaine RPM et demander un plan d’action sous 15 jours.")
        return "\n".join(lines)

    if any(k in q for k in ["orange", "vigilance", "suivi"]):
        if orange.empty:
            return "Aucun KPI en zone orange sur le périmètre filtré. Le dispositif ne présente pas de vigilance intermédiaire à ce stade."
        lines = [f"**{len(orange)} KPI en vigilance orange nécessitent un suivi renforcé :**"]
        for _, r in orange.iterrows():
            lines.append(f"- **{r['code_kpi']}** · {r['intitule']} : {r['taux_realisation_pct']}% · Responsable : {r['responsable']}")
        lines.append("\n**Lecture DOCG :** ces indicateurs ne nécessitent pas encore un arbitrage SG, mais doivent faire l’objet d’un suivi rapproché en RPM.")
        return "\n".join(lines)

    if any(k in q for k in ["synthèse", "synthese", "resume", "résumé", "docg", "rapport"]):
        return (
            f"**Synthèse DOCG — périmètre filtré**\n\n"
            f"- KPI suivis : **{nb_total}**\n"
            f"- Performance moyenne : **{avg}%**\n"
            f"- KPI verts : **{len(green)}**\n"
            f"- KPI orange : **{len(orange)}**\n"
            f"- KPI rouges : **{len(red)}**\n\n"
            f"**Message exécutif :** le dispositif présente une performance globalement maîtrisée, mais les KPI en vigilance orange doivent être traités comme des signaux faibles afin d’éviter un glissement vers une alerte SG."
        )

    if any(k in q for k in ["programme", "programmes", "tension", "p428", "p431", "p470"]):
        grouped = data.groupby("programme").agg(
            perf=("taux_realisation_pct", "mean"),
            red=("statut", lambda s: (s == "ROUGE").sum()),
            orange=("statut", lambda s: (s == "ORANGE").sum()),
            total=("code_kpi", "count"),
        ).reset_index().sort_values(["red", "orange", "perf"], ascending=[False, False, True])

        lines = ["**Lecture par programme :**"]
        for _, r in grouped.iterrows():
            lines.append(f"- **{r['programme']}** : performance moyenne {r['perf']:.1f}% · {int(r['red'])} rouge · {int(r['orange'])} orange · {int(r['total'])} KPI")
        lines.append("\n**Interprétation :** les programmes avec le plus d’alertes orange/rouge doivent être priorisés dans l’agenda RPM.")
        return "\n".join(lines)

    if any(k in q for k in ["recommandation", "action", "actions", "corriger", "correctif", "arbitrage"]):
        return "\n".join([
            "**Recommandations SIICG :**",
            "1. Prioriser les KPI rouges dans la prochaine Revue de Performance Mensuelle.",
            "2. Demander un plan d’action documenté aux responsables des KPI sous cible.",
            "3. Fiabiliser les données via un Data Owner clairement désigné pour chaque indicateur.",
            "4. Suivre les KPI orange comme signaux faibles avant escalade au SG.",
            "5. Formaliser les décisions dans le rapport mensuel DOCG."
        ])

    if any(k in q for k in ["moins de", "inférieur", "inferieur", "80", "75", "90", "sous cible"]):
        threshold = 80
        if "75" in q:
            threshold = 75
        elif "90" in q:
            threshold = 90
        under = data[data["taux_realisation_pct"] < threshold].sort_values("taux_realisation_pct")
        if under.empty:
            return f"Aucun KPI n’est inférieur à {threshold}% sur le périmètre filtré."
        lines = [f"**KPI inférieurs à {threshold}% :**"]
        for _, r in under.iterrows():
            lines.append(f"- **{r['code_kpi']} — {r['intitule']}** : {r['taux_realisation_pct']}% · {r['statut']}")
        return "\n".join(lines)

    if any(k in q for k in ["pire", "faible", "top", "priorité", "priorite"]):
        lines = ["**Top 3 priorités de pilotage :**"]
        for _, r in worst.iterrows():
            lines.append(f"- **{r['code_kpi']} — {r['intitule']}** : {r['taux_realisation_pct']}% · {r['niveau_alerte']}")
        lines.append("\n**Décision proposée :** concentrer la prochaine RPM sur ces indicateurs avant d’élargir l’analyse au reste du portefeuille KPI.")
        return "\n".join(lines)

    return (
        "Je peux analyser le portefeuille KPI selon plusieurs angles : **KPI critiques**, **vigilance orange**, "
        "**synthèse DOCG**, **programmes sous tension**, **recommandations**, ou **KPI sous un seuil**. "
        "Exemple : *Quels sont les KPI critiques ?*"
    )


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-logo-wrap">
      <img src="{MIC_LOGO}" class="sidebar-logo" alt="Logo MIC"/>
    </div>
    <div class="sidebar-doc-title">Performance Steering Cockpit</div>
    """, unsafe_allow_html=True)

    st.markdown("**Paramètres de pilotage**")

    uploaded = st.file_uploader(
        "Importer un fichier KPI CSV ou Excel",
        type=["csv", "xlsx"],
        help="Colonnes requises : programme, code_kpi, intitule, type, frequence, valeur, cible, unite, responsable, mois, commentaire."
    )

    if uploaded is not None:
        if uploaded.name.endswith(".csv"):
            raw_df = pd.read_csv(uploaded)
        else:
            raw_df = pd.read_excel(uploaded)
    else:
        raw_df = load_default_data()

    df = enrich(normalize_columns(raw_df))

    st.markdown("---")
    programmes = ["Tous"] + sorted(df["programme"].unique().tolist())
    selected_programme = st.selectbox("Programme", programmes)

    st.markdown("**Statut d'alerte**")
    col_v, col_o, col_r = st.columns(3)

    with col_v:
        st.markdown('<div class="sidebar-status-card vert">VERT</div>', unsafe_allow_html=True)
        status_vert = st.checkbox("VERT", value=True, label_visibility="collapsed", key="status_vert")

    with col_o:
        st.markdown('<div class="sidebar-status-card orange">ORANGE</div>', unsafe_allow_html=True)
        status_orange = st.checkbox("ORANGE", value=True, label_visibility="collapsed", key="status_orange")

    with col_r:
        st.markdown('<div class="sidebar-status-card rouge">ROUGE</div>', unsafe_allow_html=True)
        status_rouge = st.checkbox("ROUGE", value=True, label_visibility="collapsed", key="status_rouge")

    selected_status = []
    if status_vert:
        selected_status.append("VERT")
    if status_orange:
        selected_status.append("ORANGE")
    if status_rouge:
        selected_status.append("ROUGE")

    st.markdown("**Nature KPI**")
    available_types = sorted(df["type"].unique().tolist())
    selected_type = []

    for kpi_type in available_types:
        st.markdown(f'<div class="sidebar-type-card">{kpi_type}</div>', unsafe_allow_html=True)
        if st.checkbox(kpi_type, value=True, label_visibility="collapsed", key=f"type_{kpi_type}"):
            selected_type.append(kpi_type)

    st.markdown("---")
    st.markdown(
        '<div style="font-size:11px;color:#CBD5E1;text-align:center;">Prototype PFE — EMI × Forvis Mazars<br>Contrôle de Gestion Public — 2026</div>',
        unsafe_allow_html=True
    )

filtered = df.copy()
if selected_programme != "Tous":
    filtered = filtered[filtered["programme"] == selected_programme]
filtered = filtered[filtered["statut"].isin(selected_status)]
filtered = filtered[filtered["type"].isin(selected_type)]

# ============================================================
# CALCULATED INDICATORS
# ============================================================
avg_perf = filtered["taux_realisation_pct"].mean() if len(filtered) else 0
nb_rouge = int((filtered["statut"] == "ROUGE").sum())
nb_orange = int((filtered["statut"] == "ORANGE").sum())
nb_vert = int((filtered["statut"] == "VERT").sum())
nb_prog = filtered["programme"].nunique()
programmes_sous_tension = filtered[filtered["statut"] == "ROUGE"]["programme"].nunique()
maturity_score = max(0, min(100, round((avg_perf * 0.65) + ((nb_vert / len(filtered)) * 35 if len(filtered) else 0), 1)))

# ============================================================
# TABS
# ============================================================
tab_exec, tab_archi, tab_arbitrage, tab_heatmap, tab_rpm, tab_docs = st.tabs(["Cockpit exécutif", "Architecture SIICG", "Centre d’Arbitrage", "Performance Heatmap", "RPM Executive Mode", "Référentiel documentaire"])

with tab_exec:
    st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)

    global_card_status = "green" if avg_perf >= 90 else "orange" if avg_perf >= 70 else "red"
    critical_card_status = "red" if nb_rouge > 0 else "green"
    maturity_status = "green" if maturity_score >= 85 else "orange" if maturity_score >= 70 else "red"

    st.markdown(f"""
    <div class="exec-grid">
      <div class="exec-card {global_card_status}">
        <div class="label">Performance globale</div>
        <div class="value">{avg_perf:.1f}%</div>
        <div class="sub">Taux de réalisation moyen</div>
      </div>
      <div class="exec-card {critical_card_status}">
        <div class="label">KPI critiques</div>
        <div class="value">{nb_rouge}</div>
        <div class="sub">Arbitrage requis si rouge</div>
      </div>
      <div class="exec-card gold">
        <div class="label">Programmes sous tension</div>
        <div class="value">{programmes_sous_tension}</div>
        <div class="sub">{nb_prog} programme(s) suivis</div>
      </div>
      <div class="exec-card {maturity_status}">
        <div class="label">Maturité pilotage</div>
        <div class="value">{maturity_score}/100</div>
        <div class="sub">Score synthétique SIICG</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # STRATEGIC ALERTS + ASSISTANT
    # --------------------------------------------------------
    left_decision, right_assistant = st.columns([1.8, 1])

    with left_decision:
        st.markdown('<div class="section-title">Strategic Alerts & Arbitrages</div>', unsafe_allow_html=True)

        if len(filtered) == 0:
            st.info("Aucune donnée disponible avec les filtres sélectionnés.")
        else:
            top_attention = filtered.sort_values("taux_realisation_pct").head(min(5, len(filtered)))
            for _, r in top_attention.iterrows():
                cls = "decision-red" if r["statut"] == "ROUGE" else "decision-orange" if r["statut"] == "ORANGE" else "decision-green"
                action = "Arbitrage SG / CPP recommandé" if r["statut"] == "ROUGE" else "Suivi renforcé en RPM" if r["statut"] == "ORANGE" else "Surveillance standard"
                st.markdown(f"""
                <div class="decision-card {cls}">
                    <div class="decision-title">{status_emoji(r['statut'])} {r['code_kpi']} — {r['intitule']}</div>
                    <div class="decision-meta">Programme : {r['programme']} · Réalisation : {r['taux_realisation_pct']}% · Responsable : {r['responsable']}</div>
                    <div class="decision-action"><b>Décision proposée :</b> {action}</div>
                </div>
                """, unsafe_allow_html=True)

    with right_assistant:
        st.markdown('<div class="section-title">Assistant décisionnel SIICG</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="assistant-panel">
          <div class="assistant-header">
            <div class="assistant-title">DOCG Performance Assistant</div>
            <div class="assistant-badge">RULE-BASED AI</div>
          </div>
          <div class="assistant-note">
            Interrogez les KPI filtrés pour obtenir une synthèse, les alertes prioritaires, les programmes sous tension ou les recommandations DOCG.
          </div>
        </div>
        """, unsafe_allow_html=True)

        quick_question = st.selectbox(
            "Questions rapides",
            [
                "Quels sont les KPI critiques ?",
                "Donne-moi une synthèse DOCG.",
                "Quels programmes sont sous tension ?",
                "Quels KPI sont inférieurs à 80% ?",
                "Quelles actions correctives recommandes-tu ?",
                "Quels sont les KPI en vigilance orange ?",
            ],
        )

        custom_question = st.text_input(
            "Question personnalisée",
            placeholder="Ex. Quels KPI nécessitent un arbitrage SG ?"
        )

        question = custom_question if custom_question else quick_question
        answer = build_assistant_response(question, filtered)

        st.markdown('<div class="assistant-answer">', unsafe_allow_html=True)
        st.markdown(answer)
        st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # EXECUTIVE ANALYTICS
    # --------------------------------------------------------
    st.markdown('<div class="section-title">Executive Analytics</div>', unsafe_allow_html=True)

    col_chart, col_type = st.columns([1.5, 1])

    with col_chart:
        if len(filtered):
            color_map = {"VERT": GREEN, "ORANGE": ORANGE, "ROUGE": RED}
            fig = px.bar(
                filtered.sort_values("taux_realisation_pct"),
                x="taux_realisation_pct",
                y="code_kpi",
                orientation="h",
                color="statut",
                color_discrete_map=color_map,
                hover_data=["intitule", "programme", "valeur", "cible", "unite", "responsable"],
                labels={"taux_realisation_pct": "% de réalisation", "code_kpi": ""},
                title="Performance par KPI stratégique",
            )
            fig.add_vline(x=90, line_dash="dash", line_color=GREEN, line_width=1.4, annotation_text="", annotation_font_size=10)
            fig.add_vline(x=70, line_dash="dash", line_color=ORANGE, line_width=1.4, annotation_text="", annotation_font_size=10)
            fig.update_layout(
                height=410,
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(family="Segoe UI, Arial", size=12, color=NAVY),
                title_font_size=14,
                title_font_color=NAVY,
                legend_title_text="Statut",
                xaxis=dict(range=[0, max(115, filtered["taux_realisation_pct"].max() + 10)], gridcolor=LGRAY, gridwidth=0.5),
                yaxis=dict(gridcolor="white"),
                margin=dict(l=20, r=120, t=70, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.12,
                    xanchor="right",
                    x=1
                ),
            )
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Aucune donnée à afficher.")

    with col_type:
        if len(filtered):
            type_counts = filtered["type"].value_counts().reset_index()
            type_counts.columns = ["type", "nb"]
            fig_type = px.pie(
                type_counts,
                names="type",
                values="nb",
                title="Outcome vs Output",
                hole=0.55,
                color_discrete_sequence=[TEAL, GOLD, NAVY_2],
            )
            fig_type.update_traces(textposition="outside", textinfo="percent+label", textfont_size=12)
            fig_type.update_layout(
                height=410,
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(family="Segoe UI, Arial", size=12, color=NAVY),
                title_font_size=14,
                title_font_color=NAVY,
                showlegend=False,
                margin=dict(l=20, r=120, t=70, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.12,
                    xanchor="right",
                    x=1
                ),
            )
            st.plotly_chart(fig_type, width="stretch")
        else:
            st.info("Aucune donnée à afficher.")

    # --------------------------------------------------------
    # GOVERNANCE & RPM
    # --------------------------------------------------------
    st.markdown('<div class="section-title">Governance & RPM</div>', unsafe_allow_html=True)

    last_update = datetime.now().strftime("%d/%m/%Y")
    data_quality = round(min(100, 82 + nb_vert * 1.5 - nb_rouge * 4), 1)

    st.markdown(f"""
    <div class="gov-grid">
      <div class="gov-card">
        <div class="gov-label">Prochaine RPM</div>
        <div class="gov-value">M+1 · à planifier</div>
      </div>
      <div class="gov-card">
        <div class="gov-label">Dernière MAJ</div>
        <div class="gov-value">{last_update}</div>
      </div>
      <div class="gov-card">
        <div class="gov-label">Qualité data estimée</div>
        <div class="gov-value">{data_quality}%</div>
      </div>
      <div class="gov-card">
        <div class="gov-label">Owner dispositif</div>
        <div class="gov-value">DOCG</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    n0 = filtered[filtered["niveau_alerte"].str.startswith("N0")]
    n1 = filtered[filtered["niveau_alerte"].str.startswith("N1")]
    n2 = filtered[filtered["niveau_alerte"].str.startswith("N2")]
    n3 = filtered[filtered["niveau_alerte"].str.startswith("N3")]

    col_n0, col_n1, col_n2, col_n3 = st.columns(4)
    for col, label, count, bg, fg in [
        (col_n0, "N0 · Surveillance", len(n0), "#D1FAE5", "#065F46"),
        (col_n1, "N1 · Alerte Directeur", len(n1), "#FEF3C7", "#92400E"),
        (col_n2, "N2 · Alerte SG", len(n2), "#FEE2E2", "#991B1B"),
        (col_n3, "N3 · Alerte Ministre", len(n3), "#FEE2E2", "#7F1D1D"),
    ]:
        col.markdown(f"""
        <div style="background:{bg};border-radius:10px;padding:12px 16px;text-align:center;margin-bottom:8px;border:1px solid rgba(0,0,0,0.04);">
          <div style="font-size:11px;color:{fg};font-weight:750;text-transform:uppercase;letter-spacing:0.5px;">{label}</div>
          <div style="font-size:26px;font-weight:800;color:{fg};">{count}</div>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # DETAILED TABLE
    # --------------------------------------------------------
    st.markdown('<div class="section-title">Tableau de pilotage détaillé</div>', unsafe_allow_html=True)

    display = filtered[[
        "programme", "code_kpi", "intitule", "type", "valeur", "cible", "unite",
        "taux_realisation_pct", "statut", "niveau_alerte", "responsable", "commentaire"
    ]].copy()

    display["statut"] = display.apply(lambda r: f"{status_emoji(r['statut'])} {r['statut']}", axis=1)
    display = display.rename(columns={
        "programme": "Programme",
        "code_kpi": "Code KPI",
        "intitule": "Indicateur",
        "type": "Type",
        "valeur": "Valeur",
        "cible": "Cible",
        "unite": "Unité",
        "taux_realisation_pct": "Taux %",
        "statut": "Statut",
        "niveau_alerte": "Niveau alerte",
        "responsable": "Responsable",
        "commentaire": "Commentaire",
    })

    st.dataframe(display, width="stretch", hide_index=True, height=285)

    # --------------------------------------------------------
    # DOCG ANALYSIS
    # --------------------------------------------------------
    st.markdown('<div class="section-title">Analyse DOCG automatique</div>', unsafe_allow_html=True)

    red_df = filtered[filtered["statut"] == "ROUGE"]
    orange_df = filtered[filtered["statut"] == "ORANGE"]

    if len(red_df) > 0:
        kpi_list = "".join([
            f"<li><b>{r['code_kpi']} — {r['intitule']}</b> : {r['taux_realisation_pct']}% · Responsable : {r['responsable']}</li>"
            for _, r in red_df.iterrows()
        ])
        st.markdown(f"""
        <div class="decision-card decision-red">
          <div class="decision-title">⚠ {len(red_df)} KPI en zone rouge — Arbitrage prioritaire requis</div>
          <ul style="margin:8px 0 0 0;padding-left:20px;">{kpi_list}</ul>
        </div>
        """, unsafe_allow_html=True)

    if len(orange_df) > 0:
        kpi_list = "".join([
            f"<li>{r['code_kpi']} — {r['intitule']} : {r['taux_realisation_pct']}%</li>"
            for _, r in orange_df.iterrows()
        ])
        st.markdown(f"""
        <div class="decision-card decision-orange">
          <div class="decision-title">🔶 {len(orange_df)} KPI en zone orange — Suivi renforcé recommandé</div>
          <ul style="margin:8px 0 0 0;padding-left:20px;">{kpi_list}</ul>
        </div>
        """, unsafe_allow_html=True)

    if len(red_df) == 0 and len(orange_df) == 0:
        st.markdown("""
        <div class="decision-card decision-green">
          <div class="decision-title">✅ Tous les KPI filtrés sont en zone verte — Performance conforme aux cibles</div>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------
    st.markdown('<div class="section-title">Génération du rapport mensuel de performance</div>', unsafe_allow_html=True)

    report = generate_report(filtered)

    col_report, col_dl = st.columns([2, 1])
    with col_report:
        st.text_area("Rapport DOCG", report, height=280, label_visibility="collapsed")

    with col_dl:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            "⬇ Télécharger le rapport mensuel (.txt)",
            data=report.encode("utf-8"),
            file_name=f"rapport_DOCG_MIC_{datetime.now().strftime('%Y%m')}.txt",
            mime="text/plain",
            width="stretch",
        )
        csv_buffer = io.StringIO()
        filtered.to_csv(csv_buffer, index=False)
        st.download_button(
            "⬇ Exporter les données enrichies (.csv)",
            data=csv_buffer.getvalue().encode("utf-8"),
            file_name=f"kpi_MIC_enrichis_{datetime.now().strftime('%Y%m')}.csv",
            mime="text/csv",
            width="stretch",
        )

with tab_archi:
    st.markdown('<div class="section-title">Architecture décisionnelle SIICG</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="method-box">
    Cette vue présente la logique cible du SIICG : les données issues des systèmes métiers sont collectées,
    normalisées, certifiées puis transformées en informations décisionnelles exploitables par la DOCG,
    les Responsables de Programmes, le Secrétariat Général et les instances de pilotage.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:white;border:1px solid {LGRAY};border-radius:12px;padding:24px;box-shadow:0 2px 8px rgba(30,42,68,0.045);">
      <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px;align-items:stretch;text-align:center;">
        <div style="background:#F3F4F6;border-radius:10px;padding:18px;">
            <b>Sources métiers</b><br><span style="font-size:12px;color:{GRAY};">GID · SIRH · DPCI · EEP · Excel</span>
        </div>
        <div style="font-size:26px;color:{GOLD};align-self:center;">→</div>
        <div style="background:#EAF3F8;border-radius:10px;padding:18px;">
            <b>ETL & contrôle</b><br><span style="font-size:12px;color:{GRAY};">Nettoyage · normalisation · qualité</span>
        </div>
        <div style="font-size:26px;color:{GOLD};align-self:center;">→</div>
        <div style="background:#ECFDF5;border-radius:10px;padding:18px;">
            <b>Entrepôt KPI</b><br><span style="font-size:12px;color:{GRAY};">Historique · dictionnaire · auditabilité</span>
        </div>
        <div style="background:{NAVY};color:white;border-radius:10px;padding:18px;">
            <b>SIICG</b><br><span style="font-size:12px;color:#CBD5E1;">Cockpit · assistant · alertes · RPM · rapports</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Chaîne de valeur décisionnelle</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:white;border:1px solid {LGRAY};border-radius:12px;padding:20px;">
      <ol style="color:{NAVY};line-height:1.9;">
        <li><b>Collecter</b> les données KPI auprès des directions, DPCI et systèmes métiers.</li>
        <li><b>Certifier</b> les données par les Data Owners et la DOCG.</li>
        <li><b>Calculer</b> automatiquement les taux de réalisation, écarts et statuts d’alerte.</li>
        <li><b>Analyser</b> les écarts via l’assistant décisionnel SIICG.</li>
        <li><b>Arbitrer</b> les actions correctives au niveau Directeur, SG ou Ministre.</li>
        <li><b>Documenter</b> les décisions via le rapport mensuel de performance.</li>
      </ol>
    </div>
    """, unsafe_allow_html=True)



with tab_arbitrage:
    st.markdown('<div class="section-title">Centre d’Arbitrage & Plans d’Actions</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="method-box">
    Cette vue matérialise la logique d’arbitrage du SIICG en associant chaque KPI critique à un plan d’action,
    un niveau d’escalade, un responsable de traitement et un horizon de résolution afin de soutenir les Revues
    de Performance Mensuelles et les arbitrages du Secrétariat Général.
    </div>
    """, unsafe_allow_html=True)

    critical_df = filtered.copy()

    def priority_level(status):
        if status == "ROUGE":
            return "Critique"
        if status == "ORANGE":
            return "Élevée"
        return "Normale"

    def recommended_action(row):
        if row["statut"] == "ROUGE":
            return "Plan d’action immédiat + arbitrage SG"
        if row["statut"] == "ORANGE":
            return "Suivi renforcé en RPM"
        return "Maintien du monitoring"

    def deadline(status):
        if status == "ROUGE":
            return "15 jours"
        if status == "ORANGE":
            return "30 jours"
        return "Monitoring continu"

    critical_df["Priorité"] = critical_df["statut"].apply(priority_level)
    critical_df["Action corrective"] = critical_df.apply(recommended_action, axis=1)
    critical_df["Deadline"] = critical_df["statut"].apply(deadline)
    critical_df["Escalade"] = critical_df["niveau_alerte"]

    arb_display = critical_df[[
        "programme",
        "code_kpi",
        "intitule",
        "taux_realisation_pct",
        "statut",
        "Priorité",
        "Action corrective",
        "Escalade",
        "responsable",
        "Deadline"
    ]].copy()

    arb_display = arb_display.rename(columns={
        "programme": "Programme",
        "code_kpi": "KPI",
        "intitule": "Indicateur",
        "taux_realisation_pct": "Taux %",
        "statut": "Statut",
        "responsable": "Responsable"
    })

    st.dataframe(
        arb_display,
        width="stretch",
        hide_index=True,
        height=450
    )

    st.markdown('<div class="section-title">Vue exécutive des arbitrages</div>', unsafe_allow_html=True)

    nb_critique = len(filtered[filtered["statut"] == "ROUGE"])
    nb_elevee = len(filtered[filtered["statut"] == "ORANGE"])
    nb_normale = len(filtered[filtered["statut"] == "VERT"])

    st.markdown(f"""
    <div class="exec-grid">
      <div class="exec-card red">
        <div class="label">Arbitrages critiques</div>
        <div class="value">{nb_critique}</div>
        <div class="sub">Escalade SG / Ministre</div>
      </div>

      <div class="exec-card orange">
        <div class="label">Actions prioritaires</div>
        <div class="value">{nb_elevee}</div>
        <div class="sub">Suivi renforcé RPM</div>
      </div>

      <div class="exec-card green">
        <div class="label">KPI stabilisés</div>
        <div class="value">{nb_normale}</div>
        <div class="sub">Performance conforme</div>
      </div>

      <div class="exec-card gold">
        <div class="label">Décisions à documenter</div>
        <div class="value">{nb_critique + nb_elevee}</div>
        <div class="sub">Traçabilité DOCG</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Logique de gouvernance SIICG</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:white;border:1px solid #E5E7EB;border-radius:12px;padding:18px;line-height:1.8;">
    <b>Niveau 1 — Responsable opérationnel :</b> traitement des KPI en vigilance orange.<br><br>

    <b>Niveau 2 — Directeur / Responsable de Programme :</b> validation des plans correctifs et suivi des KPI sous tension.<br><br>

    <b>Niveau 3 — Secrétariat Général :</b> arbitrage des KPI critiques impactant les objectifs stratégiques du Ministère.<br><br>

    <b>Niveau 4 — Gouvernance stratégique :</b> consolidation des décisions et suivi des engagements dans les Revues de Performance Mensuelles.
    </div>
    """, unsafe_allow_html=True)



with tab_heatmap:
    st.markdown('<div class="section-title">Performance Heatmap — Cartographie des tensions</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="method-box">
    Cette vue consolide les indicateurs par programme afin d’identifier rapidement les zones de tension,
    les concentrations d’alertes et les priorités de pilotage. Elle permet une lecture visuelle orientée arbitrage.
    </div>
    """, unsafe_allow_html=True)

    if len(filtered) == 0:
        st.info("Aucune donnée disponible avec les filtres sélectionnés.")
    else:
        heatmap_df = filtered.copy()
        heatmap_df["Score couleur"] = heatmap_df["statut"].map({"VERT": 3, "ORANGE": 2, "ROUGE": 1})
        heatmap_df["KPI court"] = heatmap_df["code_kpi"]

        pivot = heatmap_df.pivot_table(
            index="programme",
            columns="KPI court",
            values="Score couleur",
            aggfunc="mean"
        )

        fig_heat = px.imshow(
            pivot,
            color_continuous_scale=[
                [0.0, RED],
                [0.5, ORANGE],
                [1.0, GREEN],
            ],
            aspect="auto",
            labels=dict(x="KPI", y="Programme", color="Statut"),
            title="Heatmap des statuts KPI par programme"
        )

        fig_heat.update_layout(
            height=420,
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(family="Segoe UI, Arial", size=12, color=NAVY),
            title_font_size=15,
            title_font_color=NAVY,
            margin=dict(l=20, r=20, t=50, b=20),
            coloraxis_showscale=False
        )

        st.plotly_chart(fig_heat, width="stretch")

        st.markdown('<div class="section-title">Lecture exécutive</div>', unsafe_allow_html=True)

        programme_summary = filtered.groupby("programme").agg(
            performance_moyenne=("taux_realisation_pct", "mean"),
            kpi_rouges=("statut", lambda s: (s == "ROUGE").sum()),
            kpi_oranges=("statut", lambda s: (s == "ORANGE").sum()),
            kpi_verts=("statut", lambda s: (s == "VERT").sum()),
            total_kpi=("code_kpi", "count")
        ).reset_index()

        programme_summary["Niveau de tension"] = programme_summary.apply(
            lambda r: "Critique" if r["kpi_rouges"] > 0 else "Sous vigilance" if r["kpi_oranges"] > 0 else "Maîtrisé",
            axis=1
        )

        programme_summary = programme_summary.rename(columns={
            "programme": "Programme",
            "performance_moyenne": "Performance moyenne %",
            "kpi_rouges": "KPI rouges",
            "kpi_oranges": "KPI orange",
            "kpi_verts": "KPI verts",
            "total_kpi": "Total KPI"
        })

        programme_summary["Performance moyenne %"] = programme_summary["Performance moyenne %"].round(1)

        st.dataframe(programme_summary, width="stretch", hide_index=True, height=250)

        st.markdown("""
        <div style="background:white;border:1px solid #E5E7EB;border-radius:12px;padding:16px;line-height:1.7;">
        <b>Interprétation :</b> la heatmap permet d’identifier les programmes nécessitant une attention prioritaire en RPM.
        Les zones orange traduisent des signaux faibles à traiter avant dégradation ; les zones rouges déclenchent une logique d’arbitrage.
        </div>
        """, unsafe_allow_html=True)


with tab_rpm:
    st.markdown('<div class="section-title">RPM Executive Mode — Préparation de la Revue de Performance Mensuelle</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="method-box">
    Ce module prépare une synthèse exécutive directement exploitable en Revue de Performance Mensuelle :
    messages clés, KPI prioritaires, décisions proposées et actions de suivi.
    </div>
    """, unsafe_allow_html=True)

    if len(filtered) == 0:
        st.info("Aucune donnée disponible avec les filtres sélectionnés.")
    else:
        red_df = filtered[filtered["statut"] == "ROUGE"].sort_values("taux_realisation_pct")
        orange_df = filtered[filtered["statut"] == "ORANGE"].sort_values("taux_realisation_pct")
        worst_df = filtered.sort_values("taux_realisation_pct").head(5)

        rpm_priority = "Critique" if len(red_df) > 0 else "Sous vigilance" if len(orange_df) > 0 else "Maîtrisé"
        rpm_color = RED if rpm_priority == "Critique" else ORANGE if rpm_priority == "Sous vigilance" else GREEN

        st.markdown(f"""
        <div style="background:white;border:1px solid #E5E7EB;border-radius:12px;padding:18px;margin-bottom:14px;">
            <div style="font-size:12px;color:#6B7280;text-transform:uppercase;font-weight:800;letter-spacing:.5px;">Niveau global RPM</div>
            <div style="font-size:32px;color:{rpm_color};font-weight:850;margin-top:6px;">{rpm_priority}</div>
            <div style="font-size:13px;color:#6B7280;margin-top:5px;">
                Performance moyenne : <b>{avg_perf:.1f}%</b> · KPI orange : <b>{nb_orange}</b> · KPI rouges : <b>{nb_rouge}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_msg, col_dec = st.columns([1, 1])

        with col_msg:
            st.markdown('<div class="section-title">Messages clés pour la RPM</div>', unsafe_allow_html=True)

            msg_1 = "Aucun KPI rouge n’est identifié sur le périmètre filtré." if len(red_df) == 0 else f"{len(red_df)} KPI rouge(s) nécessitent un arbitrage prioritaire."
            msg_2 = f"{len(orange_df)} KPI en vigilance orange doivent être suivis afin d’éviter une dégradation."
            msg_3 = f"La performance moyenne du portefeuille KPI est de {avg_perf:.1f}%."

            st.markdown(f"""
            <div class="decision-card decision-orange">
                <div class="decision-title">Message 1</div>
                <div class="decision-meta">{msg_1}</div>
            </div>
            <div class="decision-card decision-orange">
                <div class="decision-title">Message 2</div>
                <div class="decision-meta">{msg_2}</div>
            </div>
            <div class="decision-card decision-green">
                <div class="decision-title">Message 3</div>
                <div class="decision-meta">{msg_3}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_dec:
            st.markdown('<div class="section-title">Décisions proposées</div>', unsafe_allow_html=True)

            st.markdown("""
            <div style="background:white;border:1px solid #E5E7EB;border-radius:12px;padding:16px;line-height:1.8;">
            <b>1.</b> Valider le portefeuille des KPI sous tension.<br>
            <b>2.</b> Demander un plan d’action aux responsables des KPI orange / rouge.<br>
            <b>3.</b> Fixer une échéance de suivi dans la prochaine RPM.<br>
            <b>4.</b> Documenter les décisions dans le rapport mensuel DOCG.<br>
            <b>5.</b> Escalader au SG les écarts critiques ou persistants.
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">Top priorités à inscrire à l’ordre du jour</div>', unsafe_allow_html=True)

        rpm_display = worst_df[[
            "programme",
            "code_kpi",
            "intitule",
            "taux_realisation_pct",
            "statut",
            "niveau_alerte",
            "responsable"
        ]].copy()

        rpm_display = rpm_display.rename(columns={
            "programme": "Programme",
            "code_kpi": "KPI",
            "intitule": "Indicateur",
            "taux_realisation_pct": "Taux %",
            "statut": "Statut",
            "niveau_alerte": "Niveau d’escalade",
            "responsable": "Responsable"
        })

        st.dataframe(rpm_display, width="stretch", hide_index=True, height=260)

        rpm_note = f"""NOTE DE PRÉPARATION RPM — SIICG / MIC
Date : {datetime.now().strftime('%d/%m/%Y')}

1. Synthèse exécutive
- Performance moyenne : {avg_perf:.1f}%
- KPI rouges : {nb_rouge}
- KPI orange : {nb_orange}
- KPI verts : {nb_vert}
- Niveau global : {rpm_priority}

2. Points à traiter
- Prioriser les KPI les moins performants.
- Documenter les causes des écarts.
- Formaliser les plans d’action et responsables.
- Fixer une échéance de suivi pour la prochaine RPM.

3. Décision attendue
- Validation des actions correctives.
- Escalade des KPI critiques au niveau approprié.
"""

        st.download_button(
            "⬇ Télécharger la note de préparation RPM (.txt)",
            data=rpm_note.encode("utf-8"),
            file_name=f"note_RPM_SIICG_MIC_{datetime.now().strftime('%Y%m')}.txt",
            mime="text/plain",
            width="stretch",
        )



with tab_docs:
    st.markdown('<div class="section-title">Référentiel documentaire & cadre réglementaire</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="method-box">
    Ce module centralise le socle réglementaire, méthodologique et opérationnel du SIICG afin de garantir
    la traçabilité, l’alignement institutionnel et la standardisation des pratiques de pilotage de la performance.
    </div>
    """, unsafe_allow_html=True)

    documents = [
        {
            "title": "Loi Organique n°130-13 relative à la Loi de Finances",
            "file": "Loi Organique 130-13pdf.pdf",
            "category": "Réglementaire",
            "badge": "reg",
            "description": "Socle juridique de la budgétisation par programme, de la performance publique et de la logique objectifs-résultats."
        },
        {
            "title": "Charte de gestion budgétaire axée sur la performance — MIC",
            "file": "Charte de gestion.pdf",
            "category": "Gouvernance",
            "badge": "gov",
            "description": "Document interne structurant les rôles, responsabilités, principes de gestion, dialogue de gestion et pilotage de la performance."
        },
        {
            "title": "Guide pratique du contrôle de gestion 2024",
            "file": "Guide contrôle de gestion 2024.pdf",
            "category": "Contrôle de gestion",
            "badge": "cdg",
            "description": "Référentiel méthodologique pour la mise en œuvre du contrôle de gestion public, des tableaux de bord, indicateurs et analyses d’écarts."
        },
        {
            "title": "Guide de la performance 2022",
            "file": "Guide de la performance 2022.pdf",
            "category": "Performance",
            "badge": "perf",
            "description": "Guide de référence sur la démarche de performance, la structuration des objectifs, indicateurs, projets et rapports de performance."
        },
        {
            "title": "Pacte interne de contrôle de gestion — MIC",
            "file": "Pacte interne.pdf",
            "category": "Gouvernance",
            "badge": "gov",
            "description": "Document d’engagement interne encadrant la mise en œuvre du contrôle de gestion au sein du Ministère."
        },
        {
            "title": "Cadre stratégique de réforme de la GFP 2026-2032",
            "file": "CSR_GFP.pdf",
            "category": "Réforme GFP",
            "badge": "ref",
            "description": "Cadre stratégique national de réforme de la gestion des finances publiques, orienté résultats, transparence et redevabilité."
        },
        {
            "title": "Circulaire n°09/2021",
            "file": "Circulaire 09_2021.pdf",
            "category": "Circulaire",
            "badge": "circ",
            "description": "Circulaire relative au rôle et aux attributions du responsable de programme dans le cadre de la LOF."
        },
        {
            "title": "Circulaire n°12/2021",
            "file": "Circulaire 12_2021.pdf",
            "category": "Circulaire",
            "badge": "circ",
            "description": "Circulaire relative aux référentiels de la budgétisation par programme axée sur les résultats."
        },
        {
            "title": "Circulaire n°09/2024",
            "file": "Circulaire 9_2024.pdf",
            "category": "Circulaire",
            "badge": "circ",
            "description": "Circulaire relative aux modalités de mise en œuvre du contrôle de gestion au niveau des départements ministériels."
        },
    ]

    col_search, col_cat = st.columns([2, 1])
    with col_search:
        search_doc = st.text_input(
            "Rechercher dans le référentiel",
            placeholder="Ex. LOF, contrôle de gestion, performance, circulaire..."
        )

    with col_cat:
        categories = ["Tous"] + sorted(list({d["category"] for d in documents}))
        selected_doc_category = st.selectbox("Catégorie", categories)

    filtered_docs = documents.copy()

    if search_doc:
        q = search_doc.lower()
        filtered_docs = [
            d for d in filtered_docs
            if q in d["title"].lower()
            or q in d["category"].lower()
            or q in d["description"].lower()
            or q in d["file"].lower()
        ]

    if selected_doc_category != "Tous":
        filtered_docs = [d for d in filtered_docs if d["category"] == selected_doc_category]

    st.markdown(f"""
    <div class="exec-grid">
      <div class="exec-card gold">
        <div class="label">Documents référencés</div>
        <div class="value">{len(documents)}</div>
        <div class="sub">Socle réglementaire & méthodologique</div>
      </div>
      <div class="exec-card green">
        <div class="label">Catégories</div>
        <div class="value">{len(categories)-1}</div>
        <div class="sub">Réglementaire · CDG · Performance</div>
      </div>
      <div class="exec-card orange">
        <div class="label">Documents filtrés</div>
        <div class="value">{len(filtered_docs)}</div>
        <div class="sub">Résultat de la recherche</div>
      </div>
      <div class="exec-card gold">
        <div class="label">Usage SIICG</div>
        <div class="value">100%</div>
        <div class="sub">Traçabilité & conformité</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Bibliothèque documentaire</div>', unsafe_allow_html=True)

    if len(filtered_docs) == 0:
        st.info("Aucun document ne correspond aux filtres sélectionnés.")
    else:
        for i in range(0, len(filtered_docs), 3):
            cols = st.columns(3)
            for col, doc in zip(cols, filtered_docs[i:i+3]):
                with col:
                    st.markdown(f"""
                    <div class="doc-card">
                        <div class="doc-badge {doc['badge']}">{doc['category']}</div>
                        <div class="doc-title">{doc['title']}</div>
                        <div class="doc-desc">{doc['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    file_path = Path(doc["file"])
                    if file_path.exists():
                        with open(file_path, "rb") as f:
                            st.download_button(
                                "⬇ Télécharger",
                                data=f.read(),
                                file_name=doc["file"],
                                mime="application/pdf",
                                width="stretch",
                                key=f"download_{doc['file']}"
                            )
                    else:
                        st.warning(f"Fichier introuvable : {doc['file']}")

    st.markdown('<div class="section-title">Lecture gouvernance</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:white;border:1px solid #E5E7EB;border-radius:12px;padding:18px;line-height:1.8;">
    <b>Valeur ajoutée du module :</b> ce référentiel permet de rattacher chaque logique du SIICG à un socle documentaire clair :
    cadre légal, circulaires, guides méthodologiques, charte de gestion, pacte interne et documents de réforme de la GFP.<br><br>

    <b>Impact sur le dispositif cible :</b> amélioration de la traçabilité, harmonisation des pratiques, sécurisation méthodologique
    des KPI et appui aux Revues de Performance Mensuelles.
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
  SIICG — Executive Governance Cockpit  
Architecture décisionnelle de pilotage de la performance publique intégrant monitoring KPI, alertes stratégiques, arbitrages et assistance DOCG.

Developed by Youness ABBOUBI  
Industrial Engineering Student — École Mohammadia d’Ingénieurs (EMI)  
Strategy & Public Sector Consulting — Forvis Mazars Morocco

📧 abboubiyouness78@gmail.com  
🔗 linkedin.com/in/younessabboubi  
🌐 mic-performance-dashboard.streamlit.app
</div>
""", unsafe_allow_html=True)