from textual.screen import Screen
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option
from textual.containers import Center
from textual.app import ComposeResult

import subprocess
import json

from config import save_config_section  # import funkcji zapisu konfiguracji


def get_disks():
    result = subprocess.run(
        ["lsblk", "-d", "-o", "NAME,SIZE,MODEL,TYPE", "-J"],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(result.stdout)
    disks = []
    for device in data["blockdevices"]:
        if device.get("type") == "disk":
            label = f"/dev/{device['name']} - {device['size']} - {device.get('model', '').strip()}"
            disks.append({"id": f"/dev/{device['name']}", "label": label})
    return disks


def get_partitions():
    result = subprocess.run(
        ["lsblk", "-o", "NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT", "-J"],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(result.stdout)
    partitions = []
    for device in data["blockdevices"]:
        if device.get("type") == "disk":
            for child in device.get("children", []):
                if child.get("type") == "part":
                    label = f"/dev/{child['name']} - {child['size']} - {child.get('fstype', 'unknown')}"
                    partitions.append({"id": f"/dev/{child['name']}", "label": label})
    return partitions


class WipeDiskScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("🧹 Select disk to wipe (this will erase all data!):")
        with Center():
            disks = get_disks()
            if not disks:
                yield Static("No disks found.")
            else:
                options = [Option(disk["label"], id=disk["id"]) for disk in disks]
                yield OptionList(*options)

    async def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        selected_disk = event.option.id
        save_config_section("partitioning", {"method": "wipe", "wipe_disk": selected_disk})
        from scripts.summary import SummaryScreen
        await self.app.push_screen(SummaryScreen())


class PartitionSelectScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("📂 Select partition to install the system on:")
        with Center():
            partitions = get_partitions()
            if not partitions:
                yield Static("No partitions found.")
            else:
                options = [Option(part["label"], id=part["id"]) for part in partitions]
                yield OptionList(*options, id="system_partition_list")

    async def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        selected_system = event.option.id
        save_config_section("partitioning", {"target_partition": selected_system})

        # Przechodzimy do wyboru EFI
        self.app.push_screen(EfiPartitionSelectScreen())

class EfiPartitionSelectScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("🧩 Select EFI partition (for /boot/efi):")
        with Center():
            partitions = get_partitions()
            if not partitions:
                yield Static("No partitions found.")
            else:
                options = [Option(part["label"], id=part["id"]) for part in partitions]
                yield OptionList(*options, id="efi_partition_list")

    async def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        selected_efi = event.option.id
        save_config_section("partitioning", {"efi_partition": selected_efi})
        from scripts.summary import SummaryScreen
        await self.app.push_screen(SummaryScreen())



class PartitioningChoiceScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("🛠️ Choose partitioning method:")
        with Center():
            yield OptionList(
                Option("Wipe entire disk", id="wipe"),
                Option("Select partition", id="select"),
            )

    async def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option.id == "wipe":
            save_config_section("partitioning", {"method": "wipe"})
            await self.app.push_screen(WipeDiskScreen())
        elif event.option.id == "select":
            save_config_section("partitioning", {"method": "select"})
            await self.app.push_screen(PartitionSelectScreen())
