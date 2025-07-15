import configparser
import os

CONFIG_PATH = "/tmp/atomixinstall.config"

def load_config() -> dict:
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        return {}
    config.read(CONFIG_PATH)
    # konwersja ConfigParser na zwykły dict
    result = {section: dict(config[section]) for section in config.sections()}
    return result

def save_config_section(section: str, data: dict):
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH)
    if section not in config.sections():
        config.add_section(section)
    for key, value in data.items():
        config.set(section, key, str(value))
    with open(CONFIG_PATH, "w") as f:
        config.write(f)

