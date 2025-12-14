import json
import copy

# --- Common Cells (Code is same, Logic is same) ---
# We will define text separately

def create_notebook(lang='EN'):
    is_cn = (lang == 'CN')
    
    # Text Content
    title = "# 🧠 Cosmos-Net Story: The Two Friends in Your Head" if not is_cn else "# 🧠 Cosmos-Net 故事：你脑海里的两个朋友"
    subtitle = "## Advanced Tutorial: Bicameral Mind & Dreamtime" if not is_cn else "## 进阶教程：双脑心智与梦境时光"
    
    intro_en = """
Welcome to the **Deep Dive**. 
Today, we are going to open up the brain of our AI and see who lives inside.
We will discover that **Cosmos-Net v10.1** is not one brain, but **two**.

### 🧬 The Biological Map
| Character | Computer Name | Biological Name | Function |
| :--- | :--- | :--- | :--- |
| **The Librarian** | `LeftHemisphere` | **Left Brain (Logic)** | Loves rules, math, and geometry. Measures things precisely. |
| **The Artist** | `RightHemisphere` | **Right Brain (Intuition)** | Loves feelings, similarities, and vibes. Sees the "Whole Picture". |
| **The Bridge** | `CorpusCallosum` | **Corpus Callosum** | Connects the two friends. Decides who gets to speak. |
| **The Cleanup** | `dream()` | **Sleep Consolidation** | Cleans up the house at night. Throws away trash, keeps treasures. |
    """
    
    intro_cn = """
欢迎来到 **深度探索**。
今天，我们要切开 AI 的大脑，看看里面住着谁。
我们发现 **Cosmos-Net v10.1** 不是一个大脑，而是**两个**。

### 🧬 生物学地图
| 角色 | 代码名称 | 生物学名称 |不仅 |
| :--- | :--- | :--- | :--- |
| **图书管理员 (Librarian)** | `LeftHemisphere` | **左脑 (逻辑)** | 喜欢规则、数学和几何。精准地测量一切。 |
| **艺术家 (Artist)** | `RightHemisphere` | **右脑 (直觉)** | 喜欢感觉、相似性和氛围。看到的是“整体画面”。 |
| **桥梁 (Bridge)** | `CorpusCallosum` | **胼胝体** | 连接这两个朋友。决定谁来发言。 |
| **大扫除 (Cleanup)** | `dream()` | **睡眠整合 (Sleep)** | 在夜晚打扫房间。丢掉垃圾，保留珍宝。 |
    """
    
    intro_text = intro_cn if is_cn else intro_en
    
    step1_en = """
### 🔬 Step 1: Meet the Librarian (Left Hemisphere)
**Biology**: The Left Brain handles **Logic & Language**. It likes distinct categories.
**Code**: `LeftHemisphere` uses **Statistics**. It converts an image into numbers like "Pixel Density" (How much ink?) and "Aspect Ratio" (Is it tall or fat?).

Let's show it a "1" and a "0".
    """
    
    step1_cn = """
### 🔬 第一步：会见图书管理员 (左脑)
**生物学**: 左脑负责**逻辑和语言**。它喜欢明确的分类。
**代码**: `LeftHemisphere` 使用**统计学**。它将图像转化为数字，比如“像素密度”（有多少墨水？）和“长宽比”（是高还是胖？）。

让我们给它看一个“1”和一个“0”。
    """
    
    step2_en = """
### 🎨 Step 2: Meet the Artist (Right Hemisphere)
**Biology**: The Right Brain handles **Spatial & Holistic** processing. It recognizes faces and patterns instantly.
**Code**: `RightHemisphere` uses **Gravity (Dot Product)**. It feels the "pull" of similar memories.

The Artist doesn't measure aspect ratios. It just feels the **Vibe**.
    """
    
    step2_cn = """
### 🎨 第二步：会见艺术家 (右脑)
**生物学**: 右脑负责**空间和整体**处理。它可以瞬间认出面孔和模式。
**代码**: `RightHemisphere` 使用**引力 (点积)**。它能感受到相似记忆的“吸引力”。

艺术家不去测量长宽比。它只感受 **氛围 (Vibe)**。
    """
    
    step3_en = """
### ⚔️ Step 3: The Argument (Neuroplasticity)
**Biology**: Sometimes, our brain conflicts. Logic names it one thing, Intuition feels another. The **Corpus Callosum** must inhibit one to let the other speak.
**Code**: `brain.dominance`. This number moves Left or Right based on who gets the right answer.

Let's confuse the brain. We will show it a '7', but tell it it's a '1'. (Bad teaching!).
    """
    
    step3_cn = """
### ⚔️ 第三步：争吵 (神经可塑性)
**生物学**: 有时，我们的大脑会发生冲突。逻辑说这是A，直觉说这是B。**胼胝体**必须抑制其中一方，让另一方发言。
**代码**: `brain.dominance` (主导权)。这个数值会根据谁给出了正确答案而向左或向右移动。

让我们迷惑一下大脑。给它看一个“7”，但告诉它这是“1”。（错误的教学！）。
    """
    
    step4_en = """
### 💤 Step 4: Time for Bed (The Dreamtime)
**Biology**: We don't remember everything. During sleep (**Rapid Eye Movement**), our brain replays memories. It deletes the weak ones (**Pruning**) and merges specific events into general wisdom (**Consolidation**).
**Code**: `brain.dream()`. 

Let's overload the Artist with 50 messy sketches of '1'.
    """
    
    step4_cn = """
### 💤 第四步：该睡觉了 (梦境时光)
**生物学**: 我们不会记住所有事情。在睡眠（**快速眼动期**）中，大脑会重演记忆。它删除微弱的记忆（**修剪**），并将具体事件合并为普遍的智慧（**凝练**）。
**代码**: `brain.dream()`。

让我们塞给艺术家50张乱糟糟的“1”的速写。
    """
    
    end_en = """
### 🎉 Congratulations!
You just witnessed the biological cycle of intelligence:
1.  **Sensation**: Seeing pixels.
2.  **Conflict**: Librarian vs Artist.
3.  **Adaptation**: Changing dominance.
4.  **Consolidation**: Dreaming and evolving.

This is **Cosmos-Net**. It's alive.
    """
    
    end_cn = """
### 🎉 恭喜！
你刚刚见证了智能的生物学循环：
1.  **感觉**: 看见像素。
2.  **冲突**: 管理员 vs 艺术家。
3.  **适应**: 改变主导权。
4.  **凝练**: 做梦并进化。

这就是 **Cosmos-Net**。它是活的。
    """

    nb = {
     "cells": [
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": [title + "\n", subtitle + "\n", "\n", intro_text if not is_cn else intro_cn, "\n---"]
      },
      {
       "cell_type": "code",
       "execution_count": None,
       "metadata": {},
       "outputs": [],
       "source": [
        "# Install / 安装\n",
        "!git clone https://github.com/Roxy-DD/Cosmos-Net.git 2>/dev/null\n",
        "%cd Cosmos-Net\n",
        "!pip install -r requirements.txt -q\n",
        "\n",
        "from cosmos_net import CorpusCallosum, CosmosPhysics\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "from sklearn.datasets import fetch_openml\n",
        "\n",
        "# Wake up! / 唤醒!\n",
        "brain = CorpusCallosum()\n",
        "print(f\"🧠 Brain Awakened. Current Boss: {'Intuition (Right)' if brain.dominance > 0.5 else 'Logic (Left)'}\")"
       ]
      },
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": [step1_text := step1_cn if is_cn else step1_en]
      },
      {
       "cell_type": "code",
       "execution_count": None,
       "metadata": {},
       "outputs": [],
       "source": [
        "# Load Data / 加载数据\n",
        "X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False, parser='auto')\n",
        "X = X / 255.0\n",
        "vec_1 = X[np.where(y == '1')[0][0]]\n",
        "vec_0 = X[np.where(y == '0')[0][0]]\n",
        "\n",
        "# Show the Librarian / 展示给管理员\n",
        "brain.left_hemisphere.memorize(vec_1, '1')\n",
        "brain.left_hemisphere.memorize(vec_0, '0')\n",
        "\n",
        "# Ask / 询问\n",
        "label, conf = brain.left_hemisphere.perceive(vec_1)\n",
        "print(f\"🤓 Librarian: {label} (Conf: {conf*100:.1f}%)\")"
       ]
      },
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": [step2_text := step2_cn if is_cn else step2_en]
      },
      {
       "cell_type": "code",
       "execution_count": None,
       "metadata": {},
       "outputs": [],
       "source": [
        "# Show the Artist / 展示给艺术家\n",
        "brain.right_hemisphere.memorize(vec_1, '1')\n",
        "\n",
        "# Ask / 询问\n",
        "star, gravity = brain.right_hemisphere.perceive(vec_1)\n",
        "print(f\"🎨 Artist: {star.label} (Gravity: {gravity:.4f})\")"
       ]
      },
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": [step3_text := step3_cn if is_cn else step3_en]
      },
      {
       "cell_type": "code",
       "execution_count": None,
       "metadata": {},
       "outputs": [],
       "source": [
        "vec_7 = X[np.where(y == '7')[0][0]]\n",
        "\n",
        "# 1. Conflict / 冲突\n",
        "res, conf = brain.perceive(vec_7)\n",
        "print(f\"🤔 Initial Thought: {res.label}\")\n",
        "\n",
        "# 2. Correct / 纠正\n",
        "msg = brain.memorize(vec_7, '7')\n",
        "print(f\"Outcome: {msg}\")\n",
        "\n",
        "# 3. Shift / 变化\n",
        "print(f\"New Dominance: {brain.dominance:.2f}\")"
       ]
      },
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": [step4_text := step4_cn if is_cn else step4_en]
      },
      {
       "cell_type": "code",
       "execution_count": None,
       "metadata": {},
       "outputs": [],
       "source": [
        "# Overload / 过载\n",
        "print(f\"Stars before: {len(brain.galaxy)}\")\n",
        "for i in range(50):\n",
        "    noise = np.random.normal(0, 0.15, vec_1.shape)\n",
        "    brain.memorize(vec_1 + noise, '1')\n",
        "print(f\"Stars after: {len(brain.galaxy)}\")\n",
        "\n",
        "# Dream / 做梦\n",
        "print(\"💤 Dreaming...\")\n",
        "report = brain.dream()\n",
        "print(report)"
       ]
      },
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": [end_text := end_cn if is_cn else end_en]
      }
     ],
     "metadata": {
      "kernelspec": {
       "display_name": "Python 3",
       "language": "python",
       "name": "python3"
      },
      "language_info": {
       "codemirror_mode": {
        "name": "ipython",
        "version": 3
       },
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
    return nb

# Generate EN
nb_en = create_notebook('EN')
with open('Advanced_Bicameral_Mind_EN.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb_en, f, indent=1, ensure_ascii=False)

# Generate CN
nb_cn = create_notebook('CN')
with open('Advanced_Bicameral_Mind_CN.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb_cn, f, indent=1, ensure_ascii=False)

print("Tutorials generated: _EN.ipynb and _CN.ipynb")
