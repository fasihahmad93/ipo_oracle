#Import necessary libraries
import os
import pandas as pd
import json

#Write a function to import a CSV file
def import_csv(file_path):
    """
    Imports a CSV file and returns a pandas DataFrame.
    
    Parameters:
    file_path (str): The path to the CSV file.
    
    Returns:
    pd.DataFrame: A DataFrame containing the data from the CSV file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise ValueError(f"An error occurred while reading the CSV file: {e}")


#Write a function to import an Excel file
def import_excel(file_path, sheet_name=0):
    """
    Imports an Excel file and returns a pandas DataFrame.
    
    Parameters:
    file_path (str): The path to the Excel file.
    sheet_name (str or int, optional): The sheet name or index to read. Defaults to 0 (first sheet).
    
    Returns:
    pd.DataFrame: A DataFrame containing the data from the specified sheet of the Excel file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        raise ValueError(f"An error occurred while reading the Excel file: {e}")

    #function to import a JSON file in list of dictionaries format
def import_json(file_path):
    """
    Imports a JSON file and returns a list of dictionaries.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise ValueError(f"An error occurred while reading the JSON file: {e}")

    # Function to import yaml files
def import_yaml(file_path):
    """
    Imports a YAML file and returns a dictionary.
    
    Parameters:
    file_path (str): The path to the YAML file.
    
    Returns:
    dict: A dictionary containing the data from the YAML file.
    """
    import yaml
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except Exception as e:
        raise ValueError(f"An error occurred while reading the YAML file: {e}")

def import_text(file_path):
    """
    Imports a text file and returns its content as a string.
    
    Parameters:
    file_path (str): The path to the text file.
    
    Returns:
    str: The content of the text file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        raise ValueError(f"An error occurred while reading the text file: {e}")