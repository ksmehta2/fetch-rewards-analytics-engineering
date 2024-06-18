import json
import pandas as pd
from datetime import datetime

def parse_date(date):
    """
    Parse date from a dictionary containing a timestamp.
    
    Parameters:
    date (dict): Dictionary containing the date with '$date' key.
    
    Returns:
    str: Formatted date string.
    """
    if isinstance(date, dict) and '$date' in date:
        return datetime.fromtimestamp(date['$date'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    return date

def flatten_dict(d, parent_key='', sep='_'):
    """
    Flatten a nested dictionary.
    
    Parameters:
    d (dict): The dictionary to flatten.
    parent_key (str): The base key string for nested keys.
    sep (str): Separator for concatenating nested keys.
    
    Returns:
    dict: Flattened dictionary.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def preprocess_entry(entry):
    """
    Preprocess a single entry from the JSON data.
    
    Parameters:
    entry (dict): The entry to preprocess.
    
    Returns:
    dict: Preprocessed entry with flattened structure and parsed dates.
    """
    entry = flatten_dict(entry)  # Flatten any nested dictionaries
    for key, value in entry.items():
        if isinstance(value, list):
            entry[key] = json.dumps(value)  # Convert lists to JSON strings
        elif key.endswith('_$date'):
            entry[key] = parse_date(value)  # Parse date if it's a date object
    return entry

def preprocess_json(data):
    """
    Preprocess the JSON data.
    
    Parameters:
    data (list): List of entries from the JSON file.
    
    Returns:
    list: List of preprocessed entries.
    """
    return [preprocess_entry(entry) for entry in data]

def load_json(file_path):
    """
    Load and preprocess JSON data from a file.
    
    Parameters:
    file_path (str): Path to the JSON file.
    
    Returns:
    list: List of preprocessed entries.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return preprocess_json([json.loads(line) for line in f])

def evaluate_data_quality(data, table_name):
    """
    Evaluate the quality of the data.
    
    Parameters:
    data (list): List of preprocessed entries.
    table_name (str): Name of the table being evaluated.
    """
    df = pd.DataFrame(data)
    print(f"Data Quality Evaluation for {table_name}:")
    print(f"Total Records: {len(df)}")
    print("Missing Values:")
    print(df.isnull().sum())
    print(f"Duplicate Records: {df.duplicated().sum()}")
    print("Data Types:")
    print(df.dtypes)

# Load and preprocess data from JSON files
users = load_json('/Users/kshitijmehta/Downloads/users.json')
brands = load_json('/Users/kshitijmehta/Downloads/brands.json')
receipts = load_json('/Users/kshitijmehta/Downloads/receipts.json')

# Evaluate data quality
evaluate_data_quality(users, "Users")
evaluate_data_quality(brands, "Brands")
evaluate_data_quality(receipts, "Receipts")
