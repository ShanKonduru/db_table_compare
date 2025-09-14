import sys
import os
import logging
import pandas as pd
import numpy as np

# Add the parent directory to sys.path
# This allows for importing modules from the 'src' directory.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.logger_setup import LoggerSetup
from src.utils.performance_metrics import PerformanceMetrics
from src.utils.excel_comparer import ExcelComparer
from src.utils.html_report import HtmlReport

def setup_environment():
    """
    Initializes the logging system and sets up file paths.

    Returns:
        tuple: A tuple containing the logger and file paths.
    """
    # Initialize logger once at program start
    logger = LoggerSetup.initialize_logger('.//logs//db_compare_log.log', logging.INFO)
    logger.info("Starting Excel to Excel comparison process.")
    
    # Define file paths and number of rows
    number_of_rows = 100000  # A more manageable number for demonstration
    source_path = 'DATA\\EXEL_TO_EXCEL\\src.xlsx'
    target_path = 'DATA\\EXEL_TO_EXCEL\\tgt.xlsx'
    target_path_variation = 'DATA\\EXEL_TO_EXCEL\\tgt_varied.xlsx'
    
    return logger, number_of_rows, source_path, target_path, target_path_variation

def generate_large_excel(file_path, num_rows, seed=42):
    """
    Generates a large Excel file with synthetic data.

    Args:
        file_path (str): The path where the Excel file will be saved.
        num_rows (int): The number of rows to generate.
        seed (int, optional): The random seed for reproducibility. Defaults to 42.
    """
    logger.info(f"Generating large Excel file at {file_path} with {num_rows} rows.")
    np.random.seed(seed)
    ids = np.arange(1, num_rows + 1)
    names = np.random.choice([
        'Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank', 'Shan', 'Konduru',
        'Bhushan', 'Ravi', 'Pavan', 'Kumar', 'Sarma', 'Krishna', 'Sailaja',
        'Sri', 'Kirani', 'Rashmika', 'Anushka', 'Nani', 'Vijay', 'Ajith',
        'Thalapathy', 'Suriya', 'Ram Charan', 'Allu Arjun', 'Mahesh Babu',
        'Prabhas', 'Jr NTR', 'Yash', 'Darshan', 'Upendra', 'Kiccha Sudeep',
        'Puneeth Rajkumar', 'Radhika Pandit', 'Shraddha Srinath', 'Rashmika Mandanna',
        'Anushka Shetty', 'Tamannaah Bhatia', 'Kajal Aggarwal', 'Samantha Akkineni',
        'Nayanthara', 'Trisha Krishnan', 'Keerthy Suresh', 'Aishwarya Rai',
        'Deepika Padukone', 'Alia Bhatt', 'Katrina Kaif', 'Priyanka Chopra',
        'Ananya Panday', 'Sara Ali Khan', 'Janhvi Kapoor', 'Disha Patani',
        'Sachin Tendulkar', 'Virat Kohli', 'Rohit Sharma', 'MS Dhoni',
        'Jasprit Bumrah', 'Hardik Pandya', 'KL Rahul', 'Shikhar Dhawan',
        'Rishabh Pant', 'Yuzvendra Chahal', 'Bhuvneshwar Kumar', 'Ravindra Jadeja',
        'Ben Stokes', 'Joe Root', 'Jofra Archer', 'Jos Buttler', 'Eoin Morgan',
        'Kane Williamson', 'Ross Taylor', 'Trent Boult', 'Tim Southee',
        'Mitchell Starc', 'Pat Cummins', 'Steve Smith', 'David Warner',
        'Bill Gates', 'Elon Musk', 'Jeff Bezos', 'Warren Buffett',
        'Mark Zuckerberg', 'Larry Page', 'Sergey Brin', 'Tim Cook',
        'Sundar Pichai', 'Satya Nadella', 'Sheryl Sandberg', 'Susan Wojcicki'
    ], size=num_rows)
    ages = np.random.randint(20, 70, size=num_rows)
    countries = np.random.choice([
        'USA', 'Canada', 'UK', 'India', 'Germany', 'France', 'Russia', 'Italy',
        'Spain', 'Australia', 'Brazil', 'China', 'Japan', 'South Korea', 'Mexico',
        'Netherlands', 'Sweden', 'Norway', 'Denmark', 'Finland', 'Poland', 'Turkey',
        'Saudi Arabia', 'UAE', 'South Africa', 'Egypt', 'Nigeria', 'Argentina',
        'Chile', 'Colombia', 'Peru', 'Venezuela', 'Thailand', 'Vietnam', 'Indonesia',
        'Philippines', 'Malaysia', 'Singapore', 'New Zealand', 'Ireland', 'Belgium',
        'Switzerland', 'Austria', 'Portugal', 'Greece', 'Czech Republic', 'Hungary',
        'Romania', 'Bulgaria', 'Croatia', 'Slovakia', 'Slovenia', 'Ukraine'
    ], size=num_rows)
    
    df = pd.DataFrame({
        'ID': ids,
        'Name': names,
        'Age': ages,
        'Country': countries
    })
    
    logger.info(f"Writing DataFrame to Excel file at {file_path}.")
    df.to_excel(file_path, index=False, sheet_name='Sheet1')
    logger.info(f"Excel file {file_path} generated successfully.")

