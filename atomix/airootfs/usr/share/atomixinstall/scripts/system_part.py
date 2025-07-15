from config import load_config
import subprocess

def list_type():
    config = load_config()
    partitioning_config = config.get("partitioning", {})
    method = partitioning_config.get("method", "unknown")
    if method == "wipe":
        disk_to_wipe = partitioning_config.get('wipe_disk', None)
        try:
            subprocess.run(
                ["/usr/share/atomixinstall/scripts/bash_scripts/wipe.sh", disk_to_wipe],
                 check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {e.returncode}")
    elif method == "select":
        efi_part = partitioning_config.get('efi_partition', None)
        target_part = partitioning_config.get('target_partition', None)
        try:
            subprocess.run(
                ["/usr/share/atomixinstall/scripts/bash_scripts/part.sh", target_part, efi_part],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {e.returncode}")
            
