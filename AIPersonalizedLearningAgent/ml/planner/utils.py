import os

def check_api_credentials():
    """
    Checks for the presence of OpenAI or Gemini API credentials.
    """
    openai_key = os.environ.get("OPENAI_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    
    status = {
        "openai_available": openai_key is not None,
        "gemini_available": gemini_key is not None,
        "any_available": (openai_key is not None) or (gemini_key is not None)
    }
    return status

def format_section_header(title):
    """
    Formated pretty logs header.
    """
    border = "=" * len(title)
    return f"\n{border}\n{title}\n{border}\n"
