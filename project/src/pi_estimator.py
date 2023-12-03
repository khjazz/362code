from random import random
from concurrent.futures import ProcessPoolExecutor


def partition(n, p):
    """Partition 0 to n, both inclusive, to p partitions.
    Return a list of (start, stop) values of the partitions,
    where start is inclusive and stop is exclusive."""
    size = n // p  # partition size, except for last partition
    starts = list(range(0, n + 1, size))[0:p]  # p start values
    stops = list(range(0, n + 1, size))[1:p] + [n]  # p stop values
    return list(zip(starts, stops))


def estimate_pi(n):
    count = 0
    for _ in range(n):
        x = random()
        y = random()
        if x * x + y * y < 1:
            count += 1
    return count / n * 4


def estimate_pi_processes(simulations, concurrency, executor=ProcessPoolExecutor()):
    """
    First partition the requested simulations based on the requested concurrency level.
    Then compute the pi estimate and return the dictionary of:
    simulations,
    concurrency,
    pi and
    simulations_distribution
    """
    partitions = partition(simulations, concurrency)
    simulations_distribution = [stop - start for start, stop in partitions]
    res = executor.map(estimate_pi, simulations_distribution)
    # apply weightings to the estimates before aggregating them
    weighted_estimates_list = [
        estimate * weighting
        for estimate, weighting in zip(res, simulations_distribution)
    ]
    pi = sum(weighted_estimates_list) / sum(simulations_distribution)
    return {
        "simulations": simulations,
        "concurrency": concurrency,
        "pi": pi,
        "simulations_distribution": simulations_distribution,
    }
