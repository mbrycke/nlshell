# nlshell

A very small Python package that generates shell commands from a "natural language" description.
It will provide a explanation of the command and prefill the command line with the generated command.

You must provide a url to an openai compatible api, e.g. a local model served by e.g. Ollama, or a remote model.

**⚠️ IMPORTANT! Never run a generated command without understanding what it does. The generated command may be harmful. There is no guarantee whatsoever that what the LLM suggests is correct! DON'T BLINDLY TRUST THE GENERATED SUGGESTION!**

## Table of Contents

- [Installation](#installation)
- [Development](#development)
- [Usage](#usage)
  - [Set the base_url](#set-the-base_url)
  - [Create a command](#create-a-command)
  - [Set the API key](#set-the-api-key)
  - [Set the model](#set-the-model)
  - [Switch between local and open-router models](#switch-between-local-and-open-router-models)
  - [Use from any environment](#use-from-any-environment)
- [License](#license)
- [GitHub](#github)

## Installation

Install `nlshell` from PyPI with either `pip` or `uv`.

```bash
# Using pip
pip install nlshell

# Using uv
uv tool install nlshell

```

## Development

To run the test suite with the project-managed environment:

```bash
uv sync --group dev
uv run pytest -q
```

## Usage

Activate the virtual environment where the package is installed to use the nlshell command.

### Set the base_url

The package uses the openai client to call an LLM. By specifying a `base-url` you can use your own model, e.g. a local model.

```shell
c --base-url http://localhost:11434/v1
```

If no `base_url` is explicitly set, the package will ask which url to use.

### Create a command

```shell
c list all files in the current directory, including hidden files
```

where c is the nlshell command.
This command will generate a response like this:

```text
The 'ls' command lists directory contents. The option '-l' provides a long listing format which includes file permissions, number of links, owner, group, size, and time of last modification. The '-a' option ensures hidden files (those starting with a dot .) are also listed.
$ ls -la
```

### Set the API key

```shell
export NLSHELL_API_KEY="your-api-key"
```

The API key is read from the `NLSHELL_API_KEY` environment variable only.
It is not stored in `~/.config/nlshell/settings.ini`.

Even if you run a local model you may need to set an API key since the OpenAI client requires one, even if the key is just a dummy value.

### Set the model

```shell
c --set-model qwen3:8b
```

If no model is specified the package will ask which model to use.

### Switch between local and open-router models

You can easily switch between using a local model (via Ollama) or an open-router remote model:

```shell
# Use local model
c --use-local

# Use open-router remote model
c --use-open-router
```

The setting is saved to `~/.config/nlshell/settings.ini` and persists between sessions. Defaults to local mode.

### Use from any environment

If you have installed the package in a virtual environment you can use it from any environment by adding a simple shell script to e.g. `~/.local/bin`:

1. Create a file `~/.local/bin/c` with the following content:

    ```shell
    #!/bin/bash
    # Activate the venv and run the command from it
    source /path/to/your/environment/.venv/bin/activate
    exec c "$@"
    ```

2. Make the script executable:

    ```shell
    chmod +x ~/.local/bin/c
    ```

Now you can use the `c` command from any terminal session.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## GitHub

[https://github.com/mbrycke/nlshell](https://github.com/mbrycke/nlshell)
