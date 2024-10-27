# Command Genie

A very small Python package that generates shell commands from a "natural language" description.
It will provide a explanation of the command and prefill the command line with the generated command.

Useses an LLM model to generate the shell commands.

### _IMPORTANT! Never run a generated command without understanding what it does. The generated command may be harmful. There is no guarantee whatsoever that what the LLM suggests is correct! DON'T BLINDLY TRUST THE GENERATED SUGGESTION!_

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Installation

Instructions on how to install your package. Include both the pip and poetry methods.

```bash
# Using pip
pip install command-geni

# Using poetry
poetry add command-geni

```

## Usage

Activate the virtual environment where the package is installed to use the command-genie command.


### Set the base_url
The package uses the openai client to call an LLM. By specifying a `base_url` you can use your own model, e.g. a local model.


### Create a command
```shell
c list all files in the current directory, including hidden files
```
where c is the command-genie command.
This command will generate a response like this:
```text
The 'ls' command lists directory contents. The option '-l' provides a long listing format which includes file permissions, number of links, owner, group, size, and time of last modification. The '-a' option ensures hidden files (those starting with a dot .) are also listed.
$ ls -la
```

```shell
c --base_url http://localhost:8000 
```
If no `base_url` is explicitly set, the package will ask which url to use.

### Set the api_key
```shell
c --api_key "your-api-key"
```
Even if you run a local model you need to set an api_key since the openai client requires it, even if the key is just a dummy key.

### Set the model

```shell
c --model_name "qwen2.5-coder:7b
```
If no model is specified the package will ask which model to use.



## License
Distributed under the MIT License. See `LICENSE` for more information.      

## Contact

Mattias Brycke -  [LinkedIn](https://www.linkedin.com/in/mattias-brycke-0b3b1b1b/)