# LangGraph Agent with Long-Term Memory

Minimal CLI chat agent with:
- Long-term memory (LTM) stored in a JSON file.
- OpenAI Responses API call when `OPENAI_API_KEY` is configured.
- A LangGraph workflow that retrieves memories, passes them into the response step, decides whether the latest user message should become memory, and writes new memories back to the store.
- Interactive tracing so you can see retrieval and memory extraction during each turn.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install langgraph openai
```

## Run

```bash
export OPENAI_API_KEY=your_key_here
python langgraph-agent-with-long-term-memory/chat_agent_with_ltm.py --user-id your_username
```

## CLI Options

- `--ltm-path`: path to the LTM JSON file (default: `./ltm_store.json`)
- `--model`: OpenAI model name (default: `gpt-4.1`)
- `--openai-key`: OpenAI API key (default: reads `OPENAI_API_KEY`, falls back to `YOUR_API_KEY`)

## Commands

- `/show_ltm`: display the saved long-term memories for the current user
- `/exit`: quit the chat session

## How It Works

For each user message, the graph runs this sequence:

1. Retrieve the most recent saved memories for the current `user_id`.
2. Distill the retrieved memories into compact context.
3. Generate a reply with the OpenAI Responses API.
4. Use the model to decide whether the latest user message should be saved as new memory.
5. Write any new memories back to the JSON store.

In this chat agent, memory extraction runs automatically after each turn and uses structured JSON output with these memory types: `fact`, `preference`, `episodic`, `procedural`. Retrieval simply loads the 3 most recent saved memories so the LTM effect is easy to observe. Each turn also prints trace output for `retrieve_memory` and `distill_new_memory`. In a production system, retrieval would typically be upgraded to semantic search.
