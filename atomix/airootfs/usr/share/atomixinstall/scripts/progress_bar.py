from textual.screen import Screen
from textual.widgets import ProgressBar, Static
from textual.app import ComposeResult
from textual.reactive import reactive
import asyncio

# Import etapów instalacji
from .system_part import list_type
from .mount import mount
from .download_system import download_split_files
from .bootstrap_system import bootstrap
from .configure_system import configure
from .bootloader import bootloader_install
# Możesz dodać kolejne: mounting, user_setup, itd.

class InstallProgressScreen(Screen):
    progress = reactive(0)

    def compose(self) -> ComposeResult:
        self.status = Static("Starting installation...")
        self.bar = ProgressBar(total=100)
        yield self.status
        yield self.bar

    async def on_mount(self) -> None:
        steps = [
            ("Partitioning disks...", list_type),
            ("Mounting partitions...", mount),
            ("Downloading Atomix Linux image...", lambda: download_split_files("unstable")),
            ("Bootstraping system image...", bootstrap),
            ("Configuring system...", configure),
            ("Installing Bootloader...", bootloader_install),
            # ("Install base system", install_base),
            # itd...
        ]

        step_count = len(steps)
        for index, (name, func) in enumerate(steps):
            self.status.update(f"▶️ {name}...")
            try:
                result = func()  # lub `await func()` jeśli async
            except Exception as e:
                self.status.update(f"❌ Error in {name}: {e}")
                return

            # Aktualizacja paska postępu
            self.progress = int((index + 1) / step_count * 100)
            self.bar = self.progress
            await asyncio.sleep(0.5)  # opcjonalnie: daj użytkownikowi widoczny postęp

        self.status.update("✅ Installation complete! Now please reboot system.")
        await asyncio.sleep(2)
        await self.app.exit("Done")
