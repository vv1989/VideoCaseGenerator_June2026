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

        template_voice_map = {}

        for template_actor in case.template.actors:
            template_voice_map[template_actor.actor_id] = template_actor.voice

        actor_voice_map = {}

        for actor in case.actors:
            actor_voice_map[actor.actor_id] = template_voice_map[
                actor.template_actor_id
            ]
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

                voice = "en-GB-RyanNeural"

            elif scene.actor_id in actor_voice_map:

                voice = actor_voice_map[scene.actor_id]

            else:

                voice = "en-GB-RyanNeural"

            rate = "-10%" if scene.speaker.lower() == "narrator" else "+0%"

            self.voice_generator.generate(
                text=scene.text,
                voice=voice,
                filepath=filepath,
                rate=rate
            )
            print(
                f"✅ Audio generated: {filepath}"
            )

        print("\n✅ Audio generation complete")

