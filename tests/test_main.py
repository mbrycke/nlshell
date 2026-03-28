from types import SimpleNamespace
from unittest.mock import mock_open, patch

import nlshell.main as main


def test_extract_json_content_from_markdown_block():
    markdown_with_json = """
	Some text before
	```json
	{"key": "value"}
	```
	Some text after
	"""

    assert main.extract_json_content(markdown_with_json) == '{"key": "value"}'


def test_extract_json_content_without_markdown_returns_single_line():
    assert main.extract_json_content('{\n"key": "value"\n}') == '{"key": "value"}'


def test_generate_command_returns_parsed_json():
    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content='{"command": "ls", "explanation": "List files"}'
                )
            )
        ]
    )
    client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **_: response))
    )

    with patch.object(main, "OpenAI", return_value=client) as openai_ctor:
        result = main.generate_command(
            "list all files in the current directory",
            "http://localhost:11434/v1",
            "qwen3:8b",
            api_key="test-key",
        )

    openai_ctor.assert_called_once_with(
        api_key="test-key", base_url="http://localhost:11434/v1"
    )
    assert result == {"command": "ls", "explanation": "List files"}


def test_input_with_prefill_uses_prompt_default():
    with patch.object(main, "prompt", return_value="echo test") as prompt_mock:
        result = main.input_with_prefill("$ ", prefill="ls -la")

    prompt_mock.assert_called_once_with("$ ", default="ls -la")
    assert result == "echo test"


def test_add_to_history_updates_readline_and_history_file():
    with (
        patch.object(main.readline, "add_history") as add_history_mock,
        patch.object(main.os.path, "expanduser", return_value="/tmp/.bash_history"),
        patch("builtins.open", mock_open()) as open_mock,
    ):
        main.add_to_history("echo test")

    add_history_mock.assert_called_once_with("echo test")
    open_mock.assert_called_once_with("/tmp/.bash_history", "a")
    open_mock().write.assert_called_once_with("echo test\n")


def test_main_retries_until_valid_command():
    responses = [None, {"command": "echo ok", "explanation": "prints ok"}]

    with (
        patch.object(main, "get_model_mode", return_value="ollama-local"),
        patch.object(main, "handle_warning_message"),
        patch.object(main, "get_base_url", return_value="http://example.invalid/v1"),
        patch.object(main, "get_model", return_value="dummy-model"),
        patch.object(main, "get_api_key", return_value="dummy-key"),
        patch.object(main, "generate_command", side_effect=responses) as generate_mock,
        patch.object(main, "input_with_prefill", return_value="echo ok") as input_mock,
        patch.object(main.os, "system", return_value=0) as system_mock,
        patch.object(main, "add_to_history") as history_mock,
        patch("sys.argv", ["c", "say", "hello"]),
    ):
        main.main()

    assert generate_mock.call_count == 2
    input_mock.assert_called_once_with("$ ", prefill="echo ok")
    system_mock.assert_called_once_with("echo ok")
    history_mock.assert_called_once_with("echo ok")


def test_main_exits_cleanly_when_api_key_missing():
    with (
        patch.object(main, "get_model_mode", return_value="ollama-local"),
        patch.object(main, "handle_warning_message"),
        patch.object(main, "get_base_url", return_value="http://example.invalid/v1"),
        patch.object(main, "get_model", return_value="dummy-model"),
        patch.object(
            main, "get_api_key", side_effect=ValueError("NLSHELL_API_KEY is not set")
        ),
        patch.object(main, "generate_command") as generate_mock,
        patch("sys.argv", ["c", "say", "hello"]),
    ):
        main.main()

    generate_mock.assert_not_called()
