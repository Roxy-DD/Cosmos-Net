import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.lines import Line2D
import torch
import pickle
import os
import io
import networkx as nx
from sklearn.manifold import TSNE
from PIL import Image, ImageOps

# --- 1. 基础物理与组件 ---

class CosmosPhysics:
    @staticmethod
    def normalize(w):
        norm = np.linalg.norm(w)
        if norm == 0: return w
        return w / norm

    @staticmethod
    def compute_gravity(matter_a, matter_b):
        return np.dot(matter_a, matter_b)

    @staticmethod
    def merge_matter(star_vec, meteorite_vec, learning_rate=0.1):
        new_vec = star_vec * (1 - learning_rate) + meteorite_vec * learning_rate
        return CosmosPhysics.normalize(new_vec)

class MemoryStar:
    def __init__(self, vector, label):
        self.vector = CosmosPhysics.normalize(vector)
        self.label = label
        self.mass = 1.0

class CosmosResonator:
    def __init__(self):
        self.galaxy = [] 
        self.resonance_threshold = 0.85 
    
    def perceive(self, x):
        x = CosmosPhysics.normalize(x)
        best_star = None
        max_gravity = -1.0
        for star in self.galaxy:
            gravity = CosmosPhysics.compute_gravity(x, star.vector)
            if gravity > max_gravity:
                max_gravity = gravity
                best_star = star
        return best_star, max_gravity

    def memorize(self, x, y):
        x = CosmosPhysics.normalize(x)
        best_star, gravity = self.perceive(x)
        # 如果最强引力的恒星就是目标类别的，且引力足够大，则强化它
        # 注意：这里简化了逻辑，直接用 label 判断。
        # 在更复杂的版本中，可能允许多个同label恒星。
        if best_star is not None and best_star.label == y and gravity > self.resonance_threshold:
            best_star.vector = CosmosPhysics.merge_matter(best_star.vector, x)
            best_star.mass += 1
            return "Reinforce (强化)"
        else:
            new_star = MemoryStar(x, y)
            self.galaxy.append(new_star)
            return "New_Creation (坍缩新星)"

# --- 2. 存档系统 ---
# --- 2. 存档系统 ---
DEFAULT_SAVE_FILE = "cosmos_brain.pkl"

def save_brain(brain, filename=DEFAULT_SAVE_FILE):
    # --- 修复 PicklingError ---
    # Streamlit 热重载可能导致 session_state 中的对象类定义
    # 与当前模块不一致。这里强制重新绑定到当前类。
    if brain.__class__.__name__ == "CosmosResonator":
        brain.__class__ = CosmosResonator
    
    for star in brain.galaxy:
        if star.__class__.__name__ == "MemoryStar":
            star.__class__ = MemoryStar

    with open(filename, 'wb') as f:
        pickle.dump(brain, f)

class CosmosUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # 兼容旧存档：如果在 Colab 的 __main__ 中定义的类，
        # 现在重定向到当前模块 cosmos_net
        if module == "__main__":
            # 只要当前模块有这个类，就重定向
            if name in globals():
                return globals()[name]
        return super().find_class(module, name)

def load_or_create_brain(filename=DEFAULT_SAVE_FILE):
    if os.path.exists(filename):
        try:
            with open(filename, 'rb') as f:
                # 使用自定义 Unpickler 解决 __main__ 命名空间问题
                brain = CosmosUnpickler(f).load()
            return brain, f"✅ 成功唤醒宇宙: {filename} (包含 {len(brain.galaxy)} 颗恒星)"
        except Exception as e:
            return CosmosResonator(), f"⚠️ 唤醒失败 ({str(e)})，正在创建新宇宙..."
    return CosmosResonator(), f"✨ 创建新宇宙 ({filename})..."

# --- 3. 核心：星图可视化引擎 ---
def get_star_map_figure(brain):
    stars = brain.galaxy
    if len(stars) < 3:
        return None, "星系太小，暂不展示星图 (需要至少3颗恒星)"

    # 提取向量和标签
    vectors = np.array([s.vector for s in stars])
    labels = np.array([s.label for s in stars])
    
    # t-SNE 降维
    perp = min(30, len(stars) - 1)
    if perp < 1: perp = 1
    tsne = TSNE(n_components=2, perplexity=perp, random_state=42, init='pca', learning_rate='auto')
    try:
        vectors_2d = tsne.fit_transform(vectors)
    except Exception as e:
        return None, f"TSNE 降维失败: {e}"

    # 构建图
    G = nx.Graph()
    for i in range(len(stars)):
        G.add_node(i, pos=vectors_2d[i], label=labels[i])
    
    # 计算连接 (引力 > 0.85)
    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            gravity = np.dot(stars[i].vector, stars[j].vector)
            if gravity > 0.85:
                G.add_edge(i, j, weight=(gravity - 0.85)*10)

    # 绘图
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.get_node_attributes(G, 'pos')
    
    # 画线
    edges = G.edges()
    if edges:
        weights = [G[u][v]['weight'] for u,v in edges]
        nx.draw_networkx_edges(G, pos, alpha=0.2, width=weights, edge_color='gray', ax=ax)
    
    # 画点 (不同数字不同颜色)
    # 假设 label 是 0-9 的整数
    colors = cm.rainbow(np.linspace(0, 1, 10))
    node_colors = []
    for lab in labels:
        try:
            idx = int(lab) % 10
            node_colors.append(colors[idx])
        except:
            node_colors.append(colors[0]) # Default fallback

    nx.draw_networkx_nodes(G, pos, node_size=100, node_color=node_colors, alpha=0.8, ax=ax)
    
    # 装饰
    legend_elements = [Line2D([0], [0], marker='o', color='w', label=str(i),
                          markerfacecolor=colors[i], markersize=8) for i in range(10)]
    ax.legend(handles=legend_elements, title="Class", loc='upper right', bbox_to_anchor=(1.15, 1), fontsize='small')
    ax.set_title(f"Cosmos Neural Topology ({len(stars)} Stars)", fontsize=12)
    ax.axis('off')
    
    return fig, "Success"
