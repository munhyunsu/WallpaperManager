import yaml


def load_config(cfg_path='config.yaml'):
    with open(cfg_path, 'r') as f:
        cfg = yaml.safe_load(f)
    return cfg

