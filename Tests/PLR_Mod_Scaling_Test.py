import time
import math
import json
import sys
import os

# ==============================================================================
# PLR THEOREM - TEST 10: PRIMORIAL SCALING (Mod 30 & Mod 210)
#
# GOAL:
# Verify if the PLR v23.0 "Internal Flip" Logic maintains 100% accuracy
# when using higher-order Primorial Maps (Mod 30, Mod 210).
#
# HYPOTHESIS:
# The "Clean" scores should drop significantly (Fractal Smoothing),
# maintaining or reinforcing the 100% accuracy of the prediction.
# ==============================================================================

# --- Configuration ---
MOD30_MAP_FILE = "./data/messiness_map_v1_mod30.json"
MOD210_MAP_FILE = "./data/messiness_map_v3_mod210.json"
PRIME_INPUT_FILE = "./prime/primes_100m.txt"  # Path to your pre-generated prime file

TEST_LIMIT = 1000000      # <--- ADJUST THIS: Number of primes to test
MESSY_THRESHOLD = 20.0    # Standard threshold

def load_messiness_map(filename):
    """Robust JSON loader that handles 'Infinity' values."""
    if not os.path.exists(filename):
        print(f"[ERROR] Map file not found: {filename}")
        return None
        
    try:
        with open(filename, 'r') as f:
            content = f.read()
            # Handle non-standard JSON "Infinity"
            content = content.replace("Infinity", "null") 
            data = json.loads(content)
            
        # Convert keys to int and handle nulls
        final_map = {}
        for k, v in data.items():
            val = math.inf if v is None else float(v)
            final_map[int(k)] = val
        return final_map
    except Exception as e:
        print(f"[ERROR] Failed to load {filename}: {e}")
        return None

def load_primes_from_file(filename, limit):
    """Loads the requested number of primes from the text file."""
    if not os.path.exists(filename):
        print(f"[FATAL ERROR] Prime file not found: {filename}")
        return None
        
    print(f"Loading {limit:,} primes from {filename}...")
    start_load = time.time()
    try:
        primes = []
        with open(filename, 'r') as f:
            # We need limit + buffer (for lookahead candidates)
            required = limit + 50 
            for i, line in enumerate(f):
                if i >= required:
                    break
                primes.append(int(line.strip()))
        
        print(f"Loaded {len(primes):,} primes in {time.time() - start_load:.2f}s.")
        if len(primes) < required:
            print(f"[WARNING] File contained fewer primes ({len(primes)}) than requested.")
        return primes
    except Exception as e:
        print(f"[FATAL ERROR] Error reading prime file: {e}")
        return None

# --- The PLR v23.0 Engine (Universal) ---

def get_messiness_score(anchor, messiness_map, modulus):
    """Returns the PAS failure rate from the provided map."""
    residue = anchor % modulus
    return messiness_map.get(residue, 100.0)

def get_v23_prediction(p_n, candidates, messiness_map, modulus):
    """
    The v23.0 Logic Gate (Universal Version).
    Works for any Modulus map provided.
    """
    candidates_data = []
    messy_bin = []
    
    for q in candidates:
        gap = q - p_n
        anchor = p_n + q
        
        # 1. Get Properties
        messiness = get_messiness_score(anchor, messiness_map, modulus)
        
        # 2. Calculate Arithmetic Force
        # Force = (Messiness + 1) * Gap
        score_v11 = (messiness + 1.0) * gap
        
        data = {
            'prime': q,
            'gap': gap,
            'score': score_v11,
            'messiness': messiness
        }
        candidates_data.append(data)
        
        # 3. Filter into Messy Bin
        if messiness > MESSY_THRESHOLD:
            messy_bin.append(data)
            
    if not candidates_data: return None
    
    # 4. Arithmetic Winner
    candidates_data.sort(key=lambda x: x['score'])
    v11_winner = candidates_data[0]
    final_prediction = v11_winner['prime']

    # 5. The Internal Flip
    if messy_bin:
        messy_bin.sort(key=lambda x: x['gap'])
        messy_best = messy_bin[0]
        
        # Logic: If messy candidate is closer but was skipped, check if we should flip.
        if messy_best['gap'] < v11_winner['gap']:
            final_prediction = messy_best['prime']
            
    return final_prediction

# --- Main Test Logic ---
def run_scaling_test():
    print("\n" + "="*60)
    print("      PLR PRIMORIAL SCALING TEST (Mod 30 / Mod 210)")
    print("="*60)
    print(f"Test Limit: {TEST_LIMIT:,} Primes")
    
    # 1. Load Primes
    all_primes = load_primes_from_file(PRIME_INPUT_FILE, TEST_LIMIT)
    if not all_primes:
        return

    # 2. Define Tests
    tests = [
        ("Mod 30", 30, MOD30_MAP_FILE),
        ("Mod 210", 210, MOD210_MAP_FILE)
    ]
    
    for name, modulus, map_file in tests:
        print("\n" + "-"*60)
        print(f"Starting {name} Analysis...")
        
        messiness_map = load_messiness_map(map_file)
        if not messiness_map: continue
        
        # Check the "Super-Clean" Score (Residue 0)
        clean_score = messiness_map.get(0, 999)
        print(f"  > Loaded Map. Clean Anchor (0 mod {modulus}) Score: {clean_score:.6f}%")
        
        failures = 0
        start_time = time.time()
        
        # We iterate up to TEST_LIMIT, ensuring we don't run off the end of the loaded list
        max_index = min(len(all_primes) - 12, TEST_LIMIT)
        
        for i in range(max_index):
            p_n = all_primes[i]
            true_next = all_primes[i+1]
            candidates = all_primes[i+1 : i+11]
            
            pred = get_v23_prediction(p_n, candidates, messiness_map, modulus)
            
            if pred != true_next:
                failures += 1
                print(f"  [FAIL] p={p_n} | Pred={pred} | True={true_next}")
                # Break on first failure to analyze
                break
                
            if (i + 1) % 200000 == 0:
                print(f"  Checked {i + 1:,} primes... (100% OK)", end='\r')
        
        elapsed = time.time() - start_time
        print(f"\n  {name} Result: {failures} Failures in {elapsed:.2f}s")
        
        if failures == 0:
            print(f"  [VERDICT] {name} maintains 100.00% Accuracy.")
            if clean_score < 1.45:
                print(f"  [OBSERVATION] Clean Channel is cleaner than Mod 6 ({clean_score:.4f}% vs 1.45%).")
                if clean_score < 0.1:
                     print("  [MAJOR FINDING] The Clean Channel is effectively frictionless (Near Zero).")
                print("  This confirms the Fractal Smoothing hypothesis.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    run_scaling_test()