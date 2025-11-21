import matplotlib.pyplot as plt
import time

# ==============================================================================
# PLR SPECTRAL VISUALIZER: THE FRACTAL HIERARCHY (Mod 210)
#
# GOAL:
# Visualize the "Spectral Splitting" of the prime number line.
# We map Gap Size vs. Prime Value, colored by Structural Depth.
#
# COLOR KEY:
# - BLUE:   The Vacuum (0 mod 210) -> Lowest Resistance
# - CYAN:   Mod 30 Echoes (30, 60, 90...) -> Super-Clean
# - GREEN:  Mod 6 Echoes (6, 12, 18...) -> Semi-Clean
# - RED:    Messy Background (2, 4, 8...) -> High Resistance
# ==============================================================================

def get_structural_class(p_current, p_next):
    anchor = p_current + p_next
    residue = anchor % 210
    
    if residue == 0:
        return "Vacuum"
    elif residue % 30 == 0:
        return "Mod30_Echo"
    elif residue % 6 == 0:
        return "Mod6_Echo"
    else:
        return "Messy"

def generate_fractal_spectrum():
    print("Generating PLR Fractal Spectrum (Mod 210)...")
    
    # 1. Configuration
    LIMIT = 50000 # Scan depth for visualization
    
    # 2. Generate Primes
    sieve = [True] * (LIMIT + 1000)
    for i in range(2, int((LIMIT+1000)**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, LIMIT + 1000, i):
                sieve[j] = False
    primes = [i for i, is_p in enumerate(sieve) if is_p and i > 5] # Skip tiny primes
    
    # 3. Data Buckets
    data = {
        "Vacuum": {"x": [], "y": []},
        "Mod30_Echo": {"x": [], "y": []},
        "Mod6_Echo": {"x": [], "y": []},
        "Messy": {"x": [], "y": []}
    }
    
    print(f"Processing {len(primes)} primes...")
    
    for i in range(len(primes) - 1):
        p = primes[i]
        p_next = primes[i+1]
        gap = p_next - p
        
        # Determine Fractal Depth
        struct_type = get_structural_class(p, p_next)
        
        data[struct_type]["x"].append(p)
        data[struct_type]["y"].append(gap)

    # 4. Plotting
    print("Rendering 'PLR_Fractal_Spectrum_Mod210.png'...")
    plt.figure(figsize=(14, 8))
    
    # Plot Layers (Order matters: Messy first, then clean on top)
    
    # Layer 1: Messy (Red) - The background noise
    plt.scatter(data["Messy"]["x"], data["Messy"]["y"], 
                c='#E94A4A', label='Messy (High Resistance)', s=10, alpha=0.5)
                
    # Layer 2: Mod 6 Echoes (Green) - The semi-clean halo
    plt.scatter(data["Mod6_Echo"]["x"], data["Mod6_Echo"]["y"], 
                c='green', label='Mod 6 Echoes (Semi-Clean)', s=15, alpha=0.6)

    # Layer 3: Mod 30 Echoes (Cyan) - The super-clean structure
    plt.scatter(data["Mod30_Echo"]["x"], data["Mod30_Echo"]["y"], 
                c='cyan', label='Mod 30 Echoes (Super-Clean)', s=20, alpha=0.8)

    # Layer 4: The Vacuum (Blue) - The singularity
    plt.scatter(data["Vacuum"]["x"], data["Vacuum"]["y"], 
                c='blue', label='The Vacuum (0 mod 210)', s=40, alpha=1.0, edgecolors='black', linewidth=0.5)
    
    plt.title('The Fractal Hierarchy of Prime Gaps (Mod 210 Spectral Map)', fontsize=16)
    plt.xlabel('Prime Value (p)', fontsize=12)
    plt.ylabel('Gap Size', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    
    output_file = "PLR_Fractal_Spectrum_Mod210.png"
    plt.savefig(output_file, dpi=150)
    print(f"Graph saved to {output_file}")
    
    # 5. ASCII Summary
    print("\n" + "="*60)
    print(" FRACTAL SEPARATION CONFIRMATION")
    print("="*60)
    
    # Check what gaps are in the Vacuum
    vacuum_gaps = set(data["Vacuum"]["y"])
    print(f"Gaps found in Vacuum (0 mod 210): {sorted(list(vacuum_gaps))[:10]}...")
    
    if 6 not in vacuum_gaps:
        print("[VERDICT] CONFIRMED: Sexy Primes (Gap 6) are EXCLUDED from the Vacuum.")
    else:
        print("[VERDICT] ANOMALY: Sexy Primes found in Vacuum.")

if __name__ == "__main__":
    generate_fractal_spectrum()