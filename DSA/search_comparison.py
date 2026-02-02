"""
DSA Performance Comparison - Darlene Ayinkamiye

Comparing how fast different search methods are:
1. Linear search (loop through everything)
2. Dictionary lookup (direct access)

Spoiler: dictionary is WAY faster!
"""

import time
import sys
import os
from statistics import mean, median

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa.parser import parse_xml_to_json, create_transaction_dictionary


def linear_search(transactions_list, target_id):
    """
    Search by looping through the list one by one.
    This is slow for big datasets - O(n) time complexity
    """
    for transaction in transactions_list:
        if transaction['id'] == target_id:
            return transaction
    return None


def dictionary_lookup(transactions_dict, target_id):
    """
    Direct lookup using dictionary key.
    Super fast - O(1) constant time!
    """
    return transactions_dict.get(target_id)


def benchmark_search(transactions_list, transactions_dict, target_ids, iterations=1000):
    """
    Benchmark both search methods with multiple iterations.
    
    Args:
        transactions_list (list): List of transactions
        transactions_dict (dict): Dictionary of transactions
        target_ids (list): List of IDs to search for
        iterations (int): Number of times to repeat the search
        
    Returns:
        dict: Benchmark results
    """
    linear_times = []
    dict_times = []
    
    print(f"Running {iterations} iterations for each search method...")
    
    # Benchmark Linear Search
    for target_id in target_ids:
        start_time = time.perf_counter()
        for _ in range(iterations):
            linear_search(transactions_list, target_id)
        end_time = time.perf_counter()
        linear_times.append(end_time - start_time)
    
    # Benchmark Dictionary Lookup
    for target_id in target_ids:
        start_time = time.perf_counter()
        for _ in range(iterations):
            dictionary_lookup(transactions_dict, target_id)
        end_time = time.perf_counter()
        dict_times.append(end_time - start_time)
    
    return {
        'linear_search': {
            'total_time': sum(linear_times),
            'average_time': mean(linear_times),
            'median_time': median(linear_times),
            'times': linear_times
        },
        'dictionary_lookup': {
            'total_time': sum(dict_times),
            'average_time': mean(dict_times),
            'median_time': median(dict_times),
            'times': dict_times
        }
    }


