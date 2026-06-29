from app.pipelines.case_pipeline import CasePipeline

from app.infrastructure.images.image_generator import ImageGenerator
from app.infrastructure.audio.voice_generator import VoiceGenerator
from app.infrastructure.video.movie_generator import MovieGenerator

import os
import inspect


# =====================================================
# DEBUG IMPORTS
# =====================================================

print("\n🔥 ===== IMPORT DEBUG =====")

print(
    "🚨 GenerateCase FILE:",
    inspect.getfile(GenerateCase)
)

print(
    "🚨 CasePipeline FILE:",
    inspect.getfile(CasePipeline)
)

print("====================================\n")


def main():

    print("\n🚨 ===== MAIN STARTED =====")
    print(f"📂 Current Working Directory: {os.getcwd()}")

    # =================================================
    # PROVIDER CONFIGURATION
    # =================================================

    TEXT_PROVIDER = "groq"        # openai | gemini | claude | deepseek | groq
    IMAGE_PROVIDER = "gemini"
    AUDIO_PROVIDER = "elevenlabs"
    VIDEO_PROVIDER = "moviepy"

    print("\n🔧 ===== PROVIDER CONFIGURATION =====")

    print(f"📝 Text Provider  : {TEXT_PROVIDER}")
    print(f"🎨 Image Provider : {IMAGE_PROVIDER}")
    print(f"🎤 Audio Provider : {AUDIO_PROVIDER}")
    print(f"🎬 Video Provider : {VIDEO_PROVIDER}")

    # =================================================
    # TEXT LLM
    # =================================================

    text_llm = TextLLM(
        provider=TEXT_PROVIDER,
        api_key=None
    )

    print("\n🤖 Text LLM Initialized")
    print(f"📍 Class: {text_llm.__class__.__name__}")
    print(f"📍 Module: {text_llm.__class__.__module__}")

    # =================================================
    # IMAGE GENERATOR
    # =================================================

    image_generator = ImageGenerator(
        provider=IMAGE_PROVIDER
    )

    print("\n🎨 Image Generator Initialized")
    print(f"📍 Class: {image_generator.__class__.__name__}")
    print(f"📍 Module: {image_generator.__class__.__module__}")

    # =================================================
    # AUDIO GENERATOR
    # =================================================

    voice_generator = VoiceGenerator(
        provider=AUDIO_PROVIDER
    )

    print("\n🎤 Voice Generator Initialized")
    print(f"📍 Class: {voice_generator.__class__.__name__}")
    print(f"📍 Module: {voice_generator.__class__.__module__}")

    # =================================================
    # VIDEO GENERATOR
    # =================================================

    movie_generator = MovieGenerator(
        provider=VIDEO_PROVIDER,
        background_music="assets/audio/background_music.mp3"
    )

    print("\n🎬 Movie Generator Initialized")
    print(f"📍 Class: {movie_generator.__class__.__name__}")
    print(f"📍 Module: {movie_generator.__class__.__module__}")

    # =================================================
    # PIPELINE
    # =================================================

    pipeline = CasePipeline(
        text_llm=text_llm,
        image_generator=image_generator,
        voice_generator=voice_generator,
        movie_generator=movie_generator,
        max_retries=1
    )

    print("\n⚙️ Pipeline Initialized")
    print(f"📍 Class: {pipeline.__class__.__name__}")
    print(f"📍 Module: {pipeline.__class__.__module__}")

    # =================================================
    # USER INPUT
    # =================================================

    topic = input("\n🧠 Enter topic: ").strip()

    print(f"\n📝 Topic Selected: {topic}")

    # =================================================
    # GENERATE DILEMMAS
    # =================================================

    print("\n🚀 Generating dilemmas...")

    dilemmas = pipeline.generate_dilemmas(topic)

    print("\n📋 AVAILABLE DILEMMAS\n")

    for index, dilemma in enumerate(
        dilemmas,
        start=1
    ):
        print(f"{index}. {dilemma}")

    # =================================================
    # SELECT DILEMMA
    # =================================================

    choice = int(
        input("\n👉 Select dilemma number: ")
    ) - 1

    selected_dilemma = dilemmas[choice]

    print("\n🎯 SELECTED DILEMMA")
    print(selected_dilemma)

    # =================================================
    # BUILD COMPLETE MULTIMEDIA CASE
    # =================================================

    print(
        "\n🚀 BUILDING COMPLETE MULTIMEDIA CASE...\n"
    )

    case = pipeline.build_multimedia_case(
        topic=topic,
        dilemma=selected_dilemma,
        generate_images=True,
        generate_audio=True,
        generate_video=True
    )

    # =================================================
    # OUTPUT
    # =================================================

    print("\n✅ ===== CASE GENERATED SUCCESSFULLY =====\n")

    print(case)

    print("\n=========================================\n")

    print(
        f"📂 Output Folder: generated_cases/{case.case_id}"
    )


if __name__ == "__main__":
    main()