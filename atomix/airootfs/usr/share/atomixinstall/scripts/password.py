# password_screen.py
from textual.screen import Screen
from textual.widgets import Static, Input
from textual.app import ComposeResult
from config import save_config_section

class PasswordScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("🔒 Enter password:")
        yield Input(password=True, placeholder="Password", id="password")
        yield Static("🔒 Confirm password:")
        yield Input(password=True, placeholder="Confirm Password", id="password_confirm")
        yield Static("")  # miejsce na komunikaty

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        password = self.query_one("#password", Input).value
        password_confirm = self.query_one("#password_confirm", Input).value

        if password != password_confirm:
            self.query_one(Static).update("⚠️ Passwords do not match, please try again.")
            return

        if not password:
            self.query_one(Static).update("⚠️ Password cannot be empty.")
            return

        # Dodaj bezpieczne hash’owanie jeśli chcesz

        
        save_config_section("user", {"password": password})

        from scripts.partitions import PartitioningChoiceScreen
        await self.app.push_screen(PartitioningChoiceScreen())
