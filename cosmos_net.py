import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.lines import Line2D

import pickle
import os
import io
import networkx as nx
from sklearn.manifold import TSNE
from PIL import Image, ImageOps
import plotly.graph_objects as go

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
    """
    Cosmos-Net 的基本单元：记忆恒星 (Memory Star)
    v9.0 Upgrade: Now supports Hierarchy (Children).
    """
    def __init__(self, vector, label, creation_time=None):
        self.vector = vector
        self.label = label
        self.creation_time = creation_time if creation_time else time.time()
        self.mass = 1        # 质量 (被唤醒次数)
        self.children = []   # v9.0: Sub-stars (子恒星/具体实例)
        self.radius = 0.95   # v9.0: Concept Radius (The more massive, the tighter/looser?)

    def is_category(self):
        return len(self.children) > 0

class RightHemisphere:
    """
    v10.0: The Intuitive Core (Formerly CosmosResonator)
    Responsible for: Vector Similarity, Gravity, Perception, Art.
    Thinking System: Fast, Associative.
    """
    def __init__(self):
        self.galaxy = []  # Root nodes
        self.resonance_threshold = 0.85
        self.mitosis_threshold = 5

    def perceive(self, input_vec, pool=None):
        """Standard Cosmos-Net Perception"""
        if pool is None:
            pool = self.galaxy

        if not pool:
            return None, 0.0

        candidates = []
        for star in pool:
            gravity = CosmosPhysics.compute_gravity(star.vector, input_vec)
            candidates.append((star, gravity))

        candidates.sort(key=lambda x: (x[1], getattr(x[0], 'creation_time', 0)), reverse=True)
        best_star, max_gravity = candidates[0]

        if max_gravity > self.resonance_threshold and best_star.is_category():
            child_best, child_gravity = self.perceive(input_vec, pool=best_star.children)
            if child_best and child_gravity > max_gravity:
                 return child_best, child_gravity

        return best_star, max_gravity

    def memorize(self, x, y, pool=None):
        """Standard Cosmos-Net Gravity Memory + Mitosis"""
        x = CosmosPhysics.normalize(x)
        current_galaxy = pool if pool is not None else self.galaxy
        
        best_star = None
        max_gravity = -1.0
        
        # Local search (non-recursive for decision making)
        for star in current_galaxy:
            gravity = CosmosPhysics.compute_gravity(x, star.vector)
            if gravity > max_gravity:
                max_gravity = gravity
                best_star = star
                
        # Case A: Resonance Found
        if best_star is not None and best_star.label == y and max_gravity > self.resonance_threshold:
            if best_star.mass > self.mitosis_threshold:
                return self.memorize(x, y, pool=best_star.children)
            else:
                best_star.vector = CosmosPhysics.merge_matter(best_star.vector, x)
                best_star.mass += 1
                return f"Reinforce (Right Brain: {y})"
                
        # Case B: Novelty
        else:
            new_star = MemoryStar(x, y)
            current_galaxy.append(new_star)
            if pool is not None:
                return "Mitosis (Right Brain Branch)"
            else:
                return "New_Creation (Right Brain Star)"

    def dream(self, threshold=0.99, noise_level=0.0):
        """
        The Dreamtime: Memory Consolidation & Pruning.
        1. Prune: Remove weak memories (Mass <= 2).
        2. Consolidate: Merge very similar stars (Gravity > threshold).
        3. Noise (Sleep Spindles): Inject random noise to escape local optima.
        """
        start_count = len(self.galaxy)
        
        # 1. Prune (Forget Noise)
        # Keep stars that are either "Heavy" (Verified) OR "Young" (Just learned)
        # We don't have 'age' strictly tracked per iterate, but we can trust Mass for now.
        # Let's say mass=1 is vulnerable.
        # EXCEPT: If total galaxy is small, don't kill it.
        if start_count > 50:
            self.galaxy = [s for s in self.galaxy if s.mass > 1]
        
        pruned_count = start_count - len(self.galaxy)

        # 1.5 Noise Injection (Sleep Spindles - The Dialectical Leap)
        # Maybe chaos helps us find better order?
        if noise_level > 0.0:
            for star in self.galaxy:
                # Add noise to normalized vector
                perturbation = np.random.normal(0, noise_level, star.vector.shape)
                star.vector += perturbation
                # Re-normalize to maintain cosine similarity validity
                norm = np.linalg.norm(star.vector)
                if norm > 0:
                     star.vector /= norm
        
        # 2. Consolidate (Merge Similarity)
        # Simple greedy approach: Sort by mass (preserve important ones), then merge smaller into larger.
        self.galaxy.sort(key=lambda s: s.mass, reverse=True)
        
        merged_count = 0
        new_galaxy = []
        
        # We iterate through sorted stars. If a star is close to an existing 'kept' star, merge it.
        # Otherwise, keep it.
        for star in self.galaxy:
            merged = False
            for kept_star in new_galaxy:
                if star.label == kept_star.label: # Only merge same concepts
                    gravity = CosmosPhysics.compute_gravity(star.vector, kept_star.vector)
                    if gravity > threshold: # Extremely similar
                        # Merge star INTO kept_star
                        # Weighted average of vectors
                        total_mass = kept_star.mass + star.mass
                        rate = star.mass / total_mass
                        kept_star.vector = CosmosPhysics.merge_matter(kept_star.vector, star.vector, rate)
                        kept_star.mass = total_mass
                        
                        # Merge children if any
                        kept_star.children.extend(star.children)
                        
                        merged = True
                        merged_count += 1
                        break
            
            if not merged:
                new_galaxy.append(star)
                
        self.galaxy = new_galaxy
        final_count = len(self.galaxy)
        
        return f"Dream Cycle Complete. Pruned: {pruned_count}, Merged: {merged_count}. Stars: {start_count} -> {final_count}"

    def get_all_stars(self, pool=None):
        if pool is None: pool = self.galaxy
        all_stars = []
        for s in pool:
            all_stars.append(s)
            if s.children:
                all_stars.extend(self.get_all_stars(s.children))
        return all_stars

