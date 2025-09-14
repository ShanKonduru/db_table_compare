import pandas as pd

import logging

logger = logging.getLogger(__name__)

class ExcelComparer:
    def __init__(self, source_path, target_path, sheet_name_source='Sheet1', sheet_name_target='Sheet1', key='ID'):
        logger.info("Loading source and target Excel files.")
        self.source_df = pd.read_excel(source_path, sheet_name=sheet_name_source)
        self.target_df = pd.read_excel(target_path, sheet_name=sheet_name_target)
        self.key = key
        self.comparison_df = None
        logger.info("Excel files loaded successfully.")

    def compare(self):
        """Compare source and target DataFrames and store the comparison results."""
        logger.info("Comparing DataFrames.")
        self.comparison_df = pd.merge(
            self.source_df,
            self.target_df,
            on=self.key,
            how='outer',
            suffixes=('_src', '_tgt'),
            indicator=True
        )
        logger.info("Comparison complete.")
        return self.comparison_df

    def get_diff_summary(self):
        """Return a DataFrame with comparison and diff info."""
        if self.comparison_df is None:
            self.logger.info("No comparison data found, running compare method.")
            self.compare()
        logger.info("Generating diff summary.")
        return self.comparison_df
