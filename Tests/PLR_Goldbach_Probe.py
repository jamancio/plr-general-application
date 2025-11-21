import time
import math

# ==============================================================================
# PLR THEOREM - TEST 8: The Goldbach-PLR Connection
#
# GOAL:
# Determine if the PLR "Messiness" (Mod 6) predicts the stratification
# of Goldbach's Comet (the number of prime partitions for even numbers).
#
# HYPOTHESIS:
# Even numbers with "Clean" PLR scores (0 mod 6) will have ~2x the partitions
# of numbers with "Messy" PLR scores (2, 4 mod 6), mirroring the Sexy/Twin ratio.
# ==============================================================================

# --- Engine Setup (Standard PLR Constants) ---
# Messiness scores from your previous files
MESSINESS_SCORES = {
    0: 2.7126,   # Clean (Multiples of 6)
    2: 26.2627,  # Messy
    4: 26.2859   # Messy
}

def get_messiness_score(n):
    """Returns the PLR Messiness score for an even number n."""
    return MESSINESS_SCORES.get(n % 6, 100.0)

# --- Primes Sieve (Eratosthenes) ---
# We need a fast prime lookup to check E - p
def get_primes_and_set(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    
    primes = [i for i, is_prime in enumerate(sieve) if is_prime]
    prime_set = set(primes)
    return primes, prime_set

# --- Main Analysis ---
def run_goldbach_probe():
    print("\nStarting PLR-Goldbach Probe...")
    LIMIT = 100000  # Scan evens up to 100k
    
    # 1. Generate Primes
    print(f"Generating primes up to {LIMIT}...")
    start_t = time.time()
    primes, prime_set = get_primes_and_set(LIMIT)
    print(f"Found {len(primes):,} primes. (Time: {time.time()-start_t:.4f}s)")

    # 2. Iterate Even Numbers
    print(f"Scanning Goldbach partitions for even numbers up to {LIMIT}...")
    
    # Storage for statistics
    # Keys are the Mod 6 residues (0, 2, 4)
    stats = {
        0: {'count': 0, 'sum_partitions': 0},
        2: {'count': 0, 'sum_partitions': 0},
        4: {'count': 0, 'sum_partitions': 0}
    }
    
    start_t = time.time()
    
    # We start at 6 to avoid edge cases with 2, 4
    for E in range(6, LIMIT + 1, 2):
        if E % 5000 == 0:
            print(f"  Processing E = {E}...", end='\r')
            
        # Count Goldbach Partitions: p + q = E  (where p <= q)
        # Logic: Iterate p. Check if (E-p) is in prime_set.
        # Optimization: p <= E/2
        
        partitions = 0
        for p in primes:
            if p > E // 2: 
                break
            if (E - p) in prime_set:
                partitions += 1
        
        # PLR Classification
        residue = E % 6
        if residue in stats:
            stats[residue]['count'] += 1
            stats[residue]['sum_partitions'] += partitions
            
    print(f"\nScan complete. (Time: {time.time()-start_t:.4f}s)")
    
    # 3. Report Results
    print("\n" + "="*60)
    print(" PLR-GOLDBACH CONNECTION REPORT")
    print("="*60)
    print(f"{'PLR Type':<15} | {'Residue':<8} | {'Avg Partitions':<15} | {'Relative Scale'}")
    print("-" * 60)
    
    # Calculate averages
    avg_0 = stats[0]['sum_partitions'] / stats[0]['count']
    avg_2 = stats[2]['sum_partitions'] / stats[2]['count']
    avg_4 = stats[4]['sum_partitions'] / stats[4]['count']
    
    # Base scale (normalize against the lowest avg)
    base = min(avg_0, avg_2, avg_4)
    
    print(f"{'Clean (Low Risk)':<15} | 0 mod 6  | {avg_0:.4f}          | {avg_0/base:.4f}x")
    print(f"{'Messy (High Risk)':<15} | 2 mod 6  | {avg_2:.4f}          | {avg_2/base:.4f}x")
    print(f"{'Messy (High Risk)':<15} | 4 mod 6  | {avg_4:.4f}          | {avg_4/base:.4f}x")
    print("-" * 60)
    
    # 4. The "Professor's" Verdict Check
    combined_messy_avg = (avg_2 + avg_4) / 2
    ratio = avg_0 / combined_messy_avg
    
    print(f"\n[ANALYSIS] Ratio of Clean/Messy: {ratio:.4f}x")
    
    if 1.95 < ratio < 2.05:
        print("[VERDICT] SUCCESS. The PLR 'Messiness' perfectly predicts the Goldbach Comet bands (2:1 ratio).")
    else:
        print("[VERDICT] INCONCLUSIVE. The ratio does not align with the 2.0x prediction.")

if __name__ == "__main__":
    run_goldbach_probe()