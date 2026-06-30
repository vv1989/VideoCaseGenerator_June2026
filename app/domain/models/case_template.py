from dataclasses import dataclass
from typing import List

@dataclass
class ActorTemplate:
    actor_id: str
    gender: str
    nationality: str
    age_range: str
    image_folder: str
    voice: str

@dataclass
class CaseTemplate:
    template_id: str
    actors: List[ActorTemplate]