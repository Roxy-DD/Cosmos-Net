import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import os
from cosmos_net import load_or_create_brain, save_brain, get_star_map_figure, CosmosResonator

# --- Language & Configuration ---
if 'language' not in st.session_state:
    st.session_state.language = 'CN'

TRANSLATIONS = {
    'CN': {
        'page_title': "Cosmos-Net: 数字生命",
        'sidebar_title': "🌌 观测台",
        'version': "Cosmos-Net V7.5 (GPL-3.0)",
        'brain_core': "### 🧠 大脑核心 (Neural Core)",
        'select_brain': "选择大脑存档:",
        'new_brain': "或新建大脑 (名称):",
        'load_create': "加载/创建",
        'current_core': "当前核心",
        'star_count': "恒星数量",
        'reset_u': "重置当前宇宙",
        'reset_msg': "💥 宇宙已重置 (Big Bang)!",
        'info': "Cosmos-Net 是一个基于物理引力的自组织神经网络。每一个样本都可能成为一颗恒星。",
        'main_title': "Cosmos-Net: 数字生命交互界面",
        'perception': "👁️ 感知 (Perception)",
        'upload_label': "给予视觉刺激 (上传手写数字/图片)",
        'input_caption': "输入影像",
        'brain_consciousness': "大脑意识",
        'interaction': "### ⚡ 交互 (Interaction)",
        'interaction_hint': "如果不输入，默认判定为正确。",
        'correct_label': "纠正标签 (Correct Label)",
        'send_wave': "发送精神波 (Evolve)",
        'evolve_msg': "⚡ [演化]: {} 完成。",
        'topology': "🌌 宇宙拓扑 (Cosmos Topology)",
        'void_msg': "宇宙一片虚无... 请通过更左侧的面板喂养数据。",
        'init_msg': "初始化..."
    },
    'EN': {
        'page_title': "Cosmos-Net: Digital Life",
        'sidebar_title': "🌌 Observatory",
        'version': "Cosmos-Net V7.5 (GPL-3.0)",
        'brain_core': "### 🧠 Neural Core",
        'select_brain': "Select Brain Archive:",
        'new_brain': "Or Create New Brain (Name):",
        'load_create': "Load/Create",
        'current_core': "Current Core",
        'star_count': "Star Count",
        'reset_u': "Reset Current Cosmos",
        'reset_msg': "💥 Cosmos Reset (Big Bang)!",
        'info': "Cosmos-Net is a self-organizing neural network based on physical gravity. Every sample can become a star.",
        'main_title': "Cosmos-Net: Digital Life Interface",
        'perception': "👁️ Perception",
        'upload_label': "Visual Stimulus (Upload Digit/Image)",
        'input_caption': "Input Image",
        'brain_consciousness': "Brain Consciousness",
        'interaction': "### ⚡ Interaction",
        'interaction_hint': "If left empty, prediction is assumed correct.",
        'correct_label': "Correction Label",
        'send_wave': "Send Mental Wave (Evolve)",
        'evolve_msg': "⚡ [Evolution]: {} Complete.",
        'topology': "🌌 Cosmos Topology",
        'void_msg': "The cosmos is void... Please feed data via the left panel.",
        'init_msg': "Initializing..."
    }
}

def t(key):
    return TRANSLATIONS[st.session_state.language][key]

# --- Page Config ---
st.set_page_config(
    page_title=TRANSLATIONS['EN']['page_title'], # Default title
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for "Scientific Light" feel
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #000000;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #0068c9;
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #004b91;
    }
    .sidebar-content {
        background-color: #f0f2f6;
    }
    /* Increase text contrast globally */
    p, label, .stMarkdown {
        color: #000000 !important;
        font-size: 1.1em;
    }
    /* Reduce top padding to fix layout */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    /* Hide top header to really hit the top */
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Session State Management ---
if 'brain' not in st.session_state:
    # Default initialization (will be overwritten by loader logic below)
    st.session_state.brain = CosmosResonator()
    st.session_state.log_msg = t('init_msg')
    st.session_state.current_brain_file = "cosmos_brain.pkl"

if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

def reset_brain():
    st.session_state.brain = CosmosResonator()
    if os.path.exists(st.session_state.current_brain_file):
        os.remove(st.session_state.current_brain_file)
    st.session_state.log_msg = t('reset_msg')

