import pandas as pd
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DataFrameOperationsResult:
    results: dict
    raw_dataframe: pd.DataFrame

def dataframe_operations(df, operation_type='basic', threshold=None, column=None):
    """
    Perform various pandas DataFrame operations based on parameters.
    """
    # Validate inputs
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    if threshold is not None and not isinstance(threshold, (int, float)):
        raise ValueError("Threshold must be a numeric value.")
    if column is not None and column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

    logger.info(f"Performing operation '{operation_type}' with threshold '{threshold}'")

    results = {}

    # Basic operations
    if operation_type in ['basic', 'all']:
        results['sum'] = df.sum()
        results['mean'] = df.mean()
        results['max'] = df.max()
        results['min'] = df.min()

    # Statistical operations
    if operation_type in ['stats', 'all']:
        results['std'] = df.std()
        results['variance'] = df.var()
        results['median'] = df.median()

    # Threshold operations
    if threshold is not None:
        filtered = df[column] if column and column in df.columns else df
        results['above_threshold'] = filtered[filtered > threshold]
        results['below_threshold'] = filtered[filtered <= threshold]
        results['threshold_mean'] = (
            filtered[filtered > threshold].mean() if (filtered > threshold).any().any() else 0
        )

    # Shape operations
    results['shape'] = df.shape
    results['num_rows'] = df.shape[0]
    results['num_cols'] = df.shape[1]

    # Additional computations
    if not df.empty:
        results['normalized'] = df.apply(
            lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() != x.min() else 0
        )
        results['zscore'] = df.apply(
            lambda x: (x - x.mean()) / x.std() if x.std() != 0 else 0
        )

    return DataFrameOperationsResult(results=results, raw_dataframe=df)
