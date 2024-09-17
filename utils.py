import yaml

def load_config(file_name):
    with open(file_name) as f:
        yml_dict = yaml.safe_load(f)
    return yml_dict
