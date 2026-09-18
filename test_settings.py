#!/usr/bin/env python3
"""Round-trip checks for settings persistence. Run: python test_settings.py"""

import os
import tempfile

from quik_downloader.core.file_handler import FileHandler


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
        cwd = os.getcwd()
        os.chdir(tmp)
        try:
            handler = FileHandler()
            # A '%' in a folder name is not config interpolation syntax
            wanted = os.path.join(tmp, '100% Done')
            settings = dict(handler.default_settings, download_directory=wanted)

            assert handler.write_settings(settings), "write_settings reported failure"
            assert handler.read_settings()['download_directory'] == wanted
        finally:
            os.chdir(cwd)


if __name__ == '__main__':
    test_normalize_directory()
    test_settings_round_trip()
    print("All settings tests passed.")