# --- Sidebar ---
with st.sidebar:
    # Language Switcher
    lang_choice = st.radio("Language / 语言", options=['CN', 'EN'], horizontal=True)
    if lang_choice != st.session_state.language:
        st.session_state.language = lang_choice
        st.rerun()

    st.title(t('sidebar_title'))
    st.write(t('version'))
    
    # --- Brain File Management ---
    st.markdown(t('brain_core'))
    
    # Scan for existing brains
    brain_files = [f for f in os.listdir('.') if f.endswith('.pkl')]
    if "cosmos_brain.pkl" not in brain_files:
        brain_files.append("cosmos_brain.pkl") # Default ensure exist
    
    # File Selector
    selected_file = st.selectbox(
        t('select_brain'), 
        options=brain_files,
        index=brain_files.index(st.session_state.get('current_brain_file', 'cosmos_brain.pkl')) if st.session_state.get('current_brain_file', 'cosmos_brain.pkl') in brain_files else 0
    )
    
    # New Brain Creation
    new_brain_name = st.text_input(t('new_brain'), placeholder="e.g. new_brain.pkl")
    if st.button(t('load_create')):
        # Determine target file
        if new_brain_name:
            target_file = new_brain_name if new_brain_name.endswith('.pkl') else f"{new_brain_name}.pkl"
        else:
            target_file = selected_file
        
        # Load logic
        brain, msg = load_or_create_brain(target_file)
        st.session_state.brain = brain
        st.session_state.log_msg = msg
        st.session_state.current_brain_file = target_file
        st.rerun()

    # Just ensure we load the default if nothing is loaded yet (first run)
    if 'brain' not in st.session_state or st.session_state.brain is None:
         # Initial default load
         brain, msg = load_or_create_brain(selected_file)
         st.session_state.brain = brain
         st.session_state.log_msg = msg
         st.session_state.current_brain_file = selected_file

    st.caption(f"{t('current_core')}: `{st.session_state.current_brain_file}`")
    
    # Placeholder for star count
    star_count_placeholder = st.empty()
    star_count_placeholder.metric(t('star_count'), len(st.session_state.brain.galaxy))
    
    st.markdown("---")
    if st.button(t('reset_u')):
        reset_brain()
        st.rerun()
    
    st.markdown("---")
    st.info(t('info'))

# --- Main Interface ---
st.title(t('main_title'))

# --- Status Message Area (Top for visibility) ---
if st.session_state.log_msg:
    st.success(st.session_state.log_msg, icon="⚡")
    # Optional: Clear message after showing once? 
    # st.session_state.log_msg = "" 

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader(t('perception'))
    
    uploaded_file = st.file_uploader(t('upload_label'), type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        # Preprocessing
        image = Image.open(uploaded_file).convert('L')
        
        # Compact Layout: Image side-by-side with Result
        sub_col1, sub_col2 = st.columns([1, 2])
        with sub_col1:
            st.image(image, caption=t('input_caption'), width=100)
        
        # Vectorize
        if np.array(image).mean() > 127: 
            image = ImageOps.invert(image) 
        
        img_vec = np.array(image.resize((28, 28))).flatten()
        if np.linalg.norm(img_vec) > 0: 
            img_vec = img_vec / np.linalg.norm(img_vec)
        
        # Perceive
        star, gravity = st.session_state.brain.perceive(img_vec)
        
        # Result
        pred_label = star.label if star else "?"
        gravity_val = gravity if isinstance(gravity, (float, np.floating)) else 0.0
        
        with sub_col2:
            st.metric(t('brain_consciousness'), f"{pred_label}", delta=f"G: {gravity_val:.4f}")
        
        # Feedback Loop
        st.markdown(t('interaction'))
        st.caption(t('interaction_hint'))
        
        correction = st.text_input(t('correct_label'), placeholder=f"Default: {pred_label}", key="correction_input")
        
        if st.button(t('send_wave')):
            target_label = correction if correction.strip() else pred_label
            
            valid_label = None
            try:
                valid_label = int(target_label)
            except:
                st.error("Invalid Label!")
            
            if valid_label is not None:
                action = st.session_state.brain.memorize(img_vec, valid_label)
                save_brain(st.session_state.brain, st.session_state.current_brain_file)
                st.session_state.log_msg = t('evolve_msg').format(action)
                st.rerun()

with col2:
    st.subheader(t('topology'))
    
    if len(st.session_state.brain.galaxy) > 0:
        fig, msg = get_star_map_figure(st.session_state.brain)
        if fig:
            st.pyplot(fig)
        else:
            st.warning(msg)
    else:
        st.write(t('void_msg'))

