import pandas as pd
import logging

logger = logging.getLogger(__name__)

class ConfigurableExcelComparer:
    """
    Compares two Excel files based on a provided column mapping.
    
    This class handles differences in column names, order, and data types
    by standardizing the data before performing a merge comparison.
    """
    def __init__(self, source_path: str, target_path: str, column_mapping: dict,
                 sheet_name_source: str = 'Sheet1', sheet_name_target: str = 'Sheet1'):
        """
        Initializes the ConfigurableExcelComparer with file paths and a column mapping.

        Args:
            source_path (str): Path to the source Excel file.
            target_path (str): Path to the target Excel file.
            column_mapping (dict): A dictionary mapping source columns to target
                                   columns and their attributes (type, key, etc.).
            sheet_name_source (str): The name of the sheet in the source file.
            sheet_name_target (str): The name of the sheet in the target file.
        """
        self.source_path = source_path
        self.target_path = target_path
        self.column_mapping = column_mapping
        self.sheet_name_source = sheet_name_source
        self.sheet_name_target = sheet_name_target
        self.source_df = None
        self.target_df = None
        self.comparison_df = None
        self.key_column = None
        
        logger.info("ConfigurableExcelComparer initialized with configuration.")

    def _preprocess_dataframes(self):
        """
        Loads and standardizes source and target DataFrames based on the column mapping.
        This includes renaming columns, applying data type conversions, and identifying the key column.
        """
        try:
            # Load DataFrames and normalize column names to lowercase for robust lookup
            self.source_df = pd.read_excel(self.source_path, sheet_name=self.sheet_name_source)
            self.source_df.columns = [col.lower() for col in self.source_df.columns]
            
            self.target_df = pd.read_excel(self.target_path, sheet_name=self.sheet_name_target)
            self.target_df.columns = [col.lower() for col in self.target_df.columns]
            
            logger.info("DataFrames loaded and column names normalized. Starting preprocessing...")
            
            # --- Step 1: Initialize standardized DataFrames ---
            standardized_source = pd.DataFrame()
            standardized_target = pd.DataFrame()
            
            # --- Step 2: Process the column mapping and build standardized DataFrames ---
            for src_col_key, attributes in self.column_mapping.items():
                src_col_norm = src_col_key.lower()
                target_col_key = attributes.get("target")
                target_col_norm = target_col_key.lower() if target_col_key else None

                if attributes.get("is_key"):
                    self.key_column = src_col_norm
                
                if target_col_norm:
                    if src_col_norm in self.source_df.columns and target_col_norm in self.target_df.columns:
                        standardized_source[src_col_norm] = self.source_df[src_col_norm]
                        standardized_target[src_col_norm] = self.target_df[target_col_norm]
                        
                        data_type = attributes.get("type")
                        if data_type == 'int':
                            standardized_source[src_col_norm] = pd.to_numeric(standardized_source[src_col_norm], errors='coerce').fillna(-1).astype(int)
                            standardized_target[src_col_norm] = pd.to_numeric(standardized_target[src_col_norm], errors='coerce').fillna(-1).astype(int)
                        elif data_type == 'datetime':
                            # Use 'errors=coerce' for robustness
                            standardized_source[src_col_norm] = pd.to_datetime(standardized_source[src_col_norm], errors='coerce', format=attributes.get("format"))
                            standardized_target[src_col_norm] = pd.to_datetime(standardized_target[src_col_norm], errors='coerce', format=attributes.get("format"))
                    else:
                        logger.warning(f"Mapped column '{src_col_key}' (src) or '{target_col_key}' (tgt) not found in respective files. Skipping.")
                else:
                    if src_col_norm in self.source_df.columns:
                        standardized_source[src_col_norm] = self.source_df[src_col_norm]
                    else:
                        logger.warning(f"Source-only column '{src_col_key}' not found in the source file. Skipping.")

            # --- Step 3: Identify unmapped columns ---
            self.source_unmapped_cols = list(set(self.source_df.columns) - set(standardized_source.columns))
            self.target_unmapped_cols = list(set(self.target_df.columns) - set(standardized_target.columns))

            self.source_df = standardized_source
            self.target_df = standardized_target
            
            logger.info("Preprocessing complete.")
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise
        except KeyError as e:
            logger.error(f"Column missing in DataFrame: {e}")
            raise
                            
    def compare(self):
        """
        Performs the comparison by first preprocessing the data, then merging.
        
        Returns:
            pd.DataFrame: A DataFrame with the comparison results, including an indicator column.
        """
        if self.source_df is None or self.target_df is None:
            self._preprocess_dataframes()
            
        if self.key_column is None:
            raise ValueError("No key column was specified in the column mapping.")

        logger.info(f"Comparing DataFrames on key column: '{self.key_column}'.")

        self.comparison_df = pd.merge(
            self.source_df,
            self.target_df,
            on=self.key_column,
            how='outer',
            suffixes=('_src', '_tgt'),
            indicator=True
        )
        logger.info("Comparison complete.")
        return self.comparison_df

    def get_diff_summary(self):
        """
        Returns the comparison DataFrame. This is now a simplified method
        since all the core logic is in `compare`.
        """
        if self.comparison_df is None:
            self.compare()
        logger.info("Returning comparison summary.")
        return self.comparison_df