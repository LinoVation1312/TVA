import streamlit as st

st.set_page_config(page_title="TAVULEUR - Calculateur TVA", layout="centered")

# Configuration CSS responsive
st.markdown("""
<style>
    div[data-testid="column"] {
        padding: 1px !important;
    }
    
    .numeric-pad {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 4px;
        width: 100%;
    }
    
    .numeric-pad button {
        font-size: 24px;
        height: 70px;
        margin: 0 !important;
        padding: 0 !important;
        border-radius: 8px !important;
    }
    
    @media (max-width: 480px) {
        .numeric-pad button {
            height: 60px;
            font-size: 20px;
        }
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
if 'input_buffer' not in st.session_state:
    st.session_state.input_buffer = ''

KEY_MAPPING = {
    'Nourriture': 'food_ttc',
    'Boissons': 'drinks_ttc'
}

# Fonctions optimisées
def update_display(value: float):
    current_key = KEY_MAPPING[st.session_state.selected_input]
    st.session_state[current_key] = value

def process_input(digit: str):
    if digit == '.' and '.' in st.session_state.input_buffer:
        return
    if len(st.session_state.input_buffer) >= 6:
        return
    st.session_state.input_buffer += digit
    update_display(float(st.session_state.input_buffer) if st.session_state.input_buffer else update_display(0.0)

def clear_input():
    st.session_state.input_buffer = ''
    update_display(0.0)

# Entête
st.title("🍽️ TAVULEUR - Calculateur TVA")
st.markdown("---")

# Sélecteur de champ
current_field = st.radio("Champ actif :", 
                        ["Nourriture", "Boissons"],
                        horizontal=True,
                        label_visibility="collapsed")

# Affichage valeurs
col1, col2 = st.columns(2)
with col1:
    food = st.number_input("Nourriture (€ TTC)", 
                          value=st.session_state.food_ttc,
                          format="%.2f",
                          key="food_display")
with col2:
    drinks = st.number_input("Boissons (€ TTC)", 
                            value=st.session_state.drinks_ttc,
                            format="%.2f",
                            key="drinks_display")

# Pavé numérique optimisé
with st.container():
    st.markdown('<div class="numeric-pad">', unsafe_allow_html=True)
    
    # Rangée 1
    cols = st.columns(3)
    with cols[0]:
        if st.button("7", use_container_width=True):
            process_input('7')
    with cols[1]:
        if st.button("8", use_container_width=True):
            process_input('8')
    with cols[2]:
        if st.button("9", use_container_width=True):
            process_input('9')
    
    # Rangée 2
    cols = st.columns(3)
    with cols[0]:
        if st.button("4", use_container_width=True):
            process_input('4')
    with cols[1]:
        if st.button("5", use_container_width=True):
            process_input('5')
    with cols[2]:
        if st.button("6", use_container_width=True):
            process_input('6')
    
    # Rangée 3
    cols = st.columns(3)
    with cols[0]:
        if st.button("1", use_container_width=True):
            process_input('1')
    with cols[1]:
        if st.button("2", use_container_width=True):
            process_input('2')
    with cols[2]:
        if st.button("3", use_container_width=True):
            process_input('3')
    
    # Rangée contrôle
    cols = st.columns(3)
    with cols[0]:
        if st.button("⌫", use_container_width=True):
            st.session_state.input_buffer = st.session_state.input_buffer[:-1]
            update_display(float(st.session_state.input_buffer) if st.session_state.input_buffer else 0.0)
    with cols[1]:
        if st.button("0", use_container_width=True):
            process_input('0')
    with cols[2]:
        if st.button(".", use_container_width=True):
            process_input('.')
    
    st.markdown('</div>', unsafe_allow_html=True)

# Contrôles principaux
st.button("Effacer tout", 
         on_click=lambda: [clear_input(), update_display(0.0)], 
         type="primary")

# Calculs
if st.button("Calculer", type="secondary", use_container_width=True):
    tva_10 = st.session_state.food_ttc * 10 / 110
    tva_20 = st.session_state.drinks_ttc * 20 / 120
    total = st.session_state.food_ttc + st.session_state.drinks_ttc
    
    cols = st.columns(3)
    cols[0].metric("TVA 10%", f"{tva_10:.2f}€")
    cols[1].metric("TVA 20%", f"{tva_20:.2f}€")
    cols[2].metric("Total", f"{total:.2f}€")

st.markdown("---")
st.caption("© 2024 TAVULEUR - Interface tactile v2.0")
