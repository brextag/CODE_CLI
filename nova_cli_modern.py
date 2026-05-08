#!/usr/bin/env python3
"""
Nova CLI Modern - Modern AI-Powered CLI Agent with Rich Formatting

Features:
  - Beautiful Rich terminal output
  - Free AI API integration (Groq, Together AI, Ollama)
  - Real-time streaming responses
  - Advanced command parsing
  - Multi-model support
  - Configuration management
"""

import sys
import json
import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.markdown import Markdown
    from rich.prompt import Prompt, Confirm
    from rich.layout import Layout
    from rich import print as rprint
except ImportError:
    print("❌ Rich library not found. Install with: pip install rich")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("❌ Requests library not found. Install with: pip install requests")
    sys.exit(1)


@dataclass
class AIProvider:
    """AI Provider configuration"""
    name: str
    api_key_env: str
    endpoint: str
    model: str
    headers: Dict
    payload_fn: callable


class AIConfig:
    """Manage AI provider configurations"""
    
    CONFIG_FILE = Path.home() / ".nova_config.json"
    
    PROVIDERS = {
        "groq": {
            "name": "Groq (Fastest Free API)",
            "api_key_env": "GROQ_API_KEY",
            "endpoint": "https://api.groq.com/openai/v1/chat/completions",
            "models": ["mixtral-8x7b-32768", "llama-2-70b-chat", "gemma-7b-it"],
            "default_model": "mixtral-8x7b-32768",
            "free": True,
            "rate_limit": "30 req/min"
        },
        "together": {
            "name": "Together AI (Free Tier)",
            "api_key_env": "TOGETHER_API_KEY",
            "endpoint": "https://api.together.xyz/inference",
            "models": ["mistralai/Mixtral-8x7B-Instruct-v0.1", "meta-llama/Llama-2-70b-chat-hf"],
            "default_model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "free": True,
            "rate_limit": "10 req/hour"
        },
        "openrouter": {
            "name": "OpenRouter (Free Models)",
            "api_key_env": "OPENROUTER_API_KEY",
            "endpoint": "https://openrouter.ai/api/v1/chat/completions",
            "models": ["mistralai/mistral-7b-instruct:free", "gryphe/mythomist-7b:free"],
            "default_model": "mistralai/mistral-7b-instruct:free",
            "free": True,
            "rate_limit": "Unlimited (free)"
        },
    }
    
    @staticmethod
    def load_config() -> Dict:
        """Load configuration from file"""
        if AIConfig.CONFIG_FILE.exists():
            try:
                with open(AIConfig.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    @staticmethod
    def save_config(config: Dict):
        """Save configuration to file"""
        AIConfig.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(AIConfig.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)


class AIClient:
    """AI API client for multiple providers"""
    
    def __init__(self, provider: str = "groq", console: Console = None):
        self.console = console or Console()
        self.provider = provider
        self.config = AIConfig.PROVIDERS.get(provider)
        
        if not self.config:
            self.console.print(f"[red]❌ Provider '{provider}' not found[/red]")
            raise ValueError(f"Unknown provider: {provider}")
        
        self.api_key = os.getenv(self.config["api_key_env"])
        if not self.api_key:
            self.console.print(
                f"[yellow]⚠️  {self.config['api_key_env']} not set[/yellow]\n"
                f"Get free API key at: https://console.groq.com"
            )
            raise ValueError(f"{self.config['api_key_env']} not found")
        
        self.model = os.getenv("NOVA_AI_MODEL", self.config["default_model"])
    
    def ask(self, query: str) -> str:
        """Send query to AI provider"""
        try:
            if self.provider == "groq":
                return self._groq_request(query)
            elif self.provider == "together":
                return self._together_request(query)
            elif self.provider == "openrouter":
                return self._openrouter_request(query)
        except Exception as e:
            return f"[red]Error: {str(e)}[/red]"
    
    def _groq_request(self, query: str) -> str:
        """Send request to Groq API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are Nova, an intelligent AI assistant. Provide clear, concise, and helpful responses."},
                {"role": "user", "content": query}
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        response = requests.post(
            self.config["endpoint"],
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def _together_request(self, query: str) -> str:
        """Send request to Together AI"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "prompt": f"""You are Nova, an intelligent AI assistant.

User: {query}
Assistant:""",
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        response = requests.post(
            self.config["endpoint"],
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        return result["output"]["choices"][0]["text"]
    
    def _openrouter_request(self, query: str) -> str:
        """Send request to OpenRouter"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/brextag/CODE_CLI",
            "X-Title": "Nova CLI"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are Nova, an intelligent AI assistant."},
                {"role": "user", "content": query}
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        response = requests.post(
            self.config["endpoint"],
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]


class NovaAgentModern:
    """Modern Nova Agent with Rich CLI and AI integration"""
    
    def __init__(self):
        self.console = Console()
        self.version = "2.0.0"
        self.name = "Nova"
        self.history = []
        self.ai_client: Optional[AIClient] = None
        self.load_history()
        self.setup_ai()
    
    def setup_ai(self):
        """Setup AI client"""
        try:
            provider = os.getenv("NOVA_AI_PROVIDER", "groq")
            self.ai_client = AIClient(provider, self.console)
            self.console.print(
                f"[green]✓[/green] Connected to [bold]{self.ai_client.config['name']}[/bold]"
            )
        except ValueError as e:
            self.console.print(
                Panel(
                    f"[yellow]{str(e)}[/yellow]\n\n"
                    f"[bold]Get started with Groq (recommended):[/bold]\n"
                    f"1. Visit: https://console.groq.com\n"
                    f"2. Sign up (free)\n"
                    f"3. Get your API key\n"
                    f"4. Run: [cyan]export GROQ_API_KEY=your_key[/cyan]\n",
                    title="[red]AI API Setup Required",
                    border_style="yellow"
                )
            )
    
    def load_history(self):
        """Load command history"""
        history_file = Path.home() / ".nova_history"
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.history = []
    
    def save_history(self):
        """Save command history"""
        history_file = Path.home() / ".nova_history"
        try:
            with open(history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except IOError:
            pass
    
    def add_to_history(self, command: str, query: str):
        """Add to history"""
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "query": query[:100]
        })
        self.save_history()
    
    def ask(self, query: str):
        """Ask AI a question"""
        if not self.ai_client:
            self.console.print("[red]❌ AI client not configured[/red]")
            return
        
        self.console.print()
        with self.console.status("[bold cyan]Thinking...[/bold cyan]", spinner="dots"):
            try:
                response = self.ai_client.ask(query)
                self.add_to_history("ask", query)
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")
                return
        
        self.console.print(Panel(
            Markdown(response),
            title="[bold cyan]Nova Response[/bold cyan]",
            border_style="cyan",
            expand=False
        ))
    
    def analyze(self, target: str):
        """Analyze code or file"""
        self.console.print()
        
        try:
            file_path = Path(target)
            if file_path.exists() and file_path.is_file():
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    query = f"Analyze this {file_path.suffix} code:\n\n{content[:2000]}"
                    self.ask(query)
            else:
                self.ask(f"Explain this concept: {target}")
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
    
    def generate(self, spec: str):
        """Generate code"""
        query = f"Generate code for: {spec}"
        self.ask(query)
    
    def explain(self, concept: str):
        """Explain a concept"""
        query = f"Explain this concept in detail: {concept}"
        self.ask(query)
    
    def show_history(self):
        """Display command history"""
        if not self.history:
            self.console.print("[yellow]No history yet[/yellow]")
            return
        
        table = Table(title="Command History (Last 10)", show_header=True)
        table.add_column("#", style="cyan")
        table.add_column("Time", style="magenta")
        table.add_column("Command", style="green")
        table.add_column("Query", style="white")
        
        for i, entry in enumerate(self.history[-10:], 1):
            time_str = datetime.fromisoformat(entry['timestamp']).strftime("%H:%M:%S")
            table.add_row(
                str(i),
                time_str,
                entry['command'],
                entry['query'][:50] + "..." if len(entry['query']) > 50 else entry['query']
            )
        
        self.console.print(table)
    
    def show_providers(self):
        """Show available AI providers"""
        table = Table(title="Available AI Providers", show_header=True)
        table.add_column("Provider", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Free", style="yellow")
        table.add_column("Rate Limit", style="magenta")
        table.add_column("Setup Link", style="blue")
        
        links = {
            "groq": "https://console.groq.com",
            "together": "https://api.together.xyz",
            "openrouter": "https://openrouter.ai",
        }
        
        for key, config in AIConfig.PROVIDERS.items():
            table.add_row(
                key,
                config['name'],
                "✓" if config['free'] else "✗",
                config['rate_limit'],
                links.get(key, "N/A")
            )
        
        self.console.print(table)
    
    def interactive_mode(self):
        """Interactive mode"""
        self.console.print()
        self.console.print(Panel(
            f"[bold cyan]Welcome to {self.name} CLI v{self.version}[/bold cyan]\n"
            f"[yellow]Type 'help' for commands or 'exit' to quit[/yellow]",
            border_style="cyan"
        ))
        self.console.print()
        
        while True:
            try:
                user_input = Prompt.ask("Nova", default="help").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'exit':
                    self.console.print("[cyan]Goodbye![/cyan]")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                if user_input.lower() == 'providers':
                    self.show_providers()
                    continue
                
                # Parse commands
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if command == 'ask' and args:
                    self.ask(args)
                elif command == 'analyze' and args:
                    self.analyze(args)
                elif command == 'generate' and args:
                    self.generate(args)
                elif command == 'explain' and args:
                    self.explain(args)
                else:
                    self.console.print("[red]Unknown command. Type 'help' for available commands.[/red]")
            
            except KeyboardInterrupt:
                self.console.print("\n[cyan]Exiting...[/cyan]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")
    
    def show_help(self):
        """Show help information"""
        help_text = """
[bold cyan]Available Commands:[/bold cyan]

[green]ask <query>[/green]              Ask Nova a question
[green]analyze <file|concept>[/green]   Analyze code or concepts
[green]generate <spec>[/green]          Generate code from specification
[green]explain <concept>[/green]        Explain a concept in detail
[green]history[/green]                  View command history
[green]providers[/green]                Show available AI providers
[green]help[/green]                     Show this help message
[green]exit[/green]                     Exit the application

[bold cyan]Examples:[/bold cyan]

ask "How do I create a REST API in Python?"
analyze "main.py"
generate "Python web scraper for news"
explain "What is async/await?"

[bold cyan]Environment Variables:[/bold cyan]

GROQ_API_KEY          Your Groq API key
NOVA_AI_PROVIDER      AI provider (groq, together, openrouter)
NOVA_AI_MODEL         Specific model to use
        """
        self.console.print(Panel(
            Markdown(help_text),
            title="[bold cyan]Help[/bold cyan]",
            border_style="cyan"
        ))


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Nova - Modern AI-Powered CLI Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nova ask "What is Python?"
  nova analyze "server.py"
  nova generate "Python REST API"
  nova explain "REST APIs"
  nova --interactive
  nova --providers

Setup:
  1. Get free API key at https://console.groq.com
  2. Set environment: export GROQ_API_KEY=your_key
  3. Run: nova --interactive
        """
    )
    
    parser.add_argument('--version', action='version', version='Nova 2.0.0')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    parser.add_argument('--providers', action='store_true', help='Show available providers')
    parser.add_argument('--history', action='store_true', help='Show command history')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    ask_parser = subparsers.add_parser('ask', help='Ask a question')
    ask_parser.add_argument('query', nargs='+', help='Your question')
    
    analyze_parser = subparsers.add_parser('analyze', help='Analyze code/concepts')
    analyze_parser.add_argument('target', nargs='+', help='File or concept')
    
    generate_parser = subparsers.add_parser('generate', help='Generate code')
    generate_parser.add_argument('spec', nargs='+', help='Code specification')
    
    explain_parser = subparsers.add_parser('explain', help='Explain concept')
    explain_parser.add_argument('concept', nargs='+', help='Concept to explain')
    
    args = parser.parse_args()
    
    nova = NovaAgentModern()
    
    if args.providers:
        nova.show_providers()
        return
    
    if args.history:
        nova.show_history()
        return
    
    if args.interactive or len(sys.argv) == 1:
        nova.interactive_mode()
        return
    
    if args.command == 'ask':
        nova.ask(' '.join(args.query))
    elif args.command == 'analyze':
        nova.analyze(' '.join(args.target))
    elif args.command == 'generate':
        nova.generate(' '.join(args.spec))
    elif args.command == 'explain':
        nova.explain(' '.join(args.concept))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
