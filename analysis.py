import numpy as np
from cosmos_net import CorpusCallosum, CosmosPhysics

def calculate_system_entropy(brain):
    """
    Step 2.1: System Entropy (SE)
    Measure of 'Disorder' based on Mass Distribution.
    SE = -Sum(p_i * ln(p_i)), where p_i = star.mass / total_mass
    
    Interpretation:
    - Many small stars (Fragmentation) -> High Entropy (Chaos)
    - Few heavy stars (Consolidation) -> Low Entropy (Order)
    """
    galaxy = brain.right_hemisphere.galaxy
    if not galaxy:
        return 0.0
        
    total_mass = sum(s.mass for s in galaxy)
    if total_mass == 0:
        return 0.0
        
    entropy = 0.0
    for star in galaxy:
        p_i = star.mass / total_mass
        if p_i > 0:
            entropy -= p_i * np.log(p_i)
            
    return entropy

def calculate_conflict_degree(brain):
    """
    Step 2.2: Conflict Degree (CD)
    Measure of 'Semantic Contradiction'.
    CD = Mean(Intra-Class Variance) / Mean(Inter-Class Distance)
    
    Interpretation:
    - Stars of same concept are scattered (High Intra) -> High Conflict
    - Concepts are well separated (High Inter) -> Low Conflict
    """
    galaxy = brain.right_hemisphere.galaxy
    if not galaxy:
        return 0.0
        
    # Group by Label
    groups = {}
    for star in galaxy:
        if star.label not in groups:
            groups[star.label] = []
        groups[star.label].append(star.vector)
        
    # 1. Intra-Class Variance (How confused is the brain about 'A'?)
    variances = []
    centroids = []
    
    for label, vectors in groups.items():
        vecs = np.array(vectors)
        if len(vecs) > 1:
            # Mean Squared Distance from Centroid
            centroid = np.mean(vecs, axis=0)
            # Simple variance of Euclidean distances
            dists = np.linalg.norm(vecs - centroid, axis=1)
            var = np.mean(dists ** 2)
            variances.append(var)
        else:
            variances.append(0.0)
        centroids.append(np.mean(vecs, axis=0))
        
    mean_intra_var = np.mean(variances) if variances else 0.0
    
    # 2. Inter-Class Distance (Are 'A' and 'B' distinct?)
    if len(centroids) < 2:
        return mean_intra_var # Fallback if only 1 concept
        
    inter_dists = []
    for i in range(len(centroids)):
        for j in range(i+1, len(centroids)):
            d = np.linalg.norm(centroids[i] - centroids[j])
            inter_dists.append(d)
            
    mean_inter_dist = np.mean(inter_dists) if inter_dists else 1.0
    
    if mean_inter_dist == 0:
        return float('inf')
        
    return mean_intra_var / mean_inter_dist

def verify_metrics():
    print("🧪 Verification: Feasibility Step 2 (Technical Quantification)")
    print("-" * 60)
    
    brain = CorpusCallosum()
    
    # --- Phase 1: Generated Chaos (Simulate Step 1) ---
    print("\n[Phase 1] Detecting Chaos...")
    
    # 3 Concepts, 600 scattered stars
    centers = [np.random.rand(784) for _ in range(3)]
    labels = ["A", "B", "C"]
    
    # Force creation of separate stars (Resonance=10.0)
    brain.right_hemisphere.resonance_threshold = 10.0
    
    for i in range(200):
        for center, label in zip(centers, labels):
            noise = np.random.normal(0, 0.2, 784) # High variance for testing CD
            brain.memorize(center + noise, label)
            
    # Boost Mass to simulate 'Real' chaos (mass=2)
    for s in brain.right_hemisphere.galaxy:
        s.mass = 2
        
    cd_1 = calculate_conflict_degree(brain)
    se_1 = calculate_system_entropy(brain)
    print(f"Stats: {len(brain.right_hemisphere.galaxy)} Stars")
    print(f"Meas: CD={cd_1:.4f} | SE={se_1:.4f}")
    
    if cd_1 > 1.0 and se_1 > 5.0:
        print("✅ PASS: Successfully detected High Entropy/Conflict.")
    else:
        print("❌ FAIL: Metrics too low for Chaos.")
        
    # --- Phase 2: Dreamtime (Consolidation) ---
    print("\n[Phase 2] Detecting Order (After Dream)...")
    
    # Restore threshold and dream
    brain.right_hemisphere.resonance_threshold = 0.85
    brain.dream()
    
    cd_2 = calculate_conflict_degree(brain)
    se_2 = calculate_system_entropy(brain)
    print(f"Stats: {len(brain.right_hemisphere.galaxy)} Stars")
    print(f"Meas: CD={cd_2:.4f} | SE={se_2:.4f}")
    
    if cd_2 < cd_1 and se_2 < se_1:
         print("✅ PASS: Metrics dropped significantly.")
         print(f"    Delta CD: {cd_1:.4f} -> {cd_2:.4f}")
         print(f"    Delta SE: {se_1:.4f} -> {se_2:.4f}")
    else:
         print("❌ FAIL: Metrics did not reflect ordering.")

if __name__ == "__main__":
    verify_metrics()
