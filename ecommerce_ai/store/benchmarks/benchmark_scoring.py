import time
from store.utils.py_scorer import py_score
from store.cython_utils.scorer import fast_score

N = 1_000_000

# Python benchmark
start = time.time()
for _ in range(N):
    py_score(5, 1, 10)
py_time = time.time() - start

# Cython benchmark
start = time.time()
for _ in range(N):
    fast_score(5, 1, 10)
cy_time = time.time() - start

print(f"Python time : {py_time:.4f}s")
print(f"Cython time : {cy_time:.4f}s")
print(f"Speedup     : {py_time / cy_time:.2f}x")
