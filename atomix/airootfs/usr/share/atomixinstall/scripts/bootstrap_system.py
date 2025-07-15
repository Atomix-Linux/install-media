import subprocess

def bootstrap():
    try:
        subprocess.run(
        ["/usr/share/atomixinstall/scripts/bash_scripts/bootstrap.sh"],
        check=True,
        )
    except subprocess.CalledProcessError:
        print(f"ERROR")
