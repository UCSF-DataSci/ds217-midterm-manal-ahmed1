# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.
#
# These utilities will be imported and used in Q4-Q7 notebooks.

import pandas as pd
import numpy as np


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV file into DataFrame.

    Args:
        filepath: Path to CSV file

    Returns:
        pd.DataFrame: Loaded data

    Example:
        >>> df = load_data('data/clinical_trial_raw.csv')
        >>> df.shape
        (10000, 18)
    """
    df = pd.read_csv(filepath)
    return df
    


def clean_data(df: pd.DataFrame, remove_duplicates: bool = True,
               sentinel_value: float = -999) -> pd.DataFrame:
    """
    Basic data cleaning: remove duplicates and replace sentinel values with NaN.

    Args:
        df: Input DataFrame
        remove_duplicates: Whether to drop duplicate rows
        sentinel_value: Value to replace with NaN (e.g., -999, -1)

    Returns:
        pd.DataFrame: Cleaned data

    Example:
        >>> df_clean = clean_data(df, sentinel_value=-999)
    """
    df.drop_duplicates(inplace=True)
    df.replace(sentinel_value, np.nan,inplace=True)
    return df
    

def detect_missing(df: pd.DataFrame) -> pd.Series:
    """
    Return count of missing values per column.

    Args:
        df: Input DataFrame

    Returns:
        pd.Series: Count of missing values for each column

    Example:
        >>> missing = detect_missing(df)
        >>> missing['age']
        15
    """
    count = df.isnull().sum()
    return count
    

def fill_missing(df: pd.DataFrame, column: str, strategy: str = 'mean') -> pd.DataFrame:
    """
    Fill missing values in a column using specified strategy.

    Args:
        df: Input DataFrame
        column: Column name to fill
        strategy: Fill strategy - 'mean', 'median', or 'ffill'

    Returns:
        pd.DataFrame: DataFrame with filled values

    Example:
        >>> df_filled = fill_missing(df, 'age', strategy='median')
    """
    df_filled = df.copy()
    if strategy == "median":
        df_filled[column] = df[column].fillna(df[column].median())
    elif strategy == "mean":
        df_filled[column] = df[column].fillna(df[column].mean())
    elif strategy == "ffill":
        df_filled[column] = df[column].fillna(method='ffill')
    else:
        df_filled[column] = df[column]
    return df_filled
    


def filter_data(df: pd.DataFrame, filters: list) -> pd.DataFrame:
    """
    Apply a list of filters to DataFrame in sequence.

    Args:
        df: Input DataFrame
        filters: List of filter dictionaries, each with keys:
                'column', 'condition', 'value'
                Conditions: 'equals', 'greater_than', 'less_than', 'in_range', 'in_list'

    Returns:
        pd.DataFrame: Filtered data

    Examples:
        >>> # Single filter
        >>> filters = [{'column': 'site', 'condition': 'equals', 'value': 'Site A'}]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Multiple filters applied in order
        >>> filters = [
        ...     {'column': 'age', 'condition': 'greater_than', 'value': 18},
        ...     {'column': 'age', 'condition': 'less_than', 'value': 65},
        ...     {'column': 'site', 'condition': 'in_list', 'value': ['Site A', 'Site B']}
        ... ]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Range filter example
        >>> filters = [{'column': 'age', 'condition': 'in_range', 'value': [18, 65]}]
        >>> df_filtered = filter_data(df, filters)
        """
        
    df_filtered = df.copy()
    for f in filters:
        col = f["column"]
        cond = f["condition"]
        val = f["value"]

        if cond == "equals":
            df_filtered = df_filtered[df_filtered[col] == val]

        elif cond == "greater_than":
            df_filtered = df_filtered[df_filtered[col] > val]

        elif cond == "less_than":
            df_filtered = df_filtered[df_filtered[col] < val]

        elif cond == "in_range":
            low, high = val
            df_filtered = df_filtered[
                (df_filtered[col] >= low) & (df_filtered[col] <= high)
            ]

        elif cond == "in_list":
            df_filtered = df_filtered[df_filtered[col].isin(val)]

    return df_filtered
 


def transform_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:
    """
    Convert column data types based on mapping.

    Args:
        df: Input DataFrame
        type_map: Dict mapping column names to target types
            Supported types: 'datetime', 'numeric', 'category', 'string'

    Returns:
        pd.DataFrame: DataFrame with converted types

    Example:
        >>> type_map = {
        ...     'enrollment_date': 'datetime',
        ...     'age': 'numeric',
        ...     'site': 'category'
        ... }
        >>> df_typed = transform_types(df, type_map)
    """
    df_transform = df.copy()
    for col, typ in type_map.items():
        if typ == "datetime":
            df_transform[col] = pd.to_datetime(df_transform[col])
        elif typ == "numeric":
            df_transform[col] = pd.to_numeric(df_transform[col])
        elif typ == "category":
            df_transform[col] = df_transform[col].astype("category")
        elif typ == "string":
            df_transform[col] = df_transform[col].astype("string")
        else:
            raise ValueError(f"Unsupported type: {typ}")
    return df_transform

def create_bins(df: pd.DataFrame, column: str, bins: list,
                labels: list, new_column: str = None) -> pd.DataFrame:
    """
    Create categorical bins from continuous data using pd.cut().

    Args:
        df: Input DataFrame
        column: Column to bin
        bins: List of bin edges
        labels: List of bin labels
        new_column: Name for new binned column (default: '{column}_binned')

    Returns:
        pd.DataFrame: DataFrame with new binned column

    Example:
        >>> df_binned = create_bins(
        ...     df,
        ...     column='age',
        ...     bins=[0, 18, 35, 50, 65, 100],
        ...     labels=['<18', '18-34', '35-49', '50-64', '65+']
        ... )
    """
    df_bins = df.copy()
    df_bins[new_column] = pd.cut(df_bins[column], labels=labels, bins=bins)
    return df_bins
    


def summarize_by_group(df: pd.DataFrame, group_col: str,
                       agg_dict: dict = None) -> pd.DataFrame:
    """
    Group data and apply aggregations.

    Args:
        df: Input DataFrame
        group_col: Column to group by
        agg_dict: Dict of {column: aggregation_function(s)}
                  If None, uses .describe() on numeric columns

    Returns:
        pd.DataFrame: Grouped and aggregated data

    Examples:
        >>> # Simple summary
        >>> summary = summarize_by_group(df, 'site')
        >>>
        >>> # Custom aggregations
        >>> summary = summarize_by_group(
        ...     df,
        ...     'site',
        ...     {'age': ['mean', 'std'], 'bmi': 'mean'}
        ... )
    """

    if agg_dict == None:
        group_data = df.groupby(group_col).describe()
    else:
        group_data = df.groupby(group_col).agg(agg_dict)
    return group_data 
    




if __name__ == '__main__':
    df=load_data('data/clinical_trial_raw.csv')
    # Optional: Test your utilities here
    print("Data utilities loaded successfully!")
    print("Available functions:")
    print("  - load_data()")
    print("  - clean_data()")
    print("  - detect_missing()")
    print("  - fill_missing()")
    print("  - filter_data()")
    print("  - transform_types()")
    print("  - create_bins()")
    print("  - summarize_by_group()")
    
    # TODO: Add simple test example here

    test_df = pd.DataFrame({'age': [25, 30, 35, None], 'bmi': [22, 25, 28, -999]})
    print("Test DataFrame created:", test_df.shape)
    print("Test detect_missing:", detect_missing(test_df))
    print("Test clean_data:", clean_data(test_df, sentinel_value=-999))
    print("Test fill_missing (age, mean):", fill_missing(test_df, 'age', strategy='mean'))
    filters = [{'column': 'site', 'condition': 'equals', 'value': 'Site A'}]
    df_filtered = filter_data(df, filters)
    print("Filtered DataFrame shape:", df_filtered.shape)
    print(df.shape)
                                                                