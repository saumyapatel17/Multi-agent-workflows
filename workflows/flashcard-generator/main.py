from dotenv import load_dotenv
from llama_index.core.llms import ChatMessage
from utils import (
    get_initial_state, 
    setup_memory,
    validate_and_transform
)
from src.agents import (
    qa_generator_factory,
    reviewer_factory,
    topic_analyzer_factory,
    code_and_extra_field_expert_factory,
    formatter_agent_factory,
    orchestrator_factory,
    Speaker
)

# Load environment variables from the .env file
load_dotenv()


# Main Function
def generate_anki_cards(input_text: str) -> dict:
    # Initialize state and memory
    state = get_initial_state(input_text)
    memory = setup_memory()
    
    # Detect if input contains code
    state["has_code"] = "```" in input_text or "code" in input_text.lower()
    
    while True:
        # Get current chat history
        current_history = memory.get()
        
        # Let Orchestrator decide next step
        orchestrator = orchestrator_factory(state)
        next_agent = str(orchestrator.chat(
            "Decide which agent to run next based on the current state.",
            chat_history=current_history
        )).strip().strip('"').strip("'")
        print(f"\nOrchestrator selected: {next_agent}")
        
        if next_agent == "END":
            print("\nOrchestrator decided to end the process")
            break
            
        # Execute selected agent
        try:
            if next_agent == Speaker.TOPIC_ANALYZER.value:
                analyzer = topic_analyzer_factory()
                response = analyzer.chat(
                    f"Analyze this text for flashcard topics:\n\n{state['input_text']}",
                    chat_history=current_history
                )
                state["topics"] = str(response)
                print("\nTopic Analysis Results:")
                print(state["topics"])
                
            elif next_agent == Speaker.QA_GENERATOR.value:
                generator = qa_generator_factory()
                response = generator.chat(
                    f"Generate flashcards for this topic:\n\n{state['topics']}",
                    chat_history=current_history
                )
                state["qa_cards"] = str(response)
                print("\nGenerated Cards:")
                print(state["qa_cards"])
                
            elif next_agent == Speaker.CODE_AND_EXTRA_FIELD_EXPERT.value:
                expert = code_and_extra_field_expert_factory()
                response = expert.chat(
                    f"Enhance these flashcards with code examples and detailed explanations:\n\n{state['qa_cards']}",
                    chat_history=current_history
                )
                state["qa_cards"] = str(response)
                print("\nEnhanced Cards with Code Examples:")
                print(state["qa_cards"])
                
            elif next_agent == Speaker.REVIEWER.value:
                reviewer = reviewer_factory()
                response = reviewer.chat(
                    f"Review these flashcards:\n\n{state['qa_cards']}",
                    chat_history=current_history
                )
                state["qa_cards"] = str(response)
                state["review_status"] = "reviewed"
                print("\nReviewed Cards:")
                print(state["qa_cards"])
                
            elif next_agent == Speaker.FORMATTER.value:
                formatter = formatter_agent_factory()
                response = formatter.chat(
                    f"Format these flashcards:\n\n{state['qa_cards']}",
                    chat_history=current_history
                )
                state["qa_cards"] = str(response)
                state["formatting_status"] = "completed"
                print("\nFormatted Cards:")
                print(state["qa_cards"])
            
            # Update memory with new interaction
            memory.put(ChatMessage(role="assistant", content=str(response)))
            print(f"\nUpdated memory with {next_agent}'s response")
            
        except Exception as e:
            print(f"\nError in {next_agent}: {str(e)}")
            continue
    
    # Final validation and transformation
    try:
        final_cards = validate_and_transform(state["qa_cards"])
        return final_cards
    except Exception as e:
        print(f"\nError in final transformation: {str(e)}")
        return {}

if __name__ == "__main__":
    # Example text with concepts and code that needs to be converted into flashcards.
    sample_text = """
    To calculate the RSI (Relative Strength Index) in Python, you typically use 
    technical analysis libraries like pandas-ta or the ta library. The RSI is 
    calculated using the average gains and losses over a specified period 
    (usually 14 periods). Here's how you can implement it:

    1. Using the ta library:
    ```python
    import pandas as pd
    import ta
    
    # Assuming you have price data in a DataFrame
    df['RSI'] = ta.momentum.RSIIndicator(
        close=df['close'],
        window=14
    ).rsi()
    ```

    2. Manual implementation:
    ```python
    def calculate_rsi(data, periods=14):
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(
            window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(
            window=periods).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    ```
    """
    
    flashcards = generate_anki_cards(sample_text)
    print("Generated Flashcards with Code Examples:")
    print(flashcards)