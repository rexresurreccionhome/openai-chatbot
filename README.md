# OpenAI Chatbot

An AI chatbot that uses OpenAI's LLM combined with semantic embeddings to deliver intelligent, context-aware responses. The system converts both user questions and knowledge base content into embeddings, then retrieves the most relevant information by comparing their semantic similarity before generating responses.

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