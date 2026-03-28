#!/usr/bin/env python3

"""
LangGraph LTM demo with full lifecycle:

- Read memory
- Distill retrieved memory
- Generate response with an LLM
- Distill new memory
- Write memory

Run:
pip install langgraph openai
export OPENAI_API_KEY=your_api_key
python chat_agent_with_ltm.py --user-id your_user_id
"""

import argparse
import os
from accessor.llm_client import DEFAULT_MODEL
from accessor.storage_client import DEFAULT_STORE_PATH, get_memories
from agent.graph import build_graph


# -------------------------
# CLI
# -------------------------

def print_turn_trace(result):
    retrieved_memories = result.get("retrieved_memories", [])
    new_memory_candidates = result.get("new_memory_candidates", [])

    print("Trace> retrieve_memory")
    if retrieved_memories:
        for index, memory in enumerate(retrieved_memories, start=1):
            print(f"Trace> {index}. [{memory['type']}] {memory['text']}")
    else:
        print("Trace> none")

    print("Trace> distill_new_memory")
    if new_memory_candidates:
        for index, memory in enumerate(new_memory_candidates, start=1):
            print(f"Trace> {index}. will save [{memory['type']}] {memory['text']}")
    else:
        print("Trace> none")


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--ltm-path", default=DEFAULT_STORE_PATH)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--openai-key",
        default=os.getenv("OPENAI_API_KEY", "YOUR_API_KEY"),
    )

    args = parser.parse_args()

    app = build_graph(
        store_path=args.ltm_path,
        model=args.model,
        api_key=args.openai_key,
    )

    messages = []

    print("LTM Agent Started:")
    print("- chat: ask a question or continue the conversation")
    print("- long-term memory is extracted automatically after each user turn")
    print("- /show_ltm: display saved long-term memories for this user")
    print("- /exit: quit")

    while True:

        user_input = input("You> ")

        if user_input == "/exit":
            break
        if user_input == "/show_ltm":
            memories = get_memories(args.user_id, args.ltm_path)
            print(f"Saved LTM for user '{args.user_id}':")
            if memories:
                for index, memory in enumerate(memories, start=1):
                    print(f"{index}. [{memory['type']}] {memory['text']}")
            else:
                print("(none)")
            continue

        messages.append({"role": "user", "content": user_input})

        state = {
            "user_id": args.user_id,
            "messages": messages
        }

        result = app.invoke(state)
        print_turn_trace(result)

        reply = result["assistant_reply"]

        print("Assistant>", reply)

        messages.append({
            "role": "assistant",
            "content": reply
        })


if __name__ == "__main__":
    main()
