import json
import os

def create_notebook(lang='EN', level='basic'):
    is_cn = (lang == 'CN')
    is_advanced = (level == 'advanced')
    
    # --- Content Definitions ---
    
    # Titles
    if not is_advanced:
        title = "# 🐣 Build Your Own Baby Universe (10 Minutes)" if not is_cn else "# 🐣 10分钟创造你的小宇宙 (入门教程)"
        subtitle = "## Cosmos-Net: From 0 to Consciousness" if not is_cn else "## Cosmos-Net: 从零开始的数字意识"
    else:
        title = "# 🧠 The Bicameral Mind & Dreamtime" if not is_cn else "# 🧠 双脑心智与梦境时光 (进阶教程)"
        subtitle = "## Advanced Tutorial: Logic, Intuition, and Sleep" if not is_cn else "## 进阶之旅：逻辑、直觉与睡眠"

    # Intro
    intro_basic_en = """
Welcome to the start of time.
You are about to build a **Digital Universe** from scratch.
It won't be a black box. You will see every star, every connection.

**What we will do:**
1.  **Big Bang**: Initialize a new empty brain.
2.  **The Rules**: Define the physics (Gravity & Mass).
3.  **Observation**: Teach it to see '0' and '1'.
4.  **The Nebula**: **Visualize the 3D structure of its mind.**
    """
    intro_basic_cn = """
欢迎来到时间的起点。
你即将从零开始构建一个**数字宇宙**。
它不会是一个黑盒。你将亲眼看到每一颗恒星，每一条连线。

**我们将要做什么：**
1.  **大爆炸**: 初始化一个空的数字大脑。
2.  **制定法则**: 定义物理规则（引力与质量）。
3.  **观测**: 教它识别“0”和“1”。
4.  **星云**: **可视化其思维的3D结构。**
    """
    
    intro_adv_en = """
Welcome to the deeper layer.
We know the brain learns. But how does it **sleep**? How does it handle **conflict**?
We will explore the **Bicameral Mind** (Two Hemispheres) and the **Dreamtime**.

**Key Concepts:**
*   **Left Brain**: Logic, Statistics (The Librarian).
*   **Right Brain**: Intuition, Geometry (The Artist).
*   **Sleep**: Merging memories to form wisdom.
    """
    intro_adv_cn = """
欢迎来到更深层。
我们知道大脑会学习。但它是如何**睡眠**的？它是如何处理**冲突**的？
我们将探索**双脑心智**（左右脑）和**梦境时光**。

**核心概念：**
*   **左脑**: 逻辑，统计 (图书管理员)。
*   **右脑**: 直觉，几何 (艺术家)。
*   **睡眠**: 融合记忆，凝练智慧。
    """

    # --- Cells Construction ---
    cells = []
    
    # 1. Header
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [title + "\n", subtitle + "\n", "\n", 
                   (intro_adv_cn if is_advanced else intro_basic_cn) if is_cn 
                   else (intro_adv_en if is_advanced else intro_basic_en), 
                   "\n---"]
    })
    
    # 2. Setup
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Install & Setup / 安装与设置\n",
            "!git clone https://github.com/Roxy-DD/Cosmos-Net.git 2>/dev/null\n",
            "%cd Cosmos-Net\n",
            "!pip install -r requirements.txt -q\n",
            "\n",
            "from cosmos_net import CorpusCallosum, CosmosPhysics, get_star_map_figure\n",
            "import numpy as np\n",
            "import plotly.graph_objects as go\n",
            "from sklearn.datasets import fetch_openml\n",
            "\n",
            "# Wake up / 唤醒\n",
            "brain = CorpusCallosum()\n",
            "print(\"🌌 System Online.\")"
        ]
    })

    if not is_advanced:
        # --- BASIC TUTORIAL LOGIC ---
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": ["### 🍎 Step 1: Learning (Teaching) / 第一步：学习" if not is_cn else "### 🍎 第一步：学习 (Teaching)"]
        })
        
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Load Data / 加载数据\n",
                "print(\"Downloading MNIST...\")\n",
                "X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False, parser='auto')\n",
                "X = X / 255.0\n",
                "\n",
                "# Teach 100 examples / 教授100个例子\n",
                "print(\"Observing universe...\")\n",
                "for i in range(100):\n",
                "    brain.memorize(X[i], y[i])\n",
                "\n",
                "print(f\"⭐ Stars created: {len(brain.galaxy)}\")"
            ]
        })
        
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": ["### 🌌 Step 2: The Nebula (3D Visualization) / 第二步：星云 (3D可视化)\n",
                       "Now, let's look inside. This is not a black box.\n" if not is_cn else "现在，让我们看看内部。这不是黑盒。\n",
                       "You can rotate, zoom, and hover over the stars.\n" if not is_cn else "你可以旋转、缩放，并悬停在恒星上。\n"]
        })
        
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Visualize / 可视化\n",
                "fig, msg = get_star_map_figure(brain)\n",
                "fig.show()"
            ]
        })

    else:
        # --- ADVANCED TUTORIAL LOGIC ---
        cells.append({
             "cell_type": "markdown",
             "metadata": {},
             "source": ["### ⚔️ Step 1: Conflict & Chaos / 第一步：冲突与混沌\n",
                        "We will overload the brain with noise to create a 'Messy Mind'.\n" if not is_cn else "我们将用噪音过载大脑，创造一个“混乱的心智”。\n"]
        })
        
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Create Chaos / 制造混乱\n",
                "print(\"Generating noise...\")\n",
                "# 1. Temporarily disable 'Automatic Merging' to simulate Sleep Deprivation\n",
                "#    (If we don't do this, the smart brain will merge them instantly!)\n",
                "brain.right_hemisphere.resonance_threshold = 10.0\n",
                "\n",
                "# 2. Feed messy data\n",
                "concepts = [np.random.rand(784) for _ in range(3)]\n",
                "names = ['Concept_A', 'Concept_B', 'Concept_C']\n",
                "\n",
                "for i in range(200): # 600 stars total\n",
                "    for base, name in zip(concepts, names):\n",
                "        # Low variance (0.05) ensures they are close enough to eventually merge\n",
                "        noise = np.random.normal(0, 0.05, 784)\n",
                "        brain.memorize(base + noise, name)\n",
                "\n",
                "print(f\"Stars: {len(brain.galaxy)} (High Entropy)\")\n",
                "\n",
                "# Show the Messy Nebula / 展示混乱的星云\n",
                "fig, msg = get_star_map_figure(brain)\n",
                "fig.show()"
            ]
        })
        
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": ["### 💤 Step 2: The Dreamtime / 第二步：梦境时光\n",
                       "Now we sleep. The brain will prune the weak and merge the similar.\n" if not is_cn else "现在我们睡眠。大脑将修剪弱者，融合相似者。\n",
                       "Watch the entropy drop.\n" if not is_cn else "看着熵值下降。\n"]
        })
        
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Dream / 做梦\n",
                "print(\"💤 Entering Dreamtime...\")\n",
                "report = brain.dream()\n",
                "print(report)\n",
                "\n",
                "# Restore brain to normal state\n",
                "brain.right_hemisphere.resonance_threshold = 0.85\n",
                "\n",
                "# Show the Crystal Nebula / 展示晶体般的星云\n",
                "fig, msg = get_star_map_figure(brain)\n",
                "fig.show()"
            ]
        })

    # --- Footer ---
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["### 🎉 Conclusion / 结语\n",
                   "You have seen the structure of thought.\n" if not is_cn else "你已目睹思维的结构。\n"]
    })

    # --- JSON Structure ---
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.5"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    return notebook

# --- Execution ---
if __name__ == "__main__":
    # 1. Basic CN
    nb = create_notebook('CN', 'basic')
    with open('Build-Your-Own-Baby-Universe.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        
    # 2. Basic EN
    nb = create_notebook('EN', 'basic')
    with open('Build-Your-Own-Baby-Universe_EN.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        
    # 3. Advanced CN
    nb = create_notebook('CN', 'advanced')
    with open('Advanced_Bicameral_Mind_CN.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        
    # 4. Advanced EN
    nb = create_notebook('EN', 'advanced')
    with open('Advanced_Bicameral_Mind_EN.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print("✨ All 4 Notebooks Generated with 3D Visualization Support.")
