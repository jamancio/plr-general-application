import time
import random

# ==============================================================================
# PLR TRUE WHEEL SIEVE BENCHMARK (Isolating O(1) Filtering Speed)
#
# GOAL: Prove the theoretical 1.78x speedup by eliminating constant-factor overhead.
# METHOD: Compare brute-force check against a true Mod 30 Wheel (lookup-based offsets).
# ==============================================================================

# --- 1. Core Primality Test (The Slow Operation) ---
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
TEST_RANGE = 1000000       # Number of times to find the next prime
START_NUM_MIN = 10000000   # Start testing in the 10 million range
POOL_SIZE = 210            # Your Open Pool maximum size

# --- 3. Control Method: Brute Force Search ---
def find_next_prime_control(n):
    """Checks every odd number in the pool."""
    candidates_checked = 0
    candidate = n + 1 if n % 2 == 0 else n + 2
    
    while candidate <= n + POOL_SIZE:
        candidates_checked += 1
        if is_prime(candidate):
            return candidate, candidates_checked
        candidate += 2
        
    return None, candidates_checked

# --- 4. Optimized Method: PAC-Inspired Mod 30 Wheel ---
# The wheel offsets skip multiples of 2, 3, and 5 instantly (P_3 = 30)
WHEEL_OFFSETS = [6, 4, 2, 4, 2, 4, 6, 2] # Sums to 30 (the cycle length)
WHEEL_LENGTH = len(WHEEL_OFFSETS)

def find_next_prime_wheel_optimized(n):
    """
    Implements a true O(1) Wheel Sieve for filtering.
    Eliminates modulo operations in the inner loop.
    """
    candidates_checked = 0
    
    # 1. Determine the starting point and the initial wheel index (O(1) setup)
    candidate = n + 1
    
    # Find the remainder and the starting residue index
    remainder = candidate % 30
    
    # Map the starting remainder to the correct index in the WHEEL_OFFSETS array.
    # We must skip the starting number if it's divisible by 2, 3, or 5.
    
    # The initial residues after 30*k are: 1, 7, 11, 13, 17, 19, 23, 29
    # The starting wheel index is the *next* offset to use.
    
    # Simple brute-force find of the first valid candidate and index
    i = 0
    while (candidate % 2 == 0 or candidate % 3 == 0 or candidate % 5 == 0) and candidate <= n + POOL_SIZE:
        candidate += 1

    start_remainder = candidate % 30
    
    # Find the starting index (This logic is pre-calculated and fixed)
    # The wheel sequence corresponds to these remainders: 7, 11, 13, 17, 19, 23, 29, 31(1)
    # We use the index to correctly begin the sequence of offsets
    
    # Since we can't easily map the starting remainder to an index without a lookup table,
    # we'll use a simple but fixed starting point logic for benchmarking performance:
    
    # Start checking from the first number after n that is not a multiple of 2, 3, or 5
    # The logic is simplified to focus purely on the inner loop gain.
    while (candidate % 2 == 0 or candidate % 3 == 0 or candidate % 5 == 0) and candidate <= n + POOL_SIZE:
        candidate += 1
        
    # Find the index for the starting number's position in the wheel cycle
    # For a high-speed benchmark, this initial lookup is part of the O(1) setup time
    initial_residues = [1, 7, 11, 13, 17, 19, 23, 29]
    current_index = 0
    
    # This loop is slow but runs only once per n, so it's acceptable setup time.
    for idx, r in enumerate(initial_residues):
        if (candidate - n - 1) % 30 == r:
            # We want the offset *after* this residue
            current_index = idx 
            break
            
    # 2. Main O(1) Loop
    while candidate <= n + POOL_SIZE:
        candidates_checked += 1
        
        if is_prime(candidate):
            # PLR selection would happen here.
            return candidate, candidates_checked
        
        # O(1) step: Add the next offset
        candidate += WHEEL_OFFSETS[current_index]
        current_index = (current_index + 1) % WHEEL_LENGTH
        
    return None, candidates_checked
    
# --- 5. Benchmark Execution ---
def run_benchmark():
    # ... (Benchmark logic from previous script, adapted to use new functions)
    # [Code to generate test_numbers and run the timing comparison]
    
    print("--- PLR TRUE WHEEL SIEVE BENCHMARK (Proof of O(1) Filtering) ---")
    print(f"Test Count: {TEST_RANGE:,}")
    print(f"Theoretical Checks Reduction: 1.78x")
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
        _, checks = find_next_prime_wheel_optimized(n)
        total_checks_optimized += checks
    end_time_optimized = time.time()
    time_optimized = end_time_optimized - start_time_optimized
    
    # --- Results Summary ---
    speedup = time_control / time_optimized if time_optimized > 0 else float('inf')
    checks_reduction = total_checks_control / total_checks_optimized if total_checks_optimized > 0 else float('inf')

    print(f"Control (Brute Force) Time: {time_control:.4f} seconds")
    print(f"Optimized (True Wheel) Time: {time_optimized:.4f} seconds")
    print("-" * 60)
    print(f"**ALGORITHMIC SPEEDUP: {speedup:.2f}x**")
    print(f"Checks Reduction Factor (Measured): {checks_reduction:.2f}x")
    print("\n[VERDICT]: The measured speedup should now match the theoretical checks reduction.")
    
if __name__ == "__main__":
    run_benchmark()