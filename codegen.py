import os
import time
import anthropic
from dotenv import load_dotenv
import json
import re
import shutil

# Load environment variables
load_dotenv()

# Retrieve the API key from the .env file
api_key = os.getenv("claude_api_key")

# Set up the Claude API client
client = anthropic.Anthropic(api_key=api_key)

# Set the output directory
OUTPUT_DIRECTORY = "generated_code"

def generate_project_structure(project_description):
    print("Generating project structure based on the project description...")

    # Set up the API request payload for generating the project structure
    prompt = f"""
<project_description>
{project_description}
</project_description>

Based on the project description above, provide a high-level overview of the project structure, including the main files 
and directories that will be created. The project structure should be based on best practices. Also, include a 
description of each file's purpose. One of the top level files should be a README.md file.

Return the project structure in the following JSON format.

{{
    "files:": [
        {{
            "type": "file",
            "name": "file1.txt",
            "description": "File 1 description"
        }},
    ],
    "directories:": [
        {{
            "type": "directory",
            "name": "dir1",
            "description": "Directory 1 description",            
            "files": [
                {{
                    "type": "file",
                    "name": "file3.txt",
                    "description": "File 3 description"
                }}
            ],         
        }},
        {{ 
            "name": "dir2",
            "description": "Directory 2 description",
            "files": [
                {{
                    "type": "file",
                    "name": "file4.txt",
                    "description": "File 4 description"
                }}
            ]   
        }}
    ]
}}

example:
{{
    "files": [
        {{
            "type": "file",
            "name": "README.md",
            "description": "project README.md"
        }}
    ],
    "directories": [
        {{
            "name": "dir1",
            "description": "Directory 1 description",
            "files": [
                {{
                    "type": "file",
                    "name": "file3.txt",
                    "description": "File 3 description"
                }}
            ]
        }}
    ]
}}
"""

    # Make the API request to generate the project structure
    response = client.messages.create(
        model=os.getenv("model"),
        system="""You are a skilled and creative software developer.""",
        max_tokens=2000,
        messages=[
            {
                "role": "user", 
                "content": prompt
            },
            {
                "role": "assistant",
                "content": "{"
            }
        ]
    )

    generated_structure = '{' +response.content[0].text

    print("\nGenerated project structure:")
    print(generated_structure)

    return json.loads(generated_structure)


def create_file_structure(base_path, structure_json):
    directories = structure_json.get("directories", [])  # Use an empty list if "directories" key is not found
    for directory in directories:
        dir_path = os.path.join(base_path, directory["name"])
        os.makedirs(dir_path, exist_ok=True)
        for file in directory.get("files", []):  # Similarly, use an empty list if "files" key is not found
            file_path = os.path.join(dir_path, file["name"])
            open(file_path, "w").close()  # Create an empty file   

        
def generate_code(project_description, base_path, structure_json):    
    # Iterate through directories in the JSON structure
    for directory in structure_json.get("directories", []):
        generate_code(project_description, os.path.join(base_path, directory["name"]), directory)

    for file in structure_json.get("files", []):
        file_path = os.path.join(base_path, file["name"])
        file_description = file.get("description", "")
        
        print("Generating code for - " + file_path)
        
        prompt = f"""
                    <project_description>
                    {project_description}
                    </project_description>

                    <file_description>
                    {file_description}
                    </file_description>

                    <file_path>
                    {file_path}
                    </file_path>

                    Based on the project description, file description, and file path above, generate the code for the file. 
                    Use this format for your response:

                    <file_name>
                        file1.py
                    </file_name>
                    <code>
                        all code generation goes here
                    </code>                          

                    Here is an example:

                    <file_name>
                        file1.py
                    </file_name>

                    <code>
                        import os
                        print("hello")
                    </code>         

                    Here is another example:

                    <file_name>
                        __init__.py
                    </file_name>

                    <code>
                    </code>    
                """


        # Make the API request to generate the code for the file
        response = client.messages.create(
            model=os.getenv("model"),
            system="Given the project description, file description, and file path, generate the code for the file.  Your response should only contain the code.",
            max_tokens=2000,
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                },
                # {
                #     "role": "assistant",
                #     "content": "{"
                # }
            ]
        )

        # Assuming the response is also in JSON format
        # generated_code_json = json.loads('{' + response.content[0].text)  # Parse the response content as JSON
        # generated_code_text = generated_code_json["code"]

        # Split the response text to remove the initial descriptive part
        start = response.content[0].text.find("<code>") + len("<code>")
        end = response.content[0].text.find("</code>")
        generated_code_text = response.content[0].text[start:end].strip()

        # Save the generated code to the corresponding file        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(generated_code_text)

        print(f"Generated code for file: {file_path}")
        print(generated_code_text)


    print("\nCode generation complete.")


# Read the project description from the file
with open("project_description.txt", "r") as file:
    project_description = file.read()

# Generate the project structure
project_structure_json = generate_project_structure(project_description)


if os.path.exists(OUTPUT_DIRECTORY):
    shutil.rmtree(OUTPUT_DIRECTORY)

# Create the file structure based on the generated project structure
create_file_structure(OUTPUT_DIRECTORY, project_structure_json)

# Generate the code based on the project description and structure
generate_code(project_description, OUTPUT_DIRECTORY, project_structure_json)