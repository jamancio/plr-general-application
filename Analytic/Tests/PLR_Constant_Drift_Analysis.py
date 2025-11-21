import time
import math

# ==============================================================================
# PLR ANALYTIC TEST: CONSTANT DRIFT ANALYSIS (50M - HIGH PRECISION)
#
# GOAL:
# Determine the True Clean Constant at N=50,000,000 with the "k=1 Fix" applied.
# ==============================================================================

def run_drift_analysis_50m():
    print("\n" + "="*60)
    print("      PLR CONSTANT DRIFT ANALYSIS (50 MILLION)")
    print("="*60)
    
    # 1. Setup
    LIMIT = 50000000  # The Big Run
    CHECKPOINTS = [
        1000000, 5000000, 10000000, 15000000, 20000000, 
        25000000, 30000000, 35000000, 40000000, 45000000, 50000000
    ]
    
    print(f"Generating primes up to {LIMIT:,} (This may take 10-20s)...")
    start_sieve = time.time()
    sieve = [True] * (LIMIT + 1000)
    sieve[0] = sieve[1] = False
    for i in range(2, int((LIMIT+1000)**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, LIMIT + 1000, i):
                sieve[j] = False
    
    prime_list = [i for i, is_p in enumerate(sieve) if is_p and i >= 2]
    prime_set = set(prime_list)
    print(f"Database: {len(prime_list):,} primes loaded in {time.time()-start_sieve:.2f}s.")
    
    print("-" * 65)
    print(f"{'Checkpoint':<12} | {'Clean % (0)':<12} | {'Messy % (2)':<12} | {'Drift'}")
    print("-" * 65)

    clean_failures = 0
    clean_total = 0
    messy_failures = 0
    messy_total = 0
    
    stats_history = []
    
    # 2. The Analysis Loop
    # We use a slightly optimized logic to handle the large dataset
    
    for i in range(len(prime_list) - 2):
        p = prime_list[i]
        if p > LIMIT: break
        
        p_next = prime_list[i+1]
        anchor = p + p_next
        residue = anchor % 6
        
        found_k = False
        k_is_safe = False
        
        # Search radius increased to 400 for safety at 50M
        for k in range(1, 400): 
            # Check Neighbors (Anchor - k, Anchor + k)
            val_down = anchor - k
            val_up = anchor + k
            
            # Optimized check order
            check_down = (val_down != p and val_down != p_next and val_down in prime_set)
            check_up = (val_up != p and val_up != p_next and val_up in prime_set)
            
            if check_down or check_up:
                # Found the nearest prime structure!
                
                # THE FIX: k=1 is Safe (Twin/Cousin proximity)
                if k == 1:
                    k_is_safe = True
                # If k is prime, it is Safe
                elif k in prime_set:
                    k_is_safe = True
                # Otherwise, it is Composite (Failure)
                else:
                    k_is_safe = False
                
                found_k = True
                break
        
        if found_k:
            is_failure = not k_is_safe
            
            if residue == 0:
                clean_total += 1
                if is_failure: clean_failures += 1
            elif residue == 2 or residue == 4:
                messy_total += 1
                if is_failure: messy_failures += 1

        # --- CHECKPOINT REPORTING ---
        if CHECKPOINTS and p >= CHECKPOINTS[0]:
            current_clean_rate = (clean_failures / clean_total) * 100 if clean_total > 0 else 0
            current_messy_rate = (messy_failures / messy_total) * 100 if messy_total > 0 else 0
            
            drift_msg = "-"
            if stats_history:
                prev_c = stats_history[-1][0]
                delta = current_clean_rate - prev_c
                if delta > 0.001: drift_msg = "Rise"
                elif delta < -0.001: drift_msg = "Fall"
                else: drift_msg = "Flat"
            
            print(f"{p:<12} | {current_clean_rate:.4f}%      | {current_messy_rate:.4f}%      | {drift_msg}")
            
            stats_history.append((current_clean_rate, current_messy_rate))
            CHECKPOINTS.pop(0)

    # 3. Final Analysis
    print("-" * 65)
    print("FINAL CONSTANTS (N=50M):")
    
    end_clean = stats_history[-1][0]
    end_messy = stats_history[-1][1]
    
    print(f"Clean Channel Failure Rate: {end_clean:.4f}%")
    print(f"Messy Channel Failure Rate: {end_messy:.4f}%")
    
    # Ratio Check
    ratio = end_messy / end_clean if end_clean > 0 else 0
    print(f"Noise Ratio (Messy/Clean):  {ratio:.4f}x")
    
    if end_clean > 2.5:
        print("[VERDICT] The 2.71% constant is robust!")
    elif end_clean < 1.0:
        print("[VERDICT] The constant dropped to <1%. The previous 2.71% likely included k=1 'False Failures'.")
        print("          This implies the Clean Channel is SIGNIFICANTLY stronger than previously thought.")

if __name__ == "__main__":
    run_drift_analysis_50m()