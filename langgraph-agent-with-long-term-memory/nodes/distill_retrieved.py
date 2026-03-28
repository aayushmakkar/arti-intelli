from agent.agent_state import AgentState


def distill_retrieved(state: AgentState):
    retrieved = state.get("retrieved_memories", [])

    distilled = []
    for memory in retrieved:
        distilled.append(
            {
                "text": memory["text"],
                "type": memory["type"],
            }
        )

    return {"distilled_memories": distilled}
