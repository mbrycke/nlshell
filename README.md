# nlshell

A very small Python package that generates shell commands from a "natural language" description.
It will provide a explanation of the command and prefill the command line with the generated command.

You must provide a url to an openai compatible api, e.g. a local model served by e.g. Ollama, or a remote model.

**⚠️ IMPORTANT! Never run a generated command without understanding what it does. The generated command may be harmful. There is no guarantee whatsoever that what the LLM suggests is correct! DON'T BLINDLY TRUST THE GENERATED SUGGESTION!**

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
    - [Set the base_url](#set-the-base_url)
    - [Create a command](#create-a-command)
    - [Set the api_key](#set-the-api_key)
    - [Set the model](#set-the-model)
    - [Use from any environment](#use-from-any-environment)
- [License](#license)
- [GitHub](#github)

## Installation

Instructions on how to install your package. Include both the pip and poetry methods.

```bash
# Using pip
pip install nlshell

# Using poetry
poetry add nlshell

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

### Set the api_key

```shell
c --api-key your-api-key
```

Even if you run a local model you need to set an api_key since the openai client requires it, even if the key is just a dummy key.

### Set the model

```shell
c --model-name qwen3:8b
```

If no model is specified the package will ask which model to use.

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