def create_variations(target_file, original_df):
    """
    Creates a new Excel file with variations (dropped rows, changed values)
    based on an original DataFrame.

    Args:
        target_file (str): The path to save the new varied Excel file.
        original_df (pd.DataFrame): The DataFrame to introduce variations into.
    """
    logger.info("Creating variations in the target data.")
    df = original_df.copy()
    
    # Randomly drop 5% of the rows to test missing data detection
    drop_indices = np.random.choice(df.index, size=int(0.05 * len(df)), replace=False)
    df.drop(index=drop_indices, inplace=True)
    
    # Randomly change some values
    num_changes = int(0.02 * len(df))
    change_indices = np.random.choice(df.index, size=num_changes, replace=False)
    df.loc[change_indices, 'Age'] = np.random.randint(20, 70, size=num_changes)
    
    logger.info(f"Writing varied DataFrame to Excel file at {target_file}.")
    df.to_excel(target_file, index=False, sheet_name='Sheet1')
    logger.info(f"Varied Excel file {target_file} generated successfully.")

def run_comparison_and_report(source_path, target_path):
    """
    Executes the main comparison logic and generates an HTML report.

    Args:
        source_path (str): The file path of the source Excel file.
        target_path (str): The file path of the target Excel file.
    """
    PerformanceMetrics.start("Excel_2_Excel_Comparison")

    # Load Excel files for comparison
    PerformanceMetrics.start("excel_load")
    logger.info("Loading Excel files for comparison.")
    comparer = ExcelComparer(
        source_path=source_path,
        target_path=target_path,
        sheet_name_source="Sheet1",
        sheet_name_target="Sheet1"
    )
    PerformanceMetrics.stop("excel_load")
    
    # Run comparison
    PerformanceMetrics.start("excel_compare")
    logger.info("Comparing Excel files.")
    comparison_df = comparer.compare()
    PerformanceMetrics.stop("excel_compare")
    
    # Generate and save report
    PerformanceMetrics.start("create_report")
    logger.info("Generating HTML report for comparison results.")
    report = HtmlReport(
        comparison_df,
        comparer.source_df,
        comparer.target_df
    )
    PerformanceMetrics.stop("create_report")
    
    PerformanceMetrics.start("save_report")
    logger.info("Saving HTML report to file.")
    report.save('c:/MyProjects/db_table_compare/src/outputs/exl_2_exl_comparison_report.html')
    PerformanceMetrics.stop("save_report")
    
    PerformanceMetrics.stop("Excel_2_Excel_Comparison")
    logger.info("Comparison and reporting process completed.")

# The `if __name__ == "__main__":` block ensures that the main function
# is called only when the script is executed directly.
if __name__ == "__main__":
    logger, number_of_rows, source_path, target_path, target_path_variation = setup_environment()
    
    # Generate source and target files with unique seeds to ensure differences
    logger.info("Generating source and target Excel files.")
    generate_large_excel(source_path, number_of_rows, seed=37)
    generate_large_excel(target_path, number_of_rows, seed=12)
    
    # Read the original target data and create a new varied version for testing
    original_target_df = pd.read_excel(target_path, sheet_name='Sheet1')
    create_variations(target_path_variation, original_target_df)
    
    # Use the varied file for the comparison
    target_path = target_path_variation
    
    # Run the comparison and generate the final report
    run_comparison_and_report(source_path, target_path)