# 🚀 Nova AI API Setup Guide

## Free AI APIs for Nova

Nova supports multiple **free AI API providers**. Choose one and follow the setup instructions.

---

## 1. **Groq** (RECOMMENDED - Fastest Free API) ⚡

### Why Groq?
- **Fastest inference** (10x faster than competitors)
- **Free tier**: 30 requests/minute
- **Models**: Mixtral-8x7B, Llama-2-70B, Gemma-7B
- **No credit card** required to get started

### Setup:

```bash
# 1. Visit https://console.groq.com
# 2. Sign up (email verification)
# 3. Copy your API key from the dashboard

# 4. Set environment variable
export GROQ_API_KEY="your_api_key_here"

# 5. Run Nova
python nova_cli_modern.py --interactive
```

### Verify Installation:
```bash
python nova_cli_modern.py ask "Hello, who are you?"
```

---

## 2. **Together AI** (Alternative Free Option)

### Why Together AI?
- **Free tier**: 1M tokens/month (~40 hours of chat)
- **Models**: Mistral, Llama, Mixtral variants
- **Good performance**: Fast and reliable

### Setup:

```bash
# 1. Visit https://api.together.xyz
# 2. Sign up (free account)
# 3. Generate API key in settings

# 4. Set environment variables
export TOGETHER_API_KEY="your_api_key_here"
export NOVA_AI_PROVIDER="together"

# 5. Run Nova
python nova_cli_modern.py --interactive
```

---

## 3. **OpenRouter** (Free Models Available)

### Why OpenRouter?
- **Multiple free models** available
- **Reliable routing** to best available model
- **50+ models** to choose from

### Setup:

```bash
# 1. Visit https://openrouter.ai
# 2. Sign up (OAuth with GitHub/Google)
# 3. Copy API key from dashboard

# 4. Set environment variables
export OPENROUTER_API_KEY="your_api_key_here"
export NOVA_AI_PROVIDER="openrouter"

# 5. Run Nova
python nova_cli_modern.py --interactive
```

---

## Installation

### 1. Install Required Libraries

```bash
pip install -r requirements.txt
# or manually:
pip install rich requests python-dotenv
```

### 2. Set Up Your Environment

**On Linux/macOS:**
```bash
echo 'export GROQ_API_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc

# Verify
echo $GROQ_API_KEY
```

**On Windows (PowerShell):**
```powershell
[Environment]::SetEnvironmentVariable("GROQ_API_KEY", "your_key_here", "User")
# Restart terminal or:
$env:GROQ_API_KEY="your_key_here"
```

### 3. Test Your Setup

```bash
# Interactive mode
python nova_cli_modern.py --interactive

# Or single command
python nova_cli_modern.py ask "What is Python?"
```

---

## Using .env File (Alternative)

Create a `.env` file in your project root:

```env
# .env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
NOVA_AI_PROVIDER=groq
NOVA_AI_MODEL=mixtral-8x7b-32768
```

Then load it:
```bash
python -c "from dotenv import load_dotenv; load_dotenv()"
```

---

## Comparison of Free APIs

| Provider | Free Tier | Speed | Models | Setup |
|----------|-----------|-------|--------|-------|
| **Groq** | 30 req/min | ⚡⚡⚡ Fast | Mixtral, Llama | 5 min |
| **Together** | 1M tokens/mo | ⚡⚡ Good | Mistral, Llama | 5 min |
| **OpenRouter** | Free models | ⚡⚡ Good | 50+ models | 5 min |
| OpenAI | No free | ⚡⚡ Good | GPT-4, 3.5 | Credit card |
| Claude (Anthropic) | No free | ⚡⚡⚡ Best | Claude-3 | Credit card |

---

## Common Issues

### "API key not found" Error

**Solution:**
```bash
# Verify API key is set
echo $GROQ_API_KEY

# If empty, set it:
export GROQ_API_KEY="your_key"

# Or use .env file
echo 'GROQ_API_KEY=your_key' > .env
```

### "Rate limit exceeded" Error

**Solution:**
- Groq: Wait 60 seconds (30 req/min limit)
- Together: Check monthly token usage
- OpenRouter: Check daily limits

### "Connection timeout" Error

**Solution:**
```bash
# Check internet connection
pip install --upgrade requests

# Try different provider
export NOVA_AI_PROVIDER="together"
```

---

## Advanced Configuration

### Using a Specific Model

```bash
# Groq models
export NOVA_AI_MODEL="mixtral-8x7b-32768"
export NOVA_AI_MODEL="llama-2-70b-chat"
export NOVA_AI_MODEL="gemma-7b-it"

python nova_cli_modern.py ask "Your question"
```

### Switching Providers on the Fly

```bash
# Use Together AI
export NOVA_AI_PROVIDER="together"
export TOGETHER_API_KEY="your_key"
python nova_cli_modern.py ask "What is AI?"

# Switch back to Groq
export NOVA_AI_PROVIDER="groq"
python nova_cli_modern.py ask "What is ML?"
```

---

## Tips & Tricks

### 1. Create Shell Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias nova='python /path/to/nova_cli_modern.py'
alias nova-ask='nova ask'
alias nova-chat='nova --interactive'

# Then use:
nova-chat
nova-ask "Your question here"
```

### 2. Use with Pipes

```bash
# Analyze a file
cat myfile.py | nova analyze

# Ask question with output
echo "How do I learn Python?" | xargs nova ask
```

### 3. Save Responses to File

```bash
echo "What is REST API?" > question.txt
nova explain REST_API > response.txt
cat response.txt
```

### 4. Create Configuration Script

```bash
#!/bin/bash
# setup_nova.sh

echo "Enter your Groq API Key:"
read -s GROQ_API_KEY

echo "export GROQ_API_KEY='$GROQ_API_KEY'" >> ~/.bashrc
echo "✅ Setup complete! Run: source ~/.bashrc"
```

---

## Next Steps

1. ✅ Get your free API key (5 minutes)
2. ✅ Set environment variable
3. ✅ Test with: `python nova_cli_modern.py ask "Hello"`
4. ✅ Enjoy unlimited AI-powered CLI!

---

## Support & Resources

- **Groq Docs**: https://console.groq.com/docs
- **Together Docs**: https://docs.together.ai
- **OpenRouter Docs**: https://openrouter.ai/docs
- **GitHub Issues**: https://github.com/brextag/CODE_CLI/issues

---

**Happy coding! 🚀**
