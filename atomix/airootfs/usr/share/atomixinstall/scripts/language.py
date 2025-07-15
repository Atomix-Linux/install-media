from textual.screen import Screen
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option
from textual.app import ComposeResult
from config import save_config_section
from babel import Locale


class LanguageScreen(Screen):
    def compose(self) -> ComposeResult:
        header_lines, locale_lines = load_locale_gen_with_header()

        # Wyświetlamy nagłówek jako statyczny tekst (zachowany komentarz)
        yield Static("\n".join(header_lines), id="locale-header")

        # Tworzymy listę opcji na podstawie wszystkich linii z locale.gen (zakomentowanych i nie)
        options = []
        for line in locale_lines:
            stripped = line.strip()
            if not stripped:
                continue
            # Dla linii zaczynających się od # to jest zakomentowane, usuwamy #
            is_commented = stripped.startswith("#")
            locale_code = stripped[1:].strip().split()[0] if is_commented else stripped.split()[0]

            # Pokazujemy nazwę z babel (na podstawie części przed kropką)
            display_name = locale_code_to_display_name(locale_code.split('.')[0])

            label = f"{display_name} — {line}"
            # ID opcji to dokładna linia (żeby wiedzieć którą wybrał)
            options.append(Option(label, id=line))

        yield OptionList(*options)

    async def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        # Zapisujemy do configu wybraną linię z locale.gen (np. 'pl_PL.UTF-8 UTF-8' odkomentowaną)
        chosen_line = event.option.id

        # Jeśli linia była zakomentowana (#), to ją odkomentowujemy przy zapisie
        if chosen_line.strip().startswith("#"):
            chosen_line = chosen_line.lstrip("#").strip()

        locale_code = chosen_line.split()[0]

        save_config_section("system", {"language": chosen_line})
        save_config_section("system", {"language_code": locale_code})

        # Przechodzimy do następnego ekranu (np. wyboru klawiatury)
        from scripts.keyboard import KeyboardScreen
        await self.app.push_screen(KeyboardScreen())


def load_locale_gen_with_header():
    header_lines = []
    locale_lines = []

    try:
        with open("/etc/locale.gen", "r", encoding="utf-8") as f:
            in_header = True
            for line in f:
                if in_header:
                    if line.startswith("#") or line.strip() == "":
                        header_lines.append(line.rstrip('\n'))
                    else:
                        in_header = False
                        locale_lines.append(line.rstrip('\n'))
                else:
                    locale_lines.append(line.rstrip('\n'))
    except FileNotFoundError:
        pass
    return header_lines, locale_lines


def locale_code_to_display_name(locale_code: str) -> str:
    try:
        loc = Locale.parse(locale_code)
        return loc.get_display_name(loc).capitalize()
    except Exception:
        return locale_code
