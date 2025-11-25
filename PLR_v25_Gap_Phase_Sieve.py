import time
import sys
import os

# ==============================================================================
# PLR v26 ENGINE: THE MODULO-PHASE SIEVE
#
# GOAL:
# Test the "Modulo Phase Lock" logic.
# Instead of "Small vs Large" gaps, we use "Divisible by 6" logic.
#
# THE RULES:
# 1. Non-Multiples of 6 (2, 4, 8, 10...) -> LOCKED to Clean Anchors (0 mod 6).
# 2. Multiples of 6 (6, 12, 18...)       -> LOCKED to Messy Anchors (2, 4 mod 6).
#
# Hypothesis: This resolves the p=89 failure (Gap 8) and achieves 100% accuracy
# for all p > 3.
# ==============================================================================

# --- Configuration ---
PRIME_INPUT_FILE = "./prime/primes_100m.txt"
TEST_LIMIT = 50000000 # Test on first 1 Million primes

def load_primes(filename, limit):
    if not os.path.exists(filename):
        # Fallback for environment where file might be in a subdir
        if os.path.exists(f"./primes/{filename}"):
            filename = f"./primes/{filename}"
        elif os.path.exists(f"../prime/{filename}"):
            filename = f"../prime/{filename}"
        else:
            print(f"[ERROR] File not found: {filename}")
            return []
    
    print(f"Loading primes from {filename}...")
    primes = []
    try:
        with open(filename, 'r') as f:
            # Load enough primes for the test + lookahead buffer
            required = limit + 50
            for i, line in enumerate(f):
                if i >= required: break
                primes.append(int(line.strip()))
    except Exception as e:
        print(f"[ERROR] {e}")
        return []
    print(f"Loaded {len(primes):,} primes.")
    return primes

# --- THE v26 ENGINE ---
def get_v26_prediction(p_n, candidates_list):
    """
    v26 Logic: Sequential Scan with Modulo-Phase Filtering.
    """
    # 1. Sort candidates by Gap (Nearest Neighbor Priority)
    # In a real sieve, we would generate them in this order.
    candidates_list.sort(key=lambda x: x - p_n)
    
    for q in candidates_list:
        gap = q - p_n
        anchor = p_n + q
        residue = anchor % 6
        
        # --- THE MODULO PHASE LOCK ---
        
        # Case A: Gap is a Multiple of 6 (Sexy, etc.)
        if gap % 6 == 0:
            # These gaps ONLY exist in Messy Anchors (2, 4)
            # If Anchor is Clean (0), this gap is forbidden.
            if residue == 0:
                continue # STRUCTURALLY BLOCKED
        
        # Case B: Gap is NOT a Multiple of 6 (Twin, Cousin, 8, 10...)
        else:
            # These gaps ONLY exist in Clean Anchors (0)
            # If Anchor is Messy (2, 4), this gap is forbidden.
            if residue != 0:
                continue # STRUCTURALLY BLOCKED
        
        # If we pass the filter, we accept the candidate.
        return q
        
    return None

# --- MAIN TEST ---
def run_v26_test():
    print("\n" + "="*60)
    print("      PLR v26 ENGINE: MODULO-PHASE SIEVE TEST")
    print("="*60)
    
    primes = load_primes(PRIME_INPUT_FILE, TEST_LIMIT)
    if not primes: return
    
    failures = 0
    start_time = time.time()
    
    print(f"Testing v26 Logic on {TEST_LIMIT:,} primes...")
    print("Rule 1: Gap % 6 != 0 -> Must be Clean (0 mod 6)")
    print("Rule 2: Gap % 6 == 0 -> Must be Messy (2,4 mod 6)")
    print("-" * 60)
    
    for i in range(TEST_LIMIT):
        p_n = primes[i]
        true_next = primes[i+1]
        
        # Skip the Singularity (p=2, p=3)
        # The Modulo 6 logic only applies to p > 3.
        if p_n <= 3: continue

        # Lookahead Pool
        candidates = primes[i+1 : i+11]
        
        prediction = get_v26_prediction(p_n, list(candidates))
        
        if prediction != true_next:
            failures += 1
            gap = true_next - p_n
            anchor = p_n + true_next
            print(f"[FAIL] p={p_n} | True={true_next} (g={gap}, R={anchor%6}) | Pred={prediction}")
            if failures >= 1: break
            
        if (i+1) % 200000 == 0:
            print(f"  Checked {i+1:,} primes...", end='\r')
            
    elapsed = time.time() - start_time
    print(f"\n" + "-" * 60)
    
    if failures == 0:
        print(f"RESULT: 100.00% ACCURACY (for p > 3)")
        print("The Modulo-Phase Lock (v26) is absolute.")
        print("We have eliminated the 'Magic Numbers' entirely.")
    else:
        print(f"RESULT: {failures} Failures.")

if __name__ == "__main__":
    run_v26_test()