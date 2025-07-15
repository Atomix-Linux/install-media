from textual.screen import Screen
from textual.widgets import Static
from textual.app import ComposeResult
from textual.events import Key

from config import load_config
from .progress_bar import InstallProgressScreen
import asyncio

class SummaryScreen(Screen):
    def compose(self) -> ComposeResult:
        # Wczytujemy sekcje konfiguracji
        config = load_config()
        system_config = config.get("system", {})
        mode_config = config.get("install", {})
        partitioning_config = config.get("partitioning", {})
        user_config = config.get("user", {})

        # Przygotowujemy tekst podsumowania
        language = system_config.get("language", "unknown")
        keyboard_layout = system_config.get("keyboard_layout", "unknown")
        timezone = system_config.get("timezone", "unknown")
        hostname = system_config.get("hostname", "unknown")
        username = user_config.get("name", "unknown")
        mode = mode_config.get("type", "unknown")
        method = partitioning_config.get("method", "unknown")

        details = ""
        efi_details = "None"
        if method == "wipe":
            details = f"Wipe disk: {partitioning_config.get('wipe_disk', 'None')}"
        elif method == "select":
            details = f"Target partition: {partitioning_config.get('target_partition', 'None')}"
            efi_details = f"Target EFI partition: {partitioning_config.get('efi_partition', 'None')}"
        else:
            details = "No partitioning method selected."

        yield Static("📝 Installation Summary:")
        yield Static(f"Language: {language}")
        yield Static(f"Keyboard Layout: {keyboard_layout}")
        yield Static(f"Timezone: {timezone}")
        yield Static(f"Hostname: {hostname}")
        yield Static(f"Username: {username}")
        yield Static(f"Installation Mode: {mode}")
        yield Static(f"Partitioning method: {method}")
        yield Static(details)
        yield Static(efi_details)
        yield Static("\nPress ENTER to start installation... WARNING some partitions when you choose partiton selection, make sure you choosed right partitons before the installation...")

    async def on_key(self, event: Key) -> None:
        if event.key == "enter":
            await self.app.push_screen(MessageScreen("Starting installation in 5 seconds..."))
            await asyncio.sleep(5)
            await self.app.push_screen(InstallProgressScreen())
            #await self.app.exit("Installation started! (not implemented)")
            
class MessageScreen(Screen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Static(self.message)
