import streamlit as st

st.set_page_config(page_title="TAVULEUR - Calculateur TVA", layout="centered")

# Configuration de l'interface tactile
st.markdown("""
<style>
    .numeric-pad button {
        font-size: 24px;
        width: 100%;
        height: 60px;
        margin: 2px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation session state
if 'food_ttc' not in st.session_state:
    st.session_state.food_ttc = 0.0
if 'drinks_ttc' not in st.session_state:
    st.session_state.drinks_ttc = 0.0
if 'selected_input' not in st.session_state:
    st.session_state.selected_input = 'Nourriture'

# Dictionnaire de correspondance pour les clés
KEY_MAPPING = {
    'Nourriture': 'food_ttc',
    'Boissons': 'drinks_ttc'
}

# Entête de l'application
st.title("🍽️ TAVULEUR - Calculateur TVA")
st.markdown("---")

# Sélecteur de champ de saisie
col1, col2 = st.columns(2)
with col1:
    st.radio("Champ actif :", 
             options=('Nourriture', 'Boissons'), 
             key='selected_input',
             horizontal=True)

# Affichage des valeurs actuelles
col1, col2 = st.columns(2)
with col1:
    st.number_input("Prix TTC nourriture (€)", 
                    min_value=0.0, 
                    value=st.session_state.food_ttc,
                    key='food_input',
                    step=0.5,
                    format="%.2f")
with col2:
    st.number_input("Prix TTC boissons (€)", 
                    min_value=0.0, 
                    value=st.session_state.drinks_ttc,
                    key='drinks_input',
                    step=0.5,
                    format="%.2f")

# Pavé numérique tactile
def update_value(digit):
    current_key = KEY_MAPPING[st.session_state.selected_input]
    current_value = st.session_state[current_key]
    new_value = str(current_value).replace('.', '') + digit
    if len(new_value) > 6:  # Limite de saisie
        return
    formatted_value = float(new_value) / 100
    st.session_state[current_key] = formatted_value

def clear_value():
    current_key = KEY_MAPPING[st.session_state.selected_input]
    st.session_state[current_key] = 0.0

# Disposition du clavier
keypad = st.container()
with keypad:
    st.markdown('<div class="numeric-pad">', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, btn in enumerate(['7', '8', '9']):
        with cols[i]:
            if st.button(btn, key=btn):
                update_value(btn)
    
    cols = st.columns(3)
    for i, btn in enumerate(['4', '5', '6']):
        with cols[i]:
            if st.button(btn, key=btn):
                update_value(btn)
    
    cols = st.columns(3)
    for i, btn in enumerate(['1', '2', '3']):
        with cols[i]:
            if st.button(btn, key=btn):
                update_value(btn)
    
    cols = st.columns(3)
    with cols[0]:
        if st.button("⌫", key="backspace"):
            current_key = KEY_MAPPING[st.session_state.selected_input]
            current = str(st.session_state[current_key]).replace('.', '')[:-1]
            st.session_state[current_key] = float(current)/100 if current else 0.0
    with cols[1]:
        if st.button("0", key="0"):
            update_value('0')
    with cols[2]:
        if st.button(".", key="decimal"):
            current_key = KEY_MAPPING[st.session_state.selected_input]
            current = str(st.session_state[current_key])
            if '.' not in current:
                st.session_state[current_key] = float(current + '.0')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Effacer tout", type="primary", use_container_width=True):
        st.session_state.food_ttc = 0.0
        st.session_state.drinks_ttc = 0.0

# Calculs
st.markdown("---")
if st.button("Calculer les TVA", type="secondary", use_container_width=True):
    tva_10 = st.session_state.food_ttc * 10 / 110
    tva_20 = st.session_state.drinks_ttc * 20 / 120
    total_ttc = st.session_state.food_ttc + st.session_state.drinks_ttc
    
    cols = st.columns(3)
    cols[0].metric("TVA Nourriture (10%)", f"{tva_10:.2f}€")
    cols[1].metric("TVA Boissons (20%)", f"{tva_20:.2f}€")
    cols[2].metric("Total TTC", f"{total_ttc:.2f}€")

# Aide
st.markdown("---")
with st.expander("ℹ️ Aide & informations"):
    st.markdown("""
    **Mode d'emploi :**
    1. Sélectionnez le champ à modifier (Nourriture/Boissons)
    2. Utilisez le clavier numérique pour entrer les montants
    3. Appuyez sur 'Calculer les TVA'
    
    **Taux de TVA appliqués :**
    - Nourriture : 10% (TTC = HT × 1.10)
    - Boissons : 20% (TTC = HT × 1.20)
    
    *Les montants saisis sont toujours TTC*
    """)

st.markdown("---")
st.caption("© 2024 TAVULEUR - Interface tactile optimisée")
