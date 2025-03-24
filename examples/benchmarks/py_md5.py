import hashlib
from joblib import Parallel, delayed
from examples.benchmarks import file_list_md5, file_md5
import time


def py_md5(file_path, chunk_size=8 * 1024 * 1024):
    md5s = []
    with open(file_path, "rb") as fp:
        data = fp.read(chunk_size)
        md5s.append(hashlib.md5(data))
    return hashlib.md5().hexdigest()


# runing parallel md5 on multiple files (from 10 file to 100k files)
# using joblib for parallelization
# we do a search for the best 'n_jobs' value in [2, 4, 8, -1]
for n in [10, 100, 1000, 10_000, 100_000]:
    print(f"\nn={n}")
    best_t1 = 1e10
    best_n_job = 0
    for n_jobs in [2, 4, 8, -1]:
        # print(f"n_jobs={n_jobs}")
        start = time.time()
        results = Parallel(n_jobs=n_jobs)(delayed(py_md5)("uv.lock") for i in range(n))
        t1 = time.time() - start
        if t1 < best_t1:
            best_t1 = t1
            best_n_job = n_jobs
    print(f"best n_jobs: {best_n_job}")
    print(f"s3_etag (best): {best_t1:.4f}")

    start = time.time()
    results2 = file_list_md5(["uv.lock"] * n)
    t2 = time.time() - start
    print(f"s3Etag: {t2:.4f}")
    print(f"goroutine is {best_t1 / t2:.1f}x faster than joblib")


"""
%timeit file_md5("uv.lock")
%timeit py_md5("uv.lock")
>> 1.4x faster
"""
