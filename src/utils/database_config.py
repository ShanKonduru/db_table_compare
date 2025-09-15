import configparser
import json
from typing import List, Dict, Any

import logging

logger = logging.getLogger(__name__)

from src.utils.ini_reader import IniReader

class DatabaseConfig:
    def __init__(self):
        self.ini_reader = IniReader("src/inputs/database_config.ini")
        self.config = self.ini_reader.config
        self.logger = logging.getLogger(__name__)  # Correctly initialize logger
        self.logger.info("DatabaseConfig initialized with configuration from ini file.")

    def get_scenarios_count(self) -> int:
        """Returns the number of scenarios to execute."""
        scenarios = self.config['DATA_SCENARIOS_TO_EXECUTE']
        self.logger.info(f"Number of scenarios to execute: {len(scenarios)}")
        return len(scenarios)

    def get_scenarios_list(self) -> List[str]:
        """Returns a list of scenario names."""
        scenarios = self.config['DATA_SCENARIOS_TO_EXECUTE']
        self.logger.info(f"Scenarios to execute: {list(scenarios.values())}")
        return [scenarios[key] for key in scenarios]

    def get_scenario_name(self, scenario_key: str) -> str:
        """Returns the name of the scenario for a given key (e.g., SCENARIO_1)."""
        self.logger.info(f"Retrieving scenario name for key: {scenario_key}")
        return self.config['DATA_SCENARIOS_TO_EXECUTE'].get(scenario_key, "")

    def get_source_file_path(self, scenario_name: str) -> str:
        """Returns the source file path for a given scenario name."""
        section = self.config[scenario_name]
        self.logger.info(f"Retrieving source file path for scenario: {scenario_name}")
        return section.get('SOURCE_FILE_PATH', "")

    def get_target_file_path(self, scenario_name: str) -> str:
        """Returns the target file path for a given scenario name."""
        section = self.config[scenario_name]
        self.logger.info(f"Retrieving target file path for scenario: {scenario_name}")
        return section.get('TARGET_FILE_PATH', "")

    def get_column_mapping(self, mapping_name: str) -> Dict[str, Dict[str, Any]]:
        """
        Parses a column mapping section and returns a dictionary of dictionaries.

        Args:
            mapping_name (str): The name of the column mapping section (e.g., 'EXEL_TO_EXCEL_COLUMN_MAPPING').

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary where keys are source column names
                                       and values are dictionaries of mapping attributes.
        """
        if mapping_name not in self.config:
            self.logger.error(f"Column mapping section '{mapping_name}' not found in the config file.")
            return {}

        mapping_section = self.config[mapping_name]
        column_mapping = {}
        for src_col, attributes_str in mapping_section.items():
            try:
                # Use json.loads to parse the string into a dictionary
                attributes = json.loads(attributes_str)
                column_mapping[src_col] = attributes
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse mapping for column '{src_col}': {e}")
                column_mapping[src_col] = {"target": None}  # Provide a default fallback

        self.logger.info(f"Successfully parsed column mapping: {mapping_name}")
        return column_mapping