from enum import Enum


class MemoryType(str, Enum):
    NONE = "none"
    FACT = "fact"
    PREFERENCE = "preference"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"
