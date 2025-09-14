import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize comparer
from src.utils.excel_comparer import ExcelComparer
from src.utils.html_report import HtmlReport

comparer = ExcelComparer(
    source_path='DATA\\EXEL_TO_EXCEL\\src.xlsx',
    target_path='DATA\\EXEL_TO_EXCEL\\tgt.xlsx', 
    sheet_name_source="Sheet1", 
    sheet_name_target="Sheet1" 
)

# Run comparison
comparison_df = comparer.compare()
    
# Generate report
report = HtmlReport(
    comparison_df,
    comparer.source_df,
    comparer.target_df
)

# Save
report.save('c:/MyProjects/db_table_compare/src/outputs/exl_2_exl_comparison_report.html')
