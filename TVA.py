import streamlit as st

st.set_page_config(page_title="TAVULEUR - Calculateur de TVA")

# Entête de l'application
st.title("🍽️ TAVULEUR - Calculateur de TVA")
st.markdown("---")

# Section de saisie des données
with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        food_ttc = st.number_input("Prix TTC nourriture (€)", min_value=0.0, step=0.5, format="%.2f")
    with col2:
        drinks_ttc = st.number_input("Prix TTC boissons (€)", min_value=0.0, step=0.5, format="%.2f")
    
    submitted = st.form_submit_button("Calculer")

# Calculs lors de la soumission
if submitted:
    # Calcul des TVA
    tva_20 = drinks_ttc - (drinks_ttc  / 1.20)
    tva_10 = food_ttc - (food_ttc / 1.10)
    
    # Calcul du total TTC
    total_ttc = (food_ttc + drinks_ttc)
    
    # Affichage des résultats
    st.markdown("---")
    st.subheader("📊 Résultats")
    
    result_col1, result_col2, result_col3 = st.columns(3)
    with result_col1:
        st.metric("TVA à 20%", f"{tva_20:.2f}€")
    with result_col2:
        st.metric("TVA à 10%", f"{tva_10:.2f}€")
    with result_col3:
        st.metric("Total TTC", f"{total_ttc:.2f}€")
    
    # Section d'informations
    st.markdown("---")
    st.info("ℹ️ Rappel des taux de TVA :\n- Nourriture: 10%\n- Boissons: 20%")

# Pied de page
st.markdown("---")
st.caption("© 2024 TAVULEUR - Tous droits réservés")
