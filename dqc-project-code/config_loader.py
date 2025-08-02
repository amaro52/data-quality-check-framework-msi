import json
import os


'''
Method to load and validate JSON configuration file. 
config_path [=] file path of config file
Returns a dictionary of the parsed configuration
'''
def load_config(config_path):
    # raise error if file path does not exist
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    
    with open(config_path, "r") as f:
        config = json.load(f)

    # basic validation
    if "DataQualityChecks" not in config:
        raise ValueError(f"Missing 'DataQualityChecks' key in {config_path}")
    
    if not isinstance(config["DataQualityChecks"], dict):
        raise ValueError("'DataQualityChecks' must be a list.")
    

    return config
        