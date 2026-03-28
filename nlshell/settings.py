import configparser
import functools
import os

"""example settings.ini file:

[open-router]
base_url = https://openrouter.ai/api/v1/
model = openai/gpt-oss-120b

[ollama-local]
base_url = http://localhost:11434/v1
model = hopephoto/Qwen3-4B-Instruct-2507_q8

[default]
model_mode = open-router

"""

SETTINGS_FILE_PATH = os.path.expanduser("~/.config/nlshell/settings.ini")
DEFAULT_URL = "http://localhost:11434/v1"  # default url for local ollama
DEFAULT_MODEL = "qwen3:8b"


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


def get_base_url(model_mode="ollama-local"):
    """
    Retrieve the base url from the settings file based on model mode.
    If the base url is not set, get input from the user.
    """
    if model_mode == "ollama-local":
        config_section = "ollama-local"
    else:
        config_section = "open-router"

    base_url = get_config(config_section, "base_url")
    if not base_url:
        base_url = input(
            f"Base URL for LLM is not set. \nEnter the base url for the API (default {DEFAULT_URL} (local ollama)): "
        )
        if not base_url:
            base_url = DEFAULT_URL
        set_config(config_section, "base_url", base_url)
    return base_url


def get_model(model_mode):
    """
    Retrieve the model from the settings file based on model mode.
    If the model is not set, get input from the user.
    """
    if model_mode == "ollama-local":
        config_section = "ollama-local"
    elif model_mode == "open-router":
        config_section = "open-router"
    else:
        raise ValueError(f"Invalid model mode: {model_mode}")

    model = get_config(config_section, "model")
    if not model:
        model = input(
            f"Model for LLM is not set. \nEnter the model for the API: (default {DEFAULT_MODEL}): "
        )
        if not model:
            model = DEFAULT_MODEL
        set_config(config_section, "model", model)
    return model


def get_model_mode():
    """
    Get the current model mode (local or open-router) from settings.
    Defaults to 'local' if not set.
    """
    mode = get_config("default", "model_mode")
    if not mode:
        mode = "ollama-local"
    return mode


def get_api_key():
    """
    Retrieve API key from environment variable only.
    """
    api_key = os.environ.get("NLSHELL_API_KEY")
    if not api_key:
        raise ValueError(
            "NLSHELL_API_KEY is not set. Please export NLSHELL_API_KEY in your shell environment."
        )
    return api_key
