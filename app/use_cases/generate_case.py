import json
import uuid
import re
from collections import Counter
from app.domain.models.case import Case, Actor, Scene


class GenerateCase:

    def __init__(
        self,
        text_llm,
        max_retries=1,
        debug=True
    ):

        self.text_llm = text_llm
        self.max_retries = max_retries
        self.debug = debug

    # ==================================================
    # 🖨️ DEBUG PRINT
    # ==================================================

    def _log(self, msg):
        if self.debug:
            print(msg)

    # ==================================================
    # 🎯 MAIN EXECUTION
    # ==================================================

    # def execute(self, topic: str, dilemma: str):
    def execute(self, topic: str, dilemma: str, template):

        best_data = None
        best_score = -1
        last_prompt = None

        for attempt in range(self.max_retries):
            self._log(f"\n🔁 ===== Attempt {attempt + 1} =====")

            prompt = self._build_prompt(topic, dilemma, template)
            last_prompt = prompt

            self._log("\n🧠 PROMPT SENT:\n" + prompt[:500] + "...")

            response = self.text_llm.generate(prompt)

            self._log("\n📦 RAW LLM RESPONSE:\n" + str(response)[:1000])

            data = self._parse_json(response)

            if not data:
                self._log("❌ JSON parsing failed")
                continue

            self._log("\n✅ PARSED JSON:")
            self._log(json.dumps(data, indent=2)[:1000])

            is_valid = self._validate(data)

            if not is_valid:
                self._log("⚠️ Validation failed → attempting repair")

                repaired = self._repair(data)

                if repaired:
                    self._log("\n🛠️ REPAIRED JSON:")
                    self._log(json.dumps(repaired, indent=2)[:1000])
                    data = repaired
                else:
                    self._log("❌ Repair failed")

            score = self._score(data)
            self._log(f"⭐ Score: {score}")

            if score > best_score:
                best_score = score
                best_data = data

            if score >= 4:
                self._log("🏆 Good enough — stopping early")
                break

        if not best_data:
            raise ValueError("❌ No valid outputs generated")

        self._log(f"\n🏆 BEST SCORE SELECTED: {best_score}")

        self._print_full_output(last_prompt, best_data)

        case = self._build_case(best_data, topic, dilemma)

        # 👉 NEW: Human-readable output
        self._print_human_readable(case)

        return case

    # ==================================================
    # 🧠 PROMPT
    # ==================================================

    # ==================================================
    # 🧠 PROMPT
    # ==================================================

    def _build_actor_constraints(self, template):

        lines = []

        for i, actor in enumerate(template.actors, start=1):

            gender = "woman" if actor.gender.lower() == "female" else "man"

            lines.append(
                f"""Actor {i}:
    - {actor.nationality} {gender}
    - Age {actor.age_range}
    """
            )

        return "\n".join(lines)

    def _build_prompt(self, topic, dilemma, template):
        actor_constraints = self._build_actor_constraints(template)
        return f"""

You are generating a short business school case in a nice documentary style.

Return ONLY valid JSON.

{{
  "setting": "...",
  "actors": [
    {{"name": "...", "role": "..."}},
    {{"name": "...", "role": "..."}},
    {{"name": "...", "role": "..."}}
  ],
  "scenes": [
    {{"type": "narrator", "text": "..."}},
    {{"type": "actor", "speaker": "...", "text": "..."}}
  ],
  "visual_plan": {{
    "cover_image": "...",
    "actors": [
      {{"name": "...", "image_prompt": "..."}}
    ],
    "scene_images": [
      {{"scene_id": "...", "image_prompt": "..."}}
    ],
    "closing_image": "..."
  }}
}}

--------------------------------------
STRUCTURE
--------------------------------------

Scene 1 → narrator

Actors appear in interview format across 3 rounds.
Each actor speaks directly to the camera or interviewer.

Final scene → narrator

Total scenes ~10–12

--------------------------------------
DOCUMENTARY STYLE RULES
--------------------------------------

1. The narrator appears ONLY in the first and final scenes.

2. The opening narrator scene should establish the setting, stakes, and central dilemma.

3. The closing narrator scene should restate the decision facing the protagonists and leave the dilemma unresolved.

4. Actor scenes should feel like documentary interviews ("talking-head" format).

5. Actors do NOT speak to each other and do NOT appear to be participating in a conversation.

6. Actors should NOT mention, quote, reference, agree with, disagree with, or respond to any other actor.

7. Each actor should present their own perspective as if responding to an interviewer’s question.

8. Successive actor scenes should feel like answers to different interview questions about the same issue rather than a dialogue.

9. The viewpoints may naturally contrast, but the contrast should emerge from the content itself, not from direct interaction between actors.

10. The case must contain exactly three actors.

{actor_constraints}

Do not introduce any additional speaking characters.
All dialogue must be assigned to one of these three actors or the narrator.

--------------------------------------
VISUAL PLAN REQUIREMENTS
--------------------------------------

- Cover image: realistic setting
- Actor images: front-facing, photorealistic
- Scene images: reflect scene context
- Closing image: symbolic decision moment

--------------------------------------

Topic: {topic}

Dilemma: {dilemma}

"""

    # ==================================================
    # ⭐ SCORING
    # ==================================================

    def _score(self, data):

        score = 0
        actors = data.get("actors", [])
        scenes = data.get("scenes", [])

        if len(actors) == 3:
            score += 1

        if 9 <= len(scenes) <= 13:
            score += 1

        if scenes and scenes[0].get("type") == "narrator":
            score += 1

        if scenes and scenes[-1].get("type") == "narrator":
            score += 1

        if "visual_plan" in data:
            score += 1

        return score

    # ==================================================
    # 🖨️ OUTPUT PRINT
    # ==================================================

    def _print_full_output(self, prompt, data):

        print("\n================ PROMPT USED ================\n")
        print(prompt)

        print("\n================ VISUAL PLAN ================\n")
        print(json.dumps(data.get("visual_plan", {}), indent=2))

        self._print_image_prompts(data)

    def _print_image_prompts(self, data):

        vp = data.get("visual_plan", {})

        print("\n🎨 ===== IMAGE PROMPTS =====\n")

        if "cover_image" in vp:
            print("📌 COVER IMAGE:")
            print(vp["cover_image"], "\n")

        for actor in vp.get("actors", []):
            print(f"👤 ACTOR: {actor.get('name')}")
            print(actor.get("image_prompt"), "\n")

        for scene in vp.get("scene_images", []):
            print(f"🎬 SCENE {scene.get('scene_id')}:")
            print(scene.get("image_prompt"), "\n")

        if "closing_image" in vp:
            print("🏁 CLOSING IMAGE:")
            print(vp["closing_image"], "\n")

    # ==================================================
    # 📖 HUMAN READABLE OUTPUT
    # ==================================================

    def _print_human_readable(self, case: Case):

        print("\n================ CASE (HUMAN READABLE) ================\n")

        print(f"📌 Title: {case.title}")
        print(f"📚 Topic: {case.topic}")
        print(f"⚖️ Dilemma: {case.dilemma}\n")

        print(f"🏢 Setting:\n{case.setting}\n")

        print("👥 Actors:")
        for actor in case.actors:
            print(f"- {actor.name} ({actor.role})")
        print("\n")

        print("🎬 Scenes:\n")

        for scene in case.scenes:
            label = "Narrator" if scene.speaker == "narrator" else scene.speaker
            print(f"Scene {scene.sequence + 1}")
            print(f"[{label}]: {scene.text}\n")

        print("======================================================\n")

    # ==================================================
    # 🔧 REPAIR
    # ==================================================

    def _repair(self, data):

        prompt = f"""
Fix this JSON to satisfy ALL rules:

- Exactly 3 actors
- 9–12 scenes
- Narrator only first and last
- Each actor appears ≥ 3 times
- Actors interact

Return ONLY valid JSON.

INPUT:
{json.dumps(data)}
"""

        response = self.text_llm.generate(prompt)
        return self._parse_json(response)

    # ==================================================
    # 🧾 PARSE
    # ==================================================

    def _parse_json(self, response):

        try:
            return json.loads(response)
        except:
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    return None
        return None

    # ==================================================
    # 🔍 VALIDATE
    # ==================================================

    def _validate(self, data):

        actors = data.get("actors", [])
        scenes = data.get("scenes", [])

        if len(actors) != 3:
            return False

        if not (9 <= len(scenes) <= 13):
            return False

        if scenes[0].get("type") != "narrator":
            return False

        if scenes[-1].get("type") != "narrator":
            return False

        return True

    # ==================================================
    # 🧱 BUILD CASE
    # ==================================================

    def _build_case(self, data, topic, dilemma):

        actor_map = {}
        actors = []

        for i, a in enumerate(data["actors"]):
            actor_id = f"a{i}"
            actor_map[a["name"]] = actor_id

            actors.append(
                Actor(
                    actor_id=actor_id,
                    name=a["name"],
                    role=a["role"],
                    personality_traits=[]
                )
            )

        scenes = []

        for i, s in enumerate(data["scenes"]):

            if s["type"] == "narrator":
                speaker = "narrator"
                actor_id = None
            else:
                speaker = s["speaker"]
                actor_id = actor_map.get(speaker)

            scenes.append(
                Scene(
                    scene_id=f"s{i}",
                    sequence=i,
                    speaker=speaker,
                    actor_id=actor_id,
                    text=s["text"]
                )
            )

        return Case(
            case_id=str(uuid.uuid4()),
            title="Generated Case",
            topic=topic,
            dilemma=dilemma,
            setting=data.get("setting", ""),
            actors=actors,
            scenes=scenes,
            visual_plan=data.get("visual_plan", {}),
            generated_images={}
        )
    