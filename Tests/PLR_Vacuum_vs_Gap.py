import matplotlib.pyplot as plt
import math

def generate_race_graph():
    print("Generating 'PLR_Vacuum_vs_Gap.png'...")
    
    # Primes for Primorials p_1 to p_15
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    
    # X-Axis: Index k
    k_values = list(range(1, len(primes))) 
    
    # Data Series
    horizon_y = [] # p_{k+1}^2
    gap_y = []     # ln(P_k#)
    
    # Calculate Primorials and derived values
    current_primorial_log = 0 # Log summing for stability
    
    # Labels for X-axis (Simplified for readability)
    x_labels = []
    
    for k in k_values:
        p_k = primes[k-1]
        p_next = primes[k] # p_{k+1}
        
        # 1. Calculate Vacuum Horizon (Defense)
        horizon = p_next ** 2
        horizon_y.append(horizon)
        
        # 2. Calculate Average Gap (Threat)
        # ln(P_k#) = sum(ln(p)) for p <= p_k
        current_primorial_log += math.log(p_k)
        gap = current_primorial_log
        gap_y.append(gap)
        
        x_labels.append(f"P_{k}#")

    plt.figure(figsize=(10, 6))
    
    # Plot Lines
    plt.plot(k_values, horizon_y, color='blue', linewidth=2.5, label='Defense: Vacuum Horizon ($p_{k+1}^2$)')
    plt.plot(k_values, gap_y, color='red', linestyle='--', linewidth=2.5, label='Threat: Avg Prime Gap ($\ln N$)')
    
    # Styling
    plt.title('The Race: Vacuum Stability Condition\n(Defense vs. Threat)', fontsize=14, pad=15)
    plt.xlabel('Primorial Scale ($P_k\#$)', fontsize=12)
    plt.ylabel('Distance (Magnitude)', fontsize=12)
    plt.legend(loc='upper left', fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # X-Ticks
    plt.xticks(k_values, x_labels, rotation=45)
    
    # Fill area to highlight the safety margin
    plt.fill_between(k_values, gap_y, horizon_y, color='blue', alpha=0.1, label='Safety Margin')

    # Save
    output_file = "PLR_Vacuum_vs_Gap.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Graph saved to {output_file}")

if __name__ == "__main__":
    generate_race_graph()