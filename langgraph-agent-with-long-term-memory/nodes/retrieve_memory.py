from agent.agent_state import AgentState
from accessor.storage_client import get_memories


def build_retrieve_memory(store_path: str):
    def retrieve_memory(state: AgentState):
        user_id = state["user_id"]

        memories = get_memories(user_id, store_path)
        # For this simple chat agent, retrieval is recency-based: always surface the latest
        # few memories so the LTM effect is easy to observe in conversation.
        # A more robust long-term memory system would upgrade this to semantic
        # similarity search so retrieval is based on meaning, not just recency.
        retrieved = list(reversed(memories[-3:]))
        return {"retrieved_memories": retrieved}

    return retrieve_memory
