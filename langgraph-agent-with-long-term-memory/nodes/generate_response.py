from agent.agent_state import AgentState
from accessor.llm_client import build_response_input


def build_generate_response(client, model: str):
    def generate_response(state: AgentState):
        memories = state.get("distilled_memories", [])

        memory_lines = "\n".join(
            f"- [{memory['type']}] {memory['text']}" for memory in memories
        )
        instructions = (
            "You are a helpful chat assistant. "
            "Be very concise. "
            "Use the retrieved long-term memory only when it is relevant."
        )
        if memory_lines:
            instructions += (
                "\n\nRelevant long-term memory for this user:\n"
                f"{memory_lines}"
            )

        response = client.responses.create(
            model=model,
            instructions=instructions,
            input=build_response_input(state["messages"]),
        )

        return {"assistant_reply": response.output_text.strip()}

    return generate_response