class LeftHemisphere:
    """
    v10.0: The Logical Core (The Statistician)
    Responsible for: Rules, Geometry, Distribution Statistics.
    Thinking System: Slow, Analytic, Aggregated.
    """
    def __init__(self):
        # Memory: Stores statistical distributions for each digit (0-9)
        # Format: { label: { 'aspect_ratio': [mean, n, variance], 'density': ... } }
        self.knowledge_base = {}
        # Sensitivity for "Logic Veto"
        self.confidence_threshold = 2.0 # Sigma (Standard Deviations)

    def _extract_features(self, vector):
        """Extract geometric features from the flat vector (assuming 28x28 image)"""
        # Note: Input vector is already normalized, but for geometric features 
        # we might want the original shape. 
        # However, we only have the normalized vector here. 
        # Ideally, we should pass the original image, but let's approximate from vector.
        # Since vector is normalized, absolute values are lost, but relative shapes (distribution) remain.
        
        # 1. Pixel Density (How much "ink"?)
        density = np.sum(np.abs(vector)) 
        
        # 2. Center of Mass (roughly) - simple heuristic
        # Reshape to 28x28 roughly (vector is 784 or 1280)
        # If it's MobileNet vector (1280), we can't do geometry.
        # If it's pure pixels (784), we can.
        # Check vector size!
        is_pixel_data = (len(vector) == 784)
        
        features = {'density': density}
        
        if is_pixel_data:
            img = vector.reshape(28, 28)
            h_proj = np.sum(img, axis=1)
            w_proj = np.sum(img, axis=0)
            
            # Aspect Ratio (Height / Width of bounding box)
            h_non_zero = np.count_nonzero(h_proj > 0.1)
            w_non_zero = np.count_nonzero(w_proj > 0.1)
            if w_non_zero == 0: w_non_zero = 1
            features['aspect_ratio'] = h_non_zero / w_non_zero
            
            # Central Mass Ratio (Center 14x14 vs Outer)
            center_mass = np.sum(img[7:21, 7:21])
            total_mass = np.sum(img) + 1e-6
            features['center_ratio'] = center_mass / total_mass
            
        return features, is_pixel_data

    def memorize(self, x, y):
        """Update statistical models (Online Welford's Algorithm or simple accumulation)"""
        features, valid = self._extract_features(x)
        if not valid: return # Can't do geometry on MobileNet vectors yet
        
        if y not in self.knowledge_base:
            self.knowledge_base[y] = {}
        
        for key, val in features.items():
            if key not in self.knowledge_base[y]:
                # [count, mean, M2] (M2 for variance calculation)
                self.knowledge_base[y][key] = [0, 0.0, 0.0]
            
            n, mean, m2 = self.knowledge_base[y][key]
            n += 1
            delta = val - mean
            mean += delta / n
            delta2 = val - mean
            m2 += delta * delta2
            
            self.knowledge_base[y][key] = [n, mean, m2]

    def perceive(self, input_vec):
        """
        Analyze fit with known distributions.
        Returns: (BestLabel, ConfidenceScore)
        ConfidenceScore is based on how many Standard Deviations away the input is.
        """
        features, valid = self._extract_features(input_vec)
        if not valid or not self.knowledge_base: return None, 0.0
        
        best_label = None
        min_deviation = float('inf')
        
        # Check against all known classes
        for label, stats in self.knowledge_base.items():
            total_z_score = 0
            count = 0
            
            for key, val in features.items():
                if key in stats:
                    n, mean, m2 = stats[key]
                    if n < 2: continue # Not enough data
                    variance = m2 / (n - 1)
                    std_dev = np.sqrt(variance) + 1e-6
                    
                    # Z-Score: How weird is this input for this class?
                    z = abs(val - mean) / std_dev
                    total_z_score += z
                    count += 1
            
            if count > 0:
                avg_z = total_z_score / count
                if avg_z < min_deviation:
                    min_deviation = avg_z
                    best_label = label
        
        # Convert deviation to confidence (Lower deviation = Higher confidence)
        # If avg_z < 1.0 (within 1 sigma), confidence is distinct.
        if min_deviation < 1.0:
            return best_label, 1.0 # High Logic Confidence
        elif min_deviation < 2.0:
            return best_label, 0.5 # Moderate
        else:
            return None, 0.0 # Logic is confused

