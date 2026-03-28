from agent.agent_state import AgentState
from accessor.storage_client import write_memory


def build_write_memory_node(store_path: str):
    def write_memory_node(state: AgentState):
        user_id = state["user_id"]
        candidates = state.get("new_memory_candidates", [])

        for memory in candidates:
            write_memory(user_id, memory, store_path)

        return {}

    return write_memory_node


def should_write(state):
    if state.get("new_memory_candidates"):
        return "write_memory"
    return "__end__"
