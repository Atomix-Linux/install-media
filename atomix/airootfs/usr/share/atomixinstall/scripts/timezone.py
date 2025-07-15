from textual.screen import Screen
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option
from textual.app import ComposeResult
from config import save_config_section
from zoneinfo import available_timezones

class TimezoneScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("🕓 Choose your timezone:")

        timezones = sorted(available_timezones())
        options = [Option(tz, id=tz) for tz in timezones]

        yield OptionList(*options, id="tz_list")

    async def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        save_config_section("system", {"timezone": event.option.id})
        from scripts.hostname import HostnameScreen
        await self.app.push_screen(HostnameScreen())
