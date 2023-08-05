from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from .console import console
from .reporter import RichReporter

if TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.config.argparsing import Parser


def pytest_addoption(parser: Parser):
    """
    Add options to the pytest command line for the rich plugin

    :param parser: The pytest command line parser
    """
    group = parser.getgroup("rich")
    group.addoption(
        "--rich",
        action="store_true",
        dest="rich",
        default=False,
        help="Enable rich output for the terminal reporter (default: False)",
    )


@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config):
    """
    Configure the rich plugin

    :param config: The pytest config object
    """
    use_rich = getattr(config.option, "rich", False)

    if use_rich:
        standard_reporter = config.pluginmanager.get_plugin("terminalreporter")
        rich_reporter = RichReporter(config, console)

        config.pluginmanager.unregister(standard_reporter)
        config.pluginmanager.register(rich_reporter, "terminalreporter")
