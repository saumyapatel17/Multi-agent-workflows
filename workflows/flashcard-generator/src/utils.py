import os
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from tenacity import retry, stop_after_attempt, wait_exponential, TryAgain
from llama_index.core.prompts import ChatPromptTemplate 
from llama_index.core.llms import ChatMessage
import xml.etree.ElementTree as ET
from models import Flashcard_model

# LLM Configuration
def get_shared_llm():
    """Returns a shared LLM instance for all agents."""
    api_base = os.getenv("API_BASE")
    api_key = os.getenv("API_KEY")
    model = os.getenv("MODEL")
    temperature = float(os.getenv("TEMPERATURE"))

    return OpenAI(model=model, temperature=temperature, api_base=api_base, api_key=api_key)

# Enhanced Error Handling and Validation
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def validate_and_transform(message: str) -> dict:
    try:
        # Transform to structured data
        chat_prompt_tmpl = ChatPromptTemplate(
            message_templates=[
                ChatMessage.from_str(message, role="user")
            ]
        )
        structured_data = get_shared_llm().structured_predict(
            Flashcard_model, 
            chat_prompt_tmpl
        )
        return structured_data.model_dump()
        
    except ET.ParseError as e:
        print(f"XML validation error: {str(e)}")
        raise TryAgain
    except Exception as e:
        print(f"Transformation error: {str(e)}")
        raise TryAgain
    
# Memory Management
def setup_memory() -> ChatMemoryBuffer:
    return ChatMemoryBuffer.from_defaults(token_limit=8000)

# Enhanced State Management
def get_initial_state(text: str) -> dict:
    return {
        "input_text": text,
        "topics": "",
        "qa_cards": "",
        "review_status": "pending",
        "has_code": False,
        "formatting_status": "pending"
    }