# Nova - AI-Powered CLI Agent

🚀 A command-line interface AI agent that brings intelligent automation to your terminal.

## Features

- **Ask**: Query Nova for information and assistance
- **Analyze**: Deep analysis of code, files, and concepts
- **Generate**: Create code and content from specifications
- **Explain**: Get detailed explanations of complex topics
- **Interactive Mode**: Chat-like interface for continuous interaction
- **JSON Output**: Machine-readable output for scripting
- **Command History**: Track all executed commands

## Installation

```bash
# Clone the repository
git clone https://github.com/brextag/CODE_CLI.git
cd CODE_CLI

# Make the script executable
chmod +x nova_cli.py

# Optional: Create a symlink for easy access
ln -s $(pwd)/nova_cli.py /usr/local/bin/nova
```

## Usage

### Command Mode

```bash
# Ask a question
python nova_cli.py ask "How do I create a REST API?"

# Analyze code or concepts
python nova_cli.py analyze "main.py"

# Generate code from specification
python nova_cli.py generate "Python function for Fibonacci"

# Get detailed explanation
python nova_cli.py explain "What is async/await?"

# View command history
python nova_cli.py history

# Get version
python nova_cli.py --version
```

### Interactive Mode

```bash
# Start interactive session
python nova_cli.py --interactive

# Then interact with Nova
Nova> ask "What is machine learning?"
Nova> generate "Python web scraper"
Nova> explain "REST API"
Nova> exit
```

### JSON Output

```bash
# Get results in JSON format
python nova_cli.py ask "Hello Nova" --json
```

## Examples

```bash
# Ask for coding help
nova ask "How do I handle errors in Python?"

# Analyze a file
nova analyze "server.js"

# Generate documentation
nova generate "README for my Python project"

# Understand concepts
nova explain "What are decorators in Python?"

# Interactive learning session
nova --interactive
```

## Requirements

- Python 3.8+
- No external dependencies required for basic functionality

## Architecture

Nova is built with a modular agent architecture:

- **NovaAgent**: Core AI agent class handling command processing
- **Command Handlers**: Separate methods for each command type
- **Interactive Mode**: Chat-like interface for continuous interaction
- **History Tracking**: Maintains audit trail of all commands
- **JSON Support**: Export results for integration with other tools

## Future Enhancements

- Integration with OpenAI/Claude/other LLM APIs
- Plugin system for extending functionality
- Configuration profiles
- Advanced memory/context management
- Multi-file analysis
- Real-time code collaboration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on GitHub or visit:
https://github.com/brextag/CODE_CLI

---

**Nova** - Your AI companion in the terminal 🤖✨
