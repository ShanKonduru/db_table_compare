import pandas as pd
import numpy as np

def generate_excel_files_with_mapping():
    """
    Generates SRC.xlsx and TGT.xlsx with a specific column mapping and data differences.
    
    The files are created with the following schema:
    - SRC.xlsx: ID, NAME, AGE, COUNTRY, JOIN_DATE, SRC_SALARY
    - TGT.xlsx: TGT_ID, TGT_FULL_NAME, TGT_AGE, TGT_COUNTRY, TGT_START_DATE, TGT_EXTRA_COL
    """

    # --- Configuration ---
    num_rows = 1000000  # Number of rows for the generated files
    
    # --- Generate common data (matching rows) ---
    np.random.seed(42)
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
    ages = np.random.randint(20, 60, size=num_rows)
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
    join_dates = pd.to_datetime('2023-01-01') + pd.to_timedelta(np.arange(num_rows), unit='s')
    
    # --- Create Source DataFrame (SRC.xlsx) ---
    source_df = pd.DataFrame({
        'ID': ids,
        'NAME': names,
        'AGE': ages,
        'COUNTRY': countries,
        'JOIN_DATE': join_dates,
        'SRC_SALARY': np.random.randint(50000, 100000, size=num_rows) # Exists only in source
    })
    
    # --- Create Target DataFrame (TGT.xlsx) ---
    target_df = pd.DataFrame({
        'TGT_ID': ids,
        'TGT_FULL_NAME': names,
        'TGT_AGE': ages,
        'TGT_COUNTRY': countries,
        'TGT_START_DATE': join_dates,
        'TGT_EXTRA_COL': np.random.choice(['A', 'B', 'C'], size=num_rows) # Exists only in target
    })

    # --- Introduce Differences for Testing ---
    
    # 1. Row-wise data differences (mismatched AGE for ID 10 and 20)
    source_df.loc[9, 'AGE'] = 99  # ID=10 (index 9)
    target_df.loc[19, 'TGT_AGE'] = 111 # ID=20 (index 19)
    
    # 2. Rows in source only (delete a few from the target)
    target_df.drop(index=[100, 101, 102], inplace=True)
    
    # 3. Rows in target only (delete a few from the source)
    source_df.drop(index=[200, 201, 202], inplace=True)
    
    # 4. Column data type/format differences (join dates)
    # Convert a few dates in target to a different string format
    target_df['TGT_START_DATE'] = target_df['TGT_START_DATE'].dt.strftime('%m/%d/%Y')
    
    # --- Save to Excel files ---
    output_dir = 'DATA/EXEL_TO_EXCEL'
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    source_path = os.path.join(output_dir, 'src_mapping.xlsx')
    target_path = os.path.join(output_dir, 'tgt_mapping.xlsx')
    
    source_df.to_excel(source_path, index=False)
    target_df.to_excel(target_path, index=False)
    
    print(f"Generated {source_path} and {target_path} successfully.")

from datetime import datetime
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
from src.utils.database_config import DatabaseConfig
from src.utils.configurable_excel_comparer import ConfigurableExcelComparer
from src.utils.html_report import HtmlReport

def setup_environment():
    """Initializes the logging system and sets up file paths."""
    logger = LoggerSetup.initialize_logger('.//logs//excel_mapping_compare.log', logging.INFO)
    logger.info("Starting Excel to Excel comparison process with mapping.")
    return logger

def get_config():
    """
    Initializes and returns the DatabaseConfig instance.
    """
    try:
        config_reader = DatabaseConfig()
        return config_reader
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

def generate_html_report_file_name(filename='comparison_report.html'):
    """
    Generates a timestamped filename for the HTML report.
    """
    logger.info("Saving report with timestamped filename.")
    dir_name = os.path.dirname(filename)
    base_name = os.path.basename(filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(base_name)
    new_filename = f"{name}_{timestamp}{ext}"
    full_path = os.path.join(dir_name, new_filename)

    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    logger.info(f"Report will be saved to {full_path}")
    return full_path

def run_comparison_and_report(scenario_name: str, config_reader: DatabaseConfig):
    """
    Executes the main comparison logic and generates an HTML report
    for a specific scenario defined in the config file.

    Args:
        scenario_name (str): The name of the scenario section in the config file.
        config_reader (DatabaseConfig): The configuration reader instance.
    """
    logger.info(f"Running comparison for scenario: {scenario_name}")
    PerformanceMetrics.start(f"{scenario_name}_Comparison")

    try:
        # Get file paths and column mapping from the config
        source_path = config_reader.get_source_file_path(scenario_name)
        target_path = config_reader.get_target_file_path(scenario_name)
        mapping_name = config_reader.config[scenario_name]['COLUMN_MAPPING']
        column_mapping = config_reader.get_column_mapping(mapping_name)

        if not source_path or not target_path or not column_mapping:
            logger.error(f"Configuration for scenario '{scenario_name}' is incomplete. Skipping.")
            return

        # Initialize and run the configurable comparer
        comparer = ConfigurableExcelComparer(
            source_path=source_path,
            target_path=target_path,
            column_mapping=column_mapping
        )
        
        comparison_df = comparer.compare()

        # Generate and save the HTML report
        report = HtmlReport(
            comparison_df,
            comparer.source_df,
            comparer.target_df,
            source_file=source_path,
            target_file=target_path,
            key_column=comparer.key_column  # Pass the key_column to the report
        )

        html_report_file_name = generate_html_report_file_name(filename='c:/MyProjects/db_table_compare/src/outputs/exl_2_exl_mapping_comparison_report.html')
        report.generate_and_save_report(html_report_file_name)

    except Exception as e:
        logger.error(f"An error occurred during {scenario_name} comparison: {e}")
    finally:
        PerformanceMetrics.stop(f"{scenario_name}_Comparison")
        logger.info(f"Comparison process for {scenario_name} completed.")


if __name__ == "__main__":
    # generate_excel_files_with_mapping()
        
    logger = setup_environment()
    
    # Get configuration settings
    config_reader = get_config()
    
    # Run comparison for the specified scenario from the config file
    scenarios_to_run = config_reader.get_scenarios_list()
    if not scenarios_to_run:
        logger.warning("No scenarios found to execute in the configuration file.")
    else:
        # For this example, we'll just run the first scenario
        scenario_to_run = scenarios_to_run[0]
        run_comparison_and_report(scenario_to_run, config_reader)
