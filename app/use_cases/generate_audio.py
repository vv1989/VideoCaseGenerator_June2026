import os

class GenerateAudio:

    def __init__(self, voice_generator):

        self.voice_generator = voice_generator

    # ==================================================
    # 🎤 AUDIO GENERATION
    # ==================================================

    def execute(self, case):

        print("\n🎤 ===== GENERATING AUDIO =====")

        output_dir = os.path.join(
            "generated_cases",
            case.case_id,
            "audio"
        )

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        for scene in case.scenes:

            filepath = os.path.join(
                output_dir,
                f"{scene.scene_id}.mp3"
            )

            # ---------------------------------
            # Narrator
            # ---------------------------------

            if scene.speaker.lower() == "narrator":

                voice_key = "narrator"

            # ---------------------------------
            # Actor 1 (British woman)
            # ---------------------------------

            elif scene.actor_id == "a0":

                voice_key = "actor1"

            # ---------------------------------
            # Actor 2 (Indian man)
            # ---------------------------------

            elif scene.actor_id == "a1":

                voice_key = "actor2"

            # ---------------------------------
            # Actor 3 (American man)
            # ---------------------------------

            elif scene.actor_id == "a2":

                voice_key = "actor3"

            else:

                voice_key = "narrator"

            self.voice_generator.generate(
                text=scene.text,
                voice_key=voice_key,
                filepath=filepath
            )

            print(
                f"✅ Audio generated: {filepath}"
            )

        print("\n✅ Audio generation complete")