class CorpusCallosum:
    """
    v10.0: The Bridge (Manager)
    Resolves conflicts between Right (Intuition) and Left (Logic).
    Mechanism: Dynamic Equilibrium (Dominance Shifting).
    """
    def __init__(self):
        self.right_hemisphere = RightHemisphere()
        self.left_hemisphere = LeftHemisphere()
        # Dominance: 0.0 (Pure Left/Logic) <-> 1.0 (Pure Right/Intuition)
        # Starts perfectly balanced (Tao).
        self.dominance = 0.5 
        self.learning_rate = 0.05 # How fast dominance shifts based on success

    @property
    def galaxy(self):
        # Expose Right Brain's galaxy for visualization compatibility
        return self.right_hemisphere.galaxy

    def perceive(self, input_vec):
        """
        Parallel Processing + Inhibitory Selection
        """
        # 1. Parallel Processing (Both Think)
        r_star, r_grav = self.right_hemisphere.perceive(input_vec)
        l_label, l_conf = self.left_hemisphere.perceive(input_vec)
        
        # 2. Weighted Decision (The Battle for Expression)
        # Right Score (Intuition * Dominance)
        r_score = r_grav * self.dominance
        
        # Left Score (Logic * (1 - Dominance))
        # Note: Left returns None if confused, check valid
        if l_label is None: l_conf = 0.0
        l_score = l_conf * (1.0 - self.dominance)
        
        # 3. Arbitration (Inhibition)
        if r_score >= l_score:
            # Right Brain Wins (Inhibits Left)
            return r_star, r_grav
        else:
            # Left Brain Wins (Inhibits Right)
            # Fallback: Create a temporary Dummy Star for visualization consistency.
            # We assign the correct label (Logic's choice) but need a vector for the UI to be happy?
            # We can use the input_vec as the temporary 'star' vector.
            dummy_star = MemoryStar(input_vec, l_label)
            dummy_star.mass = 0 # Ephemeral
            return dummy_star, l_conf

    def memorize(self, x, y):
        """
        Co-Evolution & Dynamic Adaptation
        """
        # 1. Check "Who WOULD have been right?" (Hind-sight)
        r_star, r_grav = self.right_hemisphere.perceive(x)
        l_label, l_conf = self.left_hemisphere.perceive(x)
        
        r_correct = (r_star is not None and r_star.label == y)
        l_correct = (l_label == y)
        
        # 2. Shift Dominance (Survival of the Fittest Hemisphere)
        status_msg = ""
        
        if r_correct and not l_correct:
            # Right was right, Left was wrong -> Right gains dominance
            self.dominance = min(1.0, self.dominance + self.learning_rate)
            status_msg = f"Intuition Wins (+Right). Dominance: {self.dominance:.2f}"
            
        elif l_correct and not r_correct:
            # Left was right, Right was wrong -> Left gains dominance
            self.dominance = max(0.0, self.dominance - self.learning_rate)
            status_msg = f"Logic Wins (+Left). Dominance: {self.dominance:.2f}"
            
        else:
            # Both wrong or Both right -> Equilibrium maintained
            status_msg = f"Consensus/Confusion. Dominance: {self.dominance:.2f}"

        # 3. Cross-Education (Both Learn from the Truth)
        # "Inhibit Expression, Not Learning"
        self.left_hemisphere.memorize(x, y)
        r_msg = self.right_hemisphere.memorize(x, y)
        
        return f"{r_msg} | {status_msg}"

    def dream(self, threshold=0.99, noise_level=0.0):
        """
        Enter The Dreamtime.
        """
        # 1. Right Brain consolidates memories
        r_msg = self.right_hemisphere.dream(threshold=threshold, noise_level=noise_level)
        
        # 2. Left Brain could also prune outliers? (Future)
        
        return f"💤 {r_msg}"
        
    def get_all_stars(self):
        return self.right_hemisphere.get_all_stars()

