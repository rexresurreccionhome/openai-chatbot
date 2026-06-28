# OpenAI Chatbot

An AI chatbot that uses OpenAI's LLM combined with semantic embeddings to deliver intelligent, context-aware responses. The system mimics a vector database by storing embeddings of knowledge base content, then compares them with user question embeddings using cosine similarity to retrieve the most relevant information before generating responses.

## Prerequisites

- An OpenAI account with access to the LLM models for chat and embedding generation

## Running Locally

1. Ensure you have Python 3.12 installed
2. Run the chatbot with:
   ```bash
   python main.py
   ```

## Configuration

You can customize the chatbot behavior by setting environment variables. Below are the available options:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | — | Your OpenAI API key for authentication |
| `LLM_MODEL` | No | `gpt-4o-mini` | The LLM model to use for chat responses |
| `EMBEDDING_MODEL` | No | `text-embedding-3-small` | The model to use for generating embeddings |
| `RELEVANCE_THRESHOLD` | No | `0.2` | Minimum similarity score for relevant content (0-1) |
| `RELEVANCE_RETURN_LIMIT` | No | `5` | Maximum number of relevant documents to retrieve |
| `CONVERSATION_HISTORY_LIMIT` | No | `10` | Maximum number of conversation turns to retain |

### Setting Environment Variables

To set environment variables, create a `.env` file in the project root or export them directly:

```bash
export OPENAI_API_KEY="your-api-key-here"
export LLM_MODEL="gpt-4o"
export RELEVANCE_THRESHOLD="0.5"
python main.py
```

## Adding a New Persona and Knowledge Base

The chatbot automatically discovers and loads personas from the `personas/` directory. Here's how to create a new one:

### Directory Structure

```
personas/
  your-persona-name/
    prompt.md
    kb/
      entry1.json
      entry2.json
      entry3.json
```

### Step 1: Create the Persona Folder

Create a new folder under `personas/` with your persona name (e.g., `personas/coffee-shop-assistant/`).

### Step 2: Create Knowledge Base Entries

Inside the persona folder, create a `kb/` subdirectory and add JSON files for each knowledge base entry.

**JSON Entry Format:**
```json
{
  "summary": "A concise, relevant summary of the content",
  "description": "A detailed description with more context and information"
}
```

**Important Notes:**
- The `summary` field is used to compute embeddings, so make it concise and relevant
- The `description` field provides detailed information retrieved alongside the summary
- The `embedding` field is automatically computed and added on the first script run
- Keep summaries focused on key topics for better semantic matching

**Example:**
```json
{
  "summary": "Espresso-based coffee drinks and preparation methods",
  "description": "Our cafe specializes in espresso drinks including lattes, cappuccinos, and americanos. All drinks are made with freshly ground beans and steamed milk."
}
```

### Step 3: Create a Prompt Template

Create a `prompt.md` file in your persona folder that defines how the LLM should respond. The template supports three parameters:

- `{conversation_history}` - Previous conversation turns for context
- `{relevant_kb_info}` - Knowledge base entries matched to the user's question
- `{user_question}` - The current user question

**Example prompt template:**
```markdown
You are a helpful coffee shop assistant. Use the provided context to answer customer questions accurately and friendly.

## Context
{relevant_kb_info}

## Conversation History
{conversation_history}

## User Question
{user_question}

Please provide a helpful and concise response.
```

Once you've set up the folder structure and files, the script will automatically:
1. Discover your new persona
2. Load and process KB entries
3. Compute embeddings for summaries on first run
4. Use the prompt template when generating responses