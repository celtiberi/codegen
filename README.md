# Code Generation with Claude API

This Python script generates a project structure and code files based on a given project description using the Claude API from Anthropic.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.x installed
- Required libraries: `anthropic`, `python-dotenv`
- An API key for the Claude API (stored in a `.env` file)

## Setup

1. Clone the repository or download the script file.
2. Install the required libraries using pip:
3. Create a `.env` file in the same directory as the script and add your Claude API key:
4. Create a `project_description.txt` file in the same directory and provide your project description in it.

## Usage

To generate the project structure and code files, run the script:
The script will read the project description from `project_description.txt`, generate the project structure using the Claude API, and create the corresponding directories and code files in the `generated_code` directory.

## Customization

- You can modify the `OUTPUT_DIRECTORY` variable in the script to change the output directory for the generated code.

- Adjust the `max_tokens` parameter in the `anthropic.Anthropic().messages.create()` calls to control the maximum number of tokens in the generated code.

- Update the system prompts and templates in the script to customize the code generation behavior.

## Dependencies

- `anthropic`: The Python library for interacting with the Claude API.
- `python-dotenv`: A library for loading environment variables from a `.env` file.
- Other standard Python libraries: `os`, `time`, `json`, `re`, `shutil`.

## License

This code is provided under the [MIT License](LICENSE).
