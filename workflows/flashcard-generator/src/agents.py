from llama_index.agent.openai import OpenAIAgent
from pprint import pformat
from enum import Enum
from utils import get_shared_llm  


# Updated Agent Types
class Speaker(str, Enum):
    QA_GENERATOR = "Q&A Generator"
    REVIEWER = "Reviewer"
    TOPIC_ANALYZER = "Topic Analyzer"
    ORCHESTRATOR = "Orchestrator"
    CODE_AND_EXTRA_FIELD_EXPERT = "Code and Extra Field Expert"
    FORMATTER = "Formatter"

# Basic Agent Implementation
def qa_generator_factory() -> OpenAIAgent:
    system_prompt = """
    You are an educational content creator specializing in Anki flashcard generation.
    Your task is to create clear, concise flashcards following these guidelines:

    1. Each card should focus on ONE specific concept
    2. Questions should be clear and unambiguous
    3. Answers should be concise but complete
    4. Include relevant extra information in the extra field
    5. Follow the minimum information principle

    Format each card as:
    <card>
        <question>Your question here</question>
        <answer>Your answer here</answer>
        <extra>Additional context, examples, or explanations</extra>
    </card>
    """

    return OpenAIAgent.from_tools(
        [],
        llm=get_shared_llm(),
        system_prompt=system_prompt,
    )

# Reviewer Agent Implementation
def reviewer_factory() -> OpenAIAgent:
    system_prompt = """
    You are the Reviewer agent. Your task is to review and refine Anki flashcards,
    ensuring they follow the minimum information principle.

    Core Review Rules:
    1. Verify each card follows the minimum information principle
    2. Check that Q&A pairs are simple and atomic
    3. Ensure appropriate use of cloze deletions
    4. Verify extra field provides valuable context

    Review Checklist:
    1. Each card should test ONE piece of information
    2. Questions must be:
       - Simple and direct
       - Testing a single fact
       - Using cloze format when appropriate
    3. Answers must be:
       - Brief and precise
       - Limited to essential information
    4. Extra field must include:
       - Detailed explanations
       - Examples
       - Context
    """

    return OpenAIAgent.from_tools(
        [],
        llm=get_shared_llm(),
        system_prompt=system_prompt,
    )

# Topic Analyzer Implementation
def topic_analyzer_factory(state: dict) -> OpenAIAgent:
    system_prompt = f"""
    You are the Topic Analyzer agent. Your task is to analyze the given text and identify key topics for flashcard creation.
    
    Current State:
    {pformat(state, indent=2)}
    
    Instructions:
    1. Identify main concepts, sub-concepts, and their relationships
    2. Create a hierarchical structure of topics
    3. Highlight potential areas for deep-dive questions
    4. Identify cross-cutting themes or principles
    5. Suggest real-world applications or case studies

    Output format:
    <topics>
        <topic>
            <name>Main topic name</name>
            <subtopics>
                <subtopic>Subtopic 1</subtopic>
                <subtopic>Subtopic 2</subtopic>
            </subtopics>
            <applications>Potential real-world applications</applications>
            <prerequisites>Foundational knowledge needed</prerequisites>
        </topic>
    </topics>
    """

    return OpenAIAgent.from_tools(
        [],
        llm=get_shared_llm(),
        system_prompt=system_prompt,
        verbose=True
    )

# Code and Extra Field Expert Implementation
def code_and_extra_field_expert_factory() -> OpenAIAgent:
    system_prompt = """
    You are the Code and Extra Field Expert agent. Your task is to enhance Anki flashcards
    by adding relevant code snippets and comprehensive extra content.

    Instructions:
    1. Add clear, concise code examples that illustrate key concepts
    2. Ensure code snippets are well-commented and easy to understand
    3. In the extra field, provide:
       - Step-by-step explanations of code snippets 
       - Common use cases and scenarios
       - Potential pitfalls and edge cases
       - Best practices and optimization tips
    4. Use appropriate markdown formatting for code blocks
    5. Include relevant documentation links
    6. Ensure explanations are clear for a 15-year-old
    """

    return OpenAIAgent.from_tools(
        [],
        llm=get_shared_llm(),
        system_prompt=system_prompt,
    )

# Formatter Agent Implementation
def formatter_agent_factory() -> OpenAIAgent:
    system_prompt = """
    You are the Formatter agent. Your task is to ensure proper XML structure and markdown
    formatting in the flashcards.

    Formatting Rules:
    1. Maintain valid XML structure
    2. Properly escape special characters
    3. Format code blocks with appropriate language tags
    4. Use consistent indentation
    5. Ensure markdown compatibility
    6. Preserve code snippets exactly as provided
    7. Handle nested structures properly
    """

    return OpenAIAgent.from_tools(
        [],
        llm=get_shared_llm(),
        system_prompt=system_prompt,
    )


# Orchestrator Implementation
def orchestrator_factory(state: dict) -> OpenAIAgent:
    system_prompt = f"""
    You are the Orchestrator agent. Your task is to coordinate the interaction between all agents to create high-quality flashcards.

    Current State:
    {pformat(state, indent=2)}

    Available agents:
    * Topic Analyzer - Breaks down complex topics into structured hierarchical concepts
    * Q&A Generator - Creates flashcards from topics or content
    * Reviewer - Reviews and improves card quality, accuracy, and clarity
    
    Decision Guidelines:
    - Analyze the current state and quality of outputs to decide the next best action
    - You can choose any agent at any time based on need:
        * Use Topic Analyzer when you need better topic understanding or structure, it's the first agent to run
        * Use Q&A Generator when you need new or additional cards
        * Use Reviewer when cards need quality improvement
        * Choose END when the cards are comprehensive and high quality
    
    Examples of flexible decisions:
    - If topic analysis seems incomplete, you can run Topic Analyzer again
    - If cards need improvement, use Reviewer multiple times
    - If cards miss important topics, go back to Q&A Generator
    - If everything looks good, choose END

    Evaluate:
    1. Are the topics well-structured and comprehensive?
    2. Do the cards cover all important concepts?
    3. Are the cards clear, accurate, and well-written?
    4. Is there a good balance of basic and advanced concepts?

    Output only the next agent to run ("Topic Analyzer", "Q&A Generator", "Reviewer", or "END")
    """

    return OpenAIAgent.from_tools(
        [],
        llm=get_shared_llm(),
        system_prompt=system_prompt,
    )
