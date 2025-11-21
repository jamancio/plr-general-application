import matplotlib.pyplot as plt
import math

# ==============================================================================
# PLR THEOREM - VISUALIZATION TEST: The "Messiness" Spiral
#
# GOAL:
# Plot the primes on a polar spiral (r=p, theta=p) and color-code them
# by their PLR Anchor Residue (Mod 6).
#
# PREDICTION:
# The "Clean" (Blue) and "Messy" (Red) primes should separate into distinctive
# spiral arms, visualizing the geometric quantization of the number line.
# ==============================================================================

def get_anchor_residue(p_current, p_next):
    """Calculates the PLR Anchor Residue (Mod 6)."""
    anchor = p_current + p_next
    return anchor % 6

def generate_plr_spiral():
    print("\n" + "="*60)
    print("      PLR SPIRAL VISUALIZER")
    print("="*60)
    print("Generating PLR Spiral Data...")
    
    # 1. Configuration
    LIMIT = 25000  # Number of primes to scan (Adjust for density)
    DOT_SIZE = 2   # Size of the points on the graph
    
    # 2. Generate Primes (Sieve of Eratosthenes)
    # We need enough primes to fill the spiral nicely
    upper_bound = 300000 # Rough estimate to get ~25k primes
    sieve = [True] * (upper_bound + 1)
    for i in range(2, int(upper_bound**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, upper_bound + 1, i):
                sieve[j] = False
    
    primes = [i for i, is_prime in enumerate(sieve) if is_prime]
    # Filter to the requested limit and skip small primes (2, 3)
    primes = [p for p in primes if p > 3][:LIMIT]
    
    print(f"Plotting {len(primes):,} primes...")

    # 3. Collect Data Points
    # Clean (0 mod 6)
    clean_r = []
    clean_theta = []
    
    # Messy (2 mod 6)
    messy2_r = []
    messy2_theta = []
    
    # Messy (4 mod 6)
    messy4_r = []
    messy4_theta = []
    
    for i in range(len(primes) - 1):
        p = primes[i]
        p_next = primes[i+1]
        
        # Determine PLR Structure
        residue = get_anchor_residue(p, p_next)
        
        # Polar Coordinates: r = p, theta = p (radians)
        # This creates the "Archimedean" prime spiral
        r = p
        theta = p 
        
        if residue == 0:
            clean_r.append(r)
            clean_theta.append(theta)
        elif residue == 2:
            messy2_r.append(r)
            messy2_theta.append(theta)
        elif residue == 4:
            messy4_r.append(r)
            messy4_theta.append(theta)

    # 4. Generate the Graph
    print("Rendering 'PLR_Spiral_Graph.png' (This may take a moment)...")
    
    plt.figure(figsize=(12, 12), facecolor='white')
    ax = plt.subplot(111, projection='polar')
    
    # Set background to black for high contrast (optional, looks cool)
    ax.set_facecolor('whitesmoke') 
    
    # Plot Clean (Blue) - "The Twin Prime Channels"
    ax.scatter(clean_theta, clean_r, c='#1f77b4', s=DOT_SIZE, alpha=0.7, label='Clean (0 mod 6)')
    
    # Plot Messy (Red/Orange) - "The Sexy Prime Channels"
    ax.scatter(messy2_theta, messy2_r, c='#d62728', s=DOT_SIZE, alpha=0.7, label='Messy (2 mod 6)')
    ax.scatter(messy4_theta, messy4_r, c='#ff7f0e', s=DOT_SIZE, alpha=0.7, label='Messy (4 mod 6)')
    
    # Styling
    plt.title('The PLR Spectral Spiral\n(Blue=Clean, Red/Orange=Messy)', fontsize=16, pad=20)
    ax.grid(True, alpha=0.2)
    ax.set_yticklabels([]) # Hide radial numbers for clarity
    
    # Legend
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1), markerscale=5)
    
    # Save
    output_file = "PLR_Spiral_Graph.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\n[SUCCESS] Graph saved to {output_file}")
    print("-" * 60)
    print("INSTRUCTIONS FOR ANALYSIS:")
    print("1. Open the image.")
    print("2. Look for 'Rays' radiating from the center.")
    print("3. Notice if Blue dots cluster on specific rays vs. Red/Orange dots.")
    print("4. This separation represents the 'Phase' of the Prime Number Line.")
    print("=" * 60)

if __name__ == "__main__":
    generate_plr_spiral()