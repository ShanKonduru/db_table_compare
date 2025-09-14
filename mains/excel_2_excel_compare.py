import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from src.utils.logger_setup import LoggerSetup
from src.utils.performance_metrics import PerformanceMetrics

# Initialize logger once at program start
logger = LoggerSetup.initialize_logger('.//logs//db_compare_log.log', logging.INFO)

# Initialize comparer
from src.utils.excel_comparer import ExcelComparer
from src.utils.html_report import HtmlReport

import pandas as pd
import numpy as np

logger.info("Starting Excel to Excel comparison")
number_of_rows = 1000000  # Number of rows for large Excel files
source_path='DATA\\EXEL_TO_EXCEL\\src.xlsx'
target_path='DATA\\EXEL_TO_EXCEL\\tgt.xlsx' 


def generate_large_excel(file_path, num_rows, seed=42):
    logger.info(f"Generating large Excel file at {file_path} with {num_rows} rows")
    np.random.seed(seed)
    ids = np.arange(1, num_rows + 1)
    names = np.random.choice(['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank', 'Shan', 'Konduru', 'Bhushan', 'Ravi', 'Pavan', 'Kumar', 'Sarma', 'Krishna', 'Sailaja', 'Sri', 'Kirani' ], size=num_rows)
    ages = np.random.randint(20, 70, size=num_rows)
    countries = np.random.choice(['USA', 'Canada', 'UK', 'India', 'Germany', 'France', 'Russia', 'Italy'], size=num_rows)

    df = pd.DataFrame({
        'ID': ids,
        'Name': names,
        'Age': ages,
        'Country': countries
    })
    logger.info(f"Writing DataFrame to Excel file at {file_path}")
    df.to_excel(file_path, index=False, sheet_name='Sheet1')
    logger.info(f"Excel file {file_path} generated successfully")

# Generate Source and Target files
logger.info("Generating source and target Excel files")

logger.info("Generating source Excel file with some variations")
generate_large_excel(source_path, number_of_rows, 37)  # 10k rows
logger.info("Generating target Excel file with some variations")
generate_large_excel(target_path, number_of_rows, 12)  # 10k rows with some variations

PerformanceMetrics.start("Excel_2_Excel_Comparison")

PerformanceMetrics.start("excel_load")
logger.info("Loading Excel files for comparison")
comparer = ExcelComparer(
    source_path=source_path,
    target_path=target_path, 
    sheet_name_source="Sheet1", 
    sheet_name_target="Sheet1" 
)
PerformanceMetrics.stop("excel_load")
# Run comparison
PerformanceMetrics.start("excel_compare")
logger.info("Comparing Excel files")
comparison_df = comparer.compare()
PerformanceMetrics.stop("excel_compare")

PerformanceMetrics.start("create_report")
# Generate report
logger.info("Generating HTML report for comparison results")
report = HtmlReport(
    comparison_df,
    comparer.source_df,
    comparer.target_df
)
PerformanceMetrics.stop("create_report")

PerformanceMetrics.start("save_report")
# Save
logger.info("Saving HTML report to file") 
report.save('c:/MyProjects/db_table_compare/src/outputs/exl_2_exl_comparison_report.html')
PerformanceMetrics.stop("save_report")

PerformanceMetrics.stop("Excel_2_Excel_Comparison")
