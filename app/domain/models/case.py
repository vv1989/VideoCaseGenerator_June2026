from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Actor:
    actor_id: str
    name: str
    role: str
    personality_traits: List[str]


@dataclass
class Scene:
    scene_id: str
    sequence: int
    speaker: str
    actor_id: Optional[str]
    text: str


@dataclass
class Case:
    case_id: str
    title: str
    topic: str
    dilemma: str
    setting: str

    actors: List[Actor]
    scenes: List[Scene]

    # Contains image-generation instructions returned by the LLM
    visual_plan: Dict[str, Any] = field(default_factory=dict)

    # Populated after images are generated
    generated_images: Dict[str, str] = field(default_factory=dict)