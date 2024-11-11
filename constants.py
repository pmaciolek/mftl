import ell

#DEFAULT_LLM_MODEL = 'use-dict'
DEFAULT_LLM_MODEL = 'mistral:latest'
#LLM_MODEL = "gpt-4o-2024-08-06"
#LLM_MODEL = "llama3.2:latest"
#LLM_MODEL = "mistral:latest"
# LLM_MODEL = "gemma2:27b"
#LLM_MODEL = "gemma2:latest"
#LLM_MODEL = "qwen2.5:latest"

REPEAT_COUNT = 1

ANONYMIZE = False

# LLM_MODELS = ["llama3.2:latest","gemma2:latest", "qwen2.5:latest", "mistral:latest"]
LLM_MODELS = ["gemma2:latest", "qwen2.5:latest", "mistral:latest"]

# When using Ollama, you need to register the model
ell.models.ollama.register(base_url="http://localhost:11434/v1")
