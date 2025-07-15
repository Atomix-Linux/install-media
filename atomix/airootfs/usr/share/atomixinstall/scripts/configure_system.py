from config import load_config
import subprocess

def configure():
    config = load_config()
    user_config = config.get("user", {})
    system_config = config.get("system", {})
    lang = system_config.get("language", "unknown")
    lang_code = system_config.get("language_code", "unknown")
    keys = system_config.get("keyboard_layout", "unknown")
    timezone = system_config.get("timezone", "unknown")
    hostname = system_config.get("hostname", "unknown")
    user = user_config.get("name", "unknown")
    password = user_config.get("password", "unknown")
    try:
        subprocess.run(
            ["/usr/share/atomixinstall/scripts/bash_scripts/configure.sh", user, password, timezone, lang, hostname, keys, lang_code],
            check=True,
            )
    except subprocess.CalledProcessError:
        print(f"Error")
