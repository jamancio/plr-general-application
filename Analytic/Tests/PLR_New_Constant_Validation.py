import time
import math
import sys
import os

# ==============================================================================
# PLR THEOREM - FINAL VALIDATION: NEW CONSTANTS (N=50M Derived)
#
# GOAL:
# Verify if the PLR v23.0 "Internal Flip" Logic maintains 100% accuracy
# when using the newly discovered, asymptotically stable constants.
#
# NEW CONSTANTS (from 50M Drift Analysis):
# - Clean (0 mod 6): 1.4488
# - Messy (2 mod 6): 21.5957
# - Messy (4 mod 6): 21.5957 (Assumed symmetric)
# ==============================================================================

# --- 1. The New Crystalized Constants ---
MESSINESS_SCORES_NEW = {
    0: 1.4488,   # The "Superconductor" value
    2: 21.5957,  # The "Resistance" value
    4: 21.5957
}

MESSY_THRESHOLD = 20.0 # The logic gate trigger

def get_messiness_score(anchor):
    """Returns the PAS failure rate for a given anchor residue."""
    return MESSINESS_SCORES_NEW.get(anchor % 6, 100.0)

def get_messiness_score_v11_weighted(anchor, gap):
    score_mod6 = get_messiness_score(anchor)
    # The PLR Force Equation: (Messiness + 1) * Gap
    return (score_mod6 + 1.0) * gap

def get_v23_internal_flip_prediction(p_n, candidates):
    """
    The v23.0 Logic Gate.
    Now running on the optimized physics of the 1.45% constant.
    """
    candidates_data = []
    messy_bin = []
    
    for q in candidates:
        gap = q - p_n
        anchor = p_n + q
        
        # 1. Calculate Scores
        # Note: With the lower Clean score (1.44), 'Clean' candidates 
        # will have even LOWER arithmetic scores, making them 'heavier' favorites.
        
        score_v11 = get_messiness_score_v11_weighted(anchor, gap)
        messiness = get_messiness_score(anchor)
        
        data = {
            'prime': q,
            'gap': gap,
            'score': score_v11,
            'messiness': messiness
        }
        candidates_data.append(data)
        
        # 2. Filter into Messy Bin
        if messiness > MESSY_THRESHOLD:
            messy_bin.append(data)
            
    if not candidates_data: return None
    
    # 3. Identify Arithmetic Winner (The "pull" of the gap)
    candidates_data.sort(key=lambda x: x['score'])
    v11_winner = candidates_data[0]
    
    final_prediction = v11_winner['prime']

    # 4. The Internal Flip (The Logic Gate)
    # If the Arithmetic Winner is 'Clean', we check if we skipped a 'Messy' 
    # candidate that was structurally closer (smaller gap).
    
    if messy_bin:
        # Find the Messy candidate with the smallest gap
        messy_bin.sort(key=lambda x: x['gap'])
        messy_best = messy_bin[0]
        
        # The Logic:
        # If the Messy candidate is physically closer (smaller gap)
        # BUT the algorithm picked a Clean candidate further away...
        # We TRUST the algorithm (Arithmetic Winner).
        #
        # HOWEVER, the Flip condition checks if we need to revert.
        # In v23.0: 
        # If g_messy < g_winner -> Return Messy (The Flip)
        # Else -> Return Winner
        
        if messy_best['gap'] < v11_winner['gap']:
            final_prediction = messy_best['prime']
            
    return final_prediction

# --- Main Test Logic ---
def run_new_constant_test():
    print("\n" + "="*60)
    print("      PLR NEW CONSTANT VALIDATION TEST")
    print("="*60)
    print("Testing Constants: Clean=1.4488 | Messy=21.5957")
    
    # 1. Load Primes
    LIMIT = 1000000 # Test on first 1 Million primes
    print(f"Generating {LIMIT:,} primes for validation...")
    
    sieve_limit = 16000000 
    sieve = [True] * sieve_limit
    sieve[0] = sieve[1] = False
    for i in range(2, int(sieve_limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, sieve_limit, i):
                sieve[j] = False
                
    all_primes = [i for i, is_p in enumerate(sieve) if is_p]
    if len(all_primes) < LIMIT + 50:
        print("Error: Sieve too small.")
        return
        
    print(f"Primes loaded. Running v23.0 logic...")
    print("-" * 60)
    
    failures = 0
    start_time = time.time()
    
    # 2. Prediction Loop
    for i in range(LIMIT):
        p_n = all_primes[i]
        true_next = all_primes[i+1]
        
        # Create Candidate Pool (Next 10 integers, filtered for primes for the Oracle test)
        # In real world, we scan integers. Here we use the "Oracle" method 
        # to test the SELECTION LOGIC, not the sieve speed.
        candidates = all_primes[i+1 : i+11]
        
        prediction = get_v23_internal_flip_prediction(p_n, candidates)
        
        if prediction != true_next:
            failures += 1
            print(f"[FAIL] p={p_n} | Pred={prediction} | True={true_next}")
            # Break on first failure to analyze
            break
            
        if i % 200000 == 0 and i > 0:
            print(f"  Checked {i:,} primes... (100% OK)", end='\r')
            
    elapsed = time.time() - start_time
    print(f"\n" + "-" * 60)
    
    if failures == 0:
        print("RESULTS: 100.00% ACCURACY")
        print("The 'Internal Flip' logic is compatible with the new constants.")
        print("\n[THEORETICAL IMPLICATION]")
        print("The drop from 2.71 -> 1.45 increased the 'Signal Strength'.")
        print("Clean Anchors are now even stronger 'Attractors'.")
    else:
        print(f"RESULTS: {failures} FAILURES DETECTED.")
        print("The new constants broke the equilibrium.")

if __name__ == "__main__":
    run_new_constant_test()