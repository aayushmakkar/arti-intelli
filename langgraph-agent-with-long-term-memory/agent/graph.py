from typing import Optional

from langgraph.graph import END, StateGraph

from accessor.llm_client import build_openai_client
from agent.agent_state import AgentState
from nodes.distill_new_memory import build_distill_new_memory
from nodes.distill_retrieved import distill_retrieved
from nodes.generate_response import build_generate_response
from nodes.retrieve_memory import build_retrieve_memory
from nodes.write_memory import build_write_memory_node, should_write


def build_graph(store_path: str, model: str, api_key: Optional[str]):
    client = build_openai_client(api_key)

    graph = StateGraph(AgentState)

    graph.add_node("retrieve", build_retrieve_memory(store_path))
    graph.add_node("distill_retrieved", distill_retrieved)
    graph.add_node("generate", build_generate_response(client, model))
    graph.add_node("distill_new", build_distill_new_memory(client, model))
    graph.add_node("write_memory", build_write_memory_node(store_path))

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "distill_retrieved")
    graph.add_edge("distill_retrieved", "generate")
    graph.add_edge("generate", "distill_new")
    graph.add_conditional_edges("distill_new", should_write)
    graph.add_edge("write_memory", END)

    return graph.compile()
