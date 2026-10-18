# Gemini AI Agent

## Overview

`main.py` is an interactive command-line chatbot and agent script powered by the Google Gemini API (`gemini-3.5-flash-lite`). It features colored terminal output via `colorama`, handles multi-turn conversations, and supports automated function/tool-calling so the assistant can interact directly with the local operating system and workspace.

## Features

The agent has access to four core tools:

1. **`list_files`**: Lists all files and directories in a given path (`os.listdir`).
2. **`read_file`**: Reads and returns the contents of a text file with fallback encoding support (utf-8 and utf-16).
3. **`write_file`**: Writes text content to a specified file.
4. **`run_command`**: Executes shell commands on the host system via `subprocess.run` with a timeout limit.

## How It Works

- Loads environment variables (such as `GEMINI_API_KEY`) using `python-dotenv`.
- Initializes a stylish startup banner and starts an interactive chat loop (`while True`).
- Maintains conversation history (`messages`), appending user input, model thoughts/tool calls, and function execution results.
- Dynamically executes requested tool calls, prints colored status logs to the terminal, and feeds the responses back to the model until a final text response is produced.
