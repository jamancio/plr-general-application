# ==============================================================================
# PLR THEOREM - TEST 6 (Corrected v4.0): The Final Analytic Test
#
# METHODOLOGY CORRECTION (v4.0):
# - We are now using the correct analytic comparison.
# - Measured Density (per prime) = (Total Twins) / (Total Primes)
# - Theoretical Density (per prime) = (TPC Density per int) / (PNT Density per int)
# - Theoretical Density (per prime) = [2*C_2 / (ln p_N)^2] / [1 / (ln p_N)]
# - Theoretical Density (per prime) = 2*C_2 / (ln p_N)
#
# GOAL:
# To solve for the "Constant of Proportionality" (2*C_2) by calculating:
# Constant (2*C_2) = Measured_Density * ln(p_N)
#
# HYPOTHESIS:
# The calculated constant will now be stable and converge to the
# known Hardy-Littlewood Twin Prime Constant (2*C_2), which is ~1.3203.
# ==============================================================================

import time
import math
import os

# --- Configuration ---
# 1. The 100% accurate measured data (Input)
#    Assumes the script is run from the 'Tests' directory.
DENSITY_INPUT_FILE = "../Result/PLR_TPC-result.txt" 
# 2. The prime values, needed for the correct formula (Input)
PRIME_INPUT_FILE = "prime/primes_100m.txt" 

# --- (NEW) Function to load primes from a file ---
def load_primes_from_file(filename, max_index):
    """Loads primes from the text file up to the max_index needed."""
    print(f"Loading primes from {filename} (up to index {max_index:,})...")
    start_time = time.time()
    prime_list = []
    
    # Check if prime file exists
    if not os.path.exists(filename):
        print(f"FATAL ERROR: The prime file '{filename}' was not found.")
        print(f"Please ensure '{os.path.basename(filename)}' is in the '{os.path.dirname(filename)}' directory.")
        return None

    try:
        with open(filename, 'r') as f:
            # We need a 0-indexed list, so add a dummy 0
            prime_list.append(0) 
            for i, line in enumerate(f):
                if i > max_index: # Stop reading after we have the 50M-th prime
                    break
                prime_list.append(int(line.strip()))
    except Exception as e:
        print(f"FATAL ERROR reading prime file: {e}")
        return None
    
    if len(prime_list) <= max_index:
        print(f"FATAL ERROR: Prime file is too small. Found {len(prime_list)} primes, needed {max_index+1}.")
        return None
        
    end_time = time.time()
    print(f"Loaded {len(prime_list)-1:,} prime values in {end_time - start_time:.2f} seconds.")
    return prime_list

# --- Main Testing Logic ---
def run_analytic_generalization_v4():
    
    print(f"\nStarting PLR Analytic Generalization (Test 6 Corrected v4.0)...")
    
    # 1. Load Measured Densities from PLR_TPC-result.txt
    print(f"  - Loading measured densities from '{DENSITY_INPUT_FILE}'")
    if not os.path.exists(DENSITY_INPUT_FILE):
        print(f"FATAL ERROR: Input file not found: {DENSITY_INPUT_FILE}")
        return

    density_data = []
    max_n_gaps = 0
    
    try:
        with open(DENSITY_INPUT_FILE, 'r') as f:
            all_lines = f.readlines()
        
        # Define the exact header to find from your file
        table_header = "N Gaps          | Twin Density (g_n=2) | Cousin Density (g_n=4)"
        header_found = False
        data_started = False
        
        for line in all_lines:
            line = line.strip()
            
            if not header_found and table_header in line:
                header_found = True
                continue
                
            if header_found and "---" in line:
                data_started = True
                continue
                
            if data_started:
                # Stop if we reach the end of the table
                if not line or line.startswith('(') or line.startswith('='):
                    break
                
                parts = line.split('|')
                if len(parts) >= 2:
                    n_gaps_str = parts[0].strip().replace(',', '')
                    twin_density_str = parts[1].strip()
                    
                    try:
                        n_gaps = int(n_gaps_str)
                        twin_density = float(twin_density_str)
                        density_data.append((n_gaps, twin_density))
                        if n_gaps > max_n_gaps:
                            max_n_gaps = n_gaps
                    except ValueError:
                        continue # Skip any non-data lines
        
        if not density_data:
            print("FATAL ERROR: No data was successfully parsed from the table.")
            return
            
        print(f"  - Successfully loaded {len(density_data)} density checkpoints.")

    except Exception as e:
        print(f"FATAL ERROR: Could not parse {DENSITY_INPUT_FILE}: {e}")
        return

    # 2. Load Prime Values (up to the max N we found)
    prime_list = load_primes_from_file(PRIME_INPUT_FILE, max_n_gaps) 
    if prime_list is None:
        return

    # 3. Run Corrected Analysis (v4)
    print("\n" + "="*80)
    print(" 'Constant of Proportionality' (2*C_2) Analysis (Corrected v4.0)")
    print("="*80)
    print("  Constant (2*C_2) = (Measured Density / 1000) * ln(p_N)")
    print("-" * 80)
    print(f"{'N Gaps (N)':<12} | {'Prime Value (p_N)':<16} | {'Measured Density':<18} | {'ln(p_N)':<18} | {'Calculated Constant':<20}")
    print("-" * 80)

    constants = []
    for n_gaps, twin_density_per_1000 in density_data:
        if n_gaps >= len(prime_list):
             print(f"Skipping N={n_gaps}: Not enough primes loaded from file.")
             continue
        
        # Use N as the index into the prime list
        p_n = prime_list[n_gaps] 
        
        # Convert density from "per 1000" to "per 1"
        measured_density = twin_density_per_1000 / 1000.0
        
        if p_n <= 1:
            continue
            
        log_p_n = math.log(p_n) # ln(p_N)
        
        # Calculate the constant using the *correct* v4 formula
        calc_constant = measured_density * log_p_n
        constants.append(calc_constant)
        
        print(f"{n_gaps:<12,} | {p_n:<16,} | {measured_density:<18.8f} | {log_p_n:<18.4f} | {calc_constant:<20.4f}")

    # --- 4. Final Verdict ---
    if not constants:
        print("No constants were calculated. Exiting.")
        return
        
    avg_constant = sum(constants) / len(constants)
    max_dev = max(constants) - min(constants)
    
    print("-" * 80)
    print(f"\n  Average Calculated Constant: {avg_constant:.4f}")
    print(f"  Max Deviation (Stability):   {max_dev:.4f}")
    print(f"  Known TPC Constant (2*C_2):  ~1.3203")

    # Check if the constant is both STABLE (low deviation) and ACCURATE (near 1.32)
    # We expect some deviation as this is an asymptotic approximation.
    if max_dev < 0.1 and (1.25 < avg_constant < 1.4):
        print(f"\n  [VERDICT: HYPOTHESIS CONFIRMED. CONSTANT IS STABLE AND ACCURATE.]")
        print(f"  The 'Constant of Proportionality' is stable at approx {avg_constant:.4f}.")
        print(f"  This provides the final analytic link between the 100% PLR")
        print(f"  Theorem and the Hardy-Littlewood TPC.")
    else:
        print(f"\n  [VERDICT: HYPOTHESIS FALSIFIED. CONSTANT IS UNSTABLE OR INACCURATE.]")
        print(f"  The measured constant ({avg_constant:.4f}) is not converging to 1.3203.")
        print(f"  (Deviation: {max_dev:.4f})")
        
    print("="*80)

if __name__ == "__main__":
    run_analytic_generalization_v4()