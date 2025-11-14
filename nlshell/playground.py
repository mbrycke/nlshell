from prompt_toolkit import prompt
from prompt_toolkit.document import Document

def input_with_prefill(prompt_text, prefill=''):
    return prompt(prompt_text, default=prefill)

# Example
city = input_with_prefill("Enter your city: ", "New York")
print("You entered:", city)
