import random

# The seed makes the "random" sequence 100% repeatable.
# This is the "flaw" we are testing.
RANDOM_SEED = 42
NUMBERS_TO_GENERATE = 1100000 # 1M for the test + buffer
OUTPUT_FILE = "rng_output.txt"

# Set the seed
random.seed(RANDOM_SEED)

print(f"Generating {NUMBERS_TO_GENERATE:,} pseudo-random numbers with seed={RANDOM_SEED}...")

with open(OUTPUT_FILE, 'w') as f:
    for i in range(NUMBERS_TO_GENERATE):
        # We need numbers in a similar *range* to our primes
        # to ensure the v_mod6 math is comparable.
        # We'll use a range from 1 to 100,000,000.
        r_num = random.randint(1, 100000000)
        f.write(f"{r_num}\n")

print(f"File '{OUTPUT_FILE}' created successfully.")