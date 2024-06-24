import pandas as pd

def load_data(file_path):
    """
    Loads data from an Excel file.

    Args:
    file_path (str): Path to the Excel file

    Returns:
    DataFrame: Loaded data
    """
    df = pd.read_excel(file_path, engine='openpyxl')
    return df

def preprocess_data(df):
    """
    Preprocesses the data by converting time columns to timedelta.

    Args:
    df (DataFrame): DataFrame containing the data

    Returns:
    DataFrame: Preprocessed data
    """
    df['Opening hour'] = df['Opening hour'].apply(time_to_timedelta)
    df['Closing hour'] = df['Closing hour'].apply(time_to_timedelta)
    df['Length'] = pd.to_timedelta(df['Length'], unit='m')
    return df

def time_to_timedelta(t):
    """
    Converts a time object to timedelta.

    Args:
    t (datetime.time): Time object

    Returns:
    Timedelta: Corresponding timedelta object
    """
    return pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
