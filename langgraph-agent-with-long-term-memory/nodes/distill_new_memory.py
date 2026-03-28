import json
from datetime import datetime

from agent.agent_state import AgentState
from agent.memory_type import MemoryType
from accessor.llm_client import build_response_input


def build_distill_new_memory(client, model: str):
    def distill_new_memory(state: AgentState):
        instructions = (
            "You extract long-term memory from a chat conversation.\n"
            "Only save stable user information that will likely matter in future conversations.\n"
            "Good memories include enduring preferences, profile facts, and long-term goals.\n"
            "Do not save temporary requests, one-off tasks, or information that is unlikely to matter later.\n"
            f"Use one of these memory types: {', '.join(memory_type.value for memory_type in MemoryType)}.\n"
            f"If nothing should be saved, set should_save to false, memory_text to an empty string, and memory_type to {MemoryType.NONE.value}."
        )

        response = client.responses.create(
            model=model,
            instructions=instructions,
            input=build_response_input(state["messages"]),
            text={
                "format": {
                    "type": "json_schema",
                    "name": "memory_extraction",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "should_save": {"type": "boolean"},
                            "memory_text": {"type": "string"},
                            "memory_type": {
                                "type": "string",
                                "enum": [memory_type.value for memory_type in MemoryType],
                            },
                        },
                        "required": ["should_save", "memory_text", "memory_type"],
                        "additionalProperties": False,
                    },
                }
            },
        )

        payload = json.loads(response.output_text)
        if not payload.get("should_save"):
            return {"new_memory_candidates": []}

        memory_type = payload["memory_type"].strip()
        memory = {
            "text": payload["memory_text"].strip(),
            "type": memory_type or MemoryType.FACT.value,
            "timestamp": datetime.utcnow().isoformat(),
        }
        if not memory["text"] or memory["type"] == MemoryType.NONE.value:
            return {"new_memory_candidates": []}

        return {"new_memory_candidates": [memory]}

    return distill_new_memory
