import configparser

class IniReader:
    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)
    
    def get_sections(self):
        """Return a list of all section names."""
        return self.config.sections()
    
    def get_keys(self, section):
        """Return a list of all keys in the specified section."""
        if section in self.config:
            return self.config[section].keys()
        else:
            raise KeyError(f"Section '{section}' not found.")
    
    def get_value(self, section, key):
        """Return the value for a specific key in a section."""
        if section in self.config:
            if key in self.config[section]:
                return self.config[section][key]
            else:
                raise KeyError(f"Key '{key}' not found in section '{section}'.")
        else:
            raise KeyError(f"Section '{section}' not found.")
    
    def __repr__(self):
        return f"<IniReader filename={self.configfilename}>"