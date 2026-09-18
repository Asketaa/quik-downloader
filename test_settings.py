#!/usr/bin/env python3
"""Checks for settings persistence. Run: python test_settings.py"""

import os
import tempfile

from quik_downloader.core.file_handler import BASE_DIR, FileHandler
from quik_downloader.ui.settings_manager import SettingsManager


def _handler_using(path):
    """A FileHandler that reads and writes the given settings file."""
    handler = FileHandler()
    handler.settings_file = path
    return handler


def test_normalize_directory():
    """Quotes, environment variables and '~' must be resolved, not stored verbatim."""
    os.environ['QUIK_TEST_DIR'] = os.path.join('C:' + os.sep, 'Videos')

    # Windows Explorer's "Copy as path" wraps the path in double quotes
    assert FileHandler.normalize_directory('"/tmp/my videos"') == '/tmp/my videos'
    assert FileHandler.normalize_directory("'/tmp/my videos'") == '/tmp/my videos'
    # Environment variables and '~' must expand, or a literal folder gets created
    assert FileHandler.normalize_directory('%QUIK_TEST_DIR%') == os.environ['QUIK_TEST_DIR']
    assert FileHandler.normalize_directory('~') == os.path.expanduser('~')
    # A plain path is left alone
    assert FileHandler.normalize_directory('  ./downloads  ') == './downloads'


def test_settings_round_trip():
    """Saved settings must read back identically, including a literal '%'."""
    with tempfile.TemporaryDirectory() as tmp:
        handler = _handler_using(os.path.join(tmp, 'settings.ini'))
        # A '%' in a folder name is not config interpolation syntax
        wanted = os.path.join(tmp, '100% Done')

        assert handler.write_settings(dict(handler.default_settings,
                                           download_directory=wanted))
        assert handler.read_settings()['download_directory'] == wanted


def test_paths_are_anchored_to_project():
    """The app must find its own files regardless of the working directory."""
    cwd = os.getcwd()
    os.chdir(tempfile.gettempdir())
    try:
        handler = FileHandler()
        assert handler.settings_file == os.path.join(BASE_DIR, 'settings.ini')
        assert handler.urls_file == os.path.join(BASE_DIR, 'URLs.txt')
        assert os.path.isabs(handler.default_settings['download_directory'])
    finally:
        os.chdir(cwd)


def test_edit_is_saved_without_a_separate_save_step():
    """A changed setting hits disk immediately, and rolls back if the write fails."""
    # Built without __init__ so the test never touches the real settings.ini
    manager = SettingsManager.__new__(SettingsManager)

    with tempfile.TemporaryDirectory() as tmp:
        manager.file_handler = _handler_using(os.path.join(tmp, 'settings.ini'))
        manager.settings = dict(manager.file_handler.default_settings)

        assert manager._apply('video_quality', 'low')
        assert manager.file_handler.read_settings()['video_quality'] == 'low'

        # An unwritable target must leave the in-memory value untouched
        print("  (the save errors below are expected - testing the failure path)")
        manager.file_handler.settings_file = tmp  # a directory, so the write fails
        assert not manager._apply('video_quality', 'high')
        assert manager.settings['video_quality'] == 'low'


if __name__ == '__main__':
    test_normalize_directory()
    test_settings_round_trip()
    test_paths_are_anchored_to_project()
    test_edit_is_saved_without_a_separate_save_step()
    print("All settings tests passed.")
