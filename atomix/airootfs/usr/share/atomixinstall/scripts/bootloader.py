import subprocess

def bootloader_install():
    try:
        subprocess.run(
            ["/usr/share/atomixinstall/scripts/bash_scripts/bootloader.sh"],
            check=True,
            )
    except subprocess.CalledProcessError:
        print(f"ERROR")
