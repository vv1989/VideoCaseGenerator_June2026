import json
from pathlib import Path

from app.domain.models.case_template import CaseTemplate, ActorTemplate


class TemplateLoader:
    def __init__(self):
        self.templates_path = Path("app/templates")

    def load(self, template_id: str) -> CaseTemplate:
        config_path = self.templates_path / template_id / "config.json"

        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        actors = []

        for actor in data["actors"]:
            actors.append(
                ActorTemplate(
                    actor_id=actor["actor_id"],
                    gender=actor["gender"],
                    nationality=actor["nationality"],
                    age_range=actor["age_range"],
                    image_folder=actor["image_folder"],
                    voice=actor["voice"],
                )
            )

        return CaseTemplate(
            template_id=data["template_id"],
            actors=actors,
        )