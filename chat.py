import os

from openai import OpenAI

from config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    CONVERSATION_HISTORY_LIMIT,
)
from kb import KB


def choose_persona() -> list[str] | None:
    personas = os.listdir("personas")
    for i, persona in enumerate(personas):
        print(f"{i + 1}: {persona}")

    user_input = input("Choose a persona: ")
    if user_input.isdigit():
        index = int(user_input) - 1
        if 0 <= index < len(personas):
            return personas[index]

    print("Invalid persona.")
    return None


def start_chat(client: OpenAI, persona: str) -> None:
    kb = KB(client, persona)
    conversation_history = []
    while True:
        user_question = input("User: ")
        prompt = kb.prompt_template.format(
            conversation_history="\n".join(conversation_history[-CONVERSATION_HISTORY_LIMIT:]),
            user_question=user_question,
            relevant_kb_info=kb.find_relevant_kb_info(user_question)
        )
        # print(f"Prompt: {prompt}")
        response = client.responses.create(
            model=LLM_MODEL,
            input=prompt,
        )
        print(f"Assistant: {response.output_text}")
        conversation_history.append(f"User: {user_question}")
        conversation_history.append(f"Assistant: {response.output_text}")


def init_chat():
    print("Welcome to the chat!")
    persona = choose_persona()
    if persona:
        with OpenAI(api_key=OPENAI_API_KEY) as client:
            start_chat(client, persona)