# --- 2. 存档系统 ---
DEFAULT_SAVE_FILE = "cosmos_brain.pkl"

def save_brain(brain, filename=DEFAULT_SAVE_FILE):
    # Fix for pickling classes defined in __main__ (Streamlit issue)
    # We map current classes to module level to handle hot-reloading
    try:
        if brain.__class__.__name__ == "CorpusCallosum":
             brain.__class__ = CorpusCallosum
        
        # Recurse into children (Fix for 'RightHemisphere' mismatch error)
        if hasattr(brain, 'right_hemisphere') and brain.right_hemisphere:
            if brain.right_hemisphere.__class__.__name__ == "RightHemisphere":
                brain.right_hemisphere.__class__ = RightHemisphere
        
        if hasattr(brain, 'left_hemisphere') and brain.left_hemisphere:
            if brain.left_hemisphere.__class__.__name__ == "LeftHemisphere":
                brain.left_hemisphere.__class__ = LeftHemisphere
                
    except Exception as e:
        print(f"Warning: Could not rebind classes: {e}")
    
    with open(filename, 'wb') as f:
        pickle.dump(brain, f)

class CosmosUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Migration Logic for Old Brains
        if module == "__main__":
             if name in globals(): return globals()[name]
             
        # Map old names to new names if necessary? 
        # Actually, if we load an old "CosmosResonator", we can keep the class definition 
        # but locally alias it to RightHemisphere for code compatibility?
        # Or better: Load it as is, then Wrap it.
        return super().find_class(module, name)

# Alias for backward compatibility during Unpickling if strictly needed
CosmosResonator = RightHemisphere 