def display_results(results, num_records, iterations):
    """Display benchmark results in a formatted way."""
    
    print("\n" + "=" * 80)
    print("SEARCH ALGORITHM PERFORMANCE COMPARISON")
    print("=" * 80)
    
    print(f"\nDataset Size: {num_records} transactions")
    print(f"Iterations per search: {iterations}")
    
    linear = results['linear_search']
    dictionary = results['dictionary_lookup']
    
    print("\n" + "-" * 80)
    print("LINEAR SEARCH RESULTS")
    print("-" * 80)
    print(f"Total Time:    {linear['total_time']:.6f} seconds")
    print(f"Average Time:  {linear['average_time']:.6f} seconds")
    print(f"Median Time:   {linear['median_time']:.6f} seconds")
    
    print("\n" + "-" * 80)
    print("DICTIONARY LOOKUP RESULTS")
    print("-" * 80)
    print(f"Total Time:    {dictionary['total_time']:.6f} seconds")
    print(f"Average Time:  {dictionary['average_time']:.6f} seconds")
    print(f"Median Time:   {dictionary['median_time']:.6f} seconds")
    
    # Calculate speedup
    speedup = linear['average_time'] / dictionary['average_time']
    percentage_faster = ((linear['average_time'] - dictionary['average_time']) / linear['average_time']) * 100
    
    print("\n" + "=" * 80)
    print("PERFORMANCE COMPARISON")
    print("=" * 80)
    print(f"Dictionary lookup is {speedup:.2f}x faster than linear search")
    print(f"Dictionary lookup is {percentage_faster:.2f}% faster")
    
    print("\n" + "=" * 80)
    print("ANALYSIS & EXPLANATION")
    print("=" * 80)
    
    analysis = """
WHY IS DICTIONARY LOOKUP FASTER?

1. **Time Complexity Difference**
   - Linear Search: O(n) - Must check each element sequentially until found
   - Dictionary Lookup: O(1) - Direct access using hash function
   
2. **Hash Table Implementation**
   - Python dictionaries use hash tables internally
   - Hash function converts key to array index instantly
   - No need to iterate through elements
   
3. **Best, Average, and Worst Cases**
   
   Linear Search:
   - Best case: O(1) - target is first element
   - Average case: O(n/2) - target is in middle
   - Worst case: O(n) - target is last or not present
   
   Dictionary Lookup:
   - Best case: O(1) - direct hash calculation
   - Average case: O(1) - minimal hash collisions
   - Worst case: O(n) - many hash collisions (rare with good hash function)

4. **Practical Implications**
   - For 22 records: Difference seems small (milliseconds)
   - For 1,000,000 records: Dictionary is dramatically faster
   - Linear search time grows linearly with data size
   - Dictionary lookup time stays constant (approximately)

5. **Memory Trade-off**
   - Dictionary uses more memory (stores keys + values in hash table)
   - Linear search only needs the list
   - For frequently accessed data, memory trade-off is worth it

OTHER DATA STRUCTURES & ALGORITHMS TO IMPROVE SEARCH EFFICIENCY:

1. **Binary Search Tree (BST)**
   - Time Complexity: O(log n)
   - Requires sorted data
   - Better than linear, worse than hash table
   - Useful when you need ordered traversal

2. **Binary Search on Sorted List**
   - Time Complexity: O(log n)
   - Requires pre-sorted list
   - Much faster than linear for large datasets
   - Good when data is static or infrequently updated

3. **Balanced Trees (AVL, Red-Black)**
   - Time Complexity: O(log n) guaranteed
   - Auto-balancing prevents worst-case scenarios
   - Good for dynamic datasets with frequent insertions/deletions

4. **Trie (Prefix Tree)**
   - Time Complexity: O(k) where k is key length
   - Excellent for string searches
   - Useful for autocomplete, spell-check features

5. **B-Trees**
   - Time Complexity: O(log n)
   - Optimized for disk-based storage
   - Used in databases and file systems

6. **Bloom Filters**
   - Time Complexity: O(1)
   - Space-efficient probabilistic data structure
   - Quick "definitely not present" or "possibly present" checks
   - Useful for large-scale systems

RECOMMENDATION FOR MOMO TRANSACTION SYSTEM:

Primary: Dictionary (Hash Table)
- Best for frequent lookups by transaction ID
- Constant time performance
- Simple implementation in Python

Secondary: B-Tree Index (for database)
- When scaling to millions of records
- Efficient range queries (find transactions between dates)
- Good for disk-based storage

Composite: Dictionary + Sorted List
- Dictionary for ID lookups
- Sorted list by timestamp for range queries
- Both provide O(1) and O(log n) operations respectively
    """
    
    print(analysis)
    print("=" * 80)


def run_comparison():
    """Main function to run the DSA comparison."""
    
    # Load data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    xml_path = os.path.join(os.path.dirname(current_dir), 'data', 'modified_sms_v2.xml')
    
    print("Loading transaction data...")
    transactions_list = parse_xml_to_json(xml_path)
    transactions_dict = create_transaction_dictionary(transactions_list)
    
    if not transactions_list:
        print("Error: No data loaded!")
        return
    
    print(f"Loaded {len(transactions_list)} transactions")
    
    # Select test IDs (beginning, middle, end)
    test_ids = []
    if len(transactions_list) >= 3:
        test_ids = [
            transactions_list[0]['id'],           # First
            transactions_list[len(transactions_list)//2]['id'],  # Middle
            transactions_list[-1]['id']            # Last
        ]
    
    # Run benchmark
    iterations = 10000  # Increased for more accurate timing
    results = benchmark_search(transactions_list, transactions_dict, test_ids, iterations)
    
    # Display results
    display_results(results, len(transactions_list), iterations)


if __name__ == "__main__":
    run_comparison()
