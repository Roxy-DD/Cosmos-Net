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

def generate_chaos_brain():
    """Helper to generate a consistent Chaos Brain."""
    brain = CorpusCallosum()
    brain.right_hemisphere.resonance_threshold = 10.0 # Force separate stars
    
    centers = [np.random.rand(784) for _ in range(3)]
    labels = ["A", "B", "C"]
    
    for i in range(200):
        for center, label in zip(centers, labels):
            noise = np.random.normal(0, 0.2, 784)
            brain.memorize(center + noise, label)
            
    # Boost mass to survive pruning
    for s in brain.right_hemisphere.galaxy:
        s.mass = 2
        
    return brain

def find_optimal_k():
    print("\n🧪 Verification: Feasibility Step 3 (Critical Threshold Derivation)")
    print("-" * 60)
    print("Hypothesis: Threshold = k * (Conflict_Degree / System_Entropy)")
    
    # 1. Measure Chaos Baseline
    base_brain = generate_chaos_brain()
    cd_0 = calculate_conflict_degree(base_brain)
    se_0 = calculate_system_entropy(base_brain)
    ratio = cd_0 / se_0
    
    print(f"Baseline Chaos: CD={cd_0:.4f}, SE={se_0:.4f}, Ratio(CD/SE)={ratio:.4f}")
    
    # 2. Run Sweep
    print(f"\nScanning k from 0.1 to 2.0...")
    print(f"{'k':<6} | {'Threshold':<10} | {'Final Stars':<12} | {'Final CD':<10} | {'Status'}")
    print("-" * 60)
    
    best_k = 0
    best_cd = float('inf')
    
    for k in np.arange(0.1, 2.1, 0.1):
        # Fresh brain per run
        brain = generate_chaos_brain()
        
        # Calculate dynamic threshold
        # T = k * (CD/SE)
        # Note: In standard Dream, we hardcode 0.99 inside dream().
        # Here we must override that logic. We'll modify the threshold used by RightHemisphere.
        
        # Calculate dynamic threshold
        # Hypothesis: T = k * (CD/SE) (Normalized to meaningful range)
        # Note: CD/SE in chaos is ~2.3 (15/6.4). 0.85/2.3 = 0.36
        # Let's try raw ratio first, but clamp it.
        
        # Actually, let's look at the data structure.
        # We need T (0.8 ~ 1.0).
        # CD/SE is ~2.3.
        # So maybe relation is: T = 1.0 - k * (SE/CD) ? 
        # Low Entropy -> High Threshold (Precision). High Entropy -> Low Threshold (Tolerance)?
        # No, High Entropy (Chaos) means we need to MERGE heavily, so Threshold should be LOWER?
        # Wait, if T is low (0.5), EVERYTHING merges into one blob.
        # If T is high (0.99), only identical things merge.
        # To fix Chaos, we want to specific merge the 3 clouds.
        # So we probably want T around 0.95-0.99.
        
        # Let's just sweep T directly first to find the optimal T_opt.
        # Then check if T_opt relates to CD/SE.
        calc_threshold = k # Direct sweep for T
        
        brain.dream(threshold=calc_threshold)
        
        final_stars = len(brain.right_hemisphere.galaxy)
        final_cd = calculate_conflict_degree(brain)
        
        status = ""
        if final_stars == 3 and final_cd < 0.01:
            status = "✅ OPTIMAL"
            if final_cd < best_cd:
                best_cd = final_cd
                best_k = k
        elif final_stars < 3:
            status = "⚠️ Over-merge"
        elif final_stars > 3:
            status = "⚠️ Under-merge"
            
        print(f"{k:<6.2f} | {calc_threshold:<10.2f} | {final_stars:<12} | {final_cd:<10.4f} | {status}")

    print("-" * 60)
    print(f"🏆 Best Threshold Found: {best_k:.2f}")
    
    # Back-derive relationship
    # If CD_0 ~ 15, SE_0 ~ 6. Ratio ~ 2.5.
    # If Best T ~ 0.80.
    # T = k_form * Ratio? 0.8 / 2.5 = 0.32.
    print(f"Hypothetical Formula Coeff: k = Threshold / (CD/SE) = {best_k / ratio:.4f}")

if __name__ == "__main__":
    # verify_metrics()
    find_optimal_k()
