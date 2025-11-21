import matplotlib.pyplot as plt
import time

# ==============================================================================
# PLR SPECTRAL VISUALIZER
#
# GOAL:
# Graphically demonstrate the "Phase Separation" of Prime Gaps based on
# the PLR Messiness Score (Mod 6 Anchor).
#
# HYPOTHESIS:
# - "Clean" Anchors (0 mod 6) should capture ALL Twin (2) and Cousin (4) gaps.
# - "Messy" Anchors (2, 4 mod 6) should capture ALL Sexy (6) gaps.
# - This visualizes WHY the Sexy density is 2x (it combines two messy channels).
# ==============================================================================

def get_anchor_residue(p_current, p_next):
    """Calculates the PLR Anchor Residue (Mod 6)."""
    anchor = p_current + p_next
    return anchor % 6

def generate_plr_spectrum():
    print("Generating PLR Spectral Data...")
    
    # 1. Load Primes (Small sample for clear graphing)
    LIMIT = 10000
    primes = []
    sieve = [True] * (LIMIT + 1)
    for i in range(2, int(LIMIT**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, LIMIT + 1, i):
                sieve[j] = False
    primes = [i for i, is_prime in enumerate(sieve) if is_prime and i > 3] # Skip 2,3
    
    # 2. Collect Data Points
    x_clean = [] # Index for Clean
    y_clean = [] # Gap for Clean
    
    x_messy_2 = [] # Index for Messy 2
    y_messy_2 = [] # Gap for Messy 2
    
    x_messy_4 = [] # Index for Messy 4
    y_messy_4 = [] # Gap for Messy 4
    
    stats = {0: {}, 2: {}, 4: {}}
    
    for i in range(len(primes) - 1):
        p = primes[i]
        p_next = primes[i+1]
        gap = p_next - p
        anchor_res = get_anchor_residue(p, p_next)
        
        # Record Stats for Text Report
        if gap not in stats[anchor_res]: stats[anchor_res][gap] = 0
        stats[anchor_res][gap] += 1
        
        # Record Coordinates for Graph
        if anchor_res == 0:
            x_clean.append(p)
            y_clean.append(gap)
        elif anchor_res == 2:
            x_messy_2.append(p)
            y_messy_2.append(gap)
        elif anchor_res == 4:
            x_messy_4.append(p)
            y_messy_4.append(gap)

    # 3. Generate the Graph (Saved to file)
    print("Plotting 'PLR_Spectral_Graph.png'...")
    plt.figure(figsize=(12, 8))
    
    # Plot Clean (Blue)
    plt.scatter(x_clean, y_clean, c='blue', label='Clean Anchor (0 mod 6)', alpha=0.6, s=10)
    
    # Plot Messy (Red/Orange)
    plt.scatter(x_messy_2, y_messy_2, c='red', label='Messy Anchor (2 mod 6)', alpha=0.6, s=10)
    plt.scatter(x_messy_4, y_messy_4, c='orange', label='Messy Anchor (4 mod 6)', alpha=0.6, s=10)
    
    plt.title('The PLR Spectral Fingerprint: Gap Size vs. Messiness', fontsize=16)
    plt.xlabel('Prime Value (p)', fontsize=12)
    plt.ylabel('Gap Size (g)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    
    output_file = "PLR_Spectral_Graph.png"
    plt.savefig(output_file)
    print(f"Graph saved to {output_file}")
    
    # 4. Print ASCII Summary for Verification
    print("\n" + "="*60)
    print(" PLR SPECTRAL DATA SUMMARY")
    print("="*60)
    print(f"{'Anchor Type':<20} | {'Dominant Gaps Found'}")
    print("-" * 60)
    
    clean_gaps = sorted(stats[0].keys())[:5]
    messy_2_gaps = sorted(stats[2].keys())[:5]
    messy_4_gaps = sorted(stats[4].keys())[:5]
    
    print(f"{'Clean (0 mod 6)':<20} | {clean_gaps} ...")
    print(f"{'Messy (2 mod 6)':<20} | {messy_2_gaps} ...")
    print(f"{'Messy (4 mod 6)':<20} | {messy_4_gaps} ...")
    print("-" * 60)
    print("[INTERPRETATION]")
    if 2 in stats[0] and 4 in stats[0] and 6 not in stats[0]:
        print("CONFIRMED: Small Gaps (2, 4) are EXCLUSIVE to Clean Anchors.")
    if 6 in stats[2] or 6 in stats[4]:
        print("CONFIRMED: Sexy Gaps (6) are EXCLUSIVE to Messy Anchors.")
        
if __name__ == "__main__":
    generate_plr_spectrum()