def load_or_create_brain(filename=DEFAULT_SAVE_FILE):
    if os.path.exists(filename):
        try:
            with open(filename, 'rb') as f:
                brain = CosmosUnpickler(f).load()
            
            # v10.0 Migration: If we loaded an old RightHemisphere (CosmosResonator),
            # wrap it in a CorpusCallosum.
            if isinstance(brain, RightHemisphere): # CosmosResonator is alias
                print("🧠 Evolving Brain to v10.0 (Bicameral)...")
                new_brain = CorpusCallosum()
                new_brain.right_hemisphere = brain # Transfer the old galaxy
                return new_brain, f"✅ 大脑已进化为双院制心智 (v10.0). Old memories preserved in Right Hemisphere."
            
            return brain, f"✅ 成功唤醒双院制大脑: {filename}"
        except Exception as e:
            return CorpusCallosum(), f"⚠️ 唤醒失败 ({str(e)})，正在创建新大脑..."
    return CorpusCallosum(), f"✨ 创建新大脑 ({filename})..."

# --- 3. 核心：星图可视化引擎 ---
def get_star_map_figure(brain):
    # v10.1: 3D Visualization using Plotly
    stars = brain.get_all_stars()
    
    if len(stars) < 3:
        return None, "星系太小，暂不展示星图 (需要至少3颗恒星)"

    # 提取向量和标签
    vectors = np.array([s.vector for s in stars])
    labels = np.array([s.label for s in stars])
    
    if not np.all(np.isfinite(vectors)):
        return None, "数据包含无效值 (NaN/Inf)，无法绘制星图。"

    # t-SNE 降维 (3 Components for 3D)
    # Perplexity 必须小于 n_samples
    n_samples = len(vectors)
    perp = min(30, n_samples - 1)
    if perp < 1: perp = 1
    
    tsne = TSNE(n_components=3, perplexity=perp, random_state=42, init='pca', learning_rate='auto')
    try:
        vectors_3d = tsne.fit_transform(vectors)
    except Exception as e:
        return None, f"TSNE 降维失败: {e}"

    # Double Check sizes
    num_points = min(len(stars), len(vectors_3d))
    
    # 准备 3D 数据
    x_vals = vectors_3d[:num_points, 0]
    y_vals = vectors_3d[:num_points, 1]
    z_vals = vectors_3d[:num_points, 2]
    
    # 颜色映射 (0-9)
    colors = []
    # Use Plotly numerical colors
    for lab in labels[:num_points]:
        try:
            val = int(lab) % 10
            colors.append(val)
        except:
            colors.append(0)

    # 创建 3D 散点图
    fig = go.Figure(data=[go.Scatter3d(
        x=x_vals,
        y=y_vals,
        z=z_vals,
        mode='markers', # Remove 'text' mode to avoid clutter, show on hover
        marker=dict(
            size=5,
            color=colors,
            colorscale='Rainbow',
            opacity=0.8
        ),
        text=labels[:num_points], # Hover text
        hoverinfo='text'
    )])

    # 计算连接 (引力 > 0.85) - 3D Lines
    # Plotly draws lines by adding None between segments
    edge_x = []
    edge_y = []
    edge_z = []
    
    # Optimization: If too many stars, don't draw lines (Clutter reduction)
    draw_lines = (num_points <= 300)
    
    if draw_lines:
        for i in range(num_points):
            for j in range(i + 1, num_points):
                gravity = np.dot(stars[i].vector, stars[j].vector)
                if gravity > 0.85:
                    # Add line segment
                    edge_x.extend([x_vals[i], x_vals[j], None])
                    edge_y.extend([y_vals[i], y_vals[j], None])
                    edge_z.extend([z_vals[i], z_vals[j], None])

    if edge_x:
        fig.add_trace(go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode='lines',
            line=dict(color='gray', width=1, dash='solid'),
            opacity=0.1,
            hoverinfo='none'
        ))

    # 布局设置
    fig.update_layout(
        title=f"Cosmos Neural Topology (3D) - {len(stars)} Stars",
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='rgba(0,0,0,0)' # Transparent background
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return fig, "Success"
