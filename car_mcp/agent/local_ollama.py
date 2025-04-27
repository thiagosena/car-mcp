"""
Ollama LLM configuration module.

This module initializes and configures the Ollama Large Language Model using langchain.
It sets up the model with specific parameters from the config module, including
temperature, repeat penalty, and timeout settings. The model is configured to stop
generation at specific tokens to maintain conversation format.

Dependencies:
    - config: Local configuration module for Ollama settings
    - langchain_ollama: For OllamaLLM implementation
"""

from langchain_ollama import OllamaLLM

from car_mcp import config

llm = OllamaLLM(
    model=config.OLLAMA_MODEL,
    base_url=config.OLLAMA_BASE_URL,
    temperature=config.OLLAMA_TEMPERATURE,
    repeat_penalty=config.OLLAMA_REPEAT_PENALTY,
    timeout=config.OLLAMA_TIMEOUT,
    stop=[
        "\n\n",
        "Human:",
        "Assistant:",
    ],
)
