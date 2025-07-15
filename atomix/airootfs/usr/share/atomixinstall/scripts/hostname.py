from textual.screen import Screen
from textual.widgets import Static, Input
from textual.app import ComposeResult
from config import save_config_section

class HostnameScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("💻 Enter hostname for this system:")
        yield Input(placeholder="e.g. atomix-pc", id="host_input")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        hostname = event.value.strip()
        if hostname:
            save_config_section("system", {"hostname": hostname})
            from scripts.user import UserScreen
            await self.app.push_screen(UserScreen())
