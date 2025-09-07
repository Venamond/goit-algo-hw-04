#!/usr/bin/env python3
import argparse, random, timeit, statistics

# ---------------- Algorithms ----------------
def insertion_sort(arr: list) -> list   :
    '''
    Insertion Sort
        Args:
            arr: List of elements to sort.
        Returns:
            A new sorted list.
    '''
    a = arr[:]  # copy
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key
    return a

def merge(left: list, right: list) -> list:
    '''
    Merge two sorted lists.
        Args:
            left: The left sorted list.
            right: The right sorted list.
        Returns:
            A new merged and sorted list.
    '''
    res, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
    res.extend(left[i:]); res.extend(right[j:])
    return res

def merge_sort(arr: list) -> list:
    '''
    Merge Sort
        Args:
            arr: List of elements to sort.
        Returns:
            A new sorted list.
    '''
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr)//2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))

def timsort_sorted(arr: list) -> list:
    '''
    Timsort sorted
        Args:
            arr: List of elements to sort.
        Returns:
            A new sorted list.
    '''
    return sorted(arr)

def timsort_sort(arr: list) -> list:
    '''
    Timsort sort
        Args:
            arr: List of elements to sort.
        Returns:
            A new sorted list.
    '''
    arr.sort()
    return arr


# ---------------- Data Generators ----------------
def gen_random(n: int, seed: int = 42) -> list[int]:
    '''
    Generate a list of random integers.
        Args:
            n: The number of elements to generate.
            seed: The random seed for reproducibility.
        Returns:
            A list of random integers.
    '''
    rnd = random.Random(seed)
    return [rnd.randint(-10**9, 10**9) for _ in range(n)]

def gen_sorted(n: int) -> list[int]:
    '''
    Generate a sorted list of integers.
        Args:
            n: The number of elements to generate.
        Returns:
            A sorted list of integers.
    '''
    return list(range(n))

def gen_reversed(n: int) -> list[int]:
    '''
    Generate a reversed list of integers.
        Args:
            n: The number of elements to generate.
        Returns:
            A reversed list of integers.
    '''
    return list(range(n, 0, -1))


CASES = {
    "random": gen_random,
    "sorted": gen_sorted,
    "reversed": gen_reversed
}

ALGS = {
    "Insertion": insertion_sort,
    "Merge": merge_sort,
    "Timsort sorted": timsort_sorted,
    "Timsort sort": timsort_sort,
}

# ---------------- Benchmarking ----------------
def bench_once(fn: callable, data: list) -> float:
    '''
    Benchmark a single run of a sorting function.
        Args:
            fn: The sorting function to benchmark.
            data: The data to sort.
    '''
    return timeit.Timer(lambda: fn(data)).timeit(number=1)

def bench_median(fn: callable, data: list, repeats: int) -> float:
    '''
    Benchmark the median run time of a sorting function.
        Args:
            fn: The sorting function to benchmark.
            data: The data to sort.
            repeats: The number of times to repeat the benchmark.
    '''
    times = [bench_once(fn, data) for _ in range(repeats)]
    return statistics.median(times)

# Result table
def result_table(rows: list[tuple], headers: tuple[str, ...]) -> str:
    """
    Print a table
        Args:
            rows: The data rows to include in the table.
            headers: The column headers for the table.
        Returns:
            A string representing the table.
    """
    # Formatting function
    def fmt(x):
        return f"{x:.6f}" if isinstance(x, float) else str(x)

    # Prepare columns
    cols = list(zip(*([headers] + [tuple(fmt(c) for c in r) for r in rows])))
    widths = [max(len(str(cell)) for cell in col) for col in cols]

    # Row formatting function
    def format_row(row):
        return "| " + " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row)) + " |"

    lines = []
    lines.append(format_row(headers))
    lines.append("|-" + "-|-".join("-" * w for w in widths) + "-|")
    for r in rows:
        lines.append(format_row([fmt(c) for c in r]))
    return "\n".join(lines)

def parse_args():
    '''Parse command line arguments.'''
    p = argparse.ArgumentParser(
        description="Benchmark Insertion, Merge and Timsort"
    )
    p.add_argument("--sizes", default="1000,5000,10000,20000",
                   help="List of sizes separated by commas (default: 1000,5000,10000,20000)")
    p.add_argument("--repeats", type=int, default=5,
                   help="Number of repeats per point (median), default 5")
    p.add_argument("--max-insertion", type=int, default=10000,
                   help="Max n for Insertion (to avoid long waits). Default 10000")
    return p.parse_args()

def main():
    args = parse_args()
    sizes = [int(s.strip()) for s in args.sizes.split(",") if s.strip()]
    repeats = args.repeats
    max_ins = args.max_insertion

    results = [] 
    
    for case_name, gen in CASES.items():
        for n in sizes:
            data = gen(n)
            for alg_name, fn in ALGS.items():
                if alg_name == "Insertion" and n > max_ins:
                    continue
                t = bench_median(fn, data, repeats)
                results.append((case_name, n, alg_name, t))

    # sort results
    results.sort(key=lambda r: (r[0], r[1], r[2]))

    # print result table
    headers = ("case", "n", "algorithm", "time_s_median")
    print("# Sorting benchmark (Markdown)\n")
    print(result_table(results, headers))

if __name__ == "__main__":
    main()