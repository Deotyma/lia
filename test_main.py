import os
import builtins
import types
import main
from unittest import mock

class FakeUsage:
    prompt_token_count = 12
    candidates_token_count = 34

class FakeResponse:
    usage_metadata = FakeUsage()
    text = "Ciao! Questo è un testo di esempio."

def test_main_file_exists():
    """Check that main.py exists in the current directory."""
    assert os.path.exists("main.py"), "main.py file not found!"
    assert os.path.isfile("main.py"), "main.py is not a regular file!"

def test_argument_mode(capsys, monkeypatch):
    # Mock Client and generate_content
    fake_client = mock.MagicMock()
    fake_client.models.generate_content.return_value = FakeResponse()
    monkeypatch.setenv("GEMINI_API_KEY", "AIzaFakeKeyForTests")
    monkeypatch.setattr(main.genai, "Client", mock.MagicMock(return_value=fake_client))

    # Simulate running main with args
    with mock.patch("sys.argv", ["main.py", "Italian A1 text, 1 paragraph(s), topic: dog."]):
        main.italianText()

    out, err = capsys.readouterr()
    assert "Prompt tokens:" in out
    assert "Response:" in out
    assert "Questo è un testo" in out
