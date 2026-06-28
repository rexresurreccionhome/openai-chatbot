
import os
import json
from sentence_transformers import util

from openai import OpenAI

from config import (
    EMBEDDING_MODEL,
    RELEVANCE_THRESHOLD,
    RELEVANCE_RETURN_LIMIT,
)


class KB:
    PERSONAS_KB_DIR = "personas/{persona}/kb"
    NO_RELEVANT_INFO_MSG = "No relevant information found in the knowledge base."

    def __init__(self, client: OpenAI, persona: str):
        self._client = client
        self._prompt_template = self._get_prompt_template(persona)
        self._kb_embeddings = self._get_kb_embeddings(persona)

    @staticmethod
    def _get_prompt_template(persona: str) -> str:
       with open(f"personas/{persona}/prompt.md", "r") as file:
           return file.read()


    def _create_embedding(self, text: str) -> list[float]:
        model = self._client.embeddings.create(model=EMBEDDING_MODEL, input=[text])
        return model.data[0].embedding
    
    def _get_kb_embeddings(self, persona: str) -> dict[str, list[float]]:
        kb_embeddings = {}
        persona_kb_dir = self.PERSONAS_KB_DIR.format(persona=persona)
        for file_name in os.listdir(persona_kb_dir):
            persona_kb_full_path = os.path.join(persona_kb_dir, file_name)
            if file_name.endswith(".json") and os.path.isfile(persona_kb_full_path):
                with open(persona_kb_full_path, "r+") as file:
                    kb_entry = json.load(file)
                    if not kb_entry.get("embedding"):
                        kb_entry["embedding"] = self._create_embedding(kb_entry["summary"])
                        file.seek(0)
                        json.dump(kb_entry, file)
                        file.truncate()  # truncate the file to remove any leftover data after writing the new content
                    kb_embeddings[persona_kb_full_path] = kb_entry["embedding"]

        return kb_embeddings

    @property
    def prompt_template(self) -> str:
        return self._prompt_template

    def find_relevant_kb_info(self, user_question: str) -> str:
        question_embedding = self._create_embedding(user_question)
        relevant_entries = []
        for persona_kb_full_path, kb_embedding in self._kb_embeddings.items():
            similarity = util.cos_sim(question_embedding, kb_embedding)
            if similarity >= RELEVANCE_THRESHOLD:
                with open(persona_kb_full_path, "r+") as file:
                    print(persona_kb_full_path)
                    kb_entry = json.load(file)
                    relevant_entries.append(
                        (f"[Source: {os.path.basename(persona_kb_full_path)}]\n\n{kb_entry['summary']}\n\n{kb_entry['description']}", similarity)
                    )

        top_relevant_entries = sorted(
            relevant_entries, key=lambda x: x[1], reverse=True
        )[:RELEVANCE_RETURN_LIMIT]

        return "\n\n".join([entry[0] for entry in top_relevant_entries]) or self.NO_RELEVANT_INFO_MSG
