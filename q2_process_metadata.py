#!/usr/bin/env python3

# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.


def parse_config(filepath: str) -> dict:
    """
    Parse config file (key=value format) into dictionary.

    Args:
        filepath: Path to q2_config.txt

    Returns:
        dict: Configuration as key-value pairs

    Example:
        >>> config = parse_config('q2_config.txt')
        >>> config['sample_data_rows']
        '100'
    """
    # TODO: Read file, split on '=', create dict
    cfg = {}
    with open("q2_config.txt", "r") as file:
        for line in file:
            key, value = line.strip().split('=')
            cfg[key] = value
    return cfg


def validate_config(config: dict) -> dict:
    """
    Validate configuration values using if/elif/else logic.

    Rules:
    - sample_data_rows must be an int and > 0
    - sample_data_min must be an int and >= 1
    - sample_data_max must be an int and > sample_data_min

    Args:
        config: Configuration dictionary

    Returns:
        dict: Validation results {key: True/False}

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> results = validate_config(config)
        >>> results['sample_data_rows']
        True
    """
    # TODO: Implement with if/elif/else
    results = {}
    try:
        rows = int(config['sample_data_rows'])
        min_val = int(config['sample_data_min'])
        max_val = int(config['sample_data_max'])
        results['sample_data_rows'] = rows > 0
        results['sample_data_min'] = min_val >= 1
        results['sample_data_max'] = max_val > min_val
    except (KeyError, ValueError):
        results['sample_data_rows'] = False
        results['sample_data_min'] = False
        results['sample_data_max'] = False
    return results


def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random numbers for testing, one number per row with no header.
    Uses config parameters for number of rows and range.

    Args:
        filename: Output filename (e.g., 'sample_data.csv')
        config: Configuration dictionary with sample_data_rows, sample_data_min, sample_data_max

    Returns:
        None: Creates file on disk

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> generate_sample_data('sample_data.csv', config)
        # Creates file with 100 random numbers between 18-75, one per row
        >>> import random
        >>> random.randint(18, 75)  # Returns random integer between 18-75
    """
    # TODO: Parse config values (convert strings to int)
    import random
    rows = int(config['sample_data_rows'])
    min_val = int(config['sample_data_min'])
    max_val = int(config['sample_data_max'])
    # Generate random numbers and save to file
    with open(filename, 'w') as file:
        for i in range(rows):
            file.write(f'{random.randint(min_val, max_val)}\n')
    # TODO: Use random module with config-specified range
    pass

def calculate_statistics(data: list) -> dict:
    """
    Calculate basic statistics.

    Args:
        data: List of numbers

    Returns:
        dict: {mean, median, sum, count}

stats = {}
sum = 0
stats['sum'] = sum 
    Example:
        >>> stats = calculate_statistics([10, 20, 30, 40, 50])
        >>> stats['mean']
        30.0
    """
    # TODO: Calculate stats
    stats = {}
    n = len(data)
    if n == 0:
        return {'mean': None, 'median': None, 'sum': 0, 'count': 0}
    total = sum(data)
    stats['sum'] = total
    stats['count'] = n
    stats['mean'] = total / n
    sorted_data = sorted(data)
    mid = n // 2
    if n % 2 != 0:
        stats['median'] = sorted_data[mid]
    else:
        stats['median'] = (sorted_data[mid] + sorted_data[mid-1]) / 2
    return stats
    pass


if __name__ == '__main__':
    # TODO: Test your functions with sample data
    # Example:
    # config = parse_config('q2_config.txt')
    # validation = validate_config(config)
    # generate_sample_data('data/sample_data.csv', config)
    # 
    # TODO: Read the generated file and calculate statistics
    config = parse_config('q2_config.txt')
    validation = validate_config(config)
    if all(validation.values()):
        generate_sample_data('sample_data.csv', config)
        filename = 'sample_data.csv'  # Update path if needed
        try:
            with open(filename) as f:
                numbers = [int(line.strip()) for line in f if line.strip()]
            stats = calculate_statistics(numbers)
            print(stats)
     # TODO: Save statistics to output/statistics.txt
            with open('output/statistics.txt', 'w') as out:
                for k, v in stats.items():
                    out.write(f'{k}: {v}\n')
        except FileNotFoundError:
            print(f"File {filename} not found.")
    else:
        print("Invalid configuration:", validation) 
        pass


