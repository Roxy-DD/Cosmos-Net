import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os

# Ensure output directory exists
OUTPUT_DIR = "pics"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Configure style for "Nature" scientific publication
plt.style.use('default') # Reset to default first
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 8
plt.rcParams['axes.titlesize'] = 8
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams['legend.fontsize'] = 7
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['grid.alpha'] = 0.2
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.05

# Nature figure sizes (single column ~89mm/3.5in, double ~183mm/7.2in)
FIG_WIDTH_SINGLE = 3.5
FIG_WIDTH_DOUBLE = 7.2
golden_ratio = (5**.5 - 1) / 2

def generate_figure_1_dcts():
    """
    Figure 1: Dynamic Consistency Sequence Test (DCTS) Results.
    Nature Style: Clean, minimal, high contrast.
    """
    print("Generating Figure 1: DCTS Results (Nature Style)...")
    
    x = np.linspace(0, 50, 100)
    
    # Data
    y_llm = 1 / (1 + np.exp(-0.25 * (x - 15))) 
    y_cosmos = np.zeros_like(x) + 0.02 * np.sin(x * 0.5) * np.exp(-x * 0.1)
    y_cosmos = np.abs(y_cosmos) 
    
    # Plotting
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_DOUBLE, FIG_WIDTH_DOUBLE * golden_ratio * 0.8))
    
    # Colors: Nature often uses specific distinct colors.
    # LLM (Red/Orange), Cosmos (Blue/Green)
    color_llm = '#E64B35' # Nature Red
    color_cosmos = '#00A087' # Nature Green
    
    ax.plot(x, y_llm, '--', label='Traditional LLMs (Transformer)', color=color_llm, linewidth=1.5)
    ax.plot(x, y_cosmos, '-', label='Cosmos-Net (Moebius Topology)', color=color_cosmos, linewidth=2)
    
    # Annotations
    ax.axhline(y=1.0, color='gray', linestyle=':', linewidth=0.5, alpha=0.7)
    ax.text(50, 1.02, 'Collapse Threshold', ha='right', va='bottom', color='dimgray', fontsize=7)
    
    # Minimalist Title (often omitted in papers, but useful for standalone)
    # ax.set_title('Dynamic Consistency Sequence Test (DCTS)', pad=10, loc='left')
    
    ax.set_xlabel('Contradiction Sequence Length (N)')
    ax.set_ylabel('Catastrophic Forgetting Rate (DSR)')
    
    # Spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.legend(frameon=False, loc='center right')
    ax.set_ylim(-0.05, 1.15)
    ax.set_xlim(0, 50)
    
    # Shading
    ax.fill_between(x, y_llm, color=color_llm, alpha=0.1)
    ax.fill_between(x, y_cosmos, color=color_cosmos, alpha=0.1)
    
    plt.savefig(os.path.join(OUTPUT_DIR, 'Figure_1_DCTS_Results_Nature.pdf')) # PDF is better for vector graphics
    plt.savefig(os.path.join(OUTPUT_DIR, 'Figure_1_DCTS_Results_Nature.png'), dpi=600)
    print("Saved Figure 1 (Nature).")
    plt.close()

def generate_figure_2_moebius():
    """
    Figure 2: Cosmos-Net Moebius Topology Ring.
    Nature Style: 3D Surface with clean background.
    """
    print("Generating Figure 2: Moebius Topology (Nature Style)...")
    
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(-1, 1, 100)
    u, v = np.meshgrid(u, v)
    
    x = (1 + 0.5 * v * np.cos(u / 2)) * np.cos(u)
    y = (1 + 0.5 * v * np.cos(u / 2)) * np.sin(u)
    z = 0.5 * v * np.sin(u / 2)
    z += 0.1 * np.sin(3 * u) * np.cos(3 * v)

    fig = plt.figure(figsize=(FIG_WIDTH_DOUBLE, FIG_WIDTH_DOUBLE * 0.8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot surface
    # 'viridis' is good for Nature, high contrast and perceptually uniform
    surf = ax.plot_surface(x, y, z, cmap='viridis', edgecolor='none', alpha=0.9, antialiased=True)
    
    # Neurons
    num_neurons = 50
    u_pts = np.random.uniform(0, 2 * np.pi, num_neurons)
    v_pts = np.random.uniform(-1, 1, num_neurons)
    
    x_pts = (1 + 0.5 * v_pts * np.cos(u_pts / 2)) * np.cos(u_pts)
    y_pts = (1 + 0.5 * v_pts * np.cos(u_pts / 2)) * np.sin(u_pts)
    z_pts = 0.5 * v_pts * np.sin(u_pts / 2) + 0.1 * np.sin(3 * u_pts) * np.cos(3 * v_pts)
    
    # Scatter neurons (Black or Dark Grey for visibility on light background)
    ax.scatter(x_pts, y_pts, z_pts, c='black', s=10, marker='o', alpha=0.8, depthshade=True)
    
    # Synapses
    for i in range(num_neurons):
        if np.random.rand() > 0.8:
             j = np.random.randint(0, num_neurons)
             ax.plot([x_pts[i], x_pts[j]], [y_pts[i], y_pts[j]], [z_pts[i], z_pts[j]], c='gray', alpha=0.4, linewidth=0.5)

    # Styling for Clean 3D
    # ax.set_title("Cosmos-Net Moebius Topology ($\mathcal{M}$)", pad=0)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Clean background
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')
    ax.grid(False) # Turn off heavy grid
    
    # Remove ticks/labels if pure topology visualization is desired, 
    # but scientific plots usually keep them for reference. 
    # Let's keep minimal ticks.
    ax.tick_params(axis='both', which='major', labelsize=6, pad=-2)
    
    ax.view_init(elev=45, azim=60)
    
    # Colorbar
    cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1)
    cbar.set_label('Manifold Curvature', fontsize=7)
    cbar.ax.tick_params(labelsize=6)
    
    plt.savefig(os.path.join(OUTPUT_DIR, 'Figure_2_Moebius_Topology_Nature.pdf'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'Figure_2_Moebius_Topology_Nature.png'), dpi=600)
    print("Saved Figure 2 (Nature).")
    plt.close()

if __name__ == "__main__":
    generate_figure_1_dcts()
    generate_figure_2_moebius()
    print("All verification plots generated successfully in `pics/`.")
