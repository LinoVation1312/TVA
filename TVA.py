import streamlit as st

st.set_page_config(page_title="TAVULEUR - Calculateur TVA", layout="centered")

# Configuration CSS responsive
st.markdown("""
<style>
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
    st.session_state.input_buffer = {'Nourriture': '', 'Boissons': ''}

KEY_MAPPING = {
    'Nourriture': 'food_ttc',
    'Boissons': 'drinks_ttc'
}

# Fonctions optimisées
def update_display():
    current_key = KEY_MAPPING[st.session_state.selected_input]
    buffer = st.session_state.input_buffer[st.session_state.selected_input]
    try:
        value = float(buffer) if buffer else 0.0
    except:
        value = 0.0
    st.session_state[current_key] = value

def process_input(digit: str):
    buffer = st.session_state.input_buffer[st.session_state.selected_input]
    
    if digit == '.':
        if '.' in buffer:
            return
        if not buffer:
            buffer = '0'
    
    new_buffer = buffer + digit
    
    if len(new_buffer.replace('.', '')) > 6:
        return
    
    st.session_state.input_buffer[st.session_state.selected_input] = new_buffer
    update_display()

def clear_input():
    st.session_state.input_buffer[st.session_state.selected_input] = ''
    update_display()

# Entête
st.title("🍽️ TAVULEUR - Calculateur TVA")
st.markdown("---")

# Sélecteur de champ
current_field = st.radio("Champ actif :", 
                        ["Nourriture", "Boissons"],
                        key='selected_input',
                        horizontal=True,
                        label_visibility="collapsed")

# Réinitialisation du buffer quand on change de champ
if 'last_selected' not in st.session_state:
    st.session_state.last_selected = st.session_state.selected_input
elif st.session_state.last_selected != st.session_state.selected_input:
    st.session_state.last_selected = st.session_state.selected_input

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

# Pavé numérique
with st.container():
    st.markdown('<div class="numeric-pad">', unsafe_allow_html=True)
    
    # Rangées numériques
    cols = st.columns(3)
    digits = ['7', '8', '9', '4', '5', '6', '1', '2', '3']
    for i, digit in enumerate(digits):
        if i % 3 == 0:
            cols = st.columns(3)
        with cols[i % 3]:
            if st.button(digit, key=f"btn_{digit}", use_container_width=True):
                process_input(digit)
    
    # Contrôles finaux
    cols = st.columns(3)
    with cols[0]:
        if st.button("⌫", key="back", use_container_width=True):
            current_buffer = st.session_state.input_buffer[st.session_state.selected_input]
            st.session_state.input_buffer[st.session_state.selected_input] = current_buffer[:-1]
            update_display()
    with cols[1]:
        if st.button("0", key="0", use_container_width=True):
            process_input('0')
    with cols[2]:
        if st.button(".", key="dot", use_container_width=True):
            process_input('.')
    
    st.markdown('</div>', unsafe_allow_html=True)

# Contrôles
st.button("Effacer Champ", 
         on_click=clear_input, 
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
st.caption("© 2024 TAVULEUR - Interface tactile v3.0")
