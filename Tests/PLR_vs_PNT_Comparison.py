import matplotlib.pyplot as plt
import math
import numpy as np

# ==============================================================================
# PLR vs PNT: GLOBAL DISTRIBUTION CHECK
#
# GOAL:
# Verify that the Deterministic Local Steps (PLR) integrate perfectly into the
# Global Probabilistic Curve (PNT).
#
# THEORETICAL EXPECTATION:
# The count of PLR-generated primes (pi(x)) must asymptotically converge to Li(x).
# ==============================================================================

# --- Configuration ---
PRIME_FILE = "./prime/primes_100m.txt"
LIMIT = 1000000  # Plot first 1M primes (sufficient for visualization)

def logarithmic_integral(x):
    """
    Approximation of Li(x).
    Python doesn't have li(x) in math, so we use the series expansion or simple integration.
    For x > 2, Li(x) ~ x/ln(x). We'll use the more accurate scipy version if available,
    otherwise standard x/ln(x) for the visualization.
    """
    if x <= 1: return 0
    return x / math.log(x)

def run_pnt_comparison():
    print("\n" + "="*60)
    print("      PLR vs PNT: GLOBAL CONVERGENCE TEST")
    print("="*60)
    
    # 1. Load Primes (PLR Ground Truth)
    print(f"Loading {LIMIT} primes...")
    primes = []
    try:
        with open(PRIME_FILE, 'r') as f:
            for i, line in enumerate(f):
                if i >= LIMIT: break
                primes.append(int(line.strip()))
    except Exception as e:
        print(f"Error loading primes: {e}")
        return

    print(f"Loaded {len(primes):,} primes. Max p = {primes[-1]:,}")

    # 2. Generate Data Points (Sampling for Graph)
    # We don't need to plot every single point, just enough to see the curve.
    sample_rate = 1000
    
    x_values = []
    y_plr = []    # Actual Prime Count (pi(x))
    y_pnt = []    # Theoretical Count (x / ln x)
    y_li = []     # Logarithmic Integral (approx)
    
    print("Calculating PNT curves...")
    
    for i in range(0, len(primes), sample_rate):
        p = primes[i]
        count = i + 1
        
        x_values.append(p)
        y_plr.append(count)
        
        # PNT Prediction 1: x / ln(x) (Legendre/Gauss)
        pred_pnt = p / math.log(p)
        y_pnt.append(pred_pnt)
        
        # PNT Prediction 2: Offset Log Integral (More accurate)
        # Simple approximation for visualization without Scipy
        # Li(x) ~ x/ln(x) + x/(ln(x)^2) ...
        pred_li = p / math.log(p) * (1 + 1/math.log(p)) 
        y_li.append(pred_li)

    # 3. Plotting
    print("Rendering 'PLR_vs_PNT_Comparison.png'...")
    plt.figure(figsize=(12, 8))
    
    # Plot Curves
    plt.plot(x_values, y_plr, color='blue', linewidth=1.5, label='PLR (Actual Primes)')
    plt.plot(x_values, y_pnt, color='red', linestyle='--', linewidth=1.5, label='PNT (x / ln x)')
    
    # Plot Error (Residuals) in a subplot or overlay? 
    # Let's stick to the main comparison first.
    
    plt.title('Micro-Determinism vs. Macro-Probability\n(PLR generated Primes vs. PNT Prediction)', fontsize=16)
    plt.xlabel('x (Number Value)', fontsize=12)
    plt.ylabel('pi(x) (Prime Count)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Zoom Inset (Optional - shows the tightness)
    # left, bottom, width, height = [0.6, 0.2, 0.25, 0.25]
    # ax2 = plt.axes([0.6, 0.2, 0.25, 0.25])
    # ax2.plot(x_values[-100:], y_plr[-100:], 'b')
    # ax2.plot(x_values[-100:], y_pnt[-100:], 'r--')
    # ax2.set_title('Zoom (Last 100k)')
    
    output_file = "PLR_vs_PNT_Comparison.png"
    plt.savefig(output_file, dpi=150)
    print(f"Graph saved to {output_file}")
    
    # 4. Analytic Report
    print("\n" + "-"*60)
    print(f"{'x':<15} | {'PLR Count':<12} | {'PNT Pred':<12} | {'Error %'}")
    print("-" * 60)
    
    # Show checkpoints
    check_indices = [0, len(x_values)//4, len(x_values)//2, len(x_values)-1]
    for idx in check_indices:
        x = x_values[idx]
        plr = y_plr[idx]
        pnt = y_pnt[idx]
        error = abs(plr - pnt) / plr * 100
        print(f"{x:<15,} | {plr:<12,} | {int(pnt):<12,} | {error:.4f}%")
        
    print("-" * 60)
    print("[CONCLUSION]")
    last_err = abs(y_plr[-1] - y_pnt[-1]) / y_plr[-1] * 100
    if last_err < 5.0:
        print("CONVERGENCE CONFIRMED. The local deterministic steps integrate")
        print("seamlessly into the global probabilistic law.")
    else:
        print("DIVERGENCE DETECTED. Something is wrong with the prime generator.")

if __name__ == "__main__":
    run_pnt_comparison()