#!/usr/bin/env python3
"""
Nova CLI - An Intelligent AI Agent for the Command Line

Nova is a powerful CLI-based AI agent that provides intelligent assistance
with asking questions, analyzing code/concepts, generating content, and more.

Usage:
    nova ask "Your question"
    nova analyze "file.py"
    nova generate "Python REST API"
    nova explain "async/await"
    nova --interactive
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


class NovaAgent:
    """
    Nova AI Agent - Main application class
    
    Handles all command processing and responses
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.name = "Nova"
        self.history = []
        self.load_history()
    
    def load_history(self):
        """Load command history from file"""
        history_file = Path.home() / ".nova_history"
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.history = []
    
    def save_history(self):
        """Save command history to file"""
        history_file = Path.home() / ".nova_history"
        try:
            with open(history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except IOError:
            pass
    
    def add_to_history(self, command, result):
        """Add command to history"""
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "result_summary": result[:100] if isinstance(result, str) else str(result)[:100]
        })
        self.save_history()
    
    def ask(self, query):
        """
        Ask Nova a question
        
        Args:
            query (str): The question to ask
            
        Returns:
            str: Response from Nova
        """
        response = f"[Nova Analysis] Received query: '{query}'\n\n"
        response += f"Query Analysis:\n"
        response += f"  • Type: Question/Inquiry\n"
        response += f"  • Length: {len(query)} characters\n"
        response += f"  • Processing: Complete\n\n"
        response += f"Response: I'm analyzing your question. For production use, connect to OpenAI/Claude/Anthropic APIs.\n"
        response += f"Your question: {query}\n"
        
        self.add_to_history("ask", response)
        return response
    
    def analyze(self, target):
        """
        Analyze code, files, or concepts
        
        Args:
            target (str): What to analyze
            
        Returns:
            str: Analysis results
        """
        response = f"[Nova Analysis] Analyzing: '{target}'\n\n"
        response += f"Analysis Report:\n"
        response += f"  • Target: {target}\n"
        response += f"  • Scope: Deep Analysis\n"
        response += f"  • Status: In Progress\n\n"
        
        # Try to read file if it exists
        try:
            file_path = Path(target)
            if file_path.exists() and file_path.is_file():
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    response += f"File Analysis:\n"
                    response += f"  • Lines: {len(lines)}\n"
                    response += f"  • Characters: {len(content)}\n"
                    response += f"  • File Type: {file_path.suffix}\n"
            else:
                response += f"Concept Analysis:\n"
                response += f"  • Subject: {target}\n"
                response += f"  • Type: Conceptual\n"
                response += f"  • Depth: Comprehensive\n"
        except Exception as e:
            response += f"  • Error: {str(e)}\n"
        
        response += f"\nFor detailed analysis, connect to LLM APIs.\n"
        
        self.add_to_history("analyze", response)
        return response
    
    def generate(self, specification):
        """
        Generate code or content from specification
        
        Args:
            specification (str): What to generate
            
        Returns:
            str: Generated content
        """
        response = f"[Nova Generation] Task: '{specification}'\n\n"
        response += f"Generation Parameters:\n"
        response += f"  • Specification: {specification}\n"
        response += f"  • Type: Code/Content Generation\n"
        response += f"  • Status: Processing\n\n"
        response += f"Output Template:\n"
        response += f"```\n"
        response += f"# Generated Content\n"
        response += f"# Specification: {specification}\n"
        response += f"# For full generation, enable LLM integration\n"
        response += f"```\n\n"
        response += f"To generate actual code, configure API keys for OpenAI, Claude, or similar services.\n"
        
        self.add_to_history("generate", response)
        return response
    
    def explain(self, concept):
        """
        Provide detailed explanation of a concept
        
        Args:
            concept (str): What to explain
            
        Returns:
            str: Detailed explanation
        """
        response = f"[Nova Explanation] Topic: '{concept}'\n\n"
        response += f"Explanation Framework:\n"
        response += f"  • Concept: {concept}\n"
        response += f"  • Depth: Detailed\n"
        response += f"  • Format: Structured\n\n"
        response += f"Overview:\n"
        response += f"  • Definition\n"
        response += f"  • Key Components\n"
        response += f"  • Use Cases\n"
        response += f"  • Best Practices\n"
        response += f"  • Common Pitfalls\n"
        response += f"  • Examples\n\n"
        response += f"For comprehensive explanations, enable LLM integration.\n"
        
        self.add_to_history("explain", response)
        return response
    
    def get_history(self):
        """Get command history"""
        if not self.history:
            return "No command history yet.\n"
        
        response = "Command History:\n"
        response += "=" * 60 + "\n"
        for i, entry in enumerate(self.history[-10:], 1):  # Show last 10
            response += f"\n{i}. Timestamp: {entry['timestamp']}\n"
            response += f"   Command: {entry['command']}\n"
            response += f"   Summary: {entry['result_summary']}\n"
        
        return response
    
    def clear_history(self):
        """Clear command history"""
        self.history = []
        self.save_history()
        return "History cleared.\n"
    
    def interactive_mode(self):
        """Interactive chat mode"""
        print(f"\n{'='*60}")
        print(f"Welcome to {self.name} CLI AI Agent v{self.version}")
        print(f"Type 'help' for commands or 'exit' to quit")
        print(f"{'='*60}\n")
        
        while True:
            try:
                user_input = input(f"Nova> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'exit':
                    print(f"Goodbye! See you next time.")
                    break
                
                if user_input.lower() == 'help':
                    self.print_help()
                    continue
                
                if user_input.lower() == 'history':
                    print(self.get_history())
                    continue
                
                if user_input.lower() == 'clear':
                    self.clear_history()
                    print("History cleared.")
                    continue
                
                # Parse commands in interactive mode
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if command == 'ask' and args:
                    print(self.ask(args))
                elif command == 'analyze' and args:
                    print(self.analyze(args))
                elif command == 'generate' and args:
                    print(self.generate(args))
                elif command == 'explain' and args:
                    print(self.explain(args))
                else:
                    print("Unknown command. Type 'help' for available commands.\n")
            
            except KeyboardInterrupt:
                print("\n\nExiting Nova CLI...")
                break
            except Exception as e:
                print(f"Error: {str(e)}\n")
    
    def print_help(self):
        """Print help information"""
        print(f"""
{self.name} CLI - Available Commands:

  ask <query>              Ask Nova a question
  analyze <target>        Analyze code, files, or concepts
  generate <spec>         Generate code or content
  explain <concept>       Get detailed explanation
  history                 View command history
  clear                   Clear command history
  help                    Show this help message
  exit                    Exit interactive mode

Examples:
  ask "How do I use Python decorators?"
  analyze "main.py"
  generate "Python REST API with Flask"
  explain "async/await in JavaScript"

Configuration:
  For LLM integration, set environment variables:
  - OPENAI_API_KEY       (for OpenAI)
  - ANTHROPIC_API_KEY    (for Claude)

For more info: https://github.com/brextag/CODE_CLI
""")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Nova - Intelligent AI Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nova ask "What is Python?"
  nova analyze "server.py"
  nova generate "Python web scraper"
  nova explain "REST APIs"
  nova --interactive

For more information visit: https://github.com/brextag/CODE_CLI
        """
    )
    
    parser.add_argument('--version', action='version', version='Nova 1.0.0')
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Start interactive mode')
    parser.add_argument('--json', action='store_true', 
                       help='Output in JSON format')
    parser.add_argument('--history', action='store_true', 
                       help='Show command history')
    parser.add_argument('--clear-history', action='store_true', 
                       help='Clear command history')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Ask command
    ask_parser = subparsers.add_parser('ask', help='Ask Nova a question')
    ask_parser.add_argument('query', nargs='+', help='Your question')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze code/concepts')
    analyze_parser.add_argument('target', nargs='+', help='What to analyze')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate code/content')
    generate_parser.add_argument('spec', nargs='+', help='Generation specification')
    
    # Explain command
    explain_parser = subparsers.add_parser('explain', help='Explain a concept')
    explain_parser.add_argument('concept', nargs='+', help='Concept to explain')
    
    args = parser.parse_args()
    
    nova = NovaAgent()
    
    # Handle special flags
    if args.history:
        print(nova.get_history())
        return
    
    if args.clear_history:
        print(nova.clear_history())
        return
    
    # Interactive mode
    if args.interactive or (len(sys.argv) == 1):
        nova.interactive_mode()
        return
    
    # Command mode
    result = None
    
    if args.command == 'ask':
        result = nova.ask(' '.join(args.query))
    elif args.command == 'analyze':
        result = nova.analyze(' '.join(args.target))
    elif args.command == 'generate':
        result = nova.generate(' '.join(args.spec))
    elif args.command == 'explain':
        result = nova.explain(' '.join(args.concept))
    else:
        parser.print_help()
        return
    
    # Output result
    if args.json:
        output = {
            "status": "success",
            "command": args.command,
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        print(json.dumps(output, indent=2))
    else:
        print(result)


if __name__ == '__main__':
    main()
