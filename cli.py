import requests
import json
import sys
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
import argparse

console = Console()

class ChatGPTCLI:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.messages = []
        self.console = Console()

    def print_welcome(self):
        welcome_text = """
        [bold blue]KalIA GPT[/bold blue]
        
        Welcome to the KalIA GPT CLI!
        Type 'exit' to exit or 'help' to see available commands.
        """
        self.console.print(Panel(welcome_text, title="[bold green]Welcome![/bold green]"))

    def print_help(self):
        help_text = """
        [bold]Available commands:[/bold]
        
        [cyan]help[/cyan] - Shows this help message
        [cyan]exit[/cyan] - Exits the program
        [cyan]clear[/cyan] - Clears message history
        [cyan]exec <command>[/cyan] - Executes a command on the local system
        """
        self.console.print(Panel(help_text, title="[bold green]Help[/bold green]"))

    def send_message(self, message):
        try:
            self.messages.append({"role": "user", "content": message})
            
            response = requests.post(
                f"{self.base_url}/chatgpt/4o-mini",
                json={
                    "messages": self.messages
                }
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    assistant_message = result.get("content", "")
                    self.messages.append({"role": "assistant", "content": assistant_message})
                    self.console.print("\n[bold red]Kalia[/bold red]:", Markdown(assistant_message))
                else:
                    self.console.print(f"[red]Erro: {result.get('message')}[/red]")
            else:
                self.console.print(f"[red]Erro na requisição: {response.status_code}[/red]")
        except Exception as e:
            self.console.print(f"[red]Erro: {str(e)}[/red]")

    def run(self):
        self.print_welcome()
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold blue]Você[/bold blue]")
                
                if user_input.lower() == 'exit':
                    self.console.print("[yellow]Até logo![/yellow]")
                    break
                elif user_input.lower() == 'help':
                    self.print_help()
                elif user_input.lower() == 'clear':
                    self.messages = []
                    self.console.print("[green]Histórico limpo![/green]")
                elif user_input.startswith('exec '):
                    command = user_input[5:]
                    self.send_message(f"Execute o comando: {command}")
                else:
                    self.send_message(user_input)
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Até logo![/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Erro: {str(e)}[/red]")

def main():
    parser = argparse.ArgumentParser(description='ChatGPT CLI')
    parser.add_argument('--url', default='http://localhost:8080', help='URL da API (padrão: http://localhost:8080)')
    args = parser.parse_args()

    cli = ChatGPTCLI(base_url=args.url)
    cli.run()

if __name__ == "__main__":
    main() 