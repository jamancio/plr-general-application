import matplotlib.pyplot as plt
import math

# ==============================================================================
# PLR VISUALIZATION: The Sacks Spiral (Corrected)
#
# GOAL:
# Map the primes onto the "Sacks Spiral" (Archimedean Lattice) to reveal
# geometric alignments.
#
# COLOR KEY:
# - Blue:   Clean Anchor (0 mod 6) -> The "Twin/Cousin" Channel
# - Red:    Messy Anchor (2/4 mod 6) -> The "Sexy" Channel
# ==============================================================================

def get_anchor_residue(p_current, p_next):
    anchor = p_current + p_next
    return anchor % 6

def generate_sacks_spiral():
    print("\n" + "="*60)
    print("      PLR SACKS SPIRAL VISUALIZER (CORRECTED)")
    print("="*60)
    print("Generating Prime Data...")
    
    # 1. Configuration
    LIMIT = 40000   # Higher count for better spiral arms
    DOT_SIZE = 0.8  # Smaller dots for cleaner curves
    
    # 2. Sieve Primes
    upper_bound = 500000
    sieve = [True] * (upper_bound + 1)
    for i in range(2, int(upper_bound**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, upper_bound + 1, i):
                sieve[j] = False
    
    primes = [i for i, is_prime in enumerate(sieve) if is_prime and i > 3]
    primes = primes[:LIMIT]
    
    print(f"Mapping {len(primes):,} primes to spiral coordinates...")

    # 3. Prepare Coordinates
    clean_r, clean_theta = [], []
    messy_r, messy_theta = [], []
    
    for i in range(len(primes) - 1):
        p = primes[i]
        p_next = primes[i+1]
        residue = get_anchor_residue(p, p_next)
        
        # --- THE SACKS SPIRAL FORMULA ---
        # r = sqrt(p)
        # theta = sqrt(p) * 2pi
        # This aligns squares (1, 4, 9, 16) along the East ray
        
        r = math.sqrt(p)
        theta = math.sqrt(p) * 2 * math.pi
        
        if residue == 0:
            clean_r.append(r)
            clean_theta.append(theta)
        else:
            messy_r.append(r)
            messy_theta.append(theta)

    # 4. Plotting
    print("Rendering 'PLR_Sacks_Spiral.png'...")
    plt.figure(figsize=(15, 15), facecolor='white')
    ax = plt.subplot(111, projection='polar')
    ax.set_facecolor('whitesmoke')
    
    # Plot Messy First (Background Layer)
    ax.scatter(messy_theta, messy_r, c='#ff5555', s=DOT_SIZE, alpha=0.5, label='Messy (Gap 6+)')
    
    # Plot Clean (Foreground Layer)
    ax.scatter(clean_theta, clean_r, c='#0044cc', s=DOT_SIZE, alpha=0.8, label='Clean (Gap 2/4)')
    
    # Styling
    plt.title('The PLR Sacks Spiral\nGeometric Phase Separation of Prime Gaps', fontsize=20, pad=20)
    ax.grid(False)          # Turn off grid for cleaner look
    ax.set_xticks([])       # Remove angle labels
    ax.set_yticks([])       # Remove radial labels
    
    # Add Legend
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.0), markerscale=10, fontsize=12)
    
    # Save
    output_file = "PLR_Sacks_Spiral.png"
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f"[SUCCESS] Graph saved to {output_file}")

if __name__ == "__main__":
    generate_sacks_spiral()