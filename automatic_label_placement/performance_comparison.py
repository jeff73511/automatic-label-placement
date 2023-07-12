# import subprocess
import timeit
from automatic_label_placement.config_reader import seeds
from automatic_label_placement.local_search_algorithm.local_search_algorithm import (
    local_search_algorithm,
)
from automatic_label_placement.greedy_algorithm.greedy_algorithm import greedy_algorithm


def measure_execution_time(func):
    """Decorator to measure the execution time of a function."""

    def wrapper(*args, **kwargs):
        """Wrapper function that measures the execution time of the decorated function."""

        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time:.2f} seconds")
        return result

    return wrapper


@measure_execution_time
def run_local_search_algorithm(seed_value: int) -> None:
    """Run the local search algorithm to measure the performance.

    Args:
        seed_value: The seed value for random number generation.
    """

    local_search_algorithm(seed_value=seed_value)


@measure_execution_time
def run_greedy_algorithm(seed_value: int) -> None:
    """Run the greedy algorithm to measure the performance.

    Args:
        seed_value: The seed value for random number generation.
    """

    greedy_algorithm(seed_value=seed)


if __name__ == "__main__":
    for seed in seeds:
        print(f"Compare Both Algorithms with Seed {seed}")

        # Run the local search algorithm
        print("Running the Local Search Algorithm...")
        print("Local Search Algorithm Output:")
        run_local_search_algorithm(seed_value=seed)

        print("-" * 48)

        # Run the greedy algorithm
        print("Running the Greedy Algorithm...")
        print("Greedy Algorithm Output:")
        run_greedy_algorithm(seed_value=seed)

        print("=" * 48)
