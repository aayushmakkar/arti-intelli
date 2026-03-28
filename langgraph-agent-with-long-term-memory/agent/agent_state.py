from typing import Any, Dict, List, TypedDict


class AgentState(TypedDict, total=False):
    user_id: str
    messages: List[Dict[str, str]]
    retrieved_memories: List[Dict[str, Any]]
    distilled_memories: List[Dict[str, Any]]
    assistant_reply: str
    new_memory_candidates: List[Dict[str, Any]]
