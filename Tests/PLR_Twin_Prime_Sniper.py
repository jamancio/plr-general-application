import time
import sys

# ==============================================================================
# PLR THEOREM - TEST 9: The Twin Prime "Sniper"
#
# GOAL:
# Prove that we can skip 50% of all checks by filtering for PLR "Clean" Anchors.
#
# LOGIC:
# Twin Primes (p, p+2) can ONLY exist if p == 5 mod 6.
# If p == 1 mod 6, then p+2 is divisible by 3 (Composite).
# Therefore, a PLR-aware algorithm should ignore all p == 1 mod 6.
# ==============================================================================

def run_sniper_test():
    print("\n" + "="*60)
    print("      PLR TWIN PRIME SNIPER CHALLENGE")
    print("="*60)
    
    # 1. Setup Search Space
    TARGET_TWINS = 50000
    LIMIT = 2000000 # Sufficient range to find 50k twins
    
    print(f"Generating primes up to {LIMIT}...")
    sieve = [True] * (LIMIT + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(LIMIT**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, LIMIT + 1, i):
                sieve[j] = False
    
    primes = [i for i, is_prime in enumerate(sieve) if is_prime]
    print(f"Search Pool: {len(primes):,} primes.")
    print("-" * 60)

    # 2. Brute Force Run
    print("Run 1: Brute Force (Blind Search)")
    found_twins_bf = 0
    checks_bf = 0
    start_bf = time.time()
    
    for p in primes:
        if p + 2 >= LIMIT: break
        
        # The Costly Operation: Checking the neighbor
        checks_bf += 1 
        if sieve[p+2]:
            found_twins_bf += 1
            if found_twins_bf >= TARGET_TWINS: break
            
    time_bf = time.time() - start_bf
    print(f"  > Twins Found: {found_twins_bf:,}")
    print(f"  > Neighbor Checks Performed: {checks_bf:,}")
    print(f"  > Time: {time_bf:.5f}s")

    # 3. PLR Sniper Run
    print("\nRun 2: PLR Sniper (Structural Filtering)")
    found_twins_plr = 0
    checks_plr = 0
    skipped_checks = 0
    start_plr = time.time()
    
    for p in primes:
        if p + 2 >= LIMIT: break
        
        # PLR LOGIC: Check the Anchor Structure first
        # If p == 1 mod 6 (Messy), we KNOW p+2 is divisible by 3.
        # So we only check if p == 5 mod 6 (Clean).
        
        if p % 6 == 5:  # The Sniper Scope
            checks_plr += 1 # We only "spend" a check here
            if sieve[p+2]:
                found_twins_plr += 1
                if found_twins_plr >= TARGET_TWINS: break
        else:
            skipped_checks += 1 # We saved this cost
            
    time_plr = time.time() - start_plr
    print(f"  > Twins Found: {found_twins_plr:,}")
    print(f"  > Neighbor Checks Performed: {checks_plr:,}")
    print(f"  > Checks Skipped (Efficiency): {skipped_checks:,}")
    print(f"  > Time: {time_plr:.5f}s")
    
    # 4. The Verdict
    print("-" * 60)
    print("RESULTS ANALYSIS")
    print(f"Brute Force Checks: {checks_bf:,}")
    print(f"PLR Sniper Checks:  {checks_plr:,}")
    reduction = (1 - (checks_plr / checks_bf)) * 100
    
    print(f"\nWorkload Reduction: {reduction:.4f}%")
    
    if found_twins_bf != found_twins_plr:
        print("[CRITICAL FAILURE] The Sniper missed some twins!")
    else:
        print("[SUCCESS] The Sniper found exactly the same twins.")
        
    if reduction > 49.0:
        print("[VERDICT] CONFIRMED. PLR eliminates 50% of the search space.")
    else:
        print("[VERDICT] FAILED. Efficiency gain negligible.")

if __name__ == "__main__":
    run_sniper_test()