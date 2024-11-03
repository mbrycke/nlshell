import configparser
import functools
import os

SETTINGS_FILE_PATH = os.path.expanduser("~/.config/nlshell/settings.ini")
DEFAULT_URL = "http://localhost:11434/v1"  # default url for local ollama
DEFAULT_MODEL = "qwen2.5-coder:7b"


@functools.lru_cache(maxsize=None)
def get_config(section, key):
    """
    Loads the configuration file and returns the 'disable_warning' setting.
    The cache is cleared when the `set_config` function is called.
    """
    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE_PATH)
    return config.get(section, key, fallback=None)


def set_config(section, key, value):
    """
    Create a new configuration file if it doesn't exist, then add the setting.
    And clear the cache for the `get_config` function.
    """

    get_config.cache_clear()

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(SETTINGS_FILE_PATH), exist_ok=True)

    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE_PATH)
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)
    with open(SETTINGS_FILE_PATH, "w") as f:
        config.write(f)


def handle_warning_message():
    """Displays a warning unless it's disabled in the settings."""
    if not get_config("default", "disable_warning"):
        # print in red color
        print(
            "\033[91m"
            + "WARNING: Using the genereated command can cause serious harm. Never run a command you are not 100% sure of what it will do."
            + "\033[0m"
        )
        print("Disable this warning by running 'c --disable-warning'")


def get_base_url():
    """
    Retrieve the base url from the settings file.
    If the base url is not set, get input from the user.
    """

    base_url = get_config("default", "base_url")
    if not base_url:
        base_url = input(
            f"Base URL for LLM is not set. \nEnter the base url for the API (default {DEFAULT_URL} (local ollama)): "
        )
        if not base_url:
            base_url = DEFAULT_URL
        set_config("default", "base_url", base_url)
    return base_url


def get_model():
    """
    Retrieve the model from the settings file.
    If the model is not set, get input from the user.
    """

    model = get_config("default", "model")
    if not model:
        model = input(
            f"Model for LLM is not set. \nEnter the model for the API: (default {DEFAULT_MODEL}): "
        )
        if not model:
            model = DEFAULT_MODEL
        set_config("default", "model", model)
    return model


def get_api_key():
    """
    Retrieve the API key from the settings file.
    If the API key is not set, get input from the user.
    """

    api_key = get_config("default","api_key")
    if not api_key:
        api_key = input(
            f"API key for OpenAI is not set. \nEnter the API key for the API: "
        )
        set_config("default","api_key",api_key)
    return api_key
