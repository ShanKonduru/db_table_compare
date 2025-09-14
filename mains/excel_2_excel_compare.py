import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from src.utils.logger_setup import LoggerSetup
from src.utils.performance_metrics import PerformanceMetrics

# Initialize logger once at program start
LoggerSetup.initialize_logger('.//logs//db_compare_log.log', logging.INFO)

# Initialize comparer
from src.utils.excel_comparer import ExcelComparer
from src.utils.html_report import HtmlReport

PerformanceMetrics.start("Excel_2_Excel_Comparison")

PerformanceMetrics.start("excel_load")
comparer = ExcelComparer(
    source_path='DATA\\EXEL_TO_EXCEL\\src.xlsx',
    target_path='DATA\\EXEL_TO_EXCEL\\tgt.xlsx', 
    sheet_name_source="Sheet1", 
    sheet_name_target="Sheet1" 
)
PerformanceMetrics.stop("excel_load")


# Run comparison
PerformanceMetrics.start("excel_compare")
comparison_df = comparer.compare()
PerformanceMetrics.stop("excel_compare")

PerformanceMetrics.start("create_report")
# Generate report
report = HtmlReport(
    comparison_df,
    comparer.source_df,
    comparer.target_df
)
PerformanceMetrics.stop("create_report")

PerformanceMetrics.start("save_report")
# Save
report.save('c:/MyProjects/db_table_compare/src/outputs/exl_2_exl_comparison_report.html')
PerformanceMetrics.stop("save_report")

PerformanceMetrics.stop("Excel_2_Excel_Comparison")
