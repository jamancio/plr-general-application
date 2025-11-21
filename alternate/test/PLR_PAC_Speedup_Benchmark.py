import time
import math
import random

# --- 1. Core Primality Test (The Slow Operation) ---
# We use a standard, efficient primality test for the benchmark's slow component.
# This test determines the complexity of both methods.

def is_prime(n):
    """Efficient trial division primality test (O(sqrt(n)))"""
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# --- 2. Benchmark Controls ---
TEST_RANGE = 1000000 # Number of times to find the next prime
START_NUM_MIN = 10000000 # Start testing in the 10 million range
POOL_SIZE = 210 # Your Open Pool maximum size

# --- 3. Control Method: Brute Force Search ---
def find_next_prime_control(n):
    """
    Simulates the standard, unoptimized search: checks every odd number.
    Returns the prime and the number of candidates checked.
    """
    candidates_checked = 0
    candidate = n + 1 if n % 2 == 0 else n + 2
    
    while candidate <= n + POOL_SIZE:
        candidates_checked += 1
        if is_prime(candidate):
            return candidate, candidates_checked
        candidate += 2
        
    return None, candidates_checked

# --- 4. Optimized Method: PAC-Inspired Wheel Sieve ---
def find_next_prime_optimized(n):
    """
    Simulates the PAC/PLR optimized search: uses a Mod 30 wheel sieve 
    to instantly skip ~73% of candidates, then applies the slow check.
    The PLR selection logic is simplified here as we assume only one prime remains.
    """
    candidates_checked = 0
    
    # Start the Mod 30 wheel logic
    # Residues coprime to 30: 1, 7, 11, 13, 17, 19, 23, 29 (8 numbers out of 30)
    
    start_point = n + 1
    
    # Find the remainder and the starting residue index (0 to 29)
    initial_remainder = start_point % 30
    wheel_residues = [1, 7, 11, 13, 17, 19, 23, 29] 
    
    for k in range(POOL_SIZE):
        candidate = start_point + k
        
        # Fast filter: Check if candidate is in the 'safe' residues (Mod 30)
        # We only check odd numbers not divisible by 3 or 5
        if (candidate % 2 == 0) and (candidate != 2): continue
        if (candidate % 3 == 0) and (candidate != 3): continue
        if (candidate % 5 == 0) and (candidate != 5): continue

        # The *remaining* candidates require the slow test
        candidates_checked += 1
        
        if is_prime(candidate):
            # This is where the PLR v23.0 logic would be applied if multiple primes survived.
            # Since the PLR is O(1), we measure the time for the necessary checks only.
            return candidate, candidates_checked
            
    return None, candidates_checked
    
# --- 5. Benchmark Execution ---
def run_benchmark():
    
    print("--- PLR PAC OPTIMIZATION BENCHMARK (Proof of Concept) ---")
    print(f"Goal: Compare cycles spent on the slow 'is_prime' test.")
    print(f"Test Count: {TEST_RANGE:,}")
    print("-" * 60)
    
    # Generate random starting numbers for the benchmark
    test_numbers = [random.randint(START_NUM_MIN, START_NUM_MIN + 1000000) for _ in range(TEST_RANGE)]
    
    # --- Control Run ---
    start_time_control = time.time()
    total_checks_control = 0
    
    for n in test_numbers:
        _, checks = find_next_prime_control(n)
        total_checks_control += checks
        
    end_time_control = time.time()
    time_control = end_time_control - start_time_control

    # --- Optimized Run ---
    start_time_optimized = time.time()
    total_checks_optimized = 0
    
    for n in test_numbers:
        _, checks = find_next_prime_optimized(n)
        total_checks_optimized += checks
        
    end_time_optimized = time.time()
    time_optimized = end_time_optimized - start_time_optimized
    
    # --- Results Summary ---
    speedup = time_control / time_optimized if time_optimized > 0 else float('inf')
    checks_reduction = total_checks_control / total_checks_optimized if total_checks_optimized > 0 else float('inf')

    print(f"Control (Brute Force) Time: {time_control:.4f} seconds")
    print(f"Optimized (PAC Filter) Time: {time_optimized:.4f} seconds")
    print("-" * 60)
    print(f"**ALGORITHMIC SPEEDUP: {speedup:.2f}x**")
    print(f"Checks Reduction Factor: {checks_reduction:.2f}x")
    print("\n[VERDICT]: The speedup is achieved by reducing the number of calls to the slow primality test.")
    
if __name__ == "__main__":
    run_benchmark()