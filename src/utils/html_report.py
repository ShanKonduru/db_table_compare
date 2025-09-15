from datetime import datetime
import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class HtmlReport:
    """
    Generates an HTML report comparing two data sources (e.g., Excel sheets).
    
    The report includes a summary of differences and a detailed breakdown
    of row-level and column-level discrepancies.
    """
    def __init__(self, comparison_df, source_df, target_df, source_file, target_file, key_column):
        """
        Initializes the HtmlReport with comparison dataframes and file paths.

        Args:
            comparison_df (pd.DataFrame): The DataFrame resulting from a pandas merge
                                          with an indicator column.
            source_df (pd.DataFrame): The original source DataFrame.
            target_df (pd.DataFrame): The original target DataFrame.
            source_file (str): The path to the source file.
            target_file (str): The path to the target file.
            key_column (str): The key column name used for the comparison.
        """
        self.df = comparison_df
        self.source_df = source_df
        self.target_df = target_df
        self.source_file = source_file
        self.target_file = target_file
        # CRITICAL FIX: The key is now a variable passed from the comparer
        self.key = key_column
        logger.info("HtmlReport instance created.")

    def generate_summary(self):
        """
        Generates the summary section of the HTML report.
        """
        src_only = self.df[self.df['_merge'] == 'left_only']
        tgt_only = self.df[self.df['_merge'] == 'right_only']
        both_rows = self.df[self.df['_merge'] == 'both']

        # Determine rows with data differences
        mismatched_rows = self._get_mismatched_rows(both_rows)
        
        total_rows_src = len(self.source_df)
        total_rows_tgt = len(self.target_df)
        total_rows_both = len(both_rows)
        total_diff_rows = len(mismatched_rows)
        num_src_only = len(src_only)
        num_tgt_only = len(tgt_only)
        total_matched = total_rows_both - total_diff_rows

        summary_html = f'''
        <div>
            <h3>Summary</h3>
            <p><strong>Source File:</strong> {self.source_file}</p>
            <p><strong>Target File:</strong> {self.target_file}</p>
            <p><strong>Total rows in source:</strong> {total_rows_src}</p>
            <p><strong>Total rows in target:</strong> {total_rows_tgt}</p>
            <p><strong>Matching rows:</strong> {total_matched}</p>
            <p><strong>Rows only in source:</strong> {num_src_only}</p>
            <p><strong>Rows only in target:</strong> {num_tgt_only}</p>
            <p><strong>Rows with differences:</strong> {total_diff_rows}</p>
        </div>
        '''
        self.summary_html = summary_html
        return summary_html

    def _get_mismatched_rows(self, both_rows):
        """
        Helper method to identify rows with data differences.
        """
        if both_rows.empty:
            return both_rows

        # CRITICAL FIX: Use the normalized key column for exclusion
        common_cols = [col for col in both_rows.columns if not col.endswith('_src') and not col.endswith('_tgt') and col != self.key and col != '_merge']
        
        # Check for differences in common columns
        mismatched_indices = []
        for index, row in both_rows.iterrows():
            is_mismatched = False
            for col in common_cols:
                # Use .get() for safety
                src_val = row.get(f'{col}_src')
                tgt_val = row.get(f'{col}_tgt')
                
                # Check for NaNs and value differences
                if pd.notna(src_val) or pd.notna(tgt_val):
                    if not (pd.isna(src_val) and pd.isna(tgt_val)) and (src_val != tgt_val):
                        is_mismatched = True
                        break
            if is_mismatched:
                mismatched_indices.append(index)
        
        return both_rows.loc[mismatched_indices]
    
    def _is_identical(self):
        """
        Checks if the source and target dataframes are identical.
        """
        src_only_count = len(self.df[self.df['_merge'] == 'left_only'])
        tgt_only_count = len(self.df[self.df['_merge'] == 'right_only'])
        both_rows = self.df[self.df['_merge'] == 'both']
        mismatched_rows = self._get_mismatched_rows(both_rows)
        
        return src_only_count == 0 and tgt_only_count == 0 and len(mismatched_rows) == 0

    def generate_details(self):
        """
        Generates the detailed section of the HTML report.
        """
        details_html = '<h3>Details</h3>'
        
        if self._is_identical():
            details_html += '<p>Both files are identical.</p>'
            return details_html

        # CRITICAL FIX: Use the normalized key column for all lookups
        # Category 1: Rows only in source
        src_only = self.source_df[~self.source_df[self.key].isin(self.target_df[self.key])]
        if not src_only.empty:
            details_html += '<details open><summary><strong>Rows in source only</strong> ({})</summary>'.format(len(src_only))
            details_html += src_only.to_html(index=False)
            details_html += '</details>'

        # Category 2: Rows only in target
        tgt_only = self.target_df[~self.target_df[self.key].isin(self.source_df[self.key])]
        if not tgt_only.empty:
            details_html += '<details open><summary><strong>Rows in target only</strong> ({})</summary>'.format(len(tgt_only))
            details_html += tgt_only.to_html(index=False)
            details_html += '</details>'

        # Category 3: Data mismatches
        both_rows = self.df[self.df['_merge'] == 'both']
        mismatched_rows = self._get_mismatched_rows(both_rows)
        if not mismatched_rows.empty:
            details_html += '<details open><summary><strong>Data mismatches in common rows</strong> ({})</summary>'.format(len(mismatched_rows))
            
            # Highlight differences in the table (This inner function is not needed if you format the HTML string)
            # The logic below will build the table correctly
            
            # Create a combined dataframe for a clear side-by-side view
            combined_diff_df = pd.DataFrame()
            if self.key in mismatched_rows.columns:
                combined_diff_df[self.key] = mismatched_rows[self.key]
            
            # CRITICAL FIX: This part was wrong. It should iterate over the normalized columns
            for col in self.source_df.columns:
                if col != self.key:
                    combined_diff_df[f'{col}_source'] = mismatched_rows.get(f'{col}_src')
                    combined_diff_df[f'{col}_target'] = mismatched_rows.get(f'{col}_tgt')

            # Use a more detailed approach for table generation if needed
            html_table = combined_diff_df.to_html(index=False)
            
            details_html += html_table
            details_html += '</details>'

        # Category 4: Column differences
        extra_cols_src = sorted(list(set(self.source_df.columns) - set(self.target_df.columns)))
        extra_cols_tgt = sorted(list(set(self.target_df.columns) - set(self.source_df.columns)))

        if extra_cols_src or extra_cols_tgt:
            details_html += '<details open><summary><strong>Column differences</strong></summary><ul>'
            if extra_cols_src:
                details_html += '<li><strong>Columns in source only:</strong> {}</li>'.format(', '.join(extra_cols_src))
            if extra_cols_tgt:
                details_html += '<li><strong>Columns in target only:</strong> {}</li>'.format(', '.join(extra_cols_tgt))
            details_html += '</ul></details>'

        return details_html

    def generate_and_save_report(self, filename):
        """
        Generates the complete HTML report and saves it to a file.
        """
        logger.info("Generating and saving report to file.")
        
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Comparison Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h2, h3 {{ color: #333; }}
                p {{ line-height: 1.6; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .highlight {{ background-color: #f8d7da; }}
                details {{ margin-bottom: 15px; border: 1px solid #ccc; padding: 10px; border-radius: 5px; }}
                summary {{ cursor: pointer; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h2>Excel Sheets Comparison Report</h2>
            {self.generate_summary()}
            {self.generate_details()}
            <p>Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
        </html>
        '''

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Report saved to {filename}")