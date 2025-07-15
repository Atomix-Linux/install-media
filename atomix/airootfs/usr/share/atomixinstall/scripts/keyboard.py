from textual.screen import Screen
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option
from textual.app import ComposeResult
from config import save_config_section
import subprocess

class KeyboardScreen(Screen):
    def get_keymaps(self):
        try:
            # Pobranie listy układów klawiatury z localectl
            result = subprocess.run(["localectl", "list-keymaps"], capture_output=True, text=True, check=True)
            keymaps = result.stdout.splitlines()
            return keymaps
        except Exception:
            # Jeśli błąd, zwróć domyślne
            return ["us", "pl"]

    def compose(self) -> ComposeResult:
        yield Static("⌨️ Choose keyboard layout:")
        keymaps = self.get_keymaps()
        options = [Option(km, id=km) for km in keymaps]
        yield OptionList(*options)

    async def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        save_config_section("system", {"keyboard_layout": event.option.id})
        from scripts.timezone import TimezoneScreen
        await self.app.push_screen(TimezoneScreen())
