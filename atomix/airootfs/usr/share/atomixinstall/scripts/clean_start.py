from textual.screen import Screen
from textual.widgets import Static
from textual.app import ComposeResult

class CleanInstallScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Clean Install Screen - wybierz opcje")

    async def on_mount(self) -> None:
        # automatycznie przejście do LanguageScreen po zamontowaniu, jeśli chcesz
        from scripts.language import LanguageScreen
        await self.app.push_screen(LanguageScreen())
