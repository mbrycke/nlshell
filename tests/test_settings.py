import pytest
from unittest.mock import patch, MagicMock
from nlshell.main import (
    extract_json_content,
    generate_command,
    prefill_input,
    add_to_history,
)
from nlshell.settings import set_config, get_base_url, get_model, get_api_key
import nlshell
import nlshell.settings
import readline
from unittest import mock

# Mocking OpenAI client for testing
class MockOpenAIClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def chat(self, model, messages):
        class MockResponse:
            def __init__(self):
                self.choices = [{"message": {"content": '```json\n{"command": "ls", "explanation": "List files"}\n```'}}]
        return MockResponse()

# Test extract_json_content
def test_extract_json_content():
    markdown_with_json = """
    Some text before
    ```json
    {"key": "value"}
    ```
    Some text after
    """
    assert extract_json_content(markdown_with_json) == '{"key": "value"}'

# Test generate_command
def test_generate_command():
    api_key=get_api_key()
    url=nlshell.settings.DEFAULT_URL
    model=nlshell.settings.DEFAULT_MODEL
    test_generated_text= generate_command("list all files in the current directory", url, model, api_key)

    # check that it returns a dictionary with the correct keys (command and explanation)
    assert "command" in test_generated_text
    assert "explanation" in test_generated_text

# # Test prefill_input
# def test_prefill_input():
#     with patch("readline.insert_text") as mock_insert_text:
#         # with patch("readline.set_startup_hook") as mock_set_startup_hook:
#             with patch("builtins.input") as mock_input:
#                 mock_input.return_value = "command"
#                 assert prefill_input("command") == "$ "
#                 mock_insert_text.assert_called_with("command")
#                 # mock_set_startup_hook.assert_called()




# Assuming the function is defined in a module named `your_module`

def test_prefill_input():
    # Define the text to prefill
    prefill_text = "test_prefill"

    # Mock `readline` methods and `input`
    with mock.patch("readline.insert_text") as mock_insert_text, \
         mock.patch("readline.set_startup_hook") as mock_set_hook, \
         mock.patch("builtins.input", return_value="user_input") as mock_input:

        # Call the function with the prefill text
        result = prefill_input(prefill_text)

        # Verify the hook is set with the correct prefill text
        mock_insert_text.assert_called_once_with(prefill_text)
        mock_set_hook.assert_called()
        
        # Confirm `input` returned the expected output
        assert result == "user_input"

        # Ensure the startup hook was reset after calling the function
        mock_set_hook.assert_called_with()





# Test add_to_history
def test_add_to_history():
    with patch("readline.add_history") as mock_add_history:
        with patch("builtins.open", MagicMock()) as mock_open:
            add_to_history("command")
            mock_add_history.assert_called_with("command")
            # mock_open.assert_called_with("/home/user/.bash_history", "a")

    
