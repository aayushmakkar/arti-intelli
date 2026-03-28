import json
import os
from typing import Any, Dict


DEFAULT_STORE_PATH = "./ltm_store.json"


def load_store(store_path: str) -> Dict[str, Any]:
    if not os.path.exists(store_path):
        return {}
    with open(store_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_store(store_path: str, data: Dict[str, Any]) -> None:
    with open(store_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def get_memories(user_id: str, store_path: str):
    store = load_store(store_path)
    return store.get(user_id, [])


def write_memory(user_id: str, memory: Dict[str, Any], store_path: str) -> None:
    store = load_store(store_path)
    store.setdefault(user_id, [])
    store[user_id].append(memory)
    save_store(store_path, store)
