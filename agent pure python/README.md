# Gemini AI Coding Agent

## Overview

`main.py` is an interactive command-line AI coding agent powered by the Google Gemini API (`gemini-3.5-flash-lite`). It features colored terminal output via `colorama`, handles multi-turn conversations, and supports automated function/tool-calling so the assistant can act directly as a coding agent in the local environment and workspace.

## Features

The agent is equipped with a comprehensive system instruction set and has access to four core system tools:

1. **`list_files`**: Lists files and directories in a given path (`os.listdir`).
2. **`read_file`**: Reads text files with fallback encoding support (`utf-8` and `utf-16`).
3. **`write_file`**: Creates or overwrites text files with specified content.
4. **`run_command`**: Executes shell commands on the host system via `subprocess.run` (with a timeout safeguard).

## Agent Behavior & Rules

The agent is instructed to follow strict engineering guidelines:

- Inspect files and directories using tools rather than guessing.
- Read existing code before modifying it.
- Analyze errors and implement concrete, clean, and maintainable fixes.
- Explain changes clearly after updating code.
- Exercise caution with destructive actions and system commands.

## How It Works

- Loads environment variables (like `GEMINI_API_KEY`) using `python-dotenv`.
- Displays a startup banner and enters an interactive chat loop (`while True`).
- Maintains conversation state in `messages`, handling user inputs, model thoughts/tool calls, and execution feedback loops seamlessly until a final response is generated.
