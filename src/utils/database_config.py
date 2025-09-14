import configparser
from typing import List

import logging

logger = logging.getLogger(__name__)

from src.utils.ini_reader import IniReader

class DatabaseConfig:
    def __init__(self):
        self.ini_reader = IniReader("src\inputs\database_config.ini")
        self.config = self.ini_reader.config
        self.logger.info("DatabaseConfig initialized with configuration from ini file.")

    def get_scenarios_count(self) -> int:
        """Returns the number of scenarios to execute."""
        scenarios = self.ini_reader.read('DATA_SCENARIOS_TO_EXECUTE')
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
