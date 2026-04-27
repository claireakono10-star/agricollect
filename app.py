import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from datetime import datetime

st.set_page_config(
    page_title="DataCollect Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.hero-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #00d4ff;
    margin-bottom: 0.2rem;
}
.subtitle {
    color: #888;
    font-size: 1rem;
    margin-bottom: 2rem;
}
.card {
    background: rgba(0,212,255,0.05);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
}
.stat-box {
    background: rgba(0,212,255,0.08);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #00d4ff;
}
.stat-label {
    font-size: 0.8rem;
    color: #888;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# Session state
if "responses" not in st.session_state:
    st.session_state.responses = []

if "form_fields" not in st.session_state:
    st.session_state.form_fields = [
        {"label": "Âge", "type": "number"},
        {"label": "Sexe", "type": "select", "options": ["Masculin", "Féminin", "Autre"]},
        {"label": "Niveau d'études", "type": "select", "options": ["Bac", "Licence", "Master", "Doctorat", "Autre"]},
        {"label": "Revenu mensuel (FCFA)", "type": "number"},
        {"label": "Satisfaction globale (1-10)", "type": "slider"},
        {"label": "Commentaire", "type": "text"},
    ]

# Sidebar
with st.sidebar:
    st.markdown("## 📊 DataCollect Pro")
    st.markdown("*INF232 EC2 · TP Individuel*")
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["🏠 Accueil", "📝 Collecte", "📊 Analyse", "⚙️ Paramètres"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    n = len(st.session_state.responses)
    st.markdown(f"""
    <div class='stat-box'>
        <div class='stat-value'>{n}</div>
        <div class='stat-label'>Réponses collectées</div>
    </div>
    """, unsafe_allow_html=True)

    if n > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        df_dl = pd.DataFrame(st.session_state.responses)
        csv_bytes = df_dl.to_csv(index=False).encode()
        st.download_button("⬇️ Exporter CSV", csv_bytes, "donnees.csv", "text/csv", use_container_width=True)

# PAGE ACCUEIL
if page == "🏠 Accueil":
    st.markdown("<div class='hero-title'>📊 DataCollect Pro</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Application de collecte et d'analyse descriptive des données · INF232 EC2</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='stat-box'><div class='stat-value'>{len(st.session_state.responses)}</div><div class='stat-label'>Réponses</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-box'><div class='stat-value'>{len(st.session_state.form_fields)}</div><div class='stat-label'>Champs</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='stat-box'><div class='stat-value'>4</div><div class='stat-label'>Critères</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='stat-box'><div class='stat-value'>{datetime.now().strftime('%H:%M')}</div><div class='stat-label'>Heure</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card'><b>📝 Collecte de données</b><br>
        <span style='color:#888'>Formulaire dynamique configurable avec validation en temps réel.</span></div>
        <div class='card'><b>📊 Analyse descriptive</b><br>
        <span style='color:#888'>Moyenne, médiane, écart-type, quartiles, distribution.</span></div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card'><b>📈 Visualisations</b><br>
        <span style='color:#888'>Histogrammes, camemberts, boxplots, heatmap de corrélation.</span></div>
        <div class='card'><b>⬇️ Export CSV</b><br>
        <span style='color:#888'>Téléchargement des données brutes depuis la barre latérale.</span></div>
        """, unsafe_allow_html=True)

    st.info("📌 TP INF232 EC2 · Python · Individuel · Date limite : 30 avril 2026")

# PAGE COLLECTE
elif page == "📝 Collecte":
    st.markdown("<div class='hero-title'>📝 Collecte de données</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Remplissez le formulaire ci-dessous</div>", unsafe_allow_html=True)

    with st.form("data_form", clear_on_submit=True):
        values = {}
        for field in st.session_state.form_fields:
            label = field["label"]
            ftype = field["type"]
            if ftype == "number":
                values[label] = st.number_input(label, min_value=0, step=1)
            elif ftype == "select":
                values[label] = st.selectbox(label, field.get("options", []))
            elif ftype == "slider":
                values[label] = st.slider(label, 1, 10, 5)
            elif ftype == "text":
                values[label] = st.text_input(label)

        submitted = st.form_submit_button("✅ Soumettre", use_container_width=True)

    if submitted:
        values["_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.responses.append(values)
        st.success(f"✅ Réponse #{len(st.session_state.responses)} enregistrée !")
        st.balloons()

    if st.session_state.responses:
        st.markdown("### Données collectées")
        df = pd.DataFrame(st.session_state.responses)
        st.dataframe(df, use_container_width=True)
        if st.button("🗑️ Effacer toutes les données"):
            st.session_state.responses = []
            st.rerun()

# PAGE ANALYSE
elif page == "📊 Analyse":
    st.markdown("<div class='hero-title'>📊 Analyse descriptive</div>", unsafe_allow_html=True)

    if not st.session_state.responses:
        st.info("💡 Aucune donnée. Allez dans 📝 Collecte pour saisir des données d'abord.")
        st.stop()

    df = pd.DataFrame(st.session_state.responses)
    if "_timestamp" in df.columns:
        df = df.drop(columns=["_timestamp"])

    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    tab1, tab2, tab3 = st.tabs(["📋 Statistiques", "📈 Graphiques", "🔗 Corrélations"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='stat-box'><div class='stat-value'>{len(df)}</div><div class='stat-label'>Observations</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='stat-box'><div class='stat-value'>{len(num_cols)}</div><div class='stat-label'>Variables numériques</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='stat-box'><div class='stat-value'>{len(cat_cols)}</div><div class='stat-label'>Variables catégorielles</div></div>", unsafe_allow_html=True)

        if num_cols:
            st.markdown("### Statistiques descriptives")
            desc = df[num_cols].describe().T
            desc.columns = ["N", "Moyenne", "Écart-type", "Min", "Q1", "Médiane", "Q3", "Max"]
            st.dataframe(desc.round(2), use_container_width=True)

        if cat_cols:
            st.markdown("### Distribution catégorielle")
            for col in cat_cols:
                vc = df[col].value_counts()
                pct = (vc / vc.sum() * 100).round(1)
                tbl = pd.DataFrame({"Effectif": vc, "Pourcentage (%)": pct})
                st.write(f"**{col}**")
                st.dataframe(tbl, use_container_width=True)

    with tab2:
        if num_cols:
            selected_num = st.selectbox("Variable numérique", num_cols)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots(figsize=(5, 3.5))
                ax.hist(df[selected_num].dropna(), bins=15, color="#00d4ff", edgecolor="white", alpha=0.85)
                ax.set_title(f"Distribution — {selected_num}")
                ax.set_xlabel(selected_num)
                ax.set_ylabel("Fréquence")
                st.pyplot(fig)
                plt.close()
            with col2:
                fig, ax = plt.subplots(figsize=(5, 3.5))
                ax.boxplot(df[selected_num].dropna(), patch_artist=True,
                           medianprops=dict(color="red", linewidth=2))
                ax.set_title(f"Boxplot — {selected_num}")
                st.pyplot(fig)
                plt.close()

        if cat_cols:
            selected_cat = st.selectbox("Variable catégorielle", cat_cols)
            vc = df[selected_cat].value_counts()
            colors = ["#00d4ff", "#7b2ff7", "#ff6b9d", "#ffd700", "#00ff88"]
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots(figsize=(5, 3.5))
                ax.bar(vc.index, vc.values, color=colors[:len(vc)])
                ax.set_title(f"Barres — {selected_cat}")
                plt.xticks(rotation=30, ha="right")
                st.pyplot(fig)
                plt.close()
            with col2:
                fig, ax = plt.subplots(figsize=(5, 3.5))
                ax.pie(vc.values, labels=vc.index, colors=colors[:len(vc)],
                       autopct="%1.1f%%", startangle=90)
                ax.set_title(f"Camembert — {selected_cat}")
                st.pyplot(fig)
                plt.close()

    with tab3:
        if len(num_cols) >= 2:
            corr = df[num_cols].corr()
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                        ax=ax, linewidths=0.5)
            ax.set_title("Matrice de corrélation")
            st.pyplot(fig)
            plt.close()

            st.markdown("### Interprétation")
            for i in range(len(num_cols)):
                for j in range(i+1, len(num_cols)):
                    r = corr.iloc[i, j]
                    if abs(r) >= 0.5:
                        direction = "positive" if r > 0 else "négative"
                        force = "forte" if abs(r) >= 0.7 else "modérée"
                        st.write(f"**r = {r:.2f}** — Corrélation {force} {direction} entre **{num_cols[i]}** et **{num_cols[j]}**")
        else:
            st.info("Besoin d'au moins 2 variables numériques.")

# PAGE PARAMETRES
elif page == "⚙️ Paramètres":
    st.markdown("<div class='hero-title'>⚙️ Paramètres</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Personnalisez les champs du formulaire</div>", unsafe_allow_html=True)

    st.markdown("### Champs actuels")
    for i, field in enumerate(st.session_state.form_fields):
        opts = ", ".join(field.get("options", [])) if "options" in field else "—"
        st.markdown(f"<div class='card'><b>{i+1}. {field['label']}</b> · <i>{field['type']}</i><br><span style='color:#888'>{opts}</span></div>", unsafe_allow_html=True)

    st.markdown("### Ajouter un champ")
    with st.form("add_field"):
        c1, c2 = st.columns(2)
        with c1:
            new_label = st.text_input("Nom du champ")
        with c2:
            new_type = st.selectbox("Type", ["number", "text", "select", "slider"])
        new_options = st.text_input("Options séparées par virgule (pour 'select')")
        add_btn = st.form_submit_button("➕ Ajouter", use_container_width=True)

    if add_btn and new_label:
        field = {"label": new_label, "type": new_type}
        if new_type == "select" and new_options:
            field["options"] = [o.strip() for o in new_options.split(",")]
        st.session_state.form_fields.append(field)
        st.success(f"Champ « {new_label} » ajouté !")
        st.rerun()
