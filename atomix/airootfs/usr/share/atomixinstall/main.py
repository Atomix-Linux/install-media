from textual.app import App, ComposeResult
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option
from textual.containers import Center
from textual.screen import Screen

from scripts.clean_start import CleanInstallScreen
from config import save_config_section

class ModeSelect(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Atomix Installer — Choose Installation Mode:")
        with Center():
            yield OptionList(
                Option("🧹 Clean Installation", id="clean"),
                Option("🔧 Repair Existing System", id="repair"),
            )

    async def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        save_config_section("install", {"type": event.option.id})
        if event.option.id == "clean":
            self.app.push_screen(CleanInstallScreen())
        else:
            self.app.exit("Repair mode not implemented yet")

class AtomixInstallApp(App):
    CSS_PATH = "styles.css"
    SCREENS = {
        "mode_select": ModeSelect,  # <-- KLASA, nie instancja
    }

    def on_mount(self) -> None:
        self.push_screen("mode_select")

if __name__ == "__main__":
    AtomixInstallApp().run()
