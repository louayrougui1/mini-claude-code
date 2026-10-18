
import os
import subprocess
from google import genai
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colors
init(autoreset=True)

# Load environment variables
load_dotenv()

# Startup banner
print(Fore.CYAN + Style.BRIGHT + "=" * 40)
print(Fore.MAGENTA + Style.BRIGHT + "       GEMINI AI AGENT")
print(Fore.CYAN + Style.BRIGHT + "=" * 40)
print(Fore.WHITE + "Tools: Read | List | Write | Command")
print(Fore.YELLOW + "Type 'exit' or 'quit' to stop.\n")


# 1. List files in a directory
def list_files(path="."):
    try:
        return os.listdir(path)
    except FileNotFoundError:
        return f"Directory {path} not found"
    except OSError as e:
        return f"Error listing directory: {e}"


# 2. Run a system command
def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout if result.returncode == 0 else result.stderr

    except subprocess.TimeoutExpired:
        return "Command timed out"
    except OSError as e:
        return f"Error running command: {e}"


# 3. Write content to a file
def write_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Content successfully written to {path}"

    except OSError as e:
        return f"Error writing file: {e}"


# 4. Read a file
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    except FileNotFoundError:
        return f"File {path} not found"

    except UnicodeDecodeError:
        try:
            with open(path, "r", encoding="utf-16") as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            return f"Error: {path} is not a supported text file."

    except OSError as e:
        return f"Error reading file: {e}"


# Tool schemas
TOOL_SCHEMAS = [
    {
        "function_declarations": [
            {
                "name": "read_file",
                "description": "Read a text file and return its contents.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path of the file to read",
                        },
                    },
                    "required": ["path"],
                },
            },
            {
                "name": "list_files",
                "description": "List files and directories in a directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path of the directory to list",
                        },
                    },
                    "required": ["path"],
                },
            },
            {
                "name": "run_command",
                "description": "Run a system command and return its output.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "System command to execute",
                        },
                    },
                    "required": ["command"],
                },
            },
            {
                "name": "write_file",
                "description": "Write text content to a file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path of the file to write to",
                        },
                        "content": {
                            "type": "string",
                            "description": "Text content to write into the file",
                        },
                    },
                    "required": ["path", "content"],
                },
            },
        ]
    }
]


# Initialize Gemini
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

model = "gemini-3.5-flash-lite"
instruction = "You are a helpful chatbot. Answer clearly and naturally."

messages = []


# Main chat loop
while True:
    user_input = input(
        Fore.GREEN + Style.BRIGHT + "\nYou: " + Style.RESET_ALL
    )

    if user_input.strip().lower() in ("exit", "quit"):
        print(Fore.YELLOW + "\nGoodbye!")
        break

    messages.append({
        "role": "user",
        "parts": [{"text": user_input}],
    })

    # Keep calling Gemini until it stops requesting tools
    while True:
        response = client.models.generate_content(
            model=model,
            contents=messages,
            config={
                "system_instruction": instruction,
                "tools": TOOL_SCHEMAS,
            },
        )

        # Gemini has finished responding
        if not response.function_calls:
            print(
                Fore.MAGENTA + Style.BRIGHT + "\nBot: "
                + Style.RESET_ALL + (response.text or "")
            )
            messages.append(response.candidates[0].content)
            break

        # Save Gemini's tool-call message
        messages.append(response.candidates[0].content)

        function_response_parts = []

        # Execute requested tools
        for call in response.function_calls:

            if call.name == "read_file":
                args = dict(call.args)
                print(Fore.CYAN + f"\n[READ] Reading file: {args['path']}")
                result = read_file(**args)
                response_payload = {"result": result}

            elif call.name == "list_files":
                args = dict(call.args)
                print(Fore.CYAN + f"\n[LIST] Listing directory: {args['path']}")
                result = list_files(**args)
                response_payload = {"result": result}

            elif call.name == "run_command":
                args = dict(call.args)
                print(
                    Fore.YELLOW
                    + f"\n[COMMAND] Running: {args['command']}"
                )
                result = run_command(**args)
                response_payload = {"result": result}

            elif call.name == "write_file":
                args = dict(call.args)
                print(
                    Fore.MAGENTA
                    + f"\n[WRITE] Writing to file: {args['path']}"
                )
                result = write_file(**args)
                response_payload = {"result": result}

            else:
                response_payload = {
                    "error": f"Unknown tool: {call.name}"
                }
                print(
                    Fore.RED
                    + f"Warning: Unknown tool requested: {call.name}"
                )

            # Send each tool's result back to Gemini
            function_response_parts.append({
                "function_response": {
                    "name": call.name,
                    "response": response_payload,
                }
            })

        # Provide tool results to Gemini
        messages.append({
            "role": "user",
            "parts": function_response_parts,
        })
