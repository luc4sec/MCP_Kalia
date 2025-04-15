# MCP Pentest - KalIA GPT

KalIA GPT is an AI-assisted pentest tool designed to help security professionals in conducting penetration testing. Using the power of ChatGPT within Kali Linux, the tool provides insights and suggestions for pentest activities, maintaining an interaction history and allowing secure command execution.

## Key Features

- Intuitive CLI interface for AI interaction
- Secure execution of pentest commands
- Maintained interaction history for analysis
- Kali Linux integration for pentest environment
- Support for custom security testing commands

## Project Structure

- `main.py`: Main Flask server running on Kali Linux
- `cli.py`: Command line interface for local interaction
- `routes/`: API routes for AI service integration
- `config/`: Project configurations
- `requirements.txt`: Project dependencies

## Requirements

- Python 3.8+
- Kali Linux (for the server)
- pip (Python package manager)
- Access to OpenAI API

## Installation

1. Clone the repository:
```bash
git clone [REPOSITORY_URL]
cd MCP_Pentest
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root with the following variables:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Server (Kali Linux)

1. Run the server:
```bash
python main.py
```
The server will be available at `http://localhost:8080`

### CLI (Local)

1. Run the CLI:
```bash
python cli.py
```

2. Available commands:
- `help`: Shows available commands
- `exit`: Exits the program
- `clear`: Clears message history
- `exec <command>`: Executes a pentest command on the local system

## Docker (Optional)

Kali can also be run using Docker:

```bash
docker-compose up
```

## Security Notes

- The server should run on a dedicated Kali Linux machine for pentesting
- The CLI can run locally on any operating system
- Ensure you have a secure internet connection to access the ChatGPT API
- Keep your API keys secure and do not share them
- Use only for authorized testing in controlled environments 