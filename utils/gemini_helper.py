"""
gemini_helper.py — Google Gemini API Integration
=================================================
Handles all communication with the Gemini generative AI model.
Encapsulates configuration, safety settings, and response generation
so the UI layer (app.py) never touches the SDK directly.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Load environment variables from .env (no-op in Cloud Run where env is set)
load_dotenv()

# System prompt that restricts scope and controls output length
SYSTEM_PROMPT = """You are "Election Buddy", a friendly, non-partisan AI assistant \
that educates users about democratic election processes around the world.

RULES YOU MUST FOLLOW:
1. Only answer questions related to elections, voting, democracy, and civic processes.
2. If a user asks something unrelated, politely redirect them back to election topics.
3. Never express political opinions or endorse any candidate, party, or ideology.
4. Keep every response concise — aim for 150-250 words maximum.
5. Use simple, accessible language that a high-school student can understand.
6. When discussing specific countries, clearly label which country you are referring to.
7. Cite well-known, publicly verifiable sources when possible (e.g., official election \
   commission websites).
8. Format responses using Markdown for readability (headers, bullet points, bold text).
"""

# Default model — can be overridden via environment variable
DEFAULT_MODEL = "gemini-2.5-flash-lite"


def _get_api_key() -> str:
    """Retrieve the Gemini API key from environment variables.

    Returns:
        str: The API key.

    Raises:
        ValueError: If the key is not set or is the placeholder value.
    """
    key = os.getenv("GEMINI_API_KEY", "")
    if not key or key == "your_gemini_api_key_here":
        raise ValueError(
            "GEMINI_API_KEY is not configured. "
            "Please set it in your .env file or environment variables. "
            "Get a free key at https://aistudio.google.com/apikey"
        )
    return key


def configure_genai() -> None:
    """Configure the google-generativeai SDK with the API key."""
    genai.configure(api_key=_get_api_key())


def get_model(model_name: str | None = None) -> genai.GenerativeModel:
    """Create and return a configured Gemini GenerativeModel instance.

    Args:
        model_name: Optional model override. Defaults to DEFAULT_MODEL or
                     the GEMINI_MODEL environment variable.

    Returns:
        genai.GenerativeModel: The configured model instance.
    """
    configure_genai()
    name = model_name or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)

    model = genai.GenerativeModel(
        model_name=name,
        system_instruction=SYSTEM_PROMPT,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=512,      # Hard cap to control cost & latency
            temperature=0.7,            # Balanced creativity vs. accuracy
        ),
    )
    return model


def get_chat_session(model: genai.GenerativeModel, history: list | None = None):
    """Start or resume a chat session with conversation history.

    Args:
        model: A configured GenerativeModel instance.
        history: Optional list of previous messages to resume from.

    Returns:
        genai.ChatSession: An active chat session.
    """
    return model.start_chat(history=history or [])


def send_message(chat_session, user_message: str) -> str:
    """Send a user message and return the model's text response.

    Args:
        chat_session: An active Gemini ChatSession.
        user_message: The user's input string.

    Returns:
        str: The model's response text.

    Raises:
        RuntimeError: If the API call fails.
    """
    try:
        response = chat_session.send_message(user_message)
        return response.text
    except Exception as exc:
        raise RuntimeError(
            f"Gemini API error: {exc}. "
            "Please check your API key and network connection."
        ) from exc
