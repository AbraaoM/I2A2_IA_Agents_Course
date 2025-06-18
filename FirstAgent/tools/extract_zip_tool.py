from langchain.tools import tool
import pandas as pd
import zipfile
from typing import Dict, Any
import io

@tool
def extract_zip_contents(zip_path: str) -> Dict[str, Any]:
    """
    Extracts CSV files from a zip and preserves their original format.
    
    Args:
        zip_path (str): Path to the zip file containing CSV files
    
    Returns:
        dict: A dictionary where:
            - keys are filenames
            - values are pandas DataFrames with preserved data types
    """
    extracted_data = {}
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith('.csv'):
                    with zip_ref.open(file) as f:
                        # Read CSV with pandas, preserving data types
                        df = pd.read_csv(
                            io.BytesIO(f.read()),
                            parse_dates=True,  # Auto-detect and parse dates
                            dtype_backend='numpy_nullable'  # Better handle mixed types
                        )
                        extracted_data[file] = df
        
        return extracted_data

    except Exception as e:
        print(f"Error extracting ZIP: {str(e)}")
        return {}
