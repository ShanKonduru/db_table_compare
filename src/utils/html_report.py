from datetime import datetime
import os
import pandas as pd

import logging

logger = logging.getLogger(__name__)

class HtmlReport:
    def __init__(self, comparison_df, source_df, target_df, key='ID'):
        self.df = comparison_df
        self.source_df = source_df
        self.target_df = target_df
        self.key = key
        self.html = ""
        logger.info("HtmlReport instance created.")

    def generate_summary(self):
        logger.info("Generating summary section of the report.")
        # Determine common columns for comparison
        common_cols = [col for col in self.source_df.columns if col != self.key and col in self.target_df.columns]

        # Categorize rows
        logger.info("Categorizing rows for summary statistics.")
        src_only = self.df[self.df['_merge'] == 'left_only']
        tgt_only = self.df[self.df['_merge'] == 'right_only']
        both_rows = self.df[self.df['_merge'] == 'both']

        logger.info("Calculating summary statistics.")
        total_rows_src = len(self.source_df)
        total_rows_tgt = len(self.target_df)
        total_rows_both = len(both_rows)

        # Count how many rows in 'both' have all common columns matching
        logger.info("Calculating matched rows.")
        total_matched = 0
        for _, row in both_rows.iterrows():
            all_equal = True
            for col in common_cols:
                val_src = row.get(f'{col}_src')
                val_tgt = row.get(f'{col}_tgt')
                if pd.isnull(val_src) and pd.isnull(val_tgt):
                    logger.info("Both values are NaN, considered equal.")
                    continue
                if val_src != val_tgt:
                    all_equal = False
                    logger.info("Found a differing row.")
                    break
            if all_equal:
                logger.info("Found a matched row.")
                total_matched += 1

        total_diff_rows = total_rows_both - total_matched
        logger.info("Total rows calculated.")
        num_src_only = len(src_only)
        num_tgt_only = len(tgt_only)
        logger.info("Summary statistics calculated.")

        # HTML summary block
        logger.info("Creating HTML summary block.")
        summary_html = f'''
        <div>
            <h3>Summary</h3>
            <p>Total rows in source: {total_rows_src}</p>
            <p>Total rows in target: {total_rows_tgt}</p>
            <p>Matching rows: {total_matched}</p>
            <p>Rows only in source: {num_src_only}</p>
            <p>Rows only in target: {num_tgt_only}</p>
            <p>Rows with differences: {total_diff_rows}</p>
            <p>Matching Accuracy (in source): {total_matched / total_rows_src * 100:.2f}%</p>
        </div>
        '''
        logger.info("Summary HTML block created.")
        return summary_html

    def generate_details(self):
        # Find columns exclusive to each DataFrame
        logger.info("Generating details section of the report.")
        additional_cols_src = set(self.source_df.columns) - set(self.target_df.columns)
        additional_cols_tgt = set(self.target_df.columns) - set(self.source_df.columns)

        logger.info("Categorizing rows for details.")
        src_only = self.df[self.df['_merge'] == 'left_only']
        tgt_only = self.df[self.df['_merge'] == 'right_only']
        both_rows = self.df[self.df['_merge'] == 'both']

        # Common columns for comparison
        logger.info("Determining common columns for detailed comparison.")
        common_cols = [col for col in self.source_df.columns if col != self.key and col in self.target_df.columns]
        logger.info("Common columns determined.")
        details_html = '<h3>Details</h3><ul>'

        # Rows only in source
        logger.info("Processing rows only in source.")
        for _, row in src_only.iterrows():
            details_html += f'<li>Row with {self.key}={row[self.key]} present in source but missing in target.</li>'

        # Rows only in target
        logger.info("Processing rows only in target.")
        for _, row in tgt_only.iterrows():
            details_html += f'<li>Row with {self.key}={row[self.key]} present in target but missing in source.</li>'

        # Compare rows present in both
        logger.info("Processing rows present in both source and target.")
        for _, row in both_rows.iterrows():
            row_id = row[self.key]
            # Check for value differences column-wise
            for col in common_cols:
                val_src = row.get(f'{col}_src')
                val_tgt = row.get(f'{col}_tgt')
                if pd.isnull(val_src) and pd.isnull(val_tgt):
                    continue
                if val_src != val_tgt:
                    details_html += (
                        f'<li>Value change at {self.key}={row_id}, column="{col}": '
                        f'{val_src} (source) vs {val_tgt} (target)</li>'
                    )

        # Columns only in source
        logger.info("Processing columns exclusive to source and target.")
        for col in additional_cols_src:
            details_html += f'<li>Column "{col}" present in source but missing in target.</li>'

        # Columns only in target
        logger.info("Processing columns exclusive to target.")
        for col in additional_cols_tgt:
            details_html += f'<li>Column "{col}" present in target but missing in source.</li>'

        details_html += '</ul>'
        logger.info("Details HTML block created.")
        return details_html

    def generate(self):
        logger.info("Generating full HTML report.")
        summary_html = self.generate_summary()
        details_html = self.generate_details()

        self.html = f'''
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                h2 {{
                    color: #2e6c80;
                }}
                h3 {{
                    color: #1c4870;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #999;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                li {{
                    margin-bottom: 8px;
                }}
            </style>
        </head>
        <body>
            <h2>Excel Sheets Comparison Report</h2>
            {summary_html}
            {details_html}
        </body>
        </html>
        '''
        logger.info("Full HTML report generated.")
        return self.html

    def generate_and_save_report(self, filename):
        logger.info("Generating and saving report to file.")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('<html><head><style>/* styles here */</style></head><body>')
            f.write('<h2>Excel Sheets Comparison Report</h2>')
            f.write(self.generate_summary())
            f.write('<h3>Details</h3><table>')
            # Write headers
            headers = ['ID'] + [col for col in self.source_df.columns if col != self.key]
            f.write('<tr>' + ''.join([f'<th>{h}</th>' for h in headers]) + '</tr>')

            # Write rows in chunks
            for index, row in self.df.iterrows():
                row_html = '<tr>'
                row_html += f'<td>{row[self.key]}</td>'
                for col in self.source_df.columns:
                    if col == self.key:
                        continue
                    val_src = row.get(f'{col}_src', '')
                    val_tgt = row.get(f'{col}_tgt', '')
                    style = ''
                    if pd.notnull(val_src) and pd.notnull(val_tgt) and val_src != val_tgt:
                        style = 'background-color: #f8d7da;'
                    row_html += f'<td style="{style}">{val_src}</td>'
                row_html += '</tr>'
                f.write(row_html)
            f.write('</table></body></html>')
        logger.info(f"Report saved to {filename}") 

    def save(self, filename='comparison_report.html'):
        # Extract directory and filename
        logger.info("Saving report with timestamped filename.")
        dir_name = os.path.dirname(filename)
        base_name = os.path.basename(filename)
        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Append timestamp before extension
        name, ext = os.path.splitext(base_name)
        new_filename = f"{name}_{timestamp}{ext}"
        full_path = os.path.join(dir_name, new_filename)

        # Ensure directory exists
        if dir_name:
            logger.info("Ensuring output directory exists.")
            os.makedirs(dir_name, exist_ok=True)

        # Save the report with the timestamped filename
        with open(full_path, 'w') as f:
            f.write(self.generate())
        logger.info(f"Report saved to {full_path}")
        return full_path
    