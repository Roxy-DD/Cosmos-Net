import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import os
import time
from cosmos_net import load_or_create_brain, save_brain, get_star_map_figure, CosmosResonator

# --- Lazy Load Retina ---
# We put this in a function or try-except block so the app doesn't crash 
# if torch is installing or not present yet.
@st.cache_resource
def get_retina():
    try:
        from retina import Retina
        return Retina()
    except ImportError:
        return None

# --- Language & Configuration ---
if 'language' not in st.session_state:
    st.session_state.language = 'CN'

TRANSLATIONS = {
    'CN': {
        'page_title': "Cosmos-Net: 数字生命",
        'sidebar_title': "🌌 观测台",
        'version': "Cosmos-Net V8.0 (Eye-Brain Fusion)",
        'brain_core': "### 🧠 大脑核心 (Neural Core)",
        'select_brain': "选择大脑存档:",
        'new_brain': "或新建大脑 (名称):",
        'load_create': "加载/创建",
        'current_core': "当前核心",
        'star_count': "恒星数量",
        'reset_u': "重置当前宇宙",
        'reset_msg': "💥 宇宙已重置 (Big Bang)!",
        'info': "Cosmos-Net V8.0 将 MobileNetV2 (作为眼睛) 与 拓扑记忆 (作为大脑) 融合。",
        'main_title': "Cosmos-Net: 数字生命交互界面 (V8.0)",
        'perception': "👁️ 感知 (Perception)",
        'upload_label': "给予视觉刺激 (上传手写数字/图片)",
        'input_caption': "输入影像",
        'brain_consciousness': "大脑意识",
        'interaction': "### ⚡ 交互 (Interaction)",
        'interaction_hint': "如果不输入标签直接点击按钮，将执行「强化学习」(Reinforce)。",
        'correct_label': "纠正标签 (Correct Label)",
        'send_wave': "发送精神波 (Evolve/Reinforce)",
        'evolve_msg': "⚡ [学习]: {} 完成。",
        'topology': "🌌 宇宙拓扑 (Cosmos Topology)",
        'void_msg': "宇宙一片虚无... 请通过更左侧的面板喂养数据。",
        'init_msg': "初始化...",
        'retina_loading': "正在唤醒视神经 (Loading Retina)...",
        'retina_active': "✅ 视神经已连接 (MobileNetV2 Active)",
        'retina_fail': "⚠️ 视神经启动失败 (请检查 Torch 环境)。已回退到原始像素模式。",
        'dim_mismatch': "⚠️ 维度坍缩警告: 你的旧宇宙是基于像素的 (Dim: 784)，而新的眼睛看到的是语义 (Dim: 1280)。必须触发一次大爆炸来升级宇宙维度。",
        'sleep_btn': "💤 进入梦境 (睡眠与整合)",
        'dream_spinner': "正在做梦... 提炼记忆... 遗忘噪音...",
        'mass_evo_title': "📚 图书馆 (批量进化)",
        'mass_evo_expander': "批量进化 (MNIST)",
        'mass_evo_caption': "使用标准数据集喂养大脑。",
        'train_btn': "开始阅读 (训练)",
        'test_btn': "开始考试 (测试)",
        'self_reinforce': "如果正确则自我强化？",
        'downloading_train': "正在下载 MNIST (训练集)...",
        'downloading_test': "正在下载 MNIST (测试集)...",
        'dreaming_progress': "梦境演化中... {}/{}",
        'taking_exam': "正在考试... {}/{}"
    },
    'EN': {
        'page_title': "Cosmos-Net: Digital Life",
        'sidebar_title': "🌌 Observatory",
        'version': "Cosmos-Net V8.0 (Eye-Brain Fusion)",
        'brain_core': "### 🧠 Neural Core",
        'select_brain': "Select Brain Archive:",
        'new_brain': "Or Create New Brain (Name):",
        'load_create': "Load/Create",
        'current_core': "Current Core",
        'star_count': "Star Count",
        'reset_u': "Reset Current Cosmos",
        'reset_msg': "💥 Cosmos Reset (Big Bang)!",
        'info': "Cosmos-Net V8.0 fuses MobileNetV2 (The Eye) with Topological Memory (The Brain).",
        'main_title': "Cosmos-Net: Digital Life Interface (V8.0)",
        'perception': "👁️ Perception",
        'upload_label': "Visual Stimulus (Upload Digit/Image)",
        'input_caption': "Input Image",
        'brain_consciousness': "Brain Consciousness",
        'interaction': "### ⚡ Interaction",
        'interaction_hint': "If input is empty, clicking button triggers 'Reinforcement Learning'.",
        'correct_label': "Correction Label",
        'send_wave': "Send Mental Wave (Evolve/Reinforce)",
        'evolve_msg': "⚡ [Learning]: {} Complete.",
        'topology': "🌌 Cosmos Topology",
        'void_msg': "The cosmos is void... Please feed data via the left panel.",
        'init_msg': "Initializing...",
        'retina_loading': "Awakening Retina...",
        'retina_active': "✅ Retina Connected (MobileNetV2 Active)",
        'retina_fail': "⚠️ Retina Failed (Check Torch). Fallback to Pixel Mode.",
        'dim_mismatch': "⚠️ Dimensional Collapse: Old universe is Pixel-based (784), but The Eye sees Semantics (1280). A Big Bang is required.",
        'sleep_btn': "💤 Enter Dreamtime (Sleep & Consolidate)",
        'dream_spinner': "Dreaming... refining memories... forgetting noise...",
        'mass_evo_title': "📚 The Library (Mass Evolution)",
        'mass_evo_expander': "Mass Evolution (MNIST)",
        'mass_evo_caption': "Feed the brain with standard datasets.",
        'train_btn': "Start Reading (Train)",
        'test_btn': "Start Exam (Test)",
        'self_reinforce': "Self-Reinforce if Correct?",
        'downloading_train': "Downloading MNIST (Train)...",
        'downloading_test': "Downloading MNIST (Test)...",
        'dreaming_progress': "Dreaming... {}/{}",
        'taking_exam': "Taking Exam... {}/{}"
    }
}

def t(key):
    return TRANSLATIONS[st.session_state.language][key]

# --- Page Config ---
st.set_page_config(
    page_title=TRANSLATIONS['EN']['page_title'], 
    page_icon="🌌", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #000000; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #000000; font-weight: 700; }
    .stButton>button { background-color: #0068c9; color: white; border-radius: 6px; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #004b91; }
    .sidebar-content { background-color: #f0f2f6; }
    p, label, .stMarkdown { color: #000000 !important; font-size: 1.1em; }
    .block-container { padding-top: 0rem; padding-bottom: 0rem; }
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'brain' not in st.session_state:
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

# --- Initialize Retina ---
retina = get_retina()
if retina:
    st.sidebar.success(t('retina_active'))
else:
    st.sidebar.warning(t('retina_fail'))

# --- Sidebar ---
with st.sidebar:
    lang_choice = st.radio("Language / 语言", options=['CN', 'EN'], horizontal=True)
    if lang_choice != st.session_state.language:
        st.session_state.language = lang_choice
        st.rerun()

    st.title(t('sidebar_title'))
    st.write(t('version'))
    
    st.markdown(t('brain_core'))
    brain_files = [f for f in os.listdir('.') if f.endswith('.pkl')]
    if "cosmos_brain.pkl" not in brain_files:
        brain_files.append("cosmos_brain.pkl")
    
    selected_file = st.selectbox(
        t('select_brain'), 
        options=brain_files,
        index=brain_files.index(st.session_state.get('current_brain_file', 'cosmos_brain.pkl')) if st.session_state.get('current_brain_file', 'cosmos_brain.pkl') in brain_files else 0
    )
    
    new_brain_name = st.text_input(t('new_brain'), placeholder="e.g. new_brain.pkl")
    if st.button(t('load_create')):
        target_file = new_brain_name if new_brain_name.endswith('.pkl') else f"{new_brain_name}.pkl" if new_brain_name else selected_file
        brain, msg = load_or_create_brain(target_file)
        st.session_state.brain = brain
        st.session_state.log_msg = msg
        st.session_state.current_brain_file = target_file
        st.rerun()

    # Initial load ensuring
    if 'brain' not in st.session_state or st.session_state.brain is None:
         brain, msg = load_or_create_brain(selected_file)
         st.session_state.brain = brain
         st.session_state.log_msg = msg
         st.session_state.current_brain_file = selected_file

    st.caption(f"{t('current_core')}: `{st.session_state.current_brain_file}`")
    
    star_count_placeholder = st.empty()
    star_count_placeholder.metric(t('star_count'), len(st.session_state.brain.galaxy))
    
    st.markdown("---")
    if st.button(t('reset_u')):
        reset_brain()
        st.rerun()
    
    # --- Mass Evolution (The Library) ---
    st.markdown("---")
    st.subheader(t('mass_evo_title'))
    
    with st.expander(t('mass_evo_expander')):
        st.caption(t('mass_evo_caption'))
        sample_size = st.slider("Sample Size", 100, 5000, 500)
        
        col_train, col_test = st.columns(2)
        
        with col_train:
            if st.button(t('train_btn')):
                if not retina:
                     st.error("Retina not active!")
                else:
                    try:
                        from training import load_mnist, evolve_in_dreams
                        
                        status_bar = st.progress(0)
                        status_text = st.empty()
                        
                        def update_progress(current, total):
                            status_bar.progress(current / total)
                            status_text.text(t('dreaming_progress').format(current, total))
                        
                        status_text.text(t('downloading_train'))
                        dataset = load_mnist(limit=sample_size, train=True)
                        
                        msg = evolve_in_dreams(st.session_state.brain, retina, dataset, update_progress)
                        
                        st.success(msg)
                        save_brain(st.session_state.brain, st.session_state.current_brain_file)
                        st.session_state.log_msg = msg
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

        with col_test:
            self_reinforce = st.checkbox(t('self_reinforce'), value=False, help="If the brain answers correctly, it will strengthen that memory.")
            
            if st.button(t('test_btn')):
                 if not retina:
                     st.error("Retina not active!")
                 else:
                    try:
                        from training import load_mnist, evaluate_brain
                        
                        status_bar = st.progress(0)
                        status_text = st.empty()
                        
                        def update_progress(current, total):
                            status_bar.progress(current / total)
                            status_text.text(t('taking_exam').format(current, total))
                            
                        status_text.text(t('downloading_test'))
                        dataset = load_mnist(limit=sample_size, train=False)
                        
                        accuracy, msg = evaluate_brain(st.session_state.brain, retina, dataset, update_progress, self_reinforce=self_reinforce)
                        
                        if accuracy > 80:
                            st.balloons()
                        elif accuracy < 10:
                            st.toast("Needs more study...")
                            
                        st.success(msg)
                        st.session_state.log_msg = msg
                        
                        if self_reinforce:
                            save_brain(st.session_state.brain, st.session_state.current_brain_file)
                            st.info("Brain has been updated with self-reinforced memories.")
                            time.sleep(1.5)
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"Error: {e}")

                    except Exception as e:
                        st.error(f"Error: {e}")

    # --- Sleep Mode ---
    if st.button(t('sleep_btn')):
        with st.spinner(t('dream_spinner')):
            time.sleep(1) # Dramatic pause
            msg = st.session_state.brain.dream()
            save_brain(st.session_state.brain, st.session_state.current_brain_file)
            st.session_state.log_msg = msg
            st.success(msg)
            time.sleep(1)
            st.rerun()

    st.markdown("---")
    st.info(t('info'))

# --- Main Interface ---
st.title(t('main_title'))

if st.session_state.log_msg:
    st.success(st.session_state.log_msg, icon="⚡")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader(t('perception'))
    uploaded_file = st.file_uploader(t('upload_label'), type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        sub_col1, sub_col2 = st.columns([1, 2])
        with sub_col1:
            st.image(image, caption=t('input_caption'), width=100)
        
        # --- PERCEPTION LOGIC ---
        input_vec = None
        
        # 1. Try Retina (The Eye)
        if retina:
            try:
                # Retina outputs a 1280-dim vector
                input_vec = retina.perceive(image)
            except Exception as e:
                st.error(f"Retina Error: {e}")
        
        # 2. Fallback to Pixel (The Old Way)
        if input_vec is None:
            # Legacy logic
            if image.mode != 'L': image = image.convert('L')
            if np.array(image).mean() > 127: image = ImageOps.invert(image)
            input_vec = np.array(image.resize((28, 28))).flatten()
            if np.linalg.norm(input_vec) > 0: input_vec = input_vec / np.linalg.norm(input_vec)

        # 3. Check for Dimension Compatibility
        universe_dim_mismatch = False
        if len(st.session_state.brain.galaxy) > 0:
            star_dim = len(st.session_state.brain.galaxy[0].vector)
            input_dim = len(input_vec)
            if star_dim != input_dim:
                universe_dim_mismatch = True
        
        if universe_dim_mismatch:
            with sub_col2:
                st.error(t('dim_mismatch'))
                if st.button("💥 Big Bang (Reset & Upgrade)", type="primary"):
                    reset_brain()
                    st.rerun()
        else:
            # Percieve
            star, gravity = st.session_state.brain.perceive(input_vec)
            
            pred_label = star.label if star else "?"
            gravity_val = gravity if isinstance(gravity, (float, np.floating)) else 0.0
            
            with sub_col2:
                st.metric(t('brain_consciousness'), f"{pred_label}", delta=f"G: {gravity_val:.4f}")
            
            # Feedback
            st.markdown(t('interaction'))
            st.caption(t('interaction_hint'))
            
            correction = st.text_input(t('correct_label'), placeholder=f"Default: {pred_label}", key="correction_input")
            
            if st.button(t('send_wave')):
                target_label = correction if correction.strip() else pred_label
                if target_label == "?": target_label = "0" # Default fallback for new universe
                
                # Check integer or string label - we now allow strings conceptually but let's stick to simple logic
                valid_label = target_label # Allow strings now? CosmosNet supports any label type technically.
                
                action = st.session_state.brain.memorize(input_vec, valid_label)
                save_brain(st.session_state.brain, st.session_state.current_brain_file)
                st.session_state.log_msg = t('evolve_msg').format(action)
                st.rerun()

with col2:
    st.subheader(t('topology'))
    if len(st.session_state.brain.galaxy) > 0:
        fig, msg = get_star_map_figure(st.session_state.brain)
        if fig:
            # v10.1: Robust Visualization Check
            # Plotly figures have 'to_json' or 'write_html'; Matplotlib figures have 'savefig'
            is_plotly = hasattr(fig, 'to_dict') or hasattr(fig, 'update_layout')
            
            if is_plotly:
                import plotly.graph_objects as go
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.pyplot(fig)
        else:
            st.warning(msg)
    else:
        st.write(t('void_msg'))

