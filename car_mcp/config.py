"""
Configuration module for the application.

This module manages environment variables for both Ollama and OpenAI configurations.

Environment Variables:
    OLLAMA_MODEL (str): The model name to be used with Ollama
    OLLAMA_BASE_URL (str): Base URL for Ollama API
    OLLAMA_TEMPERATURE (float): Temperature setting for response generation (default: 0.7)
    OLLAMA_REPEAT_PENALTY (float): Penalty for repeated content (default: 1.1)
    OLLAMA_TIMEOUT (int): Timeout in seconds for Ollama API calls (default: 120)
"""

import os

OLLAMA_MODEL=os.getenv("OLLAMA_MODEL", "")
OLLAMA_BASE_URL=os.getenv("OLLAMA_BASE_URL", "")
OLLAMA_TEMPERATURE=float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))
OLLAMA_REPEAT_PENALTY=float(os.getenv("OLLAMA_REPEAT_PENALTY", "1.1"))
OLLAMA_TIMEOUT=int(os.getenv("OLLAMA_TIMEOUT", "120"))

MCP_SERVER_URL=os.getenv("MCP_SERVER_URL", "http://localhost:8000/sse")
