import configparser
from typing import List

from src.utils.ini_reader import IniReader

class DatabaseConfig:
    def __init__(self):
        self.ini_reader = IniReader("src\inputs\database_config.ini")
        self.config = self.ini_reader.config

    def get_scenarios_count(self) -> int:
        """Returns the number of scenarios to execute."""
        scenarios = self.ini_reader.read('DATA_SCENARIOS_TO_EXECUTE')
        return len(scenarios)

    def get_scenarios_list(self) -> List[str]:
        """Returns a list of scenario names."""
        scenarios = self.config['DATA_SCENARIOS_TO_EXECUTE']
        return [scenarios[key] for key in scenarios]

    def get_scenario_name(self, scenario_key: str) -> str:
        """Returns the name of the scenario for a given key (e.g., SCENARIO_1)."""
        return self.config['DATA_SCENARIOS_TO_EXECUTE'].get(scenario_key, "")

    def get_source_file_path(self, scenario_name: str) -> str:
        """Returns the source file path for a given scenario name."""
        section = self.config[scenario_name]
        return section.get('SOURCE_FILE_PATH', "")

    def get_target_file_path(self, scenario_name: str) -> str:
        """Returns the target file path for a given scenario name."""
        section = self.config[scenario_name]
        return section.get('TARGET_FILE_PATH', "")
