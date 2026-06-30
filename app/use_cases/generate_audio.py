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

        actor_voice_map = {}

        for actor in case.actors:
            actor_voice_map[actor.actor_id] = actor.template_actor_id

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

            elif scene.actor_id in actor_voice_map:

                voice_key = actor_voice_map[scene.actor_id]
                
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

