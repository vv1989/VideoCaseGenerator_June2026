import json
import re


class GenerateDilemmas:

    def __init__(self, text_llm):
        self.text_llm = text_llm

    def execute(self, topic: str):

        print("\n🚀 GENERATE DILEMMAS")
        print(f"🧠 Topic: {topic}")

        prompt = self._build_prompt(topic)

        response = self.text_llm.generate(
            prompt
        )

        dilemmas = self._parse_response(
            response
        )

        print(
            f"✅ Generated {len(dilemmas)} dilemmas"
        )

        return dilemmas

    # ==========================================
    # PROMPT
    # ==========================================

    def _build_prompt(
        self,
        topic: str
    ):

        return f"""
Generate exactly 5 concise, realistic business dilemmas for the topic:

{topic}

Requirements:

- Each dilemma should represent a genuine managerial trade-off.
- Keep each dilemma to 1 sentence.
- Make them realistic and suitable for a teaching case.
- Make the dilemmas substantially different from one another.

Return ONLY a JSON list.

Example:

[
  "Dilemma 1",
  "Dilemma 2",
  "Dilemma 3",
  "Dilemma 4",
  "Dilemma 5"
]

Do not include markdown.
Do not include explanations.
Do not include code fences.
"""

    # ==========================================
    # RESPONSE PARSING
    # ==========================================

    def _parse_response(
        self,
        response: str
    ):

        print("\n📥 Raw LLM Response:")
        print(response)

        # ----------------------------------
        # Attempt JSON parsing
        # ----------------------------------

        try:

            dilemmas = json.loads(
                response
            )

            if (
                isinstance(dilemmas, list)
                and len(dilemmas) > 0
            ):

                return dilemmas[:5]

        except (
            json.JSONDecodeError,
            TypeError
        ):
            pass

        # ----------------------------------
        # Extract JSON array if model
        # wrapped it in extra text
        # ----------------------------------

        try:

            match = re.search(
                r"\[.*\]",
                response,
                re.DOTALL
            )

            if match:

                dilemmas = json.loads(
                    match.group()
                )

                if isinstance(
                    dilemmas,
                    list
                ):
                    return dilemmas[:5]

        except (
            json.JSONDecodeError,
            TypeError
        ):
            pass

        # ----------------------------------
        # Fallback text parsing
        # ----------------------------------

        cleaned = []

        for line in response.splitlines():

            line = line.strip()

            if not line:
                continue

            line = re.sub(
                r"^\d+[\.\)]\s*",
                "",
                line
            )

            if line.lower().startswith(
                (
                    "here are",
                    "sure",
                    "of course"
                )
            ):
                continue

            cleaned.append(line)

        return cleaned[:5]