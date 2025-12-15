import yaml

def load_config(file_path:str="E:\\CREWAI_APPLICATION_TRACKING_SYSTEM\\Config\\configfile.yaml")->dict:
    """
    Load configuration from a YAML file.

    Args:
        file_path (str): The path to the YAML configuration file.
    """
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config