import yaml
import os

def load_config(config_path="config.yaml"):
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()

def get_api_key(service):
    return CONFIG.get("api_keys", {}).get(service, "")
