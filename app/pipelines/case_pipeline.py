from app.use_cases.generate_dilemmas import GenerateDilemmas
from app.use_cases.generate_case import GenerateCase
from app.use_cases.generate_images import GenerateImages
from app.use_cases.generate_audio import GenerateAudio
from app.use_cases.generate_video import GenerateVideo

import inspect
import os
import json


print("\n🔥 ===== PIPELINE IMPORT DEBUG =====")
print("📂 Current Working Directory:", os.getcwd())
print("📍 GenerateCase imported from:", inspect.getfile(GenerateCase))
print("📍 GenerateDilemmas imported from:", inspect.getfile(GenerateDilemmas))
print("====================================\n")


class CasePipeline:

    def __init__(
        self,
        text_llm,
        image_generator,
        voice_generator,
        movie_generator,
        max_retries=1
    ):

        print("🚨 CasePipeline INIT CALLED")

        # ==========================================
        # USE CASES
        # ==========================================

        self.dilemma_uc = GenerateDilemmas(
            text_llm
        )

        self.case_uc = GenerateCase(
            text_llm,
            max_retries=max_retries
        )

        self.image_uc = GenerateImages(
            image_generator
        )

        self.audio_uc = GenerateAudio(
            voice_generator
        )

        self.video_uc = GenerateVideo(
            movie_generator
        )

        print("✅ CasePipeline initialized successfully")

    # ==========================================
    # DILEMMAS
    # ==========================================

    def generate_dilemmas(self, topic):

        print("\n🚀 GENERATING DILEMMAS")
        print(f"🧠 Topic: {topic}")

        return self.dilemma_uc.execute(
            topic
        )

    # ==========================================
    # CASE TEXT
    # ==========================================

    def generate_case(self, topic, dilemma, template):

        print("\n🚀 GENERATING CASE TEXT")

        return self.case_uc.execute(
            topic,
            dilemma,
            template
        )
    
    def save_case_text(
        self,
        case
    ):

        text_dir = os.path.join(
            "generated_cases",
            case.case_id,
            "text"
        )

        os.makedirs(
            text_dir,
            exist_ok=True
        )

        output_file = os.path.join(
            text_dir,
            "case.txt"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "================ CASE ================\n\n"
            )

            f.write(
                f"Title: {case.title}\n\n"
            )

            f.write(
                f"Topic: {case.topic}\n\n"
            )

            f.write(
                f"Dilemma: {case.dilemma}\n\n"
            )

            f.write(
                f"Setting: {case.setting}\n\n"
            )

            f.write(
                "Actors:\n"
            )

            for actor in case.actors:

                f.write(
                    f"- {actor.name} "
                    f"({actor.role})\n"
                )

            f.write(
                "\nScenes:\n\n"
            )

            print("\n===== SCENE DEBUG =====")

            for scene in case.scenes:

                print(type(scene))
                print(vars(scene))

                break

            print("=======================\n")

            for scene in case.scenes:

                f.write(
                    f"{scene.speaker}: "
                    f"{scene.text}\n\n"
                )

        print(
            f"📄 Case text saved: "
            f"{output_file}"
        )
        
    # ==========================================
    # IMAGES
    # ==========================================

    def generate_images(self, case):

        print("\n🎨 GENERATING IMAGES")

        self.image_uc.execute(
            case
        )

    # ==========================================
    # AUDIO
    # ==========================================

    def generate_audio(self, case):

        print("\n🎤 GENERATING AUDIO")

        self.audio_uc.execute(
            case
        )

    # ==========================================
    # VIDEO
    # ==========================================

    def generate_video(self, case):

        print("\n🎬 GENERATING VIDEO")

        output_file = self.video_uc.execute(
            case
        )

        case.output_video_path = output_file
        
    # ==========================================
    # COMPLETE MULTIMEDIA CASE
    # ==========================================
        
    def build_multimedia_case(
        self,
        topic,
        dilemma,
        template,
        generate_images=True,
        generate_audio=True,
        generate_video=True
    ):

        print("\n🚀 BUILDING MULTIMEDIA CASE")

        # ----------------------------------
        # STEP 1
        # Generate Case Text
        # ----------------------------------

        case = self.generate_case(
            topic,
            dilemma,
            template
        )

        print(vars(case))
        print("\n===== ACTOR DEBUG =====")

        for actor in case.actors:

            print(type(actor))
            print(vars(actor))

        print("=======================\n")

        self.save_case_text(case)

        # ----------------------------------
        # STEP 2
        # Generate Images
        # ----------------------------------

        if generate_images:

            self.generate_images(
                case
            )

        # ----------------------------------
        # STEP 3
        # Generate Audio
        # ----------------------------------

        if generate_audio:

            self.generate_audio(
                case
            )

        # ----------------------------------
        # STEP 4
        # Generate Video
        # ----------------------------------

        if generate_video:

            self.generate_video(
                case
            )

        print("\n✅ MULTIMEDIA CASE COMPLETE")

        return case