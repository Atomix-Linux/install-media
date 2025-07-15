import subprocess

def mount():
    try:
        subprocess.run(
        ["/usr/share/atomixinstall/scripts/bash_scripts/mount.sh"],
        check=True,
    )
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.returncode}")
