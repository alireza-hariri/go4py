# Benchmarks

This document presents benchmark results comparing the performance of Go4Py against standard Python implementations for some tasks. you can find the codes in the [examples](/examples/benchmarks/) dirctory. The "speedup" indicates how much faster Go4Py is compared to the corresponding Python implementation. A value greater than 1x means Go4Py is faster, while a value less than 1x means Go4Py is slower.

*   These benchmarks are specific to the environment and versions used during testing. Results may vary depending on hardware and software configuration.
*   `n` represents an input parameter to the Python function.

## benchmarks

### Single random number

| Benchmark          |    Speedup | Description                                                                                                |
|--------------------|----------------|-----------------------------------------------------------------------------------------------------------|
| `rand`             | 0.9x           | Generate a random number (using Python's `random.random()`)         |
| `randn`            | 3.8x           | Generate a normal distributed random number (using Python's `random.normalvariate()`)  |

### Add

| Benchmark          |  Speedup | Description                                                                                                |
|---------------------|----------------|-----------------------------------------|
| `add`           | 0.4x           | Adding a constant to an integer.                                 |

### RandArray

| Benchmark          | Input (n=) |  Speedup | Description                                                                                                |
|--------------------|------------|----------------|------------------------------------------------------------------------------------------------------------|
| `RandArray`     | 10         | 1.8x           | Generating a random list (using `random.random()`).                                                  |
| `RandArray`     | 20         | 1.8x           | Generating a random list (using `random.random()`).                                                  |
| `RandArray`     | 40         | 1.9x           | Generating a random list (using `random.random()`).                                                  |
| `RandArray`     | 80         | 1.8x           | Generating a random list (using `random.random()`).                                                  |

### RandArray (VS numpy)

| Benchmark          | Input (n=) |  Speedup | Description                                                                                                |
|--------------------|------------|----------------|------------------------------------------------------------------------------------------------------------|
| `RandArray`  | 10         | 2.3x           | Generating a random array using NumPy.                                                                     |
| `RandArray`  | 20         | 2.1x           | Generating a random array using NumPy.                                                                     |
| `RandArray`  | 40         | 1.5x           | Generating a random array using NumPy.                                                                     |
| `RandArray`  | 80         | 1.2x           | Generating a random array using NumPy.                                                                     |

### Fibonacci

| Benchmark          | Input (n=) |  Speedup | Description                                                                                                |
|--------------------|------------|----------------|------------------------------------------------------------------------------------------------------------|
| `Fibo`          | 10         | 2.3x           | Calculating Fibonacci number (non-recursive).             |
| `Fibo`          | 20         | 3.3x           | Calculating Fibonacci number (non-recursive).             |
| `Fibo`          | 40         | 6.1x           | Calculating Fibonacci number (non-recursive).             |
| `Fibo`          | 80         | 10.5x          | Calculating Fibonacci number (non-recursive).             |

### FindPrimes

| Benchmark          | Input (n=) |  Speedup | Description                                                                                                |
|--------------------|------------|----------------|------------------------------------------------------------------------------------------------------------|
| `FindPrimes`    | 10         | 2.8x           | Finding primes up to n.                                 |
| `FindPrimes`    | 20         | 6.4x           | Finding primes up tp n.                                 |
| `FindPrimes`    | 40         | 8.4x           | Finding primes up tp n.                                 |
| `FindPrimes`    | 80         | 11.4x          | Finding primes up tp n.                                 |

### getRequest

| Benchmark          | Speedup | Description                                                                                                |
|--------------------|----------------|------------------------------------------------------------------------------------------------------------|
| `getRequest`       | 11.4x          | Making a HTTP request using the `requests` library in Python (to localhost).     |

### Sudoku

| Benchmark          | Speedup | Description                                                                                                |
|--------------------|----------------|------------------------------------------------------------------------------------------------------------|
| `SolveSudoku`       | 41x          | solving a 9x9 sudoku puzzle.

### MD5 hash

| Benchmark          | Input (n=) | Best n_jobs (for python) | Speedup (at least) | Description                          | 
|--------------------|------------|-------------|------------|------------------------|
| `MD5`                    | -       | -     | 1.4x    | the MD5 hash of single file  |
| `MD5 (parallel)`         | 10      | 2     | 26.0x   | the MD5 hash of 10 file      |
| `MD5 (parallel)`         | 100     | 8     | 30.8x   | the MD5 hash of 100 file     |
| `MD5 (parallel)`         | 1000    | 4     | 14.7x   | the MD5 hash of 1000 file    |
| `MD5 (parallel)`         | 10000   | -1    | 3.3x    | the MD5 hash of 10000 file   |
| `MD5 (parallel)`         | 100000  | -1    | 1.7x    | the MD5 hash of 100000 file  |
 * we use joblib to parallelize the MD5 hash calculation on python side and native go-routine on go side.
 * we do a search in the python side to find the best n_jobs for each input size.
 * when there is enough inputs the overhead of python parallelization become less significant and the speedup will be closer to the speedup of single file.

## Conclusions

* Go4Py demonstrates significant speedups in non-trival tasks like `Fibonacci` and `FindPrimes`. The speedup tends to increase with the input size `n`.

* Trival tasks like `Add` shows a slowdown. This is likely due to the overhead in the function boundry. But this can be acceptable for many use cases. because this overhead is as low as 50ns.

* The `getRequest` benchmark shows a significant speedup, indicating that Go4Py can efficiently handle network requests, even without any concurrency.

