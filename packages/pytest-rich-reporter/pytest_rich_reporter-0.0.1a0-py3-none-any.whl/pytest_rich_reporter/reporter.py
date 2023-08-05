from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from _pytest.terminal import TerminalReporter
from rich.panel import Panel
from rich.text import Text

from . import __version__ as package_version

if TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.main import Session
    from rich.console import Console


class RichReporter(TerminalReporter):
    """
    Terminal Reporter Plugin that uses Rich for terminal output

    :param config: The pytest config object
    """

    def __init__(self, config: Config, console: Console):
        super().__init__(config)
        self.console = console

    @pytest.hookimpl(trylast=True)
    def pytest_sessionstart(self, session: Session):
        """
        Called before the test session starts

        :param session: The pytest session object
        """
        panel = Panel(
            Text(
                "A pytest plugin using Rich for beautiful test result formatting.",  # noqa: E501
                justify="center",
            ),
            style="bold green",
            padding=2,
            title="pytest-rich-reporter",
            subtitle=f"v{package_version}",
        )
        self.console.print(panel)

        super().pytest_sessionstart(session)

    def summary_failures(self) -> None:
        if self.config.option.tbstyle == "no":
            return

        reports = self.getreports("failed")
        if not reports:
            return

        self.console.rule("FAILURES", style="white")

        for rep in reports:
            if self.config.option.tbstyle == "line":
                line = self._getcrashline(rep)
                self.console.print(line)
            else:
                msg = self._getfailureheadline(rep)
                self.console.rule(msg, style="bold red")
                self._outrep_summary(rep)
                self._handle_teardown_sections(rep.nodeid)
