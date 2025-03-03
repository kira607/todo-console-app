"""CLI selection menu."""

from typing import override

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Label


class SelectorApp(App[int]):
    """Simple CLI menu for selecting one of things from a list."""

    DEFAULT_CSS = """
    SelectorApp {
        background: green;
    }
    .selected {
        background: white;
        color: grey 80%;
    }
    .default {
        color: green;
    }
    """

    BINDINGS = [
        ("j", "select_next", "Select next item"),
        ("down", "select_next", "Select next item"),
        ("k", "select_prev", "Select previous item"),
        ("up", "select_prev", "Select previous item"),
        ("enter", "submit", "Sumbit selection"),
        ("q", "quit_selection", "Quit selection"),
    ]

    selected: reactive[int] = reactive(0)

    def __init__(self, options: list[str], prompt: str, default: int) -> None:
        super().__init__()
        self.options = options
        self.prompt = prompt
        self.default = default
        assert default >= -1, "Default value must be >= -1"
        self.set_reactive(SelectorApp.selected, max(default, 0))

    @override
    def compose(self) -> ComposeResult:
        yield Label(f"{self.prompt}:")
        for i, option in enumerate(self.options):
            classes = ""
            if i == self.selected:
                classes += " selected"
            if i == self.default:
                classes += " default"
            label = Label(option, id=f"item-{i}", classes=classes)
            yield label
        yield Footer(show_command_palette=False)

    def action_select_next(self) -> None:
        """Select next option."""
        if self.selected < len(self.options) - 1:
            self.selected += 1

    def action_select_prev(self) -> None:
        """Select previous option."""
        if self.selected > 0:
            self.selected -= 1

    def action_submit(self) -> None:
        """Submit selection."""
        self.exit(self.selected)

    def action_quit_selection(self) -> None:
        """Quit selection."""
        self.exit(None)

    def watch_selected(self, old: int, new: int) -> None:
        """Change options highliting when ``self.selected`` changes."""
        old_label: Label = self.query_one(f"#item-{old}")  # type: ignore
        if old == self.default:
            old_label.classes = "default"
        else:
            old_label.classes = ""

        new_label: Label = self.query_one(f"#item-{self.selected}")  # type: ignore
        if new == self.default:
            new_label.classes = "selected default"
        else:
            new_label.classes = "selected"


def select_menu(options: list[str], prompt: str = "Select an option", default: int = -1) -> str | None:
    """Open a selector menu.

    :param list[str] options: Options to select from.
    :param str prompt: Selection menu prompt, shown at the top, defaults to "Select an option"
    :param int default: Default option index, defaults to -1
    :return str | None: Selected option if selected, None otherwise.
    """
    result = SelectorApp(options, prompt, default).run(inline=False)
    if result is None:
        return None
    return options[result]
