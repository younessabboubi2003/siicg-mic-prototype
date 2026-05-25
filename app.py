import base64
import io
from pathlib import Path
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="SIICG — MIC | Pilotage de la performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Palette officielle MIC ──────────────────────────────────────
NAVY     = "#1A2B4A"
GOLD     = "#C9A961"
TEAL     = "#2D7A7A"
RED      = "#B91C1C"
ORANGE   = "#D97706"
GREEN    = "#047857"
LIGHT    = "#F5F6F8"
WHITE    = "#FFFFFF"
GRAY     = "#64748B"
LGRAY    = "#E2E8F0"

MIC_LOGO_FILE = "logo_mic.png"
MIC_LOGO_FALLBACK = "https://mcinet.gov.ma/themes/custom/mcinet/assets/image/logo-mic-2022-fr.png"

def logo_src() -> str:
    """Retourne un logo embarqué en base64 si logo_mic.png est présent.
    Sinon, utilise l’URL officielle du MIC comme fallback.
    """
    logo_path = Path(MIC_LOGO_FILE)
    if logo_path.exists():
        encoded = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    return MIC_LOGO_FALLBACK

MIC_LOGO = logo_src()

st.markdown(f"""
<style>
/* ── Reset & base ── */
html, body, [class*="css"] {{
    font-family: 'Segoe UI', Arial, sans-serif;
}}
.main {{ background-color: {LIGHT}; }}
.block-container {{ padding: 0 2rem 2rem 2rem; }}

/* ── Header band ── */
.header-band {{
    background: {NAVY};
    padding: 18px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 4px solid {GOLD};
    margin: -1.8rem -2rem 1.5rem -2rem;
}}
.header-left {{ display: flex; align-items: center; gap: 20px; }}
.header-logo {{ height: 52px; object-fit: contain; background: white; border-radius: 6px; padding: 4px 10px; }}
.header-title {{ color: {WHITE}; font-size: 20px; font-weight: 700; line-height: 1.2; }}
.header-sub {{ color: {GOLD}; font-size: 12px; font-weight: 400; margin-top: 2px; }}
.header-badge {{
    background: {GOLD}; color: {NAVY}; font-size: 11px;
    font-weight: 700; padding: 4px 12px; border-radius: 20px;
    letter-spacing: 0.5px;
}}

/* ── Section titles ── */
.section-title {{
    color: {NAVY}; font-size: 16px; font-weight: 700;
    border-left: 4px solid {GOLD}; padding-left: 12px;
    margin: 1.6rem 0 0.8rem 0;
}}

/* ── KPI metric cards ── */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 1.2rem;
}}
.kpi-card {{
    background: {WHITE};
    border-radius: 12px;
    padding: 18px 20px;
    border-top: 4px solid {NAVY};
    box-shadow: 0 2px 8px rgba(26,43,74,0.08);
}}
.kpi-card.green  {{ border-top-color: {GREEN}; }}
.kpi-card.orange {{ border-top-color: {ORANGE}; }}
.kpi-card.red    {{ border-top-color: {RED}; }}
.kpi-card.teal   {{ border-top-color: {TEAL}; }}
.kpi-label {{ font-size: 11px; color: {GRAY}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px; }}
.kpi-value {{ font-size: 28px; font-weight: 800; color: {NAVY}; line-height: 1; }}
.kpi-sub   {{ font-size: 11px; color: {GRAY}; margin-top: 4px; }}

/* ── Alert pills ── */
.pill {{
    display: inline-block; padding: 3px 10px;
    border-radius: 20px; font-size: 11px; font-weight: 700;
}}
.pill-vert   {{ background: #D1FAE5; color: #065F46; }}
.pill-orange {{ background: #FEF3C7; color: #92400E; }}
.pill-rouge  {{ background: #FEE2E2; color: #991B1B; }}

/* ── Alert banner ── */
.alert-rouge {{
    background: #FEE2E2; border-left: 5px solid {RED};
    border-radius: 8px; padding: 14px 18px; margin-bottom: 10px;
    color: #7F1D1D;
}}
.alert-orange {{
    background: #FFFBEB; border-left: 5px solid {ORANGE};
    border-radius: 8px; padding: 14px 18px; margin-bottom: 10px;
    color: #78350F;
}}
.alert-vert {{
    background: #D1FAE5; border-left: 5px solid {GREEN};
    border-radius: 8px; padding: 14px 18px; margin-bottom: 10px;
    color: #064E3B;
}}

/* ── Table ── */
.dataframe {{ font-size: 13px !important; }}
thead tr th {{ background: {NAVY} !important; color: white !important; }}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: {NAVY} !important;
}}
section[data-testid="stSidebar"] * {{
    color: {WHITE} !important;
}}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stFileUploader label {{
    color: {GOLD} !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}}
section[data-testid="stSidebar"] .stSelectbox div,
section[data-testid="stSidebar"] .stMultiSelect div {{
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.2) !important;
}}
.sidebar-logo-wrap {{
    text-align: center;
    padding: 16px 0 8px 0;
    border-bottom: 1px solid rgba(201,169,97,0.4);
    margin-bottom: 16px;
}}
.sidebar-logo {{ height: 48px; object-fit: contain; background: white; border-radius: 6px; padding: 4px 10px; }}
.sidebar-doc-title {{
    color: {GOLD} !important;
    font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.8px;
    margin-bottom: 12px; text-align: center;
}}

/* ── Report text area ── */
.stTextArea textarea {{
    font-family: 'Courier New', monospace;
    font-size: 12px;
    background: {LIGHT};
    border: 1px solid {LGRAY};
    border-radius: 8px;
}}

/* ── Download buttons ── */
.stDownloadButton > button {{
    background: {NAVY} !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
}}
.stDownloadButton > button:hover {{
    background: {TEAL} !important;
}}

/* ── Footer ── */
.footer {{
    margin-top: 2rem;
    padding: 12px 0;
    border-top: 1px solid {LGRAY};
    text-align: center;
    font-size: 11px;
    color: {GRAY};
}}

/* ── Metric override ── */
[data-testid="stMetricValue"] {{ color: {NAVY}; font-weight: 800; }}
[data-testid="stMetricLabel"] {{ font-size: 12px; color: {GRAY}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════
today_str = datetime.now().strftime("%d %B %Y")
st.markdown(f"""
<div class="header-band">
  <div class="header-left">
    <img src="{MIC_LOGO}" class="header-logo" alt="Logo MIC"/>
    <div>
      <div class="header-title">Système d’Information Intégré de Contrôle de Gestion</div>
      <div class="header-sub">Pilotage de la performance publique — Ministère de l'Industrie et du Commerce</div>
    </div>
  </div>
  <div class="header-badge">📅 {today_str}</div>
</div>
""", unsafe_allow_html=True)

st.info(
    "Ce prototype est un démonstrateur académique. "
    "Il vise à illustrer la faisabilité d’un SIICG permettant de transformer les données KPI "
    "en alertes, analyses DOCG et rapports mensuels de performance."
)

# ═══════════════════════════════════════════════════════════════
# DONNÉES
# ═══════════════════════════════════════════════════════════════
DEFAULT_FILE = "kpi_mic_sample.csv"

@st.cache_data
def load_default_data():
    return pd.read_csv(DEFAULT_FILE)

def normalize_columns(df):
    df = df.copy()
    required = ["programme","code_kpi","intitule","type","frequence",
                "valeur","cible","unite","responsable","mois","commentaire"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Colonnes manquantes : {', '.join(missing)}")
        st.stop()
    df["valeur"] = pd.to_numeric(df["valeur"], errors="coerce")
    df["cible"]  = pd.to_numeric(df["cible"],  errors="coerce")
    return df

def performance_ratio(row):
    # Cas spécifique des indicateurs de délai :
    # contrairement aux KPI classiques, une valeur plus faible est meilleure.
    # On inverse donc le ratio pour mesurer la performance par rapport à la cible.
    if "délai" in str(row["intitule"]).lower() or "delai" in str(row["intitule"]).lower():
        return row["cible"] / row["valeur"] if row["valeur"] else 0
    return row["valeur"] / row["cible"] if row["cible"] else 0

def alert_status(ratio):
    if ratio >= 0.90: return "VERT"
    if ratio >= 0.70: return "ORANGE"
    return "ROUGE"

def alert_level(status, ratio):
    if status == "VERT":   return "N0 — Surveillance"
    if status == "ORANGE": return "N1 — Alerte Directeur"
    if ratio >= 0.60:      return "N2 — Alerte SG"
    return "N3 — Alerte Ministre"

def enrich(df):
    df = df.copy()
    df["taux_realisation"]     = df.apply(performance_ratio, axis=1)
    df["taux_realisation_pct"] = (df["taux_realisation"] * 100).round(1)
    df["statut"]               = df["taux_realisation"].apply(alert_status)
    df["niveau_alerte"]        = df.apply(lambda r: alert_level(r["statut"], r["taux_realisation"]), axis=1)
    df["ecart"]                = df["valeur"] - df["cible"]
    return df

def status_emoji(status):
    return {"VERT": "🟢", "ORANGE": "🟠", "ROUGE": "🔴"}.get(status, "⚪")

def generate_report(df):
    date_str = datetime.now().strftime("%d/%m/%Y")
    nb_red    = (df["statut"] == "ROUGE").sum()
    nb_orange = (df["statut"] == "ORANGE").sum()
    nb_green  = (df["statut"] == "VERT").sum()
    avg_perf  = df["taux_realisation_pct"].mean().round(1)
    critical  = df[df["statut"] == "ROUGE"].sort_values("taux_realisation")
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
            lines.append(f"      Réalisé : {r['valeur']} {r['unite']}  |  Cible : {r['cible']} {r['unite']}  |  Taux : {r['taux_realisation_pct']}%")
            lines.append(f"      Niveau d'alerte : {r['niveau_alerte']}  |  Responsable : {r['responsable']}")
            lines.append("")
    lines += [
        "3. RECOMMANDATIONS DOCG",
        "   → Organiser la RPM sous 48h pour les KPI en zone rouge.",
        "   → Formaliser un plan d'action correctif sous 15 jours.",
        "   → Fiabiliser les sources via le dictionnaire KPI et les data owners.",
        "   → Consolider les commentaires analytiques avant arbitrage SG / CPP.",
        "",
        "──────────────────────────────────────────────────────────────",
        "Prototype académique SIICG — PFE EMI × Forvis Mazars × MIC",
    ]
    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-logo-wrap">
      <img src="{MIC_LOGO}" class="sidebar-logo" alt="Logo MIC"/>
    </div>
    <div class="sidebar-doc-title">MIC Performance Cockpit</div>
    """, unsafe_allow_html=True)

    st.markdown("**Paramètres**")
    uploaded = st.file_uploader(
        "Importer un fichier KPI CSV ou Excel",
        type=["csv", "xlsx"],
        help="Le fichier doit contenir les colonnes : programme, code_kpi, intitule, type, frequence, valeur, cible, unite, responsable, mois, commentaire."
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

    selected_status = st.multiselect(
        "Statut d'alerte",
        ["VERT", "ORANGE", "ROUGE"],
        default=["VERT", "ORANGE", "ROUGE"]
    )

    st.markdown("---")
    st.markdown('<div style="font-size:11px;color:#A0AEC0;text-align:center;">Prototype PFE — EMI × Forvis Mazars<br>Contrôle de Gestion Public — 2026</div>', unsafe_allow_html=True)

filtered = df.copy()
if selected_programme != "Tous":
    filtered = filtered[filtered["programme"] == selected_programme]
filtered = filtered[filtered["statut"].isin(selected_status)]

# ═══════════════════════════════════════════════════════════════
# MÉTRIQUES GLOBALES
# ═══════════════════════════════════════════════════════════════
avg_perf  = filtered["taux_realisation_pct"].mean() if len(filtered) else 0
nb_rouge  = int((filtered["statut"] == "ROUGE").sum())
nb_orange = int((filtered["statut"] == "ORANGE").sum())
nb_vert   = int((filtered["statut"] == "VERT").sum())
nb_prog   = filtered["programme"].nunique()

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card teal">
    <div class="kpi-label">KPI suivis</div>
    <div class="kpi-value">{len(filtered)}</div>
    <div class="kpi-sub">{nb_prog} programme(s)</div>
  </div>
  <div class="kpi-card {'green' if avg_perf >= 90 else 'orange' if avg_perf >= 75 else 'red'}">
    <div class="kpi-label">Performance moyenne</div>
    <div class="kpi-value">{avg_perf:.1f}%</div>
    <div class="kpi-sub">Taux de réalisation global</div>
  </div>
  <div class="kpi-card {'red' if nb_rouge > 0 else 'green'}">
    <div class="kpi-label">Alertes rouges</div>
    <div class="kpi-value">{nb_rouge}</div>
    <div class="kpi-sub">Action immédiate requise</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-label">KPI en zone verte</div>
    <div class="kpi-value">{nb_vert}</div>
    <div class="kpi-sub">{nb_orange} en vigilance orange</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# COCKPIT STRATÉGIQUE
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Cockpit stratégique</div>', unsafe_allow_html=True)

col_chart, col_pie = st.columns([1.5, 1])

with col_chart:
    color_map = {"VERT": GREEN, "ORANGE": ORANGE, "ROUGE": RED}
    fig = px.bar(
        filtered.sort_values("taux_realisation_pct"),
        x="taux_realisation_pct",
        y="code_kpi",
        orientation="h",
        color="statut",
        color_discrete_map=color_map,
        hover_data=["intitule","programme","valeur","cible","unite","responsable"],
        labels={"taux_realisation_pct": "% de réalisation", "code_kpi": ""},
        title="Taux de réalisation par KPI",
    )
    fig.add_vline(x=90, line_dash="dash", line_color=GREEN,  line_width=1.5, annotation_text="Seuil vert 90%",  annotation_font_size=10)
    fig.add_vline(x=70, line_dash="dash", line_color=ORANGE, line_width=1.5, annotation_text="Seuil orange 70%", annotation_font_size=10)
    fig.update_layout(
        height=420,
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Segoe UI, Arial", size=12, color=NAVY),
        title_font_size=14, title_font_color=NAVY,
        legend_title_text="Statut",
        xaxis=dict(range=[0, 115], gridcolor=LGRAY, gridwidth=0.5),
        yaxis=dict(gridcolor="white"),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

with col_pie:
    counts = filtered["statut"].value_counts().reset_index()
    counts.columns = ["statut", "nb"]
    fig2 = px.pie(
        counts, names="statut", values="nb",
        color="statut",
        color_discrete_map={"VERT": GREEN, "ORANGE": ORANGE, "ROUGE": RED},
        title="Répartition des alertes",
        hole=0.45,
    )
    fig2.update_traces(textposition="outside", textinfo="percent+label", textfont_size=12)
    fig2.update_layout(
        height=420,
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Segoe UI, Arial", size=12, color=NAVY),
        title_font_size=14, title_font_color=NAVY,
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
        annotations=[dict(
            text=f"<b>{avg_perf:.0f}%</b><br>moy.",
            x=0.5, y=0.5, font_size=16, font_color=NAVY,
            showarrow=False
        )]
    )
    st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# NIVEAUX D'ESCALADE
# ═══════════════════════════════════════════════════════════════
if len(filtered) > 0:
    col_n0, col_n1, col_n2, col_n3 = st.columns(4)
    n0 = filtered[filtered["niveau_alerte"].str.startswith("N0")]
    n1 = filtered[filtered["niveau_alerte"].str.startswith("N1")]
    n2 = filtered[filtered["niveau_alerte"].str.startswith("N2")]
    n3 = filtered[filtered["niveau_alerte"].str.startswith("N3")]
    for col, label, count, bg, fg in [
        (col_n0, "N0 · Surveillance",    len(n0), "#D1FAE5", "#065F46"),
        (col_n1, "N1 · Alerte Directeur",len(n1), "#FEF3C7", "#92400E"),
        (col_n2, "N2 · Alerte SG",       len(n2), "#FEE2E2", "#991B1B"),
        (col_n3, "N3 · Alerte Ministre", len(n3), "#FEE2E2", "#7F1D1D"),
    ]:
        col.markdown(f"""
        <div style="background:{bg};border-radius:10px;padding:12px 16px;text-align:center;margin-bottom:6px;">
          <div style="font-size:11px;color:{fg};font-weight:700;text-transform:uppercase;letter-spacing:0.5px;">{label}</div>
          <div style="font-size:26px;font-weight:800;color:{fg};">{count}</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TABLEAU DE PILOTAGE
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Tableau de pilotage détaillé</div>', unsafe_allow_html=True)

display = filtered[[
    "programme","code_kpi","intitule","type","valeur","cible","unite",
    "taux_realisation_pct","statut","niveau_alerte","responsable","commentaire"
]].copy()
display["statut"] = display.apply(lambda r: f"{status_emoji(r['statut'])} {r['statut']}", axis=1)
display = display.rename(columns={
    "programme":"Programme","code_kpi":"Code KPI","intitule":"Indicateur",
    "type":"Type","valeur":"Valeur","cible":"Cible","unite":"Unité",
    "taux_realisation_pct":"Taux %","statut":"Statut",
    "niveau_alerte":"Niveau alerte","responsable":"Responsable","commentaire":"Commentaire"
})
st.dataframe(display, use_container_width=True, hide_index=True, height=280)

# ═══════════════════════════════════════════════════════════════
# ANALYSE DOCG
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Analyse DOCG automatique</div>', unsafe_allow_html=True)

red_df    = filtered[filtered["statut"].str.contains("ROUGE")]
orange_df = filtered[filtered["statut"].str.contains("ORANGE")]

if len(red_df) > 0:
    kpi_list = "".join([f"<li><b>{r['code_kpi']} — {r['intitule']}</b> : {r['taux_realisation_pct']}% · Responsable : {r['responsable']}</li>" for _, r in red_df.iterrows()])
    st.markdown(f"""
    <div class="alert-rouge">
      <b>⚠ {len(red_df)} KPI en zone rouge — Arbitrage prioritaire et plan d'action requis</b>
      <ul style="margin:8px 0 0 0;padding-left:20px;">{kpi_list}</ul>
    </div>
    """, unsafe_allow_html=True)

if len(orange_df) > 0:
    kpi_list = "".join([f"<li>{r['code_kpi']} — {r['intitule']} : {r['taux_realisation_pct']}%</li>" for _, r in orange_df.iterrows()])
    st.markdown(f"""
    <div class="alert-orange">
      <b>🔶 {len(orange_df)} KPI en zone orange — Suivi renforcé recommandé</b>
      <ul style="margin:8px 0 0 0;padding-left:20px;">{kpi_list}</ul>
    </div>
    """, unsafe_allow_html=True)

if len(red_df) == 0 and len(orange_df) == 0:
    st.markdown('<div class="alert-vert"><b>✅ Tous les KPI filtrés sont en zone verte — Performance conforme aux cibles</b></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# RAPPORT MENSUEL
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Génération du rapport mensuel de performance</div>', unsafe_allow_html=True)

report = generate_report(filtered)

col_report, col_dl = st.columns([2, 1])
with col_report:
    st.text_area("Rapport DOCG", report, height=260, label_visibility="collapsed")

with col_dl:
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        "⬇  Télécharger le rapport mensuel (.txt)",
        data=report.encode("utf-8"),
        file_name=f"rapport_DOCG_MIC_{datetime.now().strftime('%Y%m')}.txt",
        mime="text/plain",
        use_container_width=True,
    )
    csv_buffer = io.StringIO()
    filtered.to_csv(csv_buffer, index=False)
    st.download_button(
        "⬇  Exporter les données enrichies (.csv)",
        data=csv_buffer.getvalue().encode("utf-8"),
        file_name=f"kpi_MIC_enrichis_{datetime.now().strftime('%Y%m')}.csv",
        mime="text/csv",
        use_container_width=True,
    )

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="footer">
  Prototype académique développé dans le cadre du PFE — EMI · Forvis Mazars × Ministère de l'Industrie et du Commerce · 2026<br>
  Démonstrateur SIICG — passage du reporting statique au pilotage dynamique, alerté et actionnable
</div>
""", unsafe_allow_html=True)
