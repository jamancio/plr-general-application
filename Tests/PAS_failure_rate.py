# ==============================================================================
# PLR/PAS UNIFIED ANALYSIS - TEST 5: The "Messiness Score" Verification
#
# NEW RESEARCH FRONTIER: UNIVERSALIZING THE PLR THEOREM
#
# This is the final analytic test that unifies PAS and PLR.
#
# GOAL:
# To prove that the "Messiness Scores" (2.71% and 26.29%) used in our
# 100%-accurate PLR engine are the *actual, measured*
# PAS Law I Failure Rates for their respective v_mod6 residue bins.
#
# METHODOLOGY:
# 1. Loop through all 50 million prime pairs (p_n, p_{n+1}).
# 2. For each anchor S_n = p_n + p_{n+1}, find its residue (S_n % 6).
# 3. Find the k_min (distance to the nearest prime) for that anchor.
# 4. If k_min is composite, log it as a "Law I Failure" for that residue.
# 5. At the end, print a table showing the Failure Rate for all bins.
#
# HYPOTHESIS:
# The Failure Rate for (Residue 0) will be ~2.71%.
# The Failure Rate for (Residue 2, 4) will be ~26.29%.
# This will prove the PLR engine is a direct model of PAS reality.
# ==============================================================================

import time
import math
import json
from collections import defaultdict

# --- Configuration ---
PRIME_INPUT_FILE = "prime/primes_100m.txt"
PRIMES_TO_TEST = 50000000
START_INDEX = 10 # Start at p_10

# --- Function to load primes from a file ---
def load_primes_from_file(filename):
    """Loads ALL primes and the set for lookups."""
    print(f"Loading ALL primes from {filename}...")
    start_time = time.time()
    try:
        with open(filename, 'r') as f:
            prime_list = [int(line.strip()) for line in f]
    except FileNotFoundError:
        print(f"FATAL ERROR: The prime file '{filename}' was not found.")
        return None, None
    
    prime_set = set(prime_list)
    end_time = time.time()
    print(f"Loaded {len(prime_list):,} primes and set in {end_time - start_time:.2f} seconds.")
    
    required_primes = PRIMES_TO_TEST + START_INDEX + 2
    if len(prime_list) < required_primes:
        print(f"\nFATAL ERROR: Prime file is too small for this test.")
        return None, None
        
    return prime_list, prime_set

def is_prime(k_val, prime_set):
    """Helper function to check if k is prime."""
    if k_val < 2: return False
    return k_val in prime_set

def get_k_min(anchor_sn, prime_set):
    """Finds the k_min for a given anchor."""
    min_distance_k = 0
    search_dist = 1
    while True:
        q_lower = anchor_sn - search_dist
        q_upper = anchor_sn + search_dist
        if q_lower in prime_set: min_distance_k = search_dist; break
        if q_upper in prime_set: min_distance_k = search_dist; break
        search_dist += 1
        if search_dist > 2000: return -1 # Failsafe
    return min_distance_k
    
# --- Main Testing Logic ---
def run_unified_analysis():
    
    prime_list, prime_set = load_primes_from_file(PRIME_INPUT_FILE)
    if prime_list is None: return

    print(f"\nStarting PLR/PAS Unified Analysis (Test 5) for {PRIMES_TO_TEST:,} primes...")
    print(f"  - Measuring Law I Failure Rate for all S_n % 6 residues.")
    print("-" * 80)
    start_time = time.time()
    
    total_anchors_tested = 0
    
    # --- Data structures ---
    anchor_counts = defaultdict(int)
    failure_counts = defaultdict(int)

    loop_end_index = PRIMES_TO_TEST + START_INDEX
    
    if loop_end_index >= len(prime_list) - 1:
        print(f"\nFATAL ERROR: Not enough primes loaded.")
        return

    for i in range(START_INDEX, loop_end_index):
        if (i - START_INDEX + 1) % 100000 == 0:
            elapsed = time.time() - start_time
            progress = i - START_INDEX + 1
            print(f"Progress: {progress:,} / {PRIMES_TO_TEST:,} | Time: {elapsed:.0f}s", end='\r')

        
        anchor_S_n = prime_list[i] + prime_list[i + 1]
        residue = anchor_S_n % 6
        
        total_anchors_tested += 1
        anchor_counts[residue] += 1
        
        # --- Check Law I Status ---
        k_min = get_k_min(anchor_S_n, prime_set)
        
        is_k_composite = (k_min > 1) and not is_prime(k_min, prime_set)
        
        if is_k_composite:
            failure_counts[residue] += 1
            
    # --- Final Summary ---
    progress = total_anchors_tested
    print(f"Progress: {progress:,} anchors tested | Time: {time.time() - start_time:.0f}s")
    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print("-" * 80)

    print("\n" + "="*20 + " PAS/PLR Unified Theory Report (Test 5) " + "="*20)
    print(f"\nTotal Anchors Analyzed (S_n): {total_anchors_tested:,}")
    
    print("\n" + "-" * 20 + " PAS Law I Failure Rate by Residue " + "-" * 20)
    print(f"\n{'S_n % 6 Residue':<15} | {'Total Anchors':<20} | {'Total Failures':<15} | {'Failure Rate (%)':<20}")
    print("-" * 75)

    # We know p_n + p_{n+1} (for n > 1) is always even.
    # Residues 1, 3, 5 are impossible and will have 0 anchors.
    
    residues_to_check = [0, 2, 4, 1, 3, 5]
    
    for res in residues_to_check:
        anchors = anchor_counts.get(res, 0)
        failures = failure_counts.get(res, 0)
        
        failure_rate = (failures / anchors) * 100 if anchors > 0 else 0
        
        rate_str = f"{failure_rate:.4f}%"
        if anchors == 0:
            rate_str = "N/A (Impossible)"

        print(f"{res:<15} | {anchors:<20,} | {failures:<15,} | {rate_str:<20}")
        
    
    # --- Final Conclusion ---
    print("\n\n" + "="*20 + " FINAL ANALYTIC CONCLUSION " + "="*20)
    
    rate_0 = (failure_counts.get(0, 0) / anchor_counts.get(0, 0)) * 100
    rate_2 = (failure_counts.get(2, 0) / anchor_counts.get(2, 0)) * 100
    rate_4 = (failure_counts.get(4, 0) / anchor_counts.get(4, 0)) * 100
    
    if (abs(rate_0 - 2.71) < 0.1) and (abs(rate_2 - 26.2) < 0.1) and (abs(rate_4 - 26.2) < 0.1):
        print(f"\n  [VERDICT: UNIFIED THEOREM CONFIRMED]")
        print(f"  The measured PAS Failure Rate for Residue 0 is {rate_0:.4f}%.")
        print(f"  The measured PAS Failure Rate for Residue 2 is {rate_2:.4f}%.")
        print(f"  The measured PAS Failure Rate for Residue 4 is {rate_4:.4f}%.")
        print("\n  This proves the PLR engine's 'Messiness Scores' (2.71% and 26.29%)")
        print("  are the *literal, measured structural failure rates* of the PAS.")
        print("  The entire system is one unified, deterministic law.")
    else:
        print("\n  [VERDICT: ANOMALY DETECTED]")
        print("  The measured failure rates do NOT match the PLR engine's scores.")
        print("  The link between PAS and PLR is not 1-to-1.")

    print("=" * (50 + len(" FINAL ANALYTIC CONCLUSION ")))

if __name__ == "__main__":
    run_unified_analysis()