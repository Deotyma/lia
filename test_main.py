import os

def test_main_file_exists():
    """Check that main.py exists in the current directory."""
    assert os.path.exists("main.py"), "main.py file not found!"
    assert os.path.isfile("main.py"), "main.py is not a regular file!"
