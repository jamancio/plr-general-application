import time
import math
import json
import sys
import os

# ==============================================================================
# PLR THEOREM - TEST 7 (UPDATED): Triplet Shielding & Convergence Analysis
#
# NEW FEATURE:
# Checkpoint logging every 1M gaps to visualize the convergence of the
# Sexy/Twin ratio.
# ==============================================================================

# --- Engine Setup (v23.0 "Internal Flip" Logic) ---
# (Hardcoded constants for standalone execution)
MESSINESS_SCORES = {
    0: 2.7126,  # Clean
    2: 26.2627, # Messy
    4: 26.2859  # Messy
}

def get_messiness_score(anchor):
    """Returns the PAS failure rate for a given anchor residue."""
    return MESSINESS_SCORES.get(anchor % 6, 100.0)

# --- Configuration ---
PRIME_INPUT_FILE = "./prime/primes_100m.txt" # Ensure this matches your file path
PRIMES_TO_TEST = 50000000
POOL_SIZE = 210
CHECKPOINT_INTERVAL = 1000000  # Report every 1 Million gaps

# --- Main Analysis Logic ---
def run_triplet_analysis():
    print(f"\nStarting PLR Triplet & Shielding Analysis (Test 7 - Checkpoint Mode)...")
    print(f"Target: Analyze convergence of Sexy/Twin ratio over {PRIMES_TO_TEST:,} gaps.")
    
    # 1. Load Primes
    if not os.path.exists(PRIME_INPUT_FILE):
        print(f"FATAL ERROR: '{PRIME_INPUT_FILE}' not found.")
        return

    print(f"Loading primes...")
    start_load = time.time()
    with open(PRIME_INPUT_FILE, 'r') as f:
        # Load enough primes for the test + buffer
        # We read line by line to support large files
        all_primes = [int(line.strip()) for i, line in enumerate(f) if i < PRIMES_TO_TEST + 500]
    print(f"Loaded {len(all_primes):,} primes in {time.time() - start_load:.2f}s.")

    # 2. Initialize Counters
    counts = {
        'twin': 0,      # Gap 2
        'cousin': 0,    # Gap 4
        'sexy_con': 0,  # Gap 6 (Consecutive)
        'triplet_a': 0, # Gap Sequence 2 -> 4
        'triplet_b': 0  # Gap Sequence 4 -> 2
    }
    
    prev_gap = 0
    total_gaps = 0
    
    print(f"\n{'N (Millions)':<15} | {'Twin Dens':<12} | {'Sexy Dens':<12} | {'Ratio (Target 2.0)'}")
    print("-" * 70)
    
    start_time = time.time()
    
    # 3. The Analysis Loop
    for i in range(PRIMES_TO_TEST):
        p_n = all_primes[i]
        p_next = all_primes[i+1]
        gap = p_next - p_n
        total_gaps += 1
        
        # Count Basic Gaps
        if gap == 2: counts['twin'] += 1
        elif gap == 4: counts['cousin'] += 1
        elif gap == 6: counts['sexy_con'] += 1
        
        # Count Triplets (The Shielding Effect)
        if gap == 4 and prev_gap == 2:
            counts['triplet_a'] += 1
        if gap == 2 and prev_gap == 4:
            counts['triplet_b'] += 1
            
        prev_gap = gap

        # --- CHECKPOINT LOGIC ---
        if total_gaps % CHECKPOINT_INTERVAL == 0:
            # Calculate temporary densities
            current_total = total_gaps
            d_twin = (counts['twin'] / current_total) * 1000
            d_sexy_con = (counts['sexy_con'] / current_total) * 1000
            d_triplet_a = (counts['triplet_a'] / current_total) * 1000
            d_triplet_b = (counts['triplet_b'] / current_total) * 1000
            
            d_sexy_total = d_sexy_con + d_triplet_a + d_triplet_b
            ratio = d_sexy_total / d_twin if d_twin > 0 else 0
            
            # Print Checkpoint Row
            print(f" {current_total//1000000:>3}M Gaps       | {d_twin:.4f}       | {d_sexy_total:.4f}       | {ratio:.5f}x")

    elapsed = time.time() - start_time
    print("-" * 70)
    print(f"Analysis complete in {elapsed:.2f}s.\n")
    
    # 4. Final Report Calculation (Recalculate for precision)
    d_twin = (counts['twin'] / total_gaps) * 1000
    d_cousin = (counts['cousin'] / total_gaps) * 1000
    d_sexy_con = (counts['sexy_con'] / total_gaps) * 1000
    d_triplet_a = (counts['triplet_a'] / total_gaps) * 1000
    d_triplet_b = (counts['triplet_b'] / total_gaps) * 1000
    d_sexy_total = d_sexy_con + d_triplet_a + d_triplet_b
    ratio_sexy_twin = d_sexy_total / d_twin if d_twin > 0 else 0

    # 5. Report
    print("="*60)
    print(" PLR THEOREM: STRUCTURAL TRIPLET ANALYSIS REPORT")
    print("="*60)
    print(f"{'Structure Type':<25} | {'Count':<12} | {'Density (per 1000)'}")
    print("-" * 60)
    print(f"{'Twin Primes (2)':<25} | {counts['twin']:<12,} | {d_twin:.4f}")
    print(f"{'Cousin Primes (4)':<25} | {counts['cousin']:<12,} | {d_cousin:.4f}")
    print("-" * 60)
    print(f"{'Consecutive Sexy (6)':<25} | {counts['sexy_con']:<12,} | {d_sexy_con:.4f}")
    print(f"{'Triplet A (2->4)':<25} | {counts['triplet_a']:<12,} | {d_triplet_a:.4f}")
    print(f"{'Triplet B (4->2)':<25} | {counts['triplet_b']:<12,} | {d_triplet_b:.4f}")
    print("-" * 60)
    print(f"{'TOTAL SEXY PAIRS':<25} | {(counts['sexy_con'] + counts['triplet_a'] + counts['triplet_b']):<12,} | {d_sexy_total:.4f}")
    print("=" * 60)
    
    print("\n--- ANALYTIC VERIFICATION ---")
    print(f"Theoretical Prediction (Hardy-Littlewood): Sexy Density ~= 2.0 * Twin Density")
    print(f"Final Measured Twin Density:               {d_twin:.4f}")
    print(f"Final Actual Sexy Density:                 {d_sexy_total:.4f}")
    print(f"Final Ratio:                               {ratio_sexy_twin:.5f}x")

if __name__ == "__main__":
    run_triplet_analysis()