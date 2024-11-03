import argparse
import json
import openai
import os
import pydantic
import readline
from openai import OpenAI
from pydantic import BaseModel
from nlshell.settings import (
    handle_warning_message,
    set_config,
    get_base_url,
    get_model,
    get_api_key,
)

N_GENERATION_ATTEMPTS = 3


class Command(BaseModel):
    command: str
    explanation: str


def extract_json_content(s):
    if "```json" not in s:
        # if markdown json  not present, return the whole string
        return s.replace("\n", "")

    # Find the start and end indices for the markdown JSON content
    start_index = s.find("```json") + len("```json\n")
    end_index = s.rfind("```")
    return s[start_index:end_index].strip().replace("\n", "")


# TODO: implement `return_format` when available
def generate_command(prompt, url, model="qwen2.5-coder:7b", api_key="abc123"):
    """
    Use the OpenAI client to generate a command.

    Args:
        prompt (str): The description of the command to generate.
        url (str): The URL of the OpenAI API.

    Returns:
        dict: A dictionary containing the generated command and an explanation.
    """

    client = OpenAI(api_key=api_key, base_url=url)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": 'Answer with a linux shell command. The answer should be json in the form {"command": <command>, "explanation":<explanation>}',
                },
                {"role": "user", "content": prompt},
            ],
        )
    except openai.APIConnectionError as e:
        print(
            f"Error: can't connect to LLM at url:{url}. Please set the correct url using 'c --set-base-url <url>'"
        )
        raise e

    str_json = response.choices[0].message.content
    str_json = extract_json_content(str_json)
    try:
        return json.loads(str_json)
    except json.JSONDecodeError as e:
        print("Error decoding json: ", e)


def prefill_input(prefill_text):
    def hook():
        readline.insert_text(prefill_text)

    # Set the hook to prefill the input
    readline.set_startup_hook(hook)

    try:
        return input("$ ")  # Print the prompt once, let readline handle the rest
    finally:
        readline.set_startup_hook()  # Clear the hook after use


def add_to_history(command):
    # history is stored in ~/.bash_history
    readline.add_history(command)
    with open(os.path.expanduser("~/.bash_history"), "a") as f:
        f.write(command + "\n")


def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Generates a shell command from a description."
    )
    # parser.add_argument('command', type=str, help='The shell command to run.')
    parser.add_argument(
        "description_str",
        nargs="*",
        help="A description of the command to generate. Example: c list all files in the current directory",
    )
    parser.add_argument(
        "--disable-warning",
        action="store_true",
        help="Disable the warning message.",
        default=False,
    )

    parser.add_argument(
        "--enable-warning",
        action="store_true",
        help="Enable the warning message.",
        default=False,
    )

    parser.add_argument(
        "--set-base-url",
        type=str,
        help="Set the base url for the OpenAI API.",
    )

    parser.add_argument(
        "--set-model",
        type=str,
        help="Set the model for the OpenAI API.",
    )

    return parser


def main():

    parser = parse_arguments()
    args = parser.parse_args()

    command_instr = " ".join(
        args.description_str
    ).strip()  # The instruction to generate a command

    if args.disable_warning:
        set_config("default", "disable_warning", "True")
        return

    if args.enable_warning:
        set_config("default", "disable_warning", "False")
        return

    if args.set_base_url:
        set_config("default", "base_url", args.set_base_url)
        return

    if args.set_model:
        set_config("default", "model", args.set_model)
        return

    if command_instr == "" or command_instr == "--help" or command_instr == "-h":
        parser.print_help()
        return

    handle_warning_message()

    url = get_base_url()
    model = get_model()
    api_key = get_api_key()

    # _instr Try to generate a valid command N_GENERATION_ATTEMPTS times
    for _ in range(N_GENERATION_ATTEMPTS):
        json_command = generate_command(command_instr, url, model, api_key=api_key)
        try:
            _ = Command(**json_command)  # check if the generated command is valid
            break
        except pydantic.ValidationError as e:
            pass
    else:
        print("Error: Could not generate a valid command. Please try again.")
        return

    print(
        "\033[90m" + json_command["explanation"] + "\033[0m"
    )  # Print the explanation in gray
    edited_command = prefill_input(json_command["command"])
    add_to_history(edited_command)  # Add the command to the history
    os.system(edited_command)
