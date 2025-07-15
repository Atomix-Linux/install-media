from textual.screen import Screen
from textual.widgets import Static, Input
from textual.app import ComposeResult
from config import save_config_section

class UserScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("👤 Enter username for your account:")
        yield Input(placeholder="e.g. mikolaj", id="username")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        username = event.value.strip()
        if username:
            save_config_section("user", {"name": username, "sudo": "yes"})
            from scripts.password import PasswordScreen
            await self.app.push_screen(PasswordScreen())
        else:
            self.query_one(Static).update("⚠️ Username cannot be empty.")
