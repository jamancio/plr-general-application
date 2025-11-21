import time
import math

# ==============================================================================
# PLR v25.0 ADAPTIVE RSA BREAKER vs. STANDARD TRIAL DIVISION
#
# GOAL: 1. Implement an "Adaptive Window" that expands automatically when
#          encountering large prime gaps (removing manual tuning).
#       2. Benchmark this "Smart Generator" against a standard "Brute Force"
#          Trial Division loop to measure true wall-clock speedup.
# ==============================================================================

# --- 1. The Core PLR Logic (Hardcoded Constants) ---
MESSINESS_SCORES = {0: 2.7126, 2: 26.2627, 4: 26.2859}

def get_messiness_score(anchor):
    return MESSINESS_SCORES.get(anchor % 6, 100.0)

def get_plr_prediction(p_n, candidate_pool):
    """v23.0 'Internal Flip' Logic."""
    best_v11_score = float('inf')
    v11_winner = None
    v11_gap = float('inf')
    messy_lowest_gap = float('inf')
    messy_lowest_prime = None
    
    for q in candidate_pool:
        gap = q - p_n
        anchor = p_n + q
        messiness = get_messiness_score(anchor)
        score = (messiness + 1.0) * gap
        
        if score < best_v11_score:
            best_v11_score = score
            v11_winner = q
            v11_gap = gap
            
        if messiness > 20.0:
            if gap < messy_lowest_gap:
                messy_lowest_gap = gap
                messy_lowest_prime = q
    
    # The Logic Gate (Flip)
    if messy_lowest_prime is not None and messy_lowest_gap < v11_gap:
        return messy_lowest_prime
            
    return v11_winner

# --- 2. The ADAPTIVE PLR Generator ---

def generate_primes_adaptive_plr(limit_n):
    """
    Generates primes using PLR with an ADAPTIVE SEARCH WINDOW.
    If a gap is too large for the current window, it expands and retries.
    """
    primes = [2, 3]
    p_n = 3
    
    # Adaptive Parameters
    BASE_WINDOW = 30      # Start fast and local
    MAX_WINDOW = 10000    # Safety cap
    
    current_window = BASE_WINDOW
    
    while p_n * p_n <= limit_n:
        
        candidates = []
        search_limit = p_n + current_window
        
        # --- 1. Sieve / Pool Generation ---
        # (Simulating a Wheel Sieve by checking small primes)
        for k in range(p_n + 2, search_limit, 2):
            is_prime_cand = True
            sqrt_k = int(math.sqrt(k))
            for p in primes:
                if p > sqrt_k: break
                if k % p == 0:
                    is_prime_cand = False
                    break
            if is_prime_cand:
                candidates.append(k)
        
        # --- 2. Adaptive Logic ---
        if not candidates:
            # FAILURE: The gap was larger than the window.
            # ADAPT: Double the window and try again from the SAME p_n.
            current_window *= 2
            if current_window > MAX_WINDOW: 
                break # Should not happen for reasonable keys
            continue 
            
        # SUCCESS: We found candidates. Use PLR to pick the winner.
        p_next = get_plr_prediction(p_n, candidates)
        
        if p_next:
            primes.append(p_next)
            p_n = p_next
            
            # Reset window to keep it fast (Local Optimization)
            # We only need large windows for large gaps.
            current_window = BASE_WINDOW 
            
            yield p_n
        else:
            break

def break_rsa_adaptive(target_N):
    """Attacks N using the Adaptive PLR Engine."""
    start_time = time.time()
    
    # Check trivial small factors first
    if target_N % 2 == 0: return 2, time.time() - start_time
    if target_N % 3 == 0: return 3, time.time() - start_time
    
    generator = generate_primes_adaptive_plr(target_N)
    
    checks = 0
    for prime_factor in generator:
        checks += 1
        if target_N % prime_factor == 0:
            return prime_factor, time.time() - start_time
            
    return None, time.time() - start_time

# --- 3. The STANDARD Method (Control Group) ---

def break_rsa_standard(target_N):
    """
    Attacks N using standard Brute Force Trial Division.
    Checks every odd number (3, 5, 7, 9, 11...).
    Does NOT generate primes; just divides.
    """
    start_time = time.time()
    
    if target_N % 2 == 0: return 2, time.time() - start_time
    
    limit = int(math.sqrt(target_N))
    
    # Standard naive loop: check every odd number
    for d in range(3, limit + 1, 2):
        if target_N % d == 0:
            return d, time.time() - start_time
            
    return None, time.time() - start_time

# --- 4. Benchmark Suite ---

def run_benchmark():
    print("============================================================")
    print("   PLR v25.0 ADAPTIVE vs. STANDARD DIVISION BENCHMARK")
    print("============================================================")
    
    # Test Keys (Product of two primes)
    test_keys = [
        ("Small", 7919 * 7907),                # 62,615,533
        ("Medium", 104729 * 104723),            # 10,967,535,067
        ("Large", 982451653 * 104729),          # 102,891,238,146,737 (~47-bit)
                                                # Note: 'Large' might take a moment!
    ]
    
    for label, key in test_keys:
        print(f"\n[TARGET: {label}] Key N = {key}")
        print("-" * 50)
        
        # --- Run Standard ---
        print("  > Running Standard Division...", end="", flush=True)
        std_factor, std_time = break_rsa_standard(key)
        print(f" Done. ({std_time:.4f}s)")
        
        # --- Run Adaptive PLR ---
        print("  > Running Adaptive PLR.......", end="", flush=True)
        plr_factor, plr_time = break_rsa_adaptive(key)
        print(f" Done. ({plr_time:.4f}s)")
        
        # --- Comparison ---
        if std_factor == plr_factor and std_factor is not None:
            speedup = std_time / plr_time if plr_time > 0 else 0
            print(f"  [VERIFIED] Both found factor: {std_factor}")
            print(f"  [RESULT]   PLR Speedup: {speedup:.2f}x")
            
            if speedup > 1.0:
                print("  [WINNER]   PLR Engine")
            else:
                print("  [WINNER]   Standard (Overhead likely too high for small N)")
        else:
            print(f"  [ERROR] Mismatch! Std: {std_factor}, PLR: {plr_factor}")
            
    print("\n============================================================")

if __name__ == "__main__":
    run_benchmark